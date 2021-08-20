import os.path
import shutil
import subprocess
import time


def clear_output():
    if os.path.isdir('tests/test_output/'):
        shutil.rmtree('tests/test_output/')


def version():
    print('fold-fastalike version: ')
    subprocess.run(['python', '-m', 'fold-fastalike', '--version'])


def tests():
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
                    '--output', 'tests/test_output/lunp0',
                    '--lunp', '0'])


def run_tests():
    clear_output()
    version()
    tests()
