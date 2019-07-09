#### statistic ortholog result and pich single-copy gene out
Gblocks="your/path"


```shell
# stat
python3 mclgroup2stat.py ../file.list mclOutput2groupsFile mclOutput2groupsFile.stat

# single-copy gene id
awk '$2==8 && $11==8{print $1}' mclOutput2groupsFile.stat > single_copy.ORs

# ortholog group and gene id
grep -f single_copy.ORs mclOutput2groupsFile >single_copy.groups

# get each gene sequence
python3 find_SingleCopy.py single_copy.ORs goodProteins.fasta single_copy

# align protein sequence and retrevie conserved regions
cat single_copy.ORs|while read a
do
	muscle -in single_copy/$a.pep -out single_copy/$a.aln
	$Gblocks single_copy/$a.aln -t=p -b3=8 -b4=10 -b5=n -e=-st
			
done
			
# concatenate conserved regions together
python3 generate_Gblocks.py single_copy st all.gblocks.phy
```
