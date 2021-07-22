import sys
import re


def postscript2bpdists(fp_ps_in, fp_txt_out):

    file = open(fp_ps_in, 'r')
    ps_input = file.read()
    file.close()

    seq_result = re.search(r'/sequence { \(\\[\n\r]([\S\n ]+)[\n\r]\) } def', ps_input)
    seq = seq_result.group(1).replace('\\', '').replace('\n', '')

    bpdists_result = re.search(r'%start of base pair probability data[\n\r]([\S\n ]+)[\n\r]showpage', ps_input)
    bpdists = bpdists_result.group(1)

    with open(fp_txt_out, 'w') as f:
        f.write('{}\n'.format(len(seq)))
        f.write('i j sqrt(P(i,j))\n')
        for line in bpdists.split('\n'):
            line = line.replace('ubox', '')
            f.write("{}\n".format(line))


if __name__ == "__main__":

    fp_ps = sys.argv[1]
    fp_out = sys.argv[2]
    postscript2bpdists(fp_ps, fp_out)
