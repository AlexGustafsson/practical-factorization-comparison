# -*- coding: utf-8 -*-
from timeit import default_timer as timer

###
# This file will usually not need any alteration.
###

#

# Class to wrap a benchmark (helper functions)
class Benchmark(object):
    def __init__(self):
        self.totalTime = {}
        self.iterations = {}
        self.startTime = {}
        self.depth = 0
        self.events = []
        # True will make all benchmark instances log their actions in an easy to follow manner
        # Might however use up more memory as each action is logged - defaults to False. Use with benchmark.printEvents()
        self.verbose = False

    def __str__(self):
        totalTimePrint = ', '.join('"%s": %.6f'%(key, value) for key, value in self.totalTime.items())
        iterationsPrint = ', '.join('"%s": %d'%(key, value) for key, value in self.iterations.items())
        return "Benchmark <Total time: {%s}, iterations: {%s}>"%(totalTimePrint, iterationsPrint)
    def __repr__(self):
        totalTimePrint = ', '.join('"%s": %.6f'%(key, value) for key, value in self.totalTime.items())
        iterationsPrint = ', '.join('"%s": %d'%(key, value) for key, value in self.iterations.items())
        return "Benchmark <Total time: {%s}, iterations: {%s}>"%(totalTimePrint, iterationsPrint)

    def __add__(self, other):
        self.mergeDictionaries(self.totalTime, other.totalTime)
        self.mergeDictionaries(self.iterations, other.iterations)
        self.mergeDictionaries(self.startTime, other.startTime)
        return self
    def __radd__(self, other):
        return self.__add__(other)

    def asTables(self):
        timeLatex = """$\\begin{array}{l | l}
\\text{name} & \\text{time }s\\\\
\\hline\n """
        iterationsLatex = """$\\begin{array}{l | l}
\\text{name} & \\text{iterations}\\\\
\\hline\n """

        for key, value in self.totalTime.items():
            timeLatex += "\\text{%s}&%f\\\\\n"%(key, value)
        for key, value in self.iterations.items():
                    iterationsLatex += "\\text{%s}&%d\\\\\n"%(key, value)

        timeLatex += "\\end{array}$"
        iterationsLatex += "\\end{array}$"

        return (timeLatex, iterationsLatex)

    def mergeDictionaries(self, a, b):
        for key in b.keys():
            if key not in a:
                a[key] = b[key]
            else:
                a[key] += b[key]

    def start(self, name = "default"):
        t = timer()

        if ":" in name or "," in name or "-" in name:
            raise ValueError("A benchmark name may not contain characters ':', '-' or ','")

        if name in self.startTime:
            raise ValueError("Benchmark for %s is already in progress, please stop benchmark first"%name)

        self.startTime[name] = t

        if self.verbose:
            self.events.append(("start", name, self.depth, None))
            self.depth += 1

    def stop(self, name = "default"):
        t = timer()

        if ":" in name or "," in name or "-" in name:
            raise ValueError("A benchmark name may not contain characters ':', '-' or ','")

        if name not in self.startTime:
            raise ValueError("Benchmark for %s cannot be stopped before it has been started"%name)

        if name not in self.totalTime:
            self.totalTime[name] = 0

        timeTaken = t - self.startTime[name]
        self.totalTime[name] += timeTaken
        del self.startTime[name]

        if self.verbose:
            self.depth -= 1
            self.events.append(("stop", name, self.depth, timeTaken))

    def iterate(self, name = "default"):
        if ":" in name or "," in name or "-" in name:
            raise ValueError("A benchmark name may not contain characters ':', '-' or ','")

        if name not in self.iterations:
            self.iterations[name] = 0

        self.iterations[name] += 1

        if self.verbose:
            self.events.append(("iterate", name, self.depth, None))

    def printEvents(self):
        if self.verbose == False or len(self.events) == 0:
            print "It seems like no events were captured. Try setting verbose = True on the benchmark instance"

        i = 0
        while i < len(self.events):
            type, name, depth, timeTaken = self.events[i]
            if type == "iterate":
                start = i
                # Group identical iterations to preserve output length
                for j in range(i + 1, len(self.events)):
                    otherType, otherName, otherDepth, otherTime = self.events[j]
                    if otherType == type and otherName == name:
                        i += 1
                    else:
                        break
                # Print number of occurances if multiple iterations followed each other
                if start == i:
                    print "\t" * depth + "🔂 %s"%name
                else:
                    print "\t" * depth + "🔂 %s x %d"%(name, i - start + 1)
            elif type == "start":
                print "\t" * depth + "▶️ %s"%name
            elif type == "stop":
                print "\t" * depth + "⏹ %s (%f s)"%(name, timeTaken)
            i += 1

    @classmethod
    def max(self, benchmarks):
        benchmark = Benchmark()

        totalTime = {}
        iterations = {}

        for b in benchmarks:
            for key, value in b.totalTime.items():
                if key not in totalTime:
                    totalTime[key] = []
                totalTime[key].append(value)
            for key, value in b.iterations.items():
                if key not in iterations:
                    iterations[key] = []
                iterations[key].append(value)

        for key, values in totalTime.items():
            benchmark.totalTime[key] = max(values)
        for key, values in iterations.items():
            benchmark.iterations[key] = max(values)

        return benchmark

    @classmethod
    def min(self, benchmarks):
        benchmark = Benchmark()

        totalTime = {}
        iterations = {}

        for b in benchmarks:
            for key, value in b.totalTime.items():
                if key not in totalTime:
                    totalTime[key] = []
                totalTime[key].append(value)
            for key, value in b.iterations.items():
                if key not in iterations:
                    iterations[key] = []
                iterations[key].append(value)

        for key, values in totalTime.items():
            benchmark.totalTime[key] = min(values)
        for key, values in iterations.items():
            benchmark.iterations[key] = min(values)

        return benchmark

    @classmethod
    def average(self, benchmarks):
        benchmark = Benchmark()

        totalTime = {}
        iterations = {}

        average = lambda x : sum(x) / len(x)

        for b in benchmarks:
            for key, value in b.totalTime.items():
                if key not in totalTime:
                    totalTime[key] = []
                totalTime[key].append(value)
            for key, value in b.iterations.items():
                if key not in iterations:
                    iterations[key] = []
                iterations[key].append(value)

        for key, values in totalTime.items():
            benchmark.totalTime[key] = average(values)
        for key, values in iterations.items():
            benchmark.iterations[key] = average(values)

        return benchmark