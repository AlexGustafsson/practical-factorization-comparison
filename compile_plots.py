# -*- coding: utf-8 -*-
import sys
import os
import shutil

# Note:
# This script is not meant for stable use,
# it was a quick fix to compile the plots used in the paper.
# Proceed with caution!

skeleton = """
\\begin{figure}[H]
\\centering
\\begin{tikzpicture}[scale=0.6, trim axis left, trim axis right]
\\begin{axis}[
    width=1\\textwidth,
    height=1\\textwidth,
    xlabel={$xlabel},
    ylabel={Time taken (s)},
    xmin=$xmin, xmax=$xmax,
    ymin=$ymin, ymax=$ymax,
    xticklabels={$xticklabels},
    xtick={$xtick},
    ytick={$ytick},
    ymajorgrids=true,
    grid style=dashed,
]

\\addplot+[
    blue,
    very thick,
    forget plot,
    only marks
    ]
    plot[
    very thick,
    error bars/.cd,
    y dir=plus,
    y explicit
    ]
    table[x=x,y=y,y error expr=\\thisrow{y-max}] {
    x    y    y-max
    $ymaxtable
    };

\\addplot+[
    blue,
    very thick,
    forget plot,
    only marks
    ]
    plot[
    very thick,
    error bars/.cd,
    y dir=plus,
    y explicit
    ]
    table[x=x,y=y,y error expr=\\thisrow{y-min}] {
    x    y    y-min
    $ymintable
    };

\\end{axis}
\\end{tikzpicture}
\\vspace{-0.3cm}
\\caption{$title}\label{fig:$label}
\\end{figure}
"""

if not os.path.exists("./benchmarks"):
    raise ValueError("No benchmarks found (./benchmarks directory doesn't exist)")

#benchmarks[algorithm][times, iterations][label][number of factors][data]
benchmarks = {}

for filename in os.listdir("./benchmarks"):
    algorithm = filename[0:filename.index("_")]
    file = open("./benchmarks/%s"%filename, "r")
    lines = file.read().splitlines()
    # LenstrasEllipticCurveFactorization (maximumIterations: 10)
# Small close primes
    parameters = lines[0][1+len(algorithm)::]
    parameters = parameters[2::] if parameters != "" else ""
    description = lines[1][2::]
    modeLine = lines[2].split(":")[0]
    mode = "unknown"
    if modeLine == "Number of factors":
        mode = "factors"
    elif modeLine == "Number of bits":
        mode = "bits"
    algorithmID = "%s$%s$%s$%s"%(algorithm, description, parameters, mode)
    for line in lines[3::]:
        columns = line.split(":")
        if (len(columns) < 3):
            continue
        numberOfFactors = columns[0]
        n = columns[1]
        times = columns[2]
        iterations = columns[3] if len(columns) >= 4 else ""
        times = times.split(",")
        times = [x.split("-") for x in times]
        times = {pair[0]: pair[1] for pair in times}

        if iterations != "":
            old = iterations
            iterations = iterations.split(",")
            iterations = [x.split("-") for x in iterations]
            iterations = {pair[0]: pair[1] for pair in iterations}
        else:
            iterations = {}

        if algorithmID not in benchmarks:
            benchmarks[algorithmID] = ({}, {})
        for key in times.keys():
            if key not in benchmarks[algorithmID][0]:
                benchmarks[algorithmID][0][key] = {}
            if numberOfFactors not in benchmarks[algorithmID][0][key]:
                benchmarks[algorithmID][0][key][numberOfFactors] = []
            benchmarks[algorithmID][0][key][numberOfFactors].append(times[key])
        for key in iterations.keys():
            if key not in benchmarks[algorithmID][1]:
                benchmarks[algorithmID][1][key] = {}
            if numberOfFactors not in benchmarks[algorithmID][1][key]:
                benchmarks[algorithmID][1][key][numberOfFactors] = []
            benchmarks[algorithmID][1][key][numberOfFactors].append(iterations[key])

latex = {}
for algorithmID in benchmarks.keys():
    algorithm, description, parameters, mode = algorithmID.split("$")
    xlabel = "Unknown"
    if mode == "factors":
        xlabel = "Number of factors"
    elif mode == "bits":
        xlabel = "Number of bits"
    for i in range(1):
        for label in benchmarks[algorithmID][i].keys():
            title = "%s - %s - %s - %s"%(algorithm, description, label, "total time" if i == 0 else "iterations") + (" %s"%parameters if parameters is not "" else "")
            xtick = ", ".join(map(str, sorted(map(int, benchmarks[algorithmID][i][label].keys()))))
            #ytick = []
            ymaxtable = ""
            ymintable = ""
            globalmax = 0
            globalmin = 0
            for numberOfFactors in benchmarks[algorithmID][i][label].keys():
                yvalues = map(float if i == 0 else int, benchmarks[algorithmID][i][label][numberOfFactors])
                ymax = max(yvalues)
                if ymax > globalmax:
                    globalmax = ymax
                ymin = min(yvalues)
                if globalmin == 0 or ymin < globalmin:
                    globalmin = ymin
                yaverage = sum(yvalues) / len(yvalues)
                ymaxtable += "%s\t%s\t%s\n"%(str(numberOfFactors), str(yaverage), str(ymax-yaverage))
                ymintable += "%s\t%s\t%s\n"%(str(numberOfFactors), str(yaverage), str(ymin-yaverage))
                #ytick += [ymin, yaverage, ymax]
            #ytick = sorted(ytick)[::5]
            ytick = [(globalmax-globalmin)/10*k+globalmin for k in range(0, 10)]
            ytick = ", ".join(map(str, ytick))

            xvalues = sorted(map(float if i == 0 else int, benchmarks[algorithmID][i][label].keys()))
            xmin = str(min(xvalues) - 1)
            xmax = str(max(xvalues) + 1)

            xticklabels = xtick
            plot = skeleton
            plot = plot.replace("$title", title)
            plot = plot.replace("$label", algorithmID.replace(" ", "").replace("$", ""))
            plot = plot.replace("$xticklabels", xticklabels)
            plot = plot.replace("$xtick", xtick)
            plot = plot.replace("$ytick", ytick)
            plot = plot.replace("$xmax", xmax)
            plot = plot.replace("$ymaxtable", ymaxtable)
            plot = plot.replace("$ymintable", ymintable)
            plot = plot.replace("$ymax", str(globalmax))
            plot = plot.replace("$xmin", xmin)
            plot = plot.replace("$ymin", str(globalmin))
            plot = plot.replace("$xlabel", xlabel)
            latex["%s$%s"%(algorithmID, label)] = plot

# Try to remove all plots
try:
    shutil.rmtree("./plots")
except:
    print "No plots found, nothing to remove"

# Try to recreate plots foler
os.makedirs("./plots")

# Write all plots to files
for algorithmID in latex.keys():
    handle = open("./plots/%s.tex"%algorithmID, "w")
    handle.write(latex[algorithmID])
    handle.close()
print "Plots stored"