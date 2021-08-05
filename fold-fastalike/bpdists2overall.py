import os
import sys
import numpy as np


def bpdists2overall(fp_in, fp_out):

    with open(fp_in, 'r') as f:
        lines = f.readlines()  # Parse header
        header = lines[:2]
        t = int(header[0].strip())  # Length of RNA
        probs = [0]*t  # Initialize list of zero probabilities
        ents = [0]*t
        for line in lines[2:]:
            if line.__contains__('lbox'):
                continue
            if not line.strip():
                continue
            row = line.strip().split()
            i = int(row[0])-1
            j = int(row[1])-1

            # p = 10**-float(row[2])

            p = float(row[2])**2
            probs[i] += p
            probs[j] += p

            if p > 0:
                ent = -p*np.log(p)
                ents[i] += ent
                ents[j] += ent

    if not fp_out:
        fname = os.path.splitext(fp_in)[0]
        fp_out = "{}_overall.txt".format(fname)
    with open(fp_out, 'w') as f:
        f.write("{:d}\n".format(t))
        f.write("i\tP(paired)\tEntropy\n")
        f.write("".join(["{:d}\t{:1.5f}\t{:1.5f}\n".format(i+1, prob, ent)
                         for i, (prob, ent) in enumerate(zip(probs, ents))]))


if __name__ == "__main__":
    f_in = sys.argv[1]
    f_out = None
    if len(sys.argv) > 2:
        f_out = sys.argv[2]
        if len(sys.argv) > 3:
            raise Exception('Too many input arguments provided.')

    bpdists2overall(f_in, f_out)
