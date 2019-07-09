#!/usr/bin/env python3

import sys
if len(sys.argv) < 4:
    print("Usage: python3 {} <single_copy.list> <*.pep> <outdir>".format(sys.argv[0]))
    exit()

def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.strip()
        if line.startswith(">"):
            if name:
                name = name[1:]
                yield (name, ''.join(seq))
            name, seq = line, []
        else:
                seq.append(line)
    if name:
        name = name[1:]
        yield (name, ''.join(seq))


def main():
    outdir = sys.argv[3]
    proteins = {}
    with open(sys.argv[2], 'r') as fh:
        for name, seq in read_fasta(fh):
            proteins[name] = seq

    with open(sys.argv[1], 'r') as lh:
        for g in lh:
            tmp = g.strip().split(":")
            og = tmp[0]
            genes = tmp[1].strip().split()
            output = outdir + "/" + og + ".pep"
            with open(output, 'w') as ph:
                for i in genes:
                    ph.write(">" + i + "\n" + proteins[i] + "\n")


if __name__ == '__main__':
    main()


