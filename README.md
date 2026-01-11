# Higgs-Bubble-Analysis
The Higgs Bubble Anomaly: Analysis of ATLAS Open Data (13 TeV)
Author: Peter Kyjovsky
ORCID: 0009-0008-3806-1964
Status: Under Review (Submitted to ATLAS Coordination & Fermilab)
🌌 Overview
This repository contains the source code and analytical framework used to identify a statistically significant anomaly in the ATLAS Open Data dataset (13 TeV proton-proton collisions). The analysis of 3.47 million events reveals a resonance at 82.67 GeV with a kinematic recoil ratio R > 2.0, suggesting a relativistic vacuum collapse mechanism.
📂 Repository Structure
File Description
atlas_strict_analysis.py Main analysis pipeline. Filters for High-MET, 0-Lepton, Back-to-back topology.
vacuum_expansion_sim.py Simulation of the vacuum lattice expansion under energy load.
higgs_cooling_sim.py Simulation of lattice stabilization via energy deprivation ("Calming").
lattice_3d_model.py 3D visualization of the 55-node Mackay Icosahedron structure.
Grand_Theory_Final.pdf Full theoretical paper explaining the lattice symmetry and R=2.0 limit.

📊 Key Findings to Reproduce
By running the analysis script on standard ATLAS 13 TeV samples, independent researchers can reproduce:
The Mass Peak: A stable transverse mass peak at M_T \approx 82.67 GeV.
The Energy Anomaly: A subset of events (~40%) where MET / Jet\_p_T > 2.0.
The Barrier: A sharp distribution cutoff at exactly R=2.0 (speed of light limit).
🛠️ Installation & Usage
Prerequisites
Python 3.8+
Libraries: uproot, awkward, pandas, numpy, matplotlib
Running the Analysis
pip install uproot awkward pandas matplotlib
python atlas_strict_analysis.py

🔗 Correlations
This work correlates high-energy collider data with low-temperature anomalies observed in superconducting niobium cavities:
Frequency Dips: Bafia et al. (2025) - arXiv:2103.10601
Fast Cooling: Romanenko et al. (2014) - Appl. Phys. Lett. 105
📜 License
This project is open for scientific verification. Please cite the author and ORCID when using this code.
