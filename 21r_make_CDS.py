## 21r_make_CDS.py- script to create CDS file from fasta (containing exon sequences generated by bedtools) and GTF/GFF3 file  - /Users/vikas0633/Desktop/script/python

import os,sys, getopt, re


def options(argv):
	infile = ''
	GTF = True
	try:
		opts, args = getopt.getopt(argv,"hi:f:g",["ifile="])
	except getopt.GetoptError:
		print 'python 21r_make_CDS.py -i <gene_stru> -f <fasta> -g <GFF3>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'python 21r_make_CDS.py -i <gene_stru> -f <fasta> -g <GFF3>'
			sys.exit()
		elif opt in ("-i", "--gene_stru"):
			infile = arg
		elif opt in ("-f", "--gene_stru"):
			fasta = arg
		elif opt in ("-g", "--GFF3"):
			GTF = False
	return infile, fasta, GTF


def load_fasta():
	first_line = True
	seq_hash = {}
	for line in open(fasta,'r'):
		line = line.strip()
		if len(line) > 0 :			
			if line[0] == '>':
				if first_line == False:
					seq_hash[header] = seq
				seq = ''
				header = line[1:]
			else:
				seq += line
		first_line = False			
	seq_hash[header] = seq
	
	return seq_hash
	
def make_cds():
	last_transcript_id = ''
	first_line = True
	seq = ''
	for line in open(infile,'r'):
		line = line.strip()
		if len(line) > 0: 
			if line[0] != '#':
				token = line.split('\t')
				if GTF == False:
					match = re.search(r'Parent=.+;',line)
					transcript_id = match.group().split(';')[0].replace('Parent=','')
					#transcript_id = (line.split('=')[2]).split(';')[0]
				else:
					transcript_id = line.split('"')[3]
				if (token[2] == 'exon') or (token[2] == 'CDS'):
					key = token[0]+':'+str(int(token[3])-1)+'-'+str(token[4])
					if last_transcript_id == transcript_id:
						if key in seq_hash:
							seq += seq_hash[key]
					else:
						if key in seq_hash:
							seq = seq_hash[key]
						if first_line == False:
							print '>'+last_transcript_id+' '+last_transcript_id
							print last_seq 
						first_line = False
				last_seq = seq
				last_transcript_id = transcript_id
	print '>'+last_transcript_id+' '+last_transcript_id
	print last_seq 

if __name__ == "__main__":
    
    infile, fasta, GTF = options(sys.argv[1:])    
    
    ### load the fasta file
    seq_hash = load_fasta()
    
    ### make cds file
    make_cds()
    
	
