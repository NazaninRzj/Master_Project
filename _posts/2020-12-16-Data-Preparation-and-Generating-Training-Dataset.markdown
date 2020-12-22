---
layout: post
title: Data Preparation and Generating Training Dataset
date:  2020-12-16
description: This post will explain how we generated the training dataset
img: dataset.jpg 
---
To train our new dispersion-corrected NNP, we will calculate the atomic XDM dispersion coefficients (i.e., C​6​, C​8​, C​10​) and the SCF energy for each configuration in the dataset. These properties are calculated using the PBE0 functional​ and aug-cc-pVTZ basis set using Gaussian 16 interfaced to the postg XDM code.

Because ANI potential dataset consists of ~25M molecules, with 1000 configurations defined for each molecule, we have implemented a parallel computing workflow for these calculations using GLOST (the Greedy Launcher Of Small Tasks) to reduce the time calculation.

{% highlight ruby %} 
#!/bin/bash
#SBATCH --ntasks= number of nodes 
#SBATCH --time=(DD-HH:MM)
#SBATCH --mem-per-cpu=1024M
#SBATCH --account=def-someuser

# Load GLOST module along with the modules required to run your application:

module load nixpkgs/16.09  intel/2016.4  openmpi/2.0.2 glost/0.3.1

echo "Starting run at: `date`"

# Run GLOST with the argument: list_glost.txt
srun glost_launch list_glost.txt

echo "Program glost_launch finished with exit code $? at: `date`"
{% endhighlight %}

Then we used python scripts to extract the coefficients and generate new HDF5 files. 
You could see our python scripts for [submiting all molecules](https://github.com/NazaninRzj/Master_Project/blob/git-pages/Scripts/submit_all_molecules.py) and for [genrating a new dataset](https://github.com/NazaninRzj/Master_Project/blob/git-pages/Scripts/generate_dataset.py). 

