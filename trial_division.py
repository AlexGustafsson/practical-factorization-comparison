# -*- coding: utf-8 -*-
from factorization_function import *
from benchmark import *

# Trial Division - https://en.wikipedia.org/wiki/Trial_division
class TrialDivision(FactorizationFunction):
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = True
        return c

    @classmethod
    def factorize(self, n, returnBenchmark=False, modified=False):
        # Setup
        benchmark = Benchmark()
        factors = [1]
        # Start of algorithm
        benchmark.start()
        if modified:
            while n % 2 == 0:
                benchmark.iterate()
                factors.append(2)
                n /= 2
            f = 3
            while n > 1:
                benchmark.iterate()
                if n % f == 0:
                    factors.append(f)
                    n /= f
                else:
                    f += 2
        else:
            f = 2
            while n > 1:
                benchmark.iterate()
                if (n % f == 0):
                    factors.append(f)
                    n /= f
                else:
                    f += 1
        # End of algorithm
        benchmark.stop()
        if returnBenchmark:
            return (factors, benchmark)
        else:
            return factors