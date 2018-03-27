A Practical Study and Comparison of Integer Factorization Methods
======
A project by [Alex Gustafsson](https://github.com/AlexGustafsson) and [Marcus Lenander](https://github.com/MarcusLenander) in the course MA1453 (Cryptography 2) at BTH, Sweden.

This project evaluates the relative performance of various algorithms for integer factorization, namely Trial Division, Fermat's Factorization, Pollard's Rho Algorithm, Lenstra's Elliptic Curve Factorization Algorithm and briefly the Quadratic Sieve. The algorithms are presented and described with regards to use and implementation details. No effort was made to optimize the implemented algorithms further than what is considered logical. No algorithm leverages parallel computing techniques, dynamic programming techniques or other techniques in order to gain performance. No consideration of performance was made when the software and programming stack were chosen.

The project was hosted on a private instance of [CoCalc - Collaborative Calculation in the Cloud](https://cocalc.com). CoCalc makes it easy to collaboratively develop math-oriented code using technologies such as [SageMath](http://www.sagemath.org), [R](https://cran.r-project.org/doc/manuals/r-release/R-intro.html), [Julia](https://docs.julialang.org/en/stable/manual/introduction/) and [LaTeX](https://en.wikibooks.org/wiki/LaTeX) whilst still being completely free and open source.

The paper is available in the branch [paper](https://github.com/AlexGustafsson/practical-factorization-comparison/tree/paper).

See also: [Course Notes](https://github.com/CourseNotesBTH) for BTH courses and code and examples for [Programming Courses at BTH](https://github.com/ProgrammingCoursesBTH).

# Quickstart
<a name="quickstart"></a>

1. Download this repository and launch it in a public or private CoCalc project
2. Navigate / test the code yourself or read below

# Table of contents

[Quickstart](#quickstart)<br/>
[Algorithms](#algorithms)<br />
[Utilities](#utilities)<br />
[Disclaimer](#disclaimer)

# Implemented algorithms
<a name="algorithms"></a>

Psuedocode and comments for the implemented factorization algorithms. The goal of each implemented algorithm was to be able to retrieve an unknown amount of factors. Therefore there are some changes made to some of the algorithms to allow for that goal to be fulfilled. Beyond that, we've tried to stay true to each algorithm's core meaning that we've taken no liberty to add dynamic or parallell programming techniques to speed up the factorization. In a realistic scenario, such techniques are crucial to speed factorization up - especially for numbers consisting of many (possibly equal) factors.

## Trial Division

Found in `trial_division.py`, the trial division algorithms implemented consists of the following pseudocode:

##### `TrialDivision`

```
def TrialDivision(n)
    f = 1
    while n > 1
        if n is divisible by f
            f is a factor. Divide n by f
        else
            increment f by one
```

##### `TrialDivision` (modified)

A modification of the above Trial Division that halves the needed time.

```
def TrialDivision(n)
    f = 3
    while n is divisible by 2
        2 is a factor. Divide n by 2
    while n > 1
        if n is divisible by f
            f is a factor. Divide n by f
        else
            increment f by 2
```

## Fermat's Factorization Method

Found in `fermats_factorization.py`, the Fermat's algorithm implemented consists of the following pseudocode:

```
def FermatsFactorization(n)
    if n % 2 == 0:
        return None
        
    a = ceil(sqrt(n))
    b2 = a*a - n
    while b2 is not square:
        a += 1
        b2 = a*a - n
    b = sqrt(b2)
    return p = (a + b), q = (a - b)
```

## Pollard's Rho Algorithm

Found in `pollards_rho_algorithm.py`, the Pollard's algorithm implemented consists of the following pseduocode:

```
def PollardsRhoAlgorithm(n)
    if n is 1
        1 is a factor. Stop
    add n to the stack 'stack' to try with the first g(x)
    while the stack is not empty
        pop an element a from the stack
        if a is prime
            a is a factor
        else
            f = 1, x = 2, y = 2
            while f is 1
                x = g(x), y = g(g(x))
                f = gcd(x - y, a)
            if f is n
                add a to stack to try with the next g(x)
            else
                add f and a / f to the stack
```

_Note: the function `g(x)` is tested in the following order: `g(x)=x^2+1`, `g(x)=x^3+1`, `g(x)=x+1`. If you're interested in why those functions are tested in that order, please refer to the paper._

## Lenstra's Elliptic Curve Factorization

Found in `lenstras_elliptic_curve_factorization.py`, the Lenstra's algorithm implemented consists of the following pseudocode:

```
def LenstrasEllipticCurveFactorizationAlgorithm(n)
    x, y, A = random element in Zn
    Q = (x, y)
    if a modular inverse exists:
        P = Q + Q
        while P + Q can be calculated 
            if iterations is less then maximum iterations
                if modular inverse exists in kP
                    kP = (k-1)P + Q
                else
                    add gcd(modular inverse, n) to the stack of factors
            else
                no factor found, try with new random elements
    else
        add gcd(modular inverse, n) to the stack of factors
```

## Quadratic Sieve

Found in `quadratic_sieve.py`, the Quadratic Sieve algorithm implemented is too complex to easily describe using pseudocode. Please view the file `quadratic_sieve.py` and read the source code instead.

# Utilities
<a name="utilities"></a>

Utilities produced to make testing, benchmarking and debugging easier.

## Factorization Function

Found in `factorization_function.py`, the `FactorizationFunction` class is a parent class to all implemented factorization algorithms. The class enables the same interface and testability for all algorithms. Noteworthy details are mentioned below.

##### Implementing a Factorization Function

Class implementation:
```
from factorization_function import *

class MyFactorizationFunction(FactorizationFunction)
    @classmethod
    def getCharacteristics(self):
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimeComposites = True
        c.canFactorizeEvenComposites = True
        return c

    @classmethod
    def factorize(self, n, returnBenchmark=False):
        # Setup
        factors = []
        ...
        # Start of algorithm
        ...
        # End of algorithm
        return (factors, benchmark) if returnBenchmark else factors
```

Class usage:
```
MyFactorizationFunction.factorize(3*5*6)
MyFactorizationFunction.test()
MyFactorizationFunction.benchmark(numberSuite)
```

##### Determining capabilities

Each Factorization Function supports a common interface for determining capabilities.

To retrieve a Factorization Function's capabilities, call the `getCharacteristics` method.

The result is expected to be a `FactorizationFunctionCharacteristics` object consisting of two bools:

`canFactorizePrimes` indicates whether or not the algorithm can factorize numbers consisting of prime factors. `canFactorizeNonPrimes` indicates whether or not the algorithm can factorize numbers consisting of even factors.

To add specific characteristics to your function, simply define the function like this:

```
...
class MyFactorizationFunction(FactorizationFunction)
    ...
    def getCharacteristics():
        c = FactorizationFunctionCharacteristics()
        c.canFactorizePrimes = True
        c.canFactorizeNonPrimes = False
        return c
```

##### Testing

Each Factorization Function supports a common interface for testing.

To test a Factorization Function, call the `test` method.

```
MyFactorizationFunction.test()
```

Each Factorization Function is first tested to see whether or not the `factorization` function will run at all. If not, the test will fail.

If the algorithm has been noted to support factorization to prime factors, the function is then tested using the following numbers: ```2, 3, 5, 7, 11, 15, 21, 25, 45, 77, 121, 169, 21853```. These numbers have been found by us to test the overall factorization of an algorithm, including edge cases, multiple factors and other quirks.

If the algorithm has been noted to support factorization to even factors, the function is then tested using the following numbers: ```2, 4, 12, 20, 30```. No further effort has been made to cover edge cases using even numbers. This is due to the fact that not all algorithms support even numbers without alteration. Furthermore, factorizing even numbers is often not interesting in a true to life scenario.

When common tests have been run, any function of the class starting with `test` will be run. To add specific tests to your function, simply define a function like this:

```
...
class MyFactorizationFunction(FactorizationFunction)
    ...
    def testMySpecifics():
        ...
```

##### Benchmarking

Each Factorization Function supports a common interface for benchmarking. See also the implementation details on benchmarking.

To test a Factorization Function, call the `benchmark` function with your number suite and an optional number of iterations for each benchmark (defaults to `10`).

```
MyFactorizationFunction.benchmark(numberSuite, iterations=10)
```

The number suite is expected to follow the following format:

```
# A tuple
(
    # String description of the suite
    description,
    # A list of tuples
    [
        # A tuple
        (
            # Integer indicating amount of factors in this benchmark
            numberOfFactors,
            # A list of tuples
            [
                # A tuple
                (
                    # The number to factorize
                    number,
                    # A list of factors
                    [
                        factor1,
                        factor2,
                        ...
                    ]
                )
            ]
        )
    ]
)
```

For a more comprohensive view, refer to the following example as well as the file `number_suite.sagews`.

An example number suite testing two numbers consisting of two and three factors. The number tested for two factors is `118=1*2*59`. The number tested for three factors is `159953=1*17*97*97`.
```
("Example", [(2, [(118, [1, 2, 59])]), (3, [(159953, [1, 97, 17, 97])])])`
```

To add benchmarks to your function, define benchmarks like this:

```
from benchmark import *
...
class MyFactorizationFunction(FactorizationFunction)
    ...
    def factorize():
        # Setup
        ...
        benchmark = Benchmark()
        # Start of algorithm
        benchmark.start()
        for i in range(10):
            benchmark.iterate()
            benchmark.start("another timer")
            ...
            benchmark.stop("another timer")
        # End of algorithm
        benchmark.stop()
        ...
```

The complete list of parameters supported by `.benchmark()`:
(self, numberSuite, iterations=10, optionalArgs={}, start=2, skipFactors=None):

| Parameter | Default | Description | Required |
| --------- | ------- | ----------- | -------- |
| `numberSuite` | - | See above | Yes |
| `iterations` | `10` | Number of times each number is tested | No |
| `optionalArgs` | `{}`| Map of optional parameter (key) and corresponding value (value) sent to the function that is being benchmarked | No |
| `start` | `2` | The least number of factors to test, no matter the number suite | No |
| `skipFactors` | `None` | A function that accepts a number, `numberOfFactors` and returns a boolean whether or not the benchmark should occur. Allows all numbers if `None` | No |

## Benchmark

Found in `benchmark.py`, the `Benchmark` class is a utility class to keep track of time and iterations.

##### Basic usage

```
# Import the class
from benchmark import *

# Create an instance to store values
benchmark = Benchmark()
benchmark.verbose = True

# Start a benchmark (the default one)
benchmark.start()

print "This is some heavy work"

# Stop the default benchmark
benchmark.stop()

benchmark.start("main loop")
for i in range(2):
    # Add one to the default iteration counter
    benchmark.iterate()
    benchmark.start("inner loop")
    for j in range(2):
        benchmark.iterate()
    benchmark.stop("inner loop")
benchmark.stop("main loop")

# Benchmark uses named timers and iterations
# If none is given, "default" is used - as seen above
benchmark.start("another timer")
benchmark.stop("another timer")
benchmark.iterate("another counter")

# When printing a benchmark, it is automatically formatted to be somewhat easy to read
print benchmark
```

```
This is some heavy work
Benchmark <Total time: {"default": 0.000479, "inner loop": 0.000051, "main loop": 0.000562, "another timer": 0.000119}, iterations: {"default": 6, "another counter": 1}>
```

##### Methods and attributes

A benchmark instance has the following noteworthy attributes:

* `totalTime`: a map where keys are labels and values are total time recorded for label
* `iterations`: a map where keys are labels and values are iterations recorded for label

A benchmark instance has the following noteworthy methods:

* `start(label)`: starts counting time for `label`. `label` defaults to "default"
* `stop(label)`: stops counting time for `label`. `label` defaults to "default"
* `iterate(label)`: add one to `label` iteration counter. `label` defaults to "default"

* `asTables()`: return a latex string describing the benchmark as time and iterations tables - commonly used with Sage's `show()`
* `printEvents()`: an overview of the algorithm. See "Other" below.

A benchmark instance has the following operations:

* `+`: add to benchmarks together - useful when measuring different functions and aggregating the results

Benchmark has the following static functions:

* `min(benchmarks)`: returns the minimum value for each measurement in the benchmarks array as a new benchmark
* `max(benchmarks)`: returns the maximum value for each measurement in the benchmarks array as a new benchmark
* `average(benchmarks)`: returns the average value for each measurement in the benchmarks array as a new benchmark

##### Other

Benchmarking can be used to describe the algorithm rather cleanly. You can try to set `verbose=True` on your `Benchmark` instance to record logs. An overview of the algorithm can the be printed using `.printEvents()`. The output below is from the example above ("Basic usage") with an added call to `benchmark.printEvents()`:

* ▶️: start of a timer
* ⏹: stop of a timer
* 🔂: iteration

```
This is some heavy work
Benchmark <Total time: {"default": 0.000493, "inner loop": 0.000046, "main loop": 0.000550, "another timer": 0.000118}, iterations: {"default": 6, "another counter": 1}>
▶️ default
⏹ default (0.000493 s)
▶️ main loop
	🔂 default
	▶️ inner loop
		🔂 default x 2
	⏹ inner loop (0.000025 s)
	🔂 default
	▶️ inner loop
		🔂 default x 2
	⏹ inner loop (0.000021 s)
⏹ main loop (0.000550 s)
▶️ another timer
⏹ another timer (0.000118)
🔂 another counter
```

__IMPORTANT NOTE__:

Every time either `.start()`, `.stop()` or `.iterate()` is called, somewhere around 40 bytes is added to RAM usage due to the logging of events. This might not seem as much, but when, for example, Lenstra's Elliptic Curve Factorization Method is run on larger numbers it may run several hundred thousand iterations, resulting in multiple gigabytes of RAM usage.

# Disclaimer
<a name="disclaimer"></a>

_This repository holds code created by students. Although the code is most likely correct, it may not promote best practices, be factual or grammatically correct. The code is meant as a future reference for students reading the same or a similar course. The code is also made publically available alongside the report written on the subject._
