---
layout: post
title: Introduction
date: 2020-12-16
description: This post will explain a bit about main concepts of my Master's project 
img: compchem.jpg # Add image post (optional)
useMath: true
---
Simulations of molecular systems require computational methods that can make an accurate prediction of intramolecular and intermolecular forces. In molecular  systems, the most significant forces are Pauli repulsion, electrostatic, and dispersion interactions. Ab initio methods have been developed to calculate these forces from the first principles of quantum mechanical models. Density Functional Theory (DFT) has been one of the most popular and successful of these models.  These models can calculate the Pauli repulsive and electrostatic energies from the first principles. Although these models typically omit dispersion interactions, methods have been developed to calculate dispersion interactions as a post-hoc correction to a DFT calculation.

In recent years, researchers have employed neural networks to calculate molecular forces to have accurate forces at a lower computational cost. Artificial neural networks are a kind of machine learning method in which the mathematical equations are used to determine the linear regression in a given data set. These neural network potentials have been successful in predicting the chemical interactions arising from short-range interactions (i.e., Pauli repul-sion and bonding electrostatic interactions); however, long-range interactions like dispersion are neglected. In this work, we propose to develop a new NNP that is combined with a separate NN-based method for calculating dispersion interactions to calculate more accurate forces in molecular systems at a low computational cost. The most significant innovation in this thesis is in the calculation of London dispersion interactions through a novel scheme that employs neural networks. 

## London Disperison Interaction
Dispersion interaction is a temporary attractive non-bonded force arising from the interaction between instantaneous dipole moments, which stems from fluctuations in the electron density of two atoms or molecules. Eventhough the dispersion interaction between a pair of atoms is weaker than other interactions (i.e., bonding electrostatic interactions or Pauli repulsion interaction), the dispersion energy plays a significant role in materials chemistry and biophysics, where dispersion interactions become significant in the condensed state.

The potential energy of London dispersion interaction ($V_disp$) can be approximated by,

![Z(i,j)=X(i,k) * Y(k, j); k=1 to n](http://www.sciweavers.org/tex2img.php?eq=Z_i_j%3D%5Csum_%7Bi%3D1%7D%5E%7B10%7D%20X_i_k%20%2A%20Y_k_j&bc=White&fc=Black&im=jpg&fs=12&ff=arev&edit=)

$$\mathcal{V}_{disp,ij}(\mathrm{r_{ij}})= -\sum_{n=6,8,10...} \frac{C_{n,ij}}{r_{ij}^n}$$

where $$r_{ij}$$ is the distance between atomic pairs and the *C*~n,ij~ are coefficients that depend on the chemical environment of the atom, such as its bonding partners and oxidation state. 

## Exchange-Hole Dipole Moment
The exchange-hole dipole moment (XDM) model provides an ab initio method for calculating the atomic and molecular dispersion coefficients, which is in meaningful compromise with the empirical value. Despite the XDM computational precision, it requires a computationally intensive density-functionaltheory (DFT) calculation.

## Neural Networks
Machine learning is a powerful tool because of its ability to predict unseen samples. ML models have been developed in chemistry fields to predict ab initio quantum mechanics properties (e.g., molecular potential energies, atomic charges, and molecular dipoles). Machine learning plays a vital role in chemistry recently by providing accurate predictions and having non-expensive computational calculations.

## ANI Potential
Accurate energy calculations for large molecules are significant in various fields like chemistry and biology. Having ab initio methods with high accuracy is a challenging part of theoretical chemistry. Different theoretical methods and software are aiming to describe more complex systems. Quantum mechanical (QM) methods are accurate, but are computationally expensive and scale poorly when considering large systems. ANAKIN-ME (Accurate NeurAl networK engiNe for Molecular Energies) or ANI, forshort, is a new method for developing NNPs. It employs a modified version of the Behler and Parrinello symmetry functions (SFs) to develop single-AEV being a molecular representation. Choosing the training data set is crucial since the accuracy is based on the amount, quality, and types of data in the set. The GDB-11 database involves all possible organic molecules containing up to 11 atoms of the atomic numbers C, N, O, and F. However, ANI was trained on a subset of the GDB-11 databases, including up to 8 heavy atoms containing C, N, and O to build apotential called ANI-1. The ANI-1 dataset includes approximately ∼25M molecular conformations for 57462 molecules from the GDB-11 database, which Smith et al. generated structures using normal mode displacements around the equilibrium geometry. [Read the paper for more information](https://pubs.rsc.org/en/content/articlelanding/2017/sc/c6sc05720a#!divAbstract) and access the Github repository [here](https://github.com/isayev/ANI1_dataset)

## Proposed Work
Although newly developed NNPs like ANI-1 are powerful tools to accurately predict the energy of molecules at a modest computational cost, it is not a perfect  model. Its first limitation is that the ANI potential only provides energy based on the 5 ̊A cutoff radius, and thus the dispersion energies are not described correctly. Dispersion interactions occur between atoms separated by more than 5 ̊A, and standard models calculate dispersion interactions up to 5 ̊A. As a result, predicting the potential energy of a chemical system can be more accurate by considering dispersion energies in the model. 

Secondly, the XDM, a non-empirical model, is proposed for calculating dispersion coefficients. The ωB97X functional, used in ANI-1, is not trained for use with XDM, so it is impossible to simply add an XDM correction to a NNP trained to reproduce the potential energies of this method. A combination of PBE0/aug-cc-pVTZ and XDM dispersion energy provides an accurate description of reaction energies.

In this project, we are training an ANI-type neural network to calculate the atoms’ dispersion coefficients without the DFT calculation, providing a neural network potential that describes dispersion rigorously without a significant increase in computational cost.

