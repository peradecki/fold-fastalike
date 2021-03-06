import os
import re
import subprocess
from . import filelib
from . import postscript2bpdists
from . import bpdists2overall


class FoldPipeline:
    def __init__(self, configuration):
        self.lunp = configuration['lunp']
        self.MEA = configuration['MEA']
        self.fold = configuration['fold']
        self.output = configuration['output']

    def process_sequence(self, rna_name, sequence):

        output_directory = os.path.join(self.output, rna_name)

        self.make_output_directory(rna_name)
        fasta = self.make_fasta(rna_name, sequence)

        # Run RNAfold to get MFE structure
        if self.fold:
            db, mfe = run_rnafold(output_directory, rna_name, fasta)
            filelib.write_dot_bracket(os.path.join(output_directory, f'{rna_name}_mfe.dot'),
                                      rna_name + ' (MFE={})'.format(mfe), sequence, db)

        # Get maximum expected accuracy (MEA) structure
        if self.MEA:
            db = run_rnafold_MEA(output_directory, fasta)
            filelib.write_dot_bracket(os.path.join(output_directory, f'{rna_name}_mea.dot'), rna_name, sequence, db)

        # Get probabilities of unpaired segments of a given length
        if self.lunp:
            run_rnaplfold_lunp(output_directory, rna_name, sequence, lunp=self.lunp)

        cleanup(output_directory, rna_name)

        return

    def process_sequence_wrapper(self, rna):
        return self.process_sequence(rna['rna_name'], rna['sequence'])

    def make_output_directory(self, rna_name):
        output_directory = os.path.join(self.output, rna_name)
        filelib.make_dir(output_directory)

    def make_fasta(self, rna_name, sequence):
        output_directory = os.path.join(self.output, rna_name)
        fp_out = os.path.join(output_directory, '{}.fasta'.format(rna_name))
        with open(fp_out, 'w') as f:
            f.write(">{}\n".format(rna_name))
            f.write("{}".format(sequence))
        return fp_out.split('/')[-1]


def run_rnafold(folder, name, file):

    main_folder = os.getcwd()
    os.chdir(folder)  # Enter relevant folder
    # Fold and capture output
    captured_output = subprocess.run(['RNAfold', '-p', '--noPS', f'{file}'], capture_output=True)
    subprocess.run(['mv', f'{name}_dp.ps', f'{name}_dotplot.ps'])  # Rename dot-plot
    subprocess.run(['ps2pdf14', '-dEPSCrop', f'{name}_dotplot.ps'])  # Convert dot-plot to PDF
    postscript2bpdists.postscript2bpdists(f'{name}_dotplot.ps', f'{name}_bpdists.txt')  # Parse outputs
    bpdists2overall.bpdists2overall(f'{name}_bpdists.txt', f'{name}_profiles.txt')  # Compute P(paired) and entropy
    os.chdir(main_folder)  # Return to original folder

    db_result = re.search(r'[\\n]([.()]+)[\s]', str(captured_output.stdout))  # Parse dot-bracket from output
    db = db_result.group(1)
    mfe_result = re.search(r'\((\s?\s?-?\d*\.?\d+)\)', str(captured_output.stdout))  # Parse MFE from output
    mfe = mfe_result.group(1)

    return db, mfe


def run_rnafold_MEA(folder, file):

    main_folder = os.getcwd()
    os.chdir(folder)  # Enter relevant folder
    # Fold and capture output
    captured_output = subprocess.run(['RNAfold', '--MEA', '--noPS', f'{file}'], capture_output=True)
    os.chdir(main_folder)  # Return to original folder

    db_result = re.search(r'[\\n]([.()]+)[\s]', str(captured_output.stdout))  # Parse dot-bracket from output
    db = db_result.group(1)

    return db


def run_rnaplfold_lunp(folder, name, sequence, lunp):
    rna_length = len(sequence)
    main_folder = os.getcwd()
    os.chdir(folder)  # Enter relevant folder
    # Compute full pairing probabilities with RNAplfold
    subprocess.run(['RNAplfold', '-W', f'{rna_length}', '-u', f'{lunp}'], input=bytes(sequence, 'utf-8'))
    subprocess.run(['mv', 'plfold_lunp', f'{name}_unpaired_run_probs.txt'])  # Rename output file
    os.chdir(main_folder)  # Return to original folder


def cleanup(folder, name):
    main_folder = os.getcwd()
    os.chdir(folder)  # Enter relevant folder and delete extraneous files
    if os.path.exists('rna_ss.ps'):
        os.remove('rna_ss.ps')
    if os.path.exists('rna_dotplot.ps'):
        os.remove('rna_dotplot.ps')
    if os.path.exists('plfold_dp.ps'):
        os.remove('plfold_dp.ps')
    if os.path.exists(f'{name}_dp.ps'):
        os.remove(f'{name}_dp.ps')
    os.chdir(main_folder)
