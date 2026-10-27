# Counting DNA Nucleotides
#read file
f = open('rosalind_dna.txt', 'r', encoding='utf-8')
dna = f.read()

#count the amount of each base
a_count = int(dna.count('A'))
t_count = int(dna.count('T'))
g_count = int(dna.count('G'))
c_count = int(dna.count('C'))

#print
print(a_count, c_count, g_count, t_count )

#Transcribing DNA into RNA
#read file
f = open('rosalind_rna.txt', 'r', encoding='utf-8')
dna = f.read()

# transcript
rna = dna.replace('T', 'U')

#print
print(rna)


#Complementing a Strand of DNA
# open file
f = open('rosalind_revc.txt', 'r', encoding='utf-8')
dna = f.read()

# define dictionary
complement = {"A": "T", "T": "A", "G": "C", "C": "G"}

# build complemented string character by character
dna1 = ""
for base in dna.strip():
    dna1 += complement[base]

# reverse the complemented string
complemented = dna1[::-1]
print(complemented)