︠5e70281a-eca2-4ea2-858b-d9fdc84d4c4fi︠
%md
# Playground

Here you can test the functions and play around with relevant code.
︡aa90d3a2-d3b5-4842-8397-7d67a007e9fc︡{"done":true,"md":"# Playground\n\nHere you can test the functions and play around with relevant code."}
︠1828a5b6-e125-44b8-8d54-bfaf69709ab3i︠
%md
### Trial Division
︡ec436d61-f07b-49d2-b593-27c5f411aa26︡{"done":true,"md":"### Trial Division"}
︠c1e374d0-7914-44f5-a2d9-083181e4b6e3i︠
from trial_division import *
print "Regular trial division:"
TrialDivision.test()
print "\nFast trial division:"
TrialDivision.test({"modified": True})
︡e4a29faf-a242-4372-b514-f2e9a68e7612︡{"stdout":"Regular trial division:\n"}︡{"stdout":"Can run factorization function:  ✓\nCan factorize one or more primes:  ✓\nCan factorize one or more non-primes:  ✓\n"}︡{"stdout":"\nFast trial division:\n"}︡{"stdout":"Can run factorization function:  ✓\nCan factorize one or more primes:  ✓\nCan factorize one or more non-primes:  ✓\n"}︡{"done":true}︡
︠dc0cf90e-645f-4447-a074-135e691539b2i︠
%md
### Fermats Factorization
︡2aedbef3-92d4-4f01-9462-37c14863c289︡{"done":true,"md":"### Fermats Factorization"}
︠ceaf7f81-9c6a-42a4-91be-117367800e04i︠
from fermats_factorization import *
FermatsFactorization.test()
︡7cc051fc-1427-4677-b231-23ca36c04216︡{"stdout":"Can run factorization function:  ✓\nCan factorize one or more primes:  ✓\nCan factorize one or more non-primes: ✘ (Not supported)\n"}︡{"done":true}︡
︠5bc5ccfd-23f1-4689-9af0-a50fd8423156i︠
%md
### Pollards Rho Algorithm
︡39507f70-136c-4737-8319-739b7a651a5b︡{"done":true,"md":"### Pollards Rho Algorithm"}
︠70384e67-1030-4ea4-950e-0d5d0d4556e9i︠
from pollards_rho_algorithm import *
PollardsRhoAlgorithm.test()
︡faa4f558-8634-4ac9-9128-c0eeafe637a5︡{"stdout":"Can run factorization function:  ✓\nCan factorize one or more primes:  ✓\nCan factorize one or more non-primes: ✘ (Not supported)\n"}︡{"done":true}︡
︠2591817c-fc89-4c93-bc54-b65a168bab9bi︠
%md
### Lenstras Elliptic-Curve Factorization
︡7e2bd784-5f81-4b60-9a40-262f85400f38︡{"done":true,"md":"### Lenstras Elliptic-Curve Factorization"}
︠9a542742-9297-4a7b-b376-9d29cf48240dsi︠
from lenstras_elliptic_curve_factorization import *
LenstrasEllipticCurveFactorization.test()
︡6e8bdd22-ac49-4c03-9ed4-2a6cb1b58bf1︡{"stdout":"Can run factorization function:  ✓\nCan factorize one or more primes:  ✓\nCan factorize one or more non-primes: ✘ (Not supported)\n"}︡{"done":true}︡
︠1feb5ccc-a333-44c4-aeb8-0b7f2ccb8b10i︠
%md
### Quadratic Sieve
︡e95448ae-1534-493b-915c-6aef6ece2430︡{"done":true,"md":"### Quadratic Sieve"}
︠23494045-2290-4c2e-89f4-f62d670ddeecsi︠
from quadratic_sieve import *
QuadraticSieve.test()
︡f9e8e3b6-e083-47b1-8d97-0f55a4f43f51︡{"stdout":"=== Common Tests ===\nCan run factorization function:  ✘\nWill abort tests due to error in factorization function\n"}︡{"done":true}︡
︠62e29d3c-a301-4d94-a39b-4a990ab2a0b2s︠
from quadratic_sieve import *

