# -*- coding: utf-8 -*-
from factorization_function import *
from benchmark import *

# Pollards Rho Algorithm - https://en.wikipedia.org/wiki/Pollard%27s_rho_algorithm
class PollardsRhoAlgorithm(FactorizationFunction):
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = False
        return c

    @classmethod
    def getOneFactor(self, n, start, g):
        # Setup
        benchmark = Benchmark()
        Zn = Zmod(n)
        x = y = Zn(int(ceil(sqrt(n)))) if start == "sqrt" else Zn(start)
        factor = 1
        # Start of algorithm
        benchmark.start()
        while factor == 1:
            benchmark.iterate()
            x = g(x)
            y = g(g(y))
            factor = gcd(lift(x - y), n)
        # End of algorithm
        benchmark.stop()
        return (None, benchmark) if factor == n else (factor, benchmark)

    @classmethod
    def factorize(self, n, returnBenchmark=False, start=2, g = lambda x: x**2 + 1, lambdas = None):
        # Edge case (constant time)
        if n == 1:
            return ([1], Benchmark()) if returnBenchmark else [1]
        # Setup
        benchmark = Benchmark()
        factors = [1]
        # g(x) functions to test, in order of priority. The last is always guaranteed to work
        lambdas = lambdas if lambdas is not None else [g, lambda x: x**3 + 1, lambda x: x + 1]
        # Number to factor and lambda index to use
        stack = [(n, 0)]
        P = Primes()
        # Start of algorithm
        while len(stack) > 0:
            a, gIndex = stack.pop()
            benchmark.start("primalityTest")
            isPrime = a in P
            benchmark.stop("primalityTest")

            if isPrime:
                # a is a prime, append to found factors
                factors.append(a)
            else:
                # a is not a prime, factorize
                factor, b = self.getOneFactor(a, start, lambdas[gIndex])
                benchmark += b
                if factor is None:
                    # Found no factor even though a is not prime - try a slower g(x)
                    # Note that the last g(x) is equivalent to trial division (slow), but is
                    # Guaranteed to work
                    stack += [(a, gIndex + 1 if gIndex + 1 < len(lambdas) else gIndex)]
                else:
                    # Factor is a true factor, append it and a / factor to found factors
                    stack += [(factor, 0), (a / factor, 0)]
        # End of algorithm
        return (factors, benchmark) if returnBenchmark else factors