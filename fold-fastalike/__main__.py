import sys
import argparse
import multiprocessing
from tqdm import tqdm
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
                    help="the input fasta-like file to process.")
parser.add_argument("--output", type=str, metavar="output",
                    default="-1",
                    help="the output directory to use when generating outputs for each sequence. Defaults "
                         "to a date-stamped folder with the prefix ""outputs"" in the same location as"
                         " the command was called")
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
parser.add_argument("--tasks", type=int, default=0,
                    help="Number of parallel tasks to use. Default is to use all available.")


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

    if args.tasks == 0:
        tasks = multiprocessing.cpu_count()
    else:
        tasks = args.tasks

    P = multiprocessing.Pool(processes=tasks, maxtasksperchild=1000)

    with tqdm(total=len(seqs), leave=True, unit='transcript', desc='  Progress') as pbar:
        for result in P.imap_unordered(FoldPipeline.process_sequence_wrapper,
                                       ({'rna_name': seq['name'], 'sequence': seq['sequence']} for seq in seqs)):
            pbar.update()

    P.close()
    P.join()

    # for seq in seqs:
    #     FoldPipeline.process_sequence(seq['name'], seq['sequence'])

    print("... done.")
