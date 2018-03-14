# -*- coding: utf-8 -*-
from factorization_function import *
from benchmark import *

# Fermats Factorization
class FermatsFactorization(FactorizationFunction):
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = False
        return c

    @classmethod
    def getOneFactor(self, n, benchmark = Benchmark()):
        # Edge case even numbers except 2
        if n % 2 == 0 and n != 2:
            return None
        elif n == 2:
            return [1, 2]

        # Setup
        factors = []
        a = ceil(sqrt(n))
        b2 = a**2 - n

        # Start of algorithm
        benchmark.start()
        while not b2.is_square():
            benchmark.iterate()
            a += 1
            benchmark.start("square")
            b2 = a**2 - n
            benchmark.stop("square")
        b = int(sqrt(b2))
        p = a - b
        q = a + b
        if p != 1:
            factors.append(p)
        if q != 1:
            factors.append(q)

        # End of algorithm
        benchmark.stop()
        return factors

    @classmethod
    def factorize(self, n, returnBenchmark=False):
        # Edge case (constant time)
        if n == 1:
            return ([1], Benchmark()) if returnBenchmark else [1]

        # Setup
        benchmark = Benchmark()
        factors = [1]

        # Numbers to factor
        stack = [n]
        P = Primes()

        # Start of algorithm
        while len(stack) > 0:
            a = stack.pop()
            benchmark.start("primalityTest")
            isPrime = a in P
            benchmark.stop("primalityTest")

            if isPrime:
                # a is a prime, append to found factors
                factors.append(a)
            else:
                # a is not a prime, factorize
                benchmark.iterate("algorithm iterations")
                possibleFactors = self.getOneFactor(a, benchmark)
                if possibleFactors is not None:
                    # Factor is a true factor, append it and a / factor to found factors
                    stack += possibleFactors

        # End of algorithm
        return (factors, benchmark) if returnBenchmark else factors