# n         B   V
# 21		    13	30
# 527		29	199
# 651		13	30
# 1271		13	30
# 3385		13	35
# 3465		13	25
# 4699		7	39
# 7161		13	35
# 7905		16	50
# 53357		67	4000
# 87463		19	300
# 356779		29	199
# 9505247	150	500
# 11037757	150	500
# 21593381	139	633

numbersuite = [(21, 13, 30),(527, 29, 199),(651, 13, 30),(1271, 13, 30),(3385, 13, 35),(3465, 13, 25),(4699, 7, 39),(7161, 13, 35),(7905, 16, 50),(53357, 67, 4000),(87463, 19, 300),(356779, 29, 199),(9505247, 150, 500),(11037757, 150, 500),(21593381, 139, 633)]

print "n\tB\tV\tTime"
for n, B, V in numbersuite:
    f, b = QuadraticSieve.factorize(n, True, B, V)
    time = b.totalTime["get base"] + b.totalTime["get A and B"] + b.totalTime["solve equation"] + b.totalTime["calculate factors"]
    print "%d\t%d\t%d\t%f"%(n, B, V, time)
︡2a7ec9c5-8faf-45c7-8d93-7fd4527bf123︡{"stdout":"n\tB\tV\tTime\n"}︡{"stdout":"21\t13\t30\t0.359042"}︡{"stdout":"\n527\t29\t199\t0.632922"}︡{"stdout":"\n651\t13\t30\t0.385670"}︡{"stdout":"\n1271\t13\t30\t0.315143"}︡{"stdout":"\n3385\t13\t35\t0.911191"}︡{"stdout":"\n3465\t13\t25\t1.803482"}︡{"stdout":"\n4699\t7\t39\t0.279919"}︡{"stdout":"\n7161\t13\t35\t14.161240"}︡{"stdout":"\n7905\t16\t50\t3.159273"}︡{"stdout":"\n53357\t67\t4000\t4.012484"}︡{"stdout":"\n87463\t19\t300\t0.746896"}︡{"stdout":"\n356779\t29\t199\t1.812484"}︡{"stdout":"\n9505247\t150\t500\t12.534800"}︡{"stdout":"\n11037757\t150\t500\t249.726870"}︡{"stdout":"\n21593381\t139\t633\t23.047358"}︡{"stdout":"\n"}︡{"done":true}︡
︠e0594d73-c89c-4dba-ac64-60a97199a572i︠
def old_b(x):
    return ceil(15.72376 + (172.0775 - 15.72376)/(1 + (x/2502554)^-1.216504))
def b(x):
    if x < 8000:
        return int(15.96721 + 0.004267273*x - 0.000002936011*x^2 + 4.47707e-10*x^3 - 1.822042e-14*x^4)
    elif x < 60000:
        return 49*x-31
    elif x < 200000:
        return 30
    elif x < 10000000:
        return int(3498354000000000*e^(-(x - 222652600)^2/(2*27162480^2)))
    else:
        return 145
def old_v(x):
    return ceil(659.2523 + (42.34133 - 659.2523)/(1 + (x/1262672)^0.4672363))
def v(x):
    if x < 8000:
        return int(52.54306 + 0.07723664*x - 0.000101534*x^2 + 3.785488e-8*x^3 - 5.496007e-12*x^4 + 2.752281e-16*x^5)
    elif x < 60000:
        return 100
    elif x < 200000:
        return 30
    elif x < 10000000:
        return int(98.54485 + 0.0003157615*x - 9.869007e-11*x^2 + 7.937486e-18*x^3)
    else:
        return int(7042.29 - 0.0009021364*x + 2.803262e-11*x^2)
