import os
import os.path

import sys
sys.path.append('.../ANI-1_release/readers/lib')
import pyanitools as pya

# Set the HDF5 file containing the data
hdf5file = sys.argv[1]

# Construct the data loader class
adl = pya.anidataloader(hdf5file)

for data in adl:
    P=data['path']
    fields=P.split('/')
    os.mkdir(fields[2])
    os.chdir(fields[2])
    glostout=open("list_glost.txt", 'w')
    subsetname = fields[2]
    
    X = data['coordinates']        
    for n_crd in range(len(X)):
       glostout.write('.../job.sh ' + hdf5file + ' ' + subsetname + ' ' + str(n_crd) + '\n')
       
    glostout.close()

    os.system('sbatch .../job_sbmt.sh')
    os.chdir(r'... absolute path of your directory')

