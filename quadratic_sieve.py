# -*- coding: utf-8 -*-
from sage.all import *
import numpy as np

from factorization_function import *
from benchmark import *

# Helper struct for factoring table
class QuadraticSieveFactor(object):
    def __init__(self, t, Ft):
        self.t = t
        self.origin = Ft
        self.Ft = Ft
        self.factors = []

    def __str__(self):
        return "QuadraticSieveFactor <t: %d, F(t): %d, factors: %s>"%(self.t, self.Ft, "[" + ",".join([str(x) for x in self.factors]) + "]")
    def __repr__(self):
        return "QuadraticSieveFactor <t: %d, F(t): %d, factors: %s>"%(self.t, self.Ft, "[" + ",".join([str(x) for x in self.factors]) + "]")

    def divide(self, x):
        self.Ft /= x
        self.factors.append(x)

# Quadratic Sieve
class QuadraticSieve(FactorizationFunction):
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = False
        return c

    @classmethod
    def L(self, n):
        # The expected L(n) is defined only for n > 2.72, expect integers
        if (n >= 3):
            return round(numerical_approx(e**sqrt(ln(n)*ln(ln(n)))))
        else:
            return None

    @classmethod
    def testL(self):
        case = [1, 2, 5, 10173]
        # Truth expects L(n)=e^sqrt(ln(n)*ln(ln(n)))
        truth = [None, None, 2, 93]
        def noneCheck(value):
            return str(value) if value is not None else "None"
        for i in range(len(case)):
            result = self.L(case[i])
            if result == truth[i]:
                print u"L(%s)≈%s: ✓"%(noneCheck(case[i]), noneCheck(truth[i]))
            else:
                print u"L(%s)≈%s: ✘"%(noneCheck(case[i]), noneCheck(truth[i]))
                print "\t Expected: ", truth[i]
                print "\t Got: ", result

    @classmethod
    def F(self, x, n):
        return x**2-n

    @classmethod
    def testF(self):
        case = [{'x': 2, 'n': 1}, {'x': 5, 'n': 24}]
        # Truth expects F(x)=x^2-1
        truth = [3, 1]
        for i in range(len(case)):
            result = self.F(**case[i])
            if result == truth[i]:
                print u"F(%d, %d)≈%d: ✓"%(case[i]['x'], case[i]['n'], truth[i])
            else:
                print u"F(%d, %d)≈%d: ✘"%(case[i]['x'], case[i]['n'], truth[i])
                print "\t Expected: ", truth[i]
                print "\t Got: ", result

    @classmethod
    def getBase(self, B, benchmark = Benchmark()):
        if (B < 2):
            return []
        P = Primes()
        base = [2]
        # Sage needs int to be cast as Integer
        benchmark.start("get base")
        p = P.next(Integer(base[len(base)-1]))
        while p <= B:
            benchmark.iterate("get base")
            base.append(p)
            p = P.next(Integer(base[len(base)-1]))
        benchmark.stop("get base")

        return base

    @classmethod
    def testGetBase(self):
        case = [13]
        # Truth expects F(x)=x^2-1
        truth = [[2, 3, 5, 7, 11, 13]]
        for i in range(len(case)):
            result = self.getBase(case[i])[0]
            if sorted(result) == sorted(truth[i]):
                print u"Base for %d=%s: ✓"%(case[i], "[" + ",".join(str(x) for x in truth[i]) + "]")
            else:
                print u"Base for %d=%s: ✘"%(case[i], "[" + ",".join(str(x) for x in truth[i]) + "]")
                print "\t Expected: ", truth[i]
                print "\t Got: ", result

    @classmethod
    def getAB(self, n, B = None, V = None, benchmark = Benchmark()):
        l = self.L(n)
        if B is None:
            B = l - 1
        if V is None:
            V = l + 10

        u = floor(sqrt(n)) + 1
        v = floor(sqrt(n)) + V

        base = self.getBase(B, benchmark)

        t = [QuadraticSieveFactor(x, self.F(x, n)) for x in range(u, v + 1)]

        # For each prime 2 ≤ p ≤ B
        benchmark.start("get A and B")
        for p in base:
            # Recursively solve x^2≡n (mod p^k) where k = 1, 2, 3... for as long as it's possible
            _x = var('x')
            k = 1
            solutions = [int(i[0]) for i in solve_mod(_x**2 == n, p**k)]
            while len(solutions) > 0:
                benchmark.iterate("for each possible x^k")
                # The inclusion could be checked in another, possibly more performant way
                included = []
                for x in solutions:
                    benchmark.iterate("for each sieve step")
                    # Calculate first index which yields t ≤ u (instead of stepping from i=0)
                    # This could be solved by solving a congruence equation initially
                    start = x
                    benchmark.start("determine start")
                    while start < u:
                        benchmark.iterate("calculate first step")
                        start += p**k
                    i = (u - x) // p
                    benchmark.stop("determine start")
                    for i in range(start, v + 1, p**k):
                        benchmark.iterate("for each simplification")
                        # Actual index in array
                        index = i - u
                        if index not in included:
                            t[index].divide(p)
                            included.append(index)
                if len(included) > 0:
                    k += 1
                    benchmark.start("solve x^2=n mod p^k")
                    # This could be solved faster by using the Hensel's lift
                    solutions = [int(i[0]) for i in solve_mod(_x**2 == n, p**k)]
                    benchmark.stop("solve x^2=n mod p^k")
                else:
                    solutions = []
        benchmark.stop("get A and B")

        # This could be improved to not filter through the same list multiple times
        A = filter(lambda x: x.Ft == 1, t)
        # Instead of array of factors, get map of factors and exponents
        def factorMap(x):
            values, counts = np.unique(x.factors, return_counts=True)
            return dict(zip(values, counts))
        C = [(x.origin, factorMap(x)) for x in A]
        A = map(lambda x: x.t, A)
        return (A, C, base)

    @classmethod
    def factorizeOnce(self, n, B, V, benchmark = Benchmark()):
        # Setup
        factors = []
        # Start of algorithm
        R = IntegerModRing(2)

        A, C, base = QuadraticSieve.getAB(n, B, V, benchmark)

        # If no B-smooth numbers were found
        if len(A) < 2 or len(C) < 2:
            return (None, benchmark)

        # Create matrix where each row is a prime and each column an equation possibly including that prime (1 or 0)
        coeffs = []
        for p in base:
            coeff = [C[i][1][p] % 2 if p in C[i][1] else 0 for i in range(len(C))]
            if any(coeff):
                coeffs.append(coeff)

        # Create variables string for symbolic equations
        variablesString = " ".join("x" + str(i) for i in range(len(coeffs[0]) + 1))
        variables = var(variablesString)
        equations = []

        # Create symbolic equations
        for coeff in coeffs:
            string = ""
            for i in range(len(coeff)):
                if coeff[i]:
                    string += str(variables[i]) + "*"
            string = string[:-1]
            string += "==0"
            equations.append(eval(string))

        benchmark.start("solve equation")
        solutions = solve_mod(equations, 2)
        benchmark.stop("solve equation")

        benchmark.start("calculate factors")
        # Note that solutions[0] will always be the 0 vector - could be removed
        for solution in solutions:
            if n == 1:
                break
            a = 1
            b = 1
            for i in range(len(solution)):
                benchmark.iterate("calculate factors")
                if solution[i] == 1:
                    a *= A[i]
                    b *= C[i][0]
            possibleFactors = [gcd(a - b, n), gcd(a + b, n)]
            possibleFactors = filter(lambda x: x != 1 and x != n, possibleFactors)

            while len(possibleFactors) > 0:
                p = possibleFactors.pop()
                q = n / p
                if floor(q) == q:
                    factors.append(p)
                    n = q
                    if q != 1:
                        possibleFactors.append(q)
                    else:
                        break

        benchmark.stop("calculate factors")

        return factors

    @classmethod
    def factorize(self, n, returnBenchmark=False, B = None, V = None):
        # Setup
        benchmark = Benchmark()
        factors = [1]

        P = Primes()
        stack = [n]

        while len(stack) > 0:
            a = stack.pop()

            benchmark.start("primality test")
            isPrime = a in P
            benchmark.stop("primality test")

            if isPrime:
                factors.append(a)
            else:
                possibleFactors = self.factorizeOnce(a, B, V, benchmark)
                if possibleFactors is not None:
                    stack += possibleFactors
                benchmark.iterate("algorithm runs")

        # End of algorithm
        return (factors, benchmark) if returnBenchmark else factors