︡e7f3715a-484e-4db4-af45-bde4b4b86d40︡{"done":true}︡
︠2235b736-8caf-4927-9ec2-cb0a574cc636i︠
from quadratic_sieve import *
#n = 2963*2503
#B = 78
#V = 250
def b(x):
    return int(QuadraticSieve.L(x)/2 - QuadraticSieve.L(x)/4)
def v(x):
    return int(QuadraticSieve.L(x)/2 - QuadraticSieve.L(x)/4 + 10)
︡2d5ed4e2-2032-4ba6-9110-e1c92770324c︡{"done":true}︡
︠14a75b1a-08f0-4a13-b06f-fe5d7417d220︠
%md
### Compile plots
︡ab172225-14fc-426b-a4d3-d69d8c3bc972︡{"done":true,"md":"### Compile plots"}
︠b50abe18-3a2f-440c-b538-fae4382584ce︠
from compile_plots import *
︡83934f74-39ce-4f5e-8a4f-210e86898fcb︡
︠4e644a85-ff53-4c27-990e-34b2139c30abi︠
%md
### Other plot related helper functions
︡c5906ac3-b281-42ea-a534-f44e64913ef1︡{"done":true,"md":"### Other plot related helper functions"}
︠1c539e22-3acb-4a3a-9528-ef45f474c41b︠
def ytick(globalmin, globalmax):
    return "{%s}"%", ".join(map(str, [(globalmax-globalmin)/10*k+globalmin for k in range(0, 10)]))

ytick(0.039878, 93)
︡0564fe06-d8ba-4213-8cc3-723e0de672c1︡{"stdout":"'{0.0398780000000000, 9.33589020000000, 18.6319024000000, 27.9279146000000, 37.2239268000000, 46.5199390000000, 55.8159512000000, 65.1119634000000, 74.4079756000000, 83.7039878000000}'\n"}︡{"done":true}︡
︠1a116f54-4075-4f0c-a7f9-c3e5b0437d30s︠
y = range(2, 16, 1)
wanted = range(2, len(y), 2)
"{%s}"%", ".join([str(y[i]) if y[i] in wanted else "" for i in range(len(y))])
︡c3f4f1b7-573d-44ae-b40f-45c9c6a74d3c︡{"stdout":"'{2, , 4, , 6, , 8, , 10, , 12, , , }'\n"}︡{"done":true}︡
︠d064fb8d-558c-4231-8653-a4a7aeedb7cfi︠
%md
### Compile comparison plot
︡b8630649-257b-4f28-b0d1-ef1eeb80a911︡{"done":true,"md":"### Compile comparison plot"}
︠3300d3a8-570a-4579-822a-b008aef6ea9aio︠
wantedKeys = ["PollardsRhoAlgorithm$Growing primes$$bits", "TrialDivision$large primes$(modified: True)$factors", "TrialDivision$Medium close primes$$factors", "TrialDivision$Larger primes$(modified: True)$factors", "TrialDivision$Small close primes$(modified: True)$factors", "PollardsRhoAlgorithm$medium primes$$factors", "LenstrasEllipticCurveFactorization$large primes$$factors", "LenstrasEllipticCurveFactorization$Small close primes$$factors", "PollardsRhoAlgorithm$Medium close primes$$factors", "TrialDivision$medium primes$$factors", "TrialDivision$Growing primes$$bits", "LenstrasEllipticCurveFactorization$Medium close primes$$factors", "FermatsFactorization$Medium close primes$$factors", "PollardsRhoAlgorithm$Small close primes$$factors", "PollardsRhoAlgorithm$Large close primes$$factors", "PollardsRhoAlgorithm$large primes$$factors", "LenstrasEllipticCurveFactorization$Growing primes$$bits", "TrialDivision$large primes$$factors", "FermatsFactorization$medium primes$$factors", "TrialDivision$small primes$$factors", "LenstrasEllipticCurveFactorization$small primes$$factors", "TrialDivision$Large close primes$$factors", "LenstrasEllipticCurveFactorization$Larger primes$$factors", "PollardsRhoAlgorithm$Larger primes$$factors", "FermatsFactorization$small primes$$factors", "PollardsRhoAlgorithm$small primes$$factors", "TrialDivision$Medium close primes$(modified: True)$factors", "TrialDivision$Larger primes$$factors", "FermatsFactorization$Growing primes$$bits", "TrialDivision$Growing primes$(modified: True)$bits", "LenstrasEllipticCurveFactorization$Large close primes$$factors", "FermatsFactorization$Small close primes$$factors", "LenstrasEllipticCurveFactorization$medium primes$$factors", "TrialDivision$Small close primes$$factors", "TrialDivision$small primes$(modified: True)$factors", "TrialDivision$Large close primes$(modified: True)$factors", "TrialDivision$medium primes$(modified: True)$factors"]

