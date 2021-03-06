#-----------------------------------------------------------+
#                                                           |
# 126_maf2bed.py - Script to convert from MAF to Bed format |
#                                                           |
#-----------------------------------------------------------+
#                                                           |
# AUTHOR: Vikas Gupta                                       |
# CONTACT: vikas0633@gmail.com                              |
# STARTED: 09/06/2013                                       |
# UPDATED: 09/06/2013                                       |
#                                                           |
# DESCRIPTION:                                              | 
# Short script to convert and copy the wheat BACs           |
# Run this in the parent dir that the HEX* dirs exist       |
#                                                           |
# LICENSE:                                                  |
#  GNU General Public License, Version 3                    |
#  http://www.gnu.org/licenses/gpl.html                     |  
#                                                           |
#-----------------------------------------------------------+

# Example:
# python ~/script/python/100b_fasta2flat.py -i 02_Stegodyphous_cdna.refined.fa.orf.tr_longest_frame


### import modules
import os,sys,getopt, re, classMAF


### global variables
global ifile

### make a logfile
import datetime
now = datetime.datetime.now()
o = open(str(now.strftime("%Y-%m-%d_%H%M."))+'logfile','w')



### write logfile

def logfile(infile):
    o.write("Program used: \t\t%s" % "100b_fasta2flat.py"+'\n')
    o.write("Program was run at: \t%s" % str(now.strftime("%Y-%m-%d_%H%M"))+'\n')
    o.write("Infile used: \t\t%s" % infile+'\n')
            
    
def help():
    print '''
            python 100b_fasta2flat.py -i <ifile>
            '''
    sys.exit(2)

### main argument to 

def options(argv):
    global ifile
    ifile = ''
    try:
        opts, args = getopt.getopt(argv,"hi:",["ifile="])
    except getopt.GetoptError:
        help()
    for opt, arg in opts:
        if opt == '-h':
            help()
        elif opt in ("-i", "--ifile"):
            ifile = arg
            
    logfile(ifile)
            
def hashAlignment():
    objs = ''
    new_black = True
    ref_align = True
    obj_count=1
    obj = classMAF.MAF(obj_count)
    objs_list = [obj]
    for line in open(ifile, 'r'):
        line = line.strip()
        if line == '':
            obj_count += 1
            ref_align = True
            obj = classMAF.MAF(obj_count)
            objs_list.append(obj)
        else:
            if not line.startswith('s '):
                obj.addData(line)
            else:
                if ref_align == True:
                    obj.addRefAlign(line)
                    ref_align = False
                else:
                    obj.addtargetAlign(line)
    
    for ob in objs_list[:-1]:
        print str(ob.RefChro()) + '\t'+ \
        str(ob.RefStart()) + '\t'+ \
        str(ob.RefEnd()) + '\t' + \
        str(ob.TargetChro()) + '_'+ \
        str(ob.TargetStart()) + '_'+ \
        str(ob.TargetEnd()) + '_' + \
        str(ob.TargetStrand()) + '\t' + \
        str(ob.identity()) + '\t' + \
        str(ob.RefStrand())
                            
        

if __name__ == "__main__":
    
    options(sys.argv[1:])
    
    hashAlignment()
    
    ### close the logfile
    o.close()