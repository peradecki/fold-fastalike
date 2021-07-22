# fold-fastalike


This tool reads in a fasta-like file and performs various RNA folding analyses.


## Overview

This tool reads in a fasta-like file and performs various RNA folding analyses using the [ViennaRNA](https://www.tbi.univie.ac.at/RNA/) toolset.

Currently, it's capable of:
* Generating minimum free energy (MFE) structures in dot-bracket format (`--MFE` flag)
* Computing base-pairing probabilities for all i, j partners (`--pfold` flag)
* Computing overall base-pairing probability profiles (Prob(paired) / Prob(unpaired)) (`--pfold` flag)
* Computing Shannon entropy profiles (`--pfold` flag)
* Producing pairing probability "dot-plots" in PDF format (`--MFE` flag)
* Computing unpaired segment probabilities (the probability of an unpaired run of length *L* at each position) (`--lunp [L]` flag)
 
All outputs will be saved to a folder that contains a folder for each transcript in the provided fasta-like file. Within each of these folders will be the generated files.

It does not currently support the incorporation of structure profiling data (reactivities).


## Installation

No automated installation routines are currently configured, but it's recommended to add the folder containing the `fold-fastalike` module to your `$PYTHONPATH` so that the tool can be called from anywhere. If you don't add the module to your path, you'll only be able to call the module when your current working directory is this repository.

The tool has a set of dependecies in order to properly function:
* Python 3 with `numpy` installed
* ViennaRNA command line tools (`RNAfold`, `RNAplfold`, etc.)
* [`ps2pdf14`](https://manpages.debian.org/stretch/ghostscript/ps2pdf14.1.en.html) (comes preinstalled on some systems, otherwise most easily installed as a part of [Ghostscript](https://www.ghostscript.com) with [HomeBrew](https://formulae.brew.sh/formula/ghostscript))


## Usage

`fold-fastalike` is a Python module that can be run with the syntax `python -m fold-fastalike [OPTIONS]`.

Run `python -m fold-fastalike --version` to check that your Python interpreter is functional and the correct version of the module is returned.




## Examples



### Notes