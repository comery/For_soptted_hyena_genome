#!/usr/bin/env python3

import sys
import glob,os
if len(sys.argv) < 4:
    print("Usage: python3 {} <inputdir> <suffix> <all.gblocks.phy>".format(sys.argv[0]))
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
    #suffix=input('Input the prefix of images:')
    suffix = sys.argv[2]
    inputdir = sys.argv[1]
    files = glob.glob(inputdir + '/*-' + suffix)

    gblocks = {}
    for f in files:
        #print("process..." + f)
        with open(f, 'r') as fh:
            for name, seq in read_fasta(fh):
                species = name.split("|")[0]
                seq = seq.replace(" ", "")
                if species not in gblocks.keys():
                    gblocks[species] = seq
                else:
                    gblocks[species] += seq
    species_num = len(gblocks.keys())
    length = len(list(gblocks.values())[0])

    with open(sys.argv[3], 'w') as fh:
        fh.write("{} {}\n".format(species_num, length))
        for x in gblocks.keys():
            fh.write("{} {}\n".format(x, gblocks[x]))


if __name__ == '__main__':
    main()


