# -*- coding: utf-8 -*-
from sage.all import *
import random as rnd

from factorization_function import *
from benchmark import *

# Lenstras Elliptic Curve Factorization
class LenstrasEllipticCurveFactorization(FactorizationFunction):
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = False
        return c

    # Detta fungerar aldrig (stannar i loopen):
    #for i in range(100):
    #    res = LenstrasEllipticCurveFactorization.getOneFactor(1294712089654123)
    @classmethod
    def getOneFactor(self, n, benchmark = Benchmark(), maximumIterations = -1):
        # Setup
        iteration = 0
        # If no iteration lock is set, use sqrt(n)
        maximumIterations = int(ceil(sqrt(n))) if maximumIterations == -1 else maximumIterations
        factor = 1
        x = ZZ.random_element(2, n, "uniform") #Element in Zn \{0, 1}
        y = ZZ.random_element(2, n, "uniform") #Element in Zn \{0, 1}
        A = ZZ.random_element(2, n, "uniform") #Element in Zn \{0, 1}
        LT = (3 * x**2 + A)
        LN = (2 * y)

        # Start of algorithm
        benchmark.start()
        if gcd(LN, n) == 1:
            L = (LT * inverse_mod(LN, n)) % n
            x2 = (L**2 - x*2) % n
            y2 = (L*(x - x2) - y) % n

            while True:
                benchmark.iterate()
                iteration += 1

                if iteration < maximumIterations:
                    LT = (y2 - y) % n
                    LN = (x2 - x) % n

                    if gcd(LN, n) == 1:
                        L = (LT * inverse_mod(LN, n)) % n
                        x3 = (L**2 - x - x2) % n
                        y3 = (L*(x - x3) - y) % n
                        x2 = x3; y2 = y3
                    else:
                        factor = gcd(LN, n)
                        break
                else:
                    #print "More than sqrt(n) iterations. Stop"
                    #print "n=%d, x=%d, y=%d, A=%d"%(n, x, y, A)
                    benchmark.stop()
                    return None
        else:
            factor = gcd(LN, n)

        # End of algorithm
        benchmark.stop()
        return None if factor == n else factor

    @classmethod
    def factorize(self, n, returnBenchmark = False, maximumIterations = -1):
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
                factor = self.getOneFactor(a, benchmark, maximumIterations)
                if factor is None:
                    # Factor is not a prime, but no solution was found - try again
                    # (Lenstras algorithm is non-deterministic)
                    stack += [a]
                else:
                    # Factor is a true factor, append it and a / factor to found factors
                    stack += [factor, a / factor]
        # End of algorithm
        return (factors, benchmark) if returnBenchmark else factors
