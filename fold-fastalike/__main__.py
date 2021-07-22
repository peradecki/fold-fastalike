import sys
import argparse
from . import filelib
from . import foldlib

parser = argparse.ArgumentParser(prog="fold-fastalike",
                                 description="Fold and process information for a batch of sequences "
                                             "in a fasta-like file.",
                                 epilog="")
parser.add_argument("--version",
                    action="version",
                    version="1.0")
parser.add_argument("input", type=str, metavar="input",
                    help="The input fasta-like file to process.")
parser.add_argument("--output", type=str, metavar="output",
                    default="-1",
                    help="the output directory to use when generating outputs for each sequence. Defaults "
                         "to a date-stamped folder with the prefix ""outputs"" in the same location as"
                         " the command was called.")
parser.add_argument("--lunp", type=int, default=0,
                    help="compute unpaired run probabilities up to length LUNP")
parser.add_argument("--MFE", action="store_true",
                    help="compute Minimum Free Energy (MEA) structures")
parser.add_argument("--MEA", action="store_true",
                    help="compute Maximum Expected Accuracy (MEA) structures")
parser.add_argument("--pfold", action="store_true",
                    help="compute all base-pairing probabilities and Shannon entropies")
parser.add_argument("--full-fold", action="store_true",
                    help="activates --MFE, --MEA, and --pfold")


if __name__ == "__main__":

    args = parser.parse_args(sys.argv[1:])
    seqs = filelib.parse_fastalike(args.input)

    output = filelib.prepare_output_directory(args.output)

    FoldPipeline = foldlib.FoldPipeline(configuration={'output': output,
                                                       'lunp': args.lunp,
                                                       'MEA': args.MEA,
                                                       'MFE': args.MFE,
                                                       'pfold': args.pfold,
                                                       'full-fold': args.full_fold})

    for seq in seqs:
        FoldPipeline.process_sequence(seq['name'], seq['sequence'])

    print("... done.")
