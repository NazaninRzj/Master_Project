import pandas as pd
import numpy as np
import sys
sys.path.append('.../ANI-1_release/readers/lib')
import pyanitools as pya
import h5py
import os.path
import gc

def panda(postg_all):
    '''number of structures'''
    count = 0
    df = pd.DataFrame(columns=['num_str', 'c6', 'c8', 'c10', 'Rc', 'Rvdw', 'scf'])
    with open(postg_all, 'r') as file:
        file_readlines = file.readlines()
        for i, line in enumerate(file_readlines):
            if ("#! gdb11_s06-") in file_readlines[i]:
                num_str = file_readlines[i].split(" ")[2][:-1]
                count += 1
                while "coefficients and distances (a.u.)" not in file_readlines[i]:
                    i += 1
                i += 2

                c6 = np.zeros(0)
                c8 = np.zeros(0)
                c10 = np.zeros(0)
                Rc = np.zeros(0)
                Rvdw = np.zeros(0)
                scf = np.zeros(0)

                while '#' not in file_readlines[i]:
                    f = file_readlines[i].split()
                    if f[0] == f[1]:
                        c6 = np.append(c6, float(f[3]))
                        c8 = np.append(c8, float(f[4]))
                        c10 = np.append(c10, float(f[5]))
                        Rc = np.append(Rc, float(f[6]))
                        Rvdw = np.append(Rvdw, float(f[7]))

                    i = i + 1

                while "scf energy" not in file_readlines[i]:
                    i += 1

                scf = np.append(scf, float(file_readlines[i].split()[2]))
                '''df includes coefficients from beginning to the end of the postg_all file'''
                df = df.append({"num_str": int(num_str), "c6" : c6, "c8": c8, "c10": c10, "Rc": Rc, "Rvdw": Rvdw, "scf":scf}, ignore_index=True)

    df = df.set_index('num_str')
    return (df, count)

'''Set the HDF5 file containing the data'''
hdf5file = (".../ANI-1_release/ani_gdb_s06.h5")

'''Construct the data loader class'''
adl = pya.anidataloader(hdf5file)

'''Set a name for the output file'''
fhout = h5py.File(".hdf5", "w")

'''k is a data set like gdb11_s03'''
for k in adl.store.keys():
    group1 = fhout.create_group(k)
    
    '''k2 is sub data set like: gdb11_s03-0, gdb11_s03-1'''
    for k2 in adl.store[k].keys():
        group2 = group1.create_group(adl.store[k][k2].name)
        (nstruct, natom, ncart) = adl.store[k][k2]["coordinates"].shape
        group2.create_dataset("energies", (nstruct,), dtype="f8", data=adl.store[k][k2]['energies'])
        group2.create_dataset("energiesHE", (len(adl.store[k][k2]["energiesHE"]),), dtype="f8",
                              data=adl.store[k][k2]['energiesHE'])
        group2.create_dataset("smiles", (len(adl.store[k][k2]["smiles"]),), dtype="|S1",
                              data=adl.store[k][k2]['smiles'])
        group2.create_dataset("species", (len(adl.store[k][k2]["species"]),), dtype="|S1",
                              data=adl.store[k][k2]['species'])
        group2.create_dataset("coordinates", (nstruct, natom, 3), dtype="f4", data=adl.store[k][k2]['coordinates'])
        group2.create_dataset("coordinatesHE", adl.store[k][k2]["coordinatesHE"].shape, dtype="f4",
                              data=adl.store[k][k2]['coordinatesHE'])

        G21_items = list(adl.store[k][k2])

        if ("c6" and "c8" and "c10" and "Rc" and "Rvdw" and "scf") in G21_items:
            group2.create_dataset("c6", (nstruct,natom), dtype="f8", data= adl.store[k][k2]['c6'])
            group2.create_dataset("c8", (nstruct, natom), dtype="f8", data=adl.store[k][k2]['c8'])
            group2.create_dataset("c10", (nstruct, natom), dtype="f8", data=adl.store[k][k2]['c10'])
            group2.create_dataset("Rc", (nstruct, natom), dtype="f8", data=adl.store[k][k2]['Rc'])
            group2.create_dataset("Rvdw", (nstruct, natom), dtype="f8", data=adl.store[k][k2]['Rvdw'])
            group2.create_dataset("scf", (nstruct,), dtype="f8", data=adl.store[k][k2]['scf'])

        '''change the directory'''
        os.chdir(r'.../dataset/' + k2)
        
        (df, count) = panda("postg_all.txt")

        c6_all = np.zeros((count,natom))
        c8_all = np.zeros((count,natom))
        c10_all = np.zeros((count,natom))
        Rc_all = np.zeros((count,natom))
        Rvdw_all = np.zeros((count,natom))
        scf_all = np.zeros((count))

        for i in range(count):
            c6_all[i] = df.loc[i, "c6"]
            c8_all[i] = df.loc[i, "c8"]
            c10_all[i] = df.loc[i, "c10"]
            Rc_all[i] = df.loc[i, "Rc"]
            Rvdw_all[i] = df.loc[i, "Rvdw"]
            scf_all[i] = df.loc[i, "scf"]
                
        if (len(c6_all) and len(c8_all) and len(c10_all) and len(Rc_all) and len(Rvdw_all) and len(scf_all)) == nstruct:
            f = group2.create_dataset("c6", (nstruct, natom), dtype="f8", data=c6_all)
            t = group2.create_dataset("c8", (nstruct, natom), dtype="f8", data=c8_all)
            a = group2.create_dataset("c10", (nstruct, natom), dtype="f8", data=c10_all)
            b = group2.create_dataset("Rc", (nstruct, natom), dtype="f8", data=Rc_all)
            c = group2.create_dataset("Rvdw", (nstruct, natom), dtype="f8", data=Rvdw_all)
            d = group2.create_dataset("scf", (nstruct,), dtype="f8", data=scf_all)

fhout.close()
adl.cleanup()