numberSuites = {}
for key in wantedKeys:
    suite = key.split("$")[1]
    if suite not in numberSuites:
        numberSuites[suite] = []
    numberSuites[suite].append(key)

values = {}
for suite, keys in numberSuites.items():
    for key in keys:
        values[key] = {i: min(map(float, benchmarks[key][0]["default"][i])) for i in benchmarks[key][0]["default"].keys()}
︡b0fa32e1-ec9a-4d6a-81ba-5765b9cc877a︡{"done":true}︡
︠06ff8258-b93e-45a0-b4d5-6b658e0ce7b2io︠
lowest = {}

for key in values:
    if "Growing" not in key:
        continue
    print key
    minKey = min(map(int, values[key].keys()))
    maxKey = max(map(int, values[key].keys()))
    minValue = min(map(float, values[key].values()))
    maxValue = max(map(float, values[key].values()))
    print "%d, %d"%(minKey, maxKey)
    print "%f, %f"%(minValue, maxValue)
    for i in range(2, maxKey+1):
        k = str(i)
        v = values[key][k]
        if k not in lowest:
            lowest[k] = ("unknown", -1)
        if lowest[k][1] == -1 or v < lowest[k][1]:
            lowest[k] = (key.split("$")[0], v)
        print "%s\t%s"%(k, v)
    print "\n-----\n"
