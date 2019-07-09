#!/usr/bin/env python3

import sys
if len(sys.argv) < 4:
    print("Usage: python3 {} <catelog> <mclOutput2groupsFile> <result.stat>".format(sys.argv[0]))
    exit()

def get_sps(catalog_file):
    species = []
    with open(catalog_file) as fh:
        for i in fh:
            tmp = i.strip().split()
            species.append(tmp[0])
    return species

def record_stat(species, record):
    copies = {}
    # init gene's copy number for each species
    for i in species:
        copies[i] = 0
    # scan genes in this OR group
    res = record.split()
    for r in res:
        tag = r.split("|")[0]
        gene = r.split("|")[1]
        copies[tag] += 1

    copy_number = []
    tmp = []
    total_genes = 0
    spec_num = 0
    for s in species:
        tmp.append(copies[s])
        total_genes += copies[s]
        if copies[s] > 0:
            spec_num += 1
    copy_number.append(total_genes)
    for t in tmp:
        copy_number.append(t)
    ## appending species number (of gene number >0) to this array
    copy_number.append(spec_num)
    return copy_number

def main():
    species = get_sps(sys.argv[1])
    orthologs = []
    copy_matrix = []
    with open(sys.argv[2], 'r') as fh:
        for line in fh:
            tmp = line.strip().split(":")
            orgh = tmp[0]
            record = tmp[1]
            if len(record) == 0:
                continue
            orthologs.append(orgh)
            copy_matrix.append(record_stat(species, record))

    with open(sys.argv[3], 'w') as sh:
        head = "#fam_id\ttotal\t"
        head += ("\t").join(species)
        head += "\t spec_num\n"
        # ortholog species1 species2 ... species_number
        sh.write(head)
        for o in range(len(orthologs)):
            counts = ("\t").join([str(i) for i in copy_matrix[o]])
            sh.write("{}\t{}\n".format(orthologs[o], counts))


if __name__ == '__main__':
    main()



