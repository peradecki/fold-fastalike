# fold-fastalike


This parallelized Python tool reads in a fasta-like file and performs various RNA folding analyses.


## Overview

The tool reads in a fasta-like file and performs various RNA folding analyses using the [ViennaRNA](https://www.tbi.univie.ac.at/RNA/) toolset.

Currently, it's capable of:
* Generating minimum free energy (MFE) structures in dot-bracket format (`--fold` flag)
* Computing base-pairing probabilities for all possible i, j partners (`--fold` flag)
* Computing overall base-pairing probability profiles (Prob(paired) / Prob(unpaired)) (`--fold` flag)
* Computing Shannon entropy profiles (`--fold` flag)
* Producing pairing probability "dot-plots" in PDF format (`--fold` flag)
* Generating maximum expected accuracy (MEA) structures in dot-bracket format (`--MEA` flag)
* Computing unpaired segment probabilities (the probability of an unpaired run of length *L* at each position) (`--lunp [LUNP]` flag)
 
All outputs will be saved to a folder that contains a folder for each transcript in the provided fasta-like file. Within each of these folders will be the generated files.

It does not currently support the incorporation of structure profiling data (reactivities).


## Installation

No automated installation routines are currently configured, but it's recommended to add the folder containing the `fold-fastalike` module to your `$PYTHONPATH` so that the tool can be called from anywhere. If you don't add the module to your path, you'll only be able to call the module when your current working directory is this repository.

The tool has a set of required dependecies in order to properly function:
* Python 3 with `numpy` and `tqdm` installed
* [ViennaRNA](https://www.tbi.univie.ac.at/RNA/documentation.html) command line tools (`RNAfold`, `RNAplfold`, etc.)
* [`ps2pdf14`](https://manpages.debian.org/stretch/ghostscript/ps2pdf14.1.en.html) (comes preinstalled on some systems, otherwise most easily installed as a part of [Ghostscript](https://www.ghostscript.com) with [HomeBrew](https://formulae.brew.sh/formula/ghostscript))


## Usage

`fold-fastalike` is a Python module that can be run with the syntax `python -m fold-fastalike [input] [OPTIONS]`. The input should be a fasta-like file containing a set of RNA sequences for processing (see `sample_data`). Any type of FASTA-formatted file should work so long as the transcript names are preceeded by `>` at the beginning of the line and the nucleotide sequence is provided below it.

Run `python -m fold-fastalike --version` to check that your Python interpreter is functional and the correct version of the module is returned.

Run `python -m fold-fastalike -h` to see available options.

```
usage: fold-fastalike [-h] [--version] [--output output] [--lunp LUNP] [--MEA]
                      [--fold] [--tasks TASKS]
                      input

Fold and process information for a batch of sequences in a fasta-like file.

positional arguments:
  input            the input fasta-like file to process.

optional arguments:
  -h, --help       show this help message and exit
  --version        show program's version number and exit
  --output output  the output directory to use when generating outputs for
                   each sequence. Defaults to a date-stamped folder with the
                   prefix outputs in the same location as the command was
                   called
  --lunp LUNP      compute unpaired run probabilities up to length LUNP
  --MEA            compute Maximum Expected Accuracy (MEA) structures
  --fold           compute MFE structure and partition function.
  --tasks TASKS    Number of parallel tasks to use. Default is to use all
                   available.
```

## Examples

The simplest use of the module is via the `--fold` flag. This activates the MFE and base pair probability routines.

For example: 

`python -m fold-fastalike sample_data/test_sequences.fasta --fold`

This will create a folder called `outputs-{%date%}_{%time%}` and four folders within this folder, one for each transcript in the used file. Each folder will have:

* `{%name%}.fasta` >> Single-transcript fasta file
* `{%name%}_dotplot.pdf` >> Dot-plot in PDF format
* `{%name%}_dotplot.ps` >> Dot-plot is PostScript format
* `{%name%}_mfe.dot` >> MFE structure in dot-bracket format
* `{%name%}_bpdists.txt` >> Pairing probabilities (Prob(i, j)) in text format
* `{%name%}_profiles.txt` >> Overall pairing probabilities (P(paired)) and entropy profiles


### Compute MEA structures

To compute MFE structures and a PDF dot-plot for each transcript in the provided sample data, run

`python -m fold-fastalike sample_data/test_sequences.fasta --MEA`

Outputs will be produced with the same folder structure as before, and each folder will have:

* `{%name%}.fasta` >> Single-transcript fasta file
* `{%name%}_mea.dot` >> MFE structure in dot-bracket format


### Compute unpaired run probabilities

To compute the probabilities of unpaired runs up to a certain length across the provided transcripts, run

`python -m fold-fastalike sample_data/test_sequences.fasta --lunp [LUNP]`

For instance, to compute probabilities up to a length of 10 nt, we would run:

`python -m fold-fastalike sample_data/test_sequences.fasta --lunp 10`

Outputs will be produced with the same folder structure as before, and each folder will have:

* `{%name%}.fasta` >> Single-transcript fasta file
* `{%name%}_unpaired_run_probs.ps` >> Unpaired run probabilities in PostScript format


### Notes

* The program will, by default, create a new output folder each time that it's called. To instead save outputs to a predefined location, use the `--output [output]` flag to specify an output directory.

* Base pairing probabilities of the form Prob(i,j) are typically encoded as the square-root of the actual value. Note the headers of the relevant files and be sure to convert to the raw probabilities by squaring when necessary.

* The routines used to post-process some ViennaRNA outputs are also available within the module as standalone scripts.
    * `python -m fold-fastalike.postscript2bpdists [PS_FILE_IN] [TXT_FILE_OUT]`
    * `python -m fold-fastalike.bpdists2overall [TXT_FILE_IN] [TXT_FILE_OUT]`