︡9c084ebc-ef69-4af0-8eec-76c1097e961b︡{"stdout":"FermatsFactorization$Growing primes$$bits\n2, 42\n0.000007, 22132.913785\n2\t7e-06\n3\t1.2e-05\n4\t1.2e-05\n5\t1.3e-05\n6\t1.2e-05\n7\t1.2e-05\n8\t1.2e-05\n9\t1.2e-05\n10\t2e-05\n11\t1.2e-05\n12\t0.000248\n13\t0.000395\n14\t0.000193\n15\t4.3e-05\n16\t3.4e-05\n17\t0.001709\n18\t0.054375\n19\t0.008587\n20\t0.015791\n21\t0.003153\n22\t1.554476\n23\t0.060514\n24\t1.728928\n25\t3.631607\n26\t0.14655\n27\t0.085645\n28\t5.815362\n29\t33.053399\n30\t226.758307\n31\t17.447728\n32\t0.004225\n33\t176.186694\n34\t10.152104\n35\t2724.053894\n36\t1222.896002\n37\t1.186023\n38\t22132.913785\n39\t2120.144309\n40\t11128.625773\n41\t15742.323432\n42\t4071.78641\n\n-----\n\nTrialDivision$Growing primes$(modified: True)$bits\n2, 33\n0.000021, 9208.879762\n2\t2.1e-05\n3\t2.7e-05\n4\t4.2e-05\n5\t5.5e-05\n6\t7.3e-05\n7\t0.000132\n8\t0.000199\n9\t0.000454\n10\t0.000822\n11\t0.001141\n12\t0.005496\n13\t0.00855\n14\t0.014583\n15\t0.025985\n16\t0.063302\n17\t0.099917\n18\t0.398008\n19\t0.592638\n20\t0.888626\n21\t1.386275\n22\t7.642371\n23\t8.677196\n24\t23.084672\n25\t43.861922\n26\t57.12664\n27\t100.000305\n28\t298.17366\n29\t541.862359\n30\t1579.287302\n31\t1663.577217\n32\t4126.774185\n33\t9208.879762\n\n-----\n\nPollardsRhoAlgorithm$Growing primes$$bits\n2, 60\n0.000015, 11321.818036\n2\t2e-05\n3\t1.5e-05\n4\t2.5e-05\n5\t4.4e-05\n6\t4.4e-05\n7\t6.9e-05\n8\t0.000111\n9\t0.000136\n10\t0.000311\n11\t9.3e-05\n12\t0.000129\n13\t0.000845\n14\t0.000957\n15\t0.001752\n16\t0.001157\n17\t0.005106\n18\t0.001918\n19\t0.003824\n20\t0.008817\n21\t0.005369\n22\t0.010484\n23\t0.004726\n24\t0.033146\n25\t0.064159\n26\t0.043284\n27\t0.035551\n28\t0.084783\n29\t0.191224\n30\t0.161975\n31\t0.078828\n32\t0.849543\n33\t0.439183\n34\t0.310229\n35\t0.926861\n36\t2.69102\n37\t1.311169\n38\t1.542419\n39\t10.141911\n40\t5.029217\n41\t12.837914\n42\t33.154922\n43\t17.83201\n44\t76.279777\n45\t91.73595\n46\t101.69973\n47\t120.210968\n48\t108.761925\n49\t71.629152\n50\t149.559654\n51\t533.089112\n52\t260.846512\n53\t1288.400668\n54\t1460.274068\n55\t1498.098507\n56\t3083.286482\n57\t1583.803046\n58\t8416.254496\n59\t11321.818036\n60\t9655.960219\n\n-----\n\nTrialDivision$Growing primes$$bits\n2, 31\n0.000025, 3317.729958\n2\t2.5e-05\n3\t3.5e-05\n4\t6.6e-05\n5\t9.5e-05\n6\t0.000126\n7\t0.000245\n8\t0.000383\n9\t0.000895\n10\t0.001621\n11\t0.002277\n12\t0.011034\n13\t0.017062\n14\t0.029064\n15\t0.051494\n16\t0.126403\n17\t0.19966\n18\t0.800795\n19\t1.184511\n20\t1.766958\n21\t2.722402\n22\t15.131646\n23\t17.208378\n24\t46.139483\n25\t87.671617\n26\t114.011857\n27\t200.506368\n28\t604.359222\n29\t1079.771318\n30\t3166.677136\n31\t3317.729958\n\n-----\n\nLenstrasEllipticCurveFactorization$Growing primes$$bits\n2, 31\n0.000003, 4278.084354\n2\t3e-06\n3\t5e-06\n4\t5e-06\n5\t1.6e-05\n6\t1.6e-05\n7\t4e-06\n8\t2.8e-05\n9\t0.000207\n10\t4e-06\n11\t0.000292\n12\t0.001117\n13\t0.001211\n14\t0.00613\n15\t0.000197\n16\t0.000826\n17\t0.028723\n18\t0.054721\n19\t0.355728\n20\t0.059941\n21\t0.04495\n22\t1.432769\n23\t0.965226\n24\t4.155155\n25\t29.678446\n26\t4.422546\n27\t0.506453\n28\t275.493572\n29\t299.483471\n30\t1895.64421\n31\t4278.084354\n\n-----\n\n"}︡{"done":true}︡
︠eb083d97-8549-4351-b36b-433f43c86ea4oi︠
minKey = min(map(int, lowest.keys()))
maxKey = max(map(int, lowest.keys()))

times = {}

for i in range(minKey, maxKey+1):
    key = str(i)
    algo = lowest[key][0]
    if algo not in times:
        times[algo] = 0
    times[algo] += 1
    print "%s\t%s\t%f"%(key, lowest[key][0], float(lowest[key][1]))
