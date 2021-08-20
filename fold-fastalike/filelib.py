import os
import warnings
from datetime import datetime


def parse_fastalike(fp_fasta):

    seqs = []

    with open(fp_fasta, 'r') as f:
        while f:
            line = f.readline()
            if not line:
                break
            sequence_name = line.split('>')[1].strip()  # RNA name
            sequence = f.readline().strip()  # Nucleotide sequence

            if not sequence:
                print(f"Warning: empty transcript \"f{sequence_name}\"")
                continue

            seqs.append({'name': sequence_name,
                         'sequence': sequence})

    # Check duplicate RNA names
    names = [seq['name'] for seq in seqs]
    unique_names = create_unique_names(names.copy())

    if unique_names != names:
        warnings.warn('Duplicate RNA names were detected, thus RNA names were augmented with tags '
                      'to ensure uniqueness of processed transcripts. It is recommended to provide '
                      'FASTA files of unique RNA names only.')
        for seq, new_name in zip(seqs, unique_names):  # Set unique names to all transcripts
            seq['name'] = new_name

    return seqs


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def prepare_output_directory(folder_path):
    if folder_path == "-1":
        folder_path = "outputs-{}".format(datetime.now().strftime('%Y%m%d_%H%M%S'))
    make_dir(folder_path)
    return folder_path


def write_dot_bracket(fp, name, seq, db):
    with open(fp, 'w') as f_out:
        f_out.write('> {}\n'.format(name))
        f_out.write('{}\n'.format(seq))
        f_out.write('{}\n'.format(db))


def create_unique_names(names):
    # Store the frequency of strings
    name_counts = {}

    # Iterate over the array
    for i in range(0, len(names)):

        # For the fist occurrence,
        # update the frequency count
        if names[i] not in name_counts:
            name_counts[names[i]] = 1

        # Otherwise
        else:
            count = name_counts[names[i]]
            name_counts[names[i]] += 1

            # Append frequency count
            # to end of the string
            names[i] += '_' + str(count)

    return names
