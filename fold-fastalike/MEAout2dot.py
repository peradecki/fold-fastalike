import sys
import re


def mea_out2dot(output, fp_out):

    name_result = re.search(r'>(.*)[\r\n]', output)
    name = name_result.group(1)

    seq_result = re.search(r'\s([ATGCU]+)[\r\n]', output)
    seq = seq_result.group(1)

    db_result = re.search(r'\s(.*)\s{\s*-?\d*\.?\d+ MEA=-?\d*\.?\d+}', output)
    db = db_result.group(1)

    # print(name)
    # print(seq)
    # print(db)

    assert len(seq) == len(db)

    with open(fp_out, 'w') as f:
        f.write(">{}\n".format(name))
        f.write("{}\n".format(seq))
        f.write("{}\n".format(db))


if __name__ == "__main__":

    output_run = sys.argv[1]
    fp_out = sys.argv[2]
    mea_out2dot(output_run, fp_out)