times
︡67fb1788-c1a5-496e-9551-4b37c246e1ee︡{"stdout":"2\tLenstrasEllipticCurveFactorization\t0.000003\n3\tLenstrasEllipticCurveFactorization\t0.000005\n4\tLenstrasEllipticCurveFactorization\t0.000005\n5\tFermatsFactorization\t0.000013\n6\tFermatsFactorization\t0.000012\n7\tLenstrasEllipticCurveFactorization\t0.000004\n8\tFermatsFactorization\t0.000012\n9\tFermatsFactorization\t0.000012\n10\tLenstrasEllipticCurveFactorization\t0.000004\n11\tFermatsFactorization\t0.000012\n12\tPollardsRhoAlgorithm\t0.000129\n13\tFermatsFactorization\t0.000395\n14\tFermatsFactorization\t0.000193\n15\tFermatsFactorization\t0.000043\n16\tFermatsFactorization\t0.000034\n17\tFermatsFactorization\t0.001709\n18\tPollardsRhoAlgorithm\t0.001918\n19\tPollardsRhoAlgorithm\t0.003824\n20\tPollardsRhoAlgorithm\t0.008817\n21\tFermatsFactorization\t0.003153\n22\tPollardsRhoAlgorithm\t0.010484\n23\tPollardsRhoAlgorithm\t0.004726\n24\tPollardsRhoAlgorithm\t0.033146\n25\tPollardsRhoAlgorithm\t0.064159\n26\tPollardsRhoAlgorithm\t0.043284\n27\tPollardsRhoAlgorithm\t0.035551\n28\tPollardsRhoAlgorithm\t0.084783\n29\tPollardsRhoAlgorithm\t0.191224\n30\tPollardsRhoAlgorithm\t0.161975\n31\tPollardsRhoAlgorithm\t0.078828\n32\tFermatsFactorization\t0.004225\n33\tPollardsRhoAlgorithm\t0.439183\n34\tPollardsRhoAlgorithm\t0.310229\n35\tPollardsRhoAlgorithm\t0.926861\n36\tPollardsRhoAlgorithm\t2.691020\n37\tFermatsFactorization\t1.186023\n38\tPollardsRhoAlgorithm\t1.542419\n39\tPollardsRhoAlgorithm\t10.141911\n40\tPollardsRhoAlgorithm\t5.029217\n41\tPollardsRhoAlgorithm\t12.837914\n42\tPollardsRhoAlgorithm\t33.154922\n43\tPollardsRhoAlgorithm\t17.832010\n44\tPollardsRhoAlgorithm\t76.279777\n45\tPollardsRhoAlgorithm\t91.735950\n46\tPollardsRhoAlgorithm\t101.699730\n47\tPollardsRhoAlgorithm\t120.210968\n48\tPollardsRhoAlgorithm\t108.761925\n49\tPollardsRhoAlgorithm\t71.629152\n50\tPollardsRhoAlgorithm\t149.559654\n51\tPollardsRhoAlgorithm\t533.089112\n52\tPollardsRhoAlgorithm\t260.846512\n53\tPollardsRhoAlgorithm\t1288.400668\n54\tPollardsRhoAlgorithm\t1460.274068\n55\tPollardsRhoAlgorithm\t1498.098507\n56\tPollardsRhoAlgorithm\t3083.286482\n57\tPollardsRhoAlgorithm\t1583.803046\n58\tPollardsRhoAlgorithm\t8416.254496\n59\tPollardsRhoAlgorithm\t11321.818036\n60\tPollardsRhoAlgorithm\t9655.960219\n"}︡{"stdout":"{'PollardsRhoAlgorithm': 41, 'FermatsFactorization': 13, 'LenstrasEllipticCurveFactorization': 5}\n"}︡{"done":true}︡
︠71628e47-6eb8-486b-b32e-e87aaf35bfa1









