#!/usr/bin/env bash

# This scripts take all python source code files and
# format them to be syntax highlit and includable in LaTex.
# All output files will be in ./appendices.

# Create the (temporary) directory ./appendices if needed
mkdir -p appendices

# Create a file to be included in LaTex
echo "% This file should be included in the article" > appendices/appendices.tex

# For each python file
ls | grep ".py$" | while read -r filename ; do
    # Get LaTeX file name
    safeName=$(echo "$filename" | sed -e "s/_/\\\_/g")
    out=$(echo "$filename" | sed -e "s/.py/.tex/g")
    # Write LaTeX heading
    echo "\\chapter{$safeName}" > "appendices/$out"
    echo "\\begin{minted}[frame=lines, framesep=2mm, baselinestretch=1.2, bgcolor=white, fontsize=\\footnotesize, linenos]{python}" >> "appendices/$out"
    # Append file content
    cat $filename >> "appendices/$out"
    echo "" >> "appendices/$out"
    # Append LaTeX footer
    echo "\end{minted}" >> "appendices/$out"
    # Append filename to included in appendices
    echo "\\input{appendices/$out}" >> appendices/appendices.tex
done



# Zip the appendices
zip -r appendices.zip appendices

# Remove the temporary folder
rm -r appendices