import os.path
import shutil
import subprocess
import time
import pathlib


# Handle paths and prepare output
test_folder = pathlib.Path(__file__).parent.resolve()
output_folder = os.path.join(test_folder, 'test_outputs')
if os.path.isdir(output_folder):
    shutil.rmtree(output_folder)


def test_version():
    print('fold-fastalike version: ')
    subprocess.run(['python', '-m', 'fold-fastalike', '--version'])


def test_commands():
    print('Running test commands ... ')
    time.sleep(1)
    subprocess.run(['python', '-m', 'fold-fastalike', 'tests/test_sequences.fasta',
                    '--output', 'tests/test_output/ff/',
                    '--fold'])

    subprocess.run(['python', '-m', 'fold-fastalike', 'tests/test_sequences.fasta',
                    '--output', 'tests/test_output/lunp1/',
                    '--lunp', '1'])

    subprocess.run(['python', '-m', 'fold-fastalike', 'tests/test_sequences.fasta',
                    '--output', 'tests/test_output/lunp10',
                    '--lunp', '10'])

    subprocess.run(['python', '-m', 'fold-fastalike', 'tests/test_sequences.fasta',
                    '--output', 'tests/test_output/lunp0',
                    '--lunp', '0'])

    subprocess.run(['python', '-m', 'fold-fastalike', 'tests/test_sequences.fasta',
                    '--output', 'tests/test_output/MEA',
                    '--MEA'])
