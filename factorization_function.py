# -*- coding: utf-8 -*-
import sys
from sage.all import *
import datetime
import os
import os.path

from benchmark import *

###
# This file will usually not need any alteration. Create subclasses of FactorizationFunction.
###

class FactorizationFunctionCharacteristics(object):
    def __init__(self):
        self.canFactorizePrimes = False
        self.canFactorizeNonPrimes = False

    def __str__(self):
        return "Factorization Function Characteristics <Can factorize primes: %c, Can factorize non-primes: %c>"%(self.canFactorizePrimes, self.canFactorizeNonPrimes)
    def __repr__(self):
        return "Factorization Function Characteristics <Can factorize primes: %c, Can factorize non-primes: %c>"%(self.canFactorizePrimes, self.canFactorizeNonPrimes)

# FactorizationFunction is inherited to create benchmarkable, testable factorization functions
class FactorizationFunction(object):
    @classmethod
    # Return characteristics of the specific algorithm
    def getCharacteristics(self):
        return None

    @classmethod
    # Run factorization
    # n: number to factor
    # returnBenchmark: return factors if False, tuple of (factors, benchmark) if True
    def factorize(self, n, returnBenchmark=False):
        return (None, None)

    @classmethod
    # Runs benchmark on the factorization function
    # iterations: number of times to run the function
    # numberOfFactors: number of factors included in factorized number
    # factorLowerLimit: lower limit from which primes are generated
    # factorUpperLimit: upper limit from which primes are generated
    # Returns tuple (times, iterations)
    def benchmark(self, numberSuite, iterations=10, optionalArgs={}, start=2, end=None, skipFactors=None, mode="factors"):
        benchmarks = []
        description, suite = numberSuite

        modeLine = "Unknown"
        if mode == "factors":
            modeLine = "Number of factors"
        elif mode == "bits":
            modeLine = "Number of bits"

        now = datetime.datetime.now()
        name = str(self)
        name = name[name.rfind(".")+1:-2]
        filename = "./benchmarks/%s_%s.txt"%(name, now.strftime('%Y-%m-%d_%H:%M:%S'))
        originalFilename = filename[:-4]

        serial = 1
        while os.path.isfile(filename):
            filename = "%s_%d.txt"%(originalFilename, serial)
            serial += 1

        def writeToFile(line):
            mode = "a" if os.path.exists(filename) else "w"
            handle = open(filename, mode)
            handle.write(line + "\n")
            handle.close()

        # Write header and description to file
        def formatParameter(parameter):
            string = str(parameter)
            if "<function" in string:
                string = string.split(" ")[1]
            return string
        def formatParameters(parameters):
            if isinstance(parameters, list):
                return "[%s]"%', '.join(map(formatParameter, parameters))
            return str(parameters)
        writeToFile("# %s"%name + (" (%s)"%",".join("%s: %s"%(pair[0], formatParameters(pair[1])) for pair in optionalArgs.items()) if len(optionalArgs) > 0 else ""))
        writeToFile("# %s"%description)
        writeToFile("%s:Number to factorize:Time taken:Iterations taken"%modeLine)

        for numberOfFactors, numbers in suite:
            if numberOfFactors < start:
                continue
            if end is not None and numberOfFactors > end:
                continue
            if skipFactors is not None:
                if callable(skipFactors) and skipFactors(numberOfFactors):
                    continue
            bs = []
            for i in range(iterations):
                for n, factors in numbers:
                    resultingFactors, b = self.factorize(n, true, **optionalArgs)
                    # Only take into account correct factorizations
                    if sorted(resultingFactors) == sorted(factors):
                        bs.append(b)
                        formattedTime = ",".join("%s-%f"%pair for pair in b.totalTime.items())
                        formattedIterations = ",".join("%s-%d"%pair for pair in b.iterations.items())
                        writeToFile("%d:%d:%s:%s"%(numberOfFactors, n, formattedTime, formattedIterations))
            benchmarks.append((numberOfFactors, bs))

        # Result, one tuple per number of factors:
        # (numberOfFactors, minimum benchmark, maximum benchmark, average benchmark)
        res = [(bs[0], Benchmark.min(bs[1]), Benchmark.max(bs[1]), Benchmark.average(bs[1])) for bs in benchmarks]

        return res

    @classmethod
    def testFactorization(self, cases, truths, optionalArgs):
        passed = True

        for i in range(len(cases)):
            n = cases[i]
            truth = sorted(truths[i])

            result = sorted(self.factorize(n, **optionalArgs))
            factorString = "*".join(str(x) for x in truth)

            def togglePassed(passed):
                if passed:
                    print u"✘"
                    passed = False
                return passed

            if result is None:
                passed = togglePassed(passed)
                print "Can factorize %d=%s: ✘"%(n, factorString)
                print "\t Expected: ", truth
                print "\t Got: None. Most likely means that the function does not support the given input"
            elif result != truth:
                passed = togglePassed(passed)
                print u"Can correctly factor %d=%s: ✘"%(n, factorString)
                print "\t Expected: ", truth
                print "\t Got: ", result

        if passed:
            print u"✓"

    @classmethod
    # Runs test on the factorization function
    # optionalArgs is expected to be a map and is passed to factorize function
    def test(self, optionalArgs={}):
        testFunctions = filter(lambda x : x.find("test") == 0 and x != "test" and x != "testFactorization", dir(self))

        if len(testFunctions) > 0:
            print "=== Common Tests ==="

        print "Can run factorization function: ",
        try:
            self.factorize(15)
            print u"✓"
        except:
            print u"✘"
            print "Will abort tests due to error in factorization function"
            return

        c = self.getCharacteristics()

        if c.canFactorizePrimeComposites:
            print "Can factorize one or more primes: ",
            cases = [2, 3, 5, 7, 11, 15, 21, 25, 45, 77, 121, 169, 21853]
            truths = [[1, 2], [1, 3], [1, 5], [1, 7], [1, 11], [1, 3, 5], [1, 3, 7], [1, 5, 5], [1, 3, 3, 5], [1, 7, 11], [1, 11, 11], [1, 13, 13], [1, 13, 41, 41]]
            self.testFactorization(cases, truths, optionalArgs)
        else:
            print u"Can factorize one or more primes: ✘ (Not supported)"

        if c.canFactorizeEvenComposites:
            print "Can factorize one or more non-primes: ",
            cases = [2, 4, 12, 20, 30]
            truths = [[1, 2], [1, 2, 2], [1, 2, 2, 3], [1, 2, 2, 5], [1, 2, 3, 5]]
            self.testFactorization(cases, truths, optionalArgs)
        else:
            print u"Can factorize one or more non-primes: ✘ (Not supported)"

        # Run class specific tests
        if len(testFunctions) > 0:
            print "\n=== Algorithm Specific Tests ==="
        for func in testFunctions:
            method = getattr(self, func)
            method()