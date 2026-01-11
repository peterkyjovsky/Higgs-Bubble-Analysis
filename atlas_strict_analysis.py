import uproot
import awkward as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# CONFIGURATION
limit_high_met = 50.0

# VARIABLE NAMES MAPPING (ATLAS Open Data Compatibility)
possible_electron_names = [["AnalysisElectronsAuxDyn.pt", "AnalysisElectronsAuxDyn.eta"], ["el_pt", "el_eta"]]
possible_muon_names = [["AnalysisMuonsAuxDyn.pt", "AnalysisMuonsAuxDyn.eta"], ["mu_pt", "mu_eta"]]
possible_jet_names = [["AnalysisJetsAuxDyn.pt", "AnalysisJetsAuxDyn.phi"], ["jet_pt", "jet_phi"]]

def find_branches(tree_keys, candidates):
    for variant in candidates:
        if all(col in tree_keys for col in variant): return variant
    return None

def calculate_delta_phi(phi1, phi2):
    dphi = np.abs(phi1 - phi2)
    dphi = np.where(dphi > np.pi, 2*np.pi - dphi, dphi)
    return dphi

print("--- HIGGS BUBBLE ANALYSIS: ATLAS OPEN DATA 13 TeV ---")
root_files = glob.glob("*.root*")
if not root_files: 
    print("[WARNING] No .root files found in current directory. Please upload ATLAS data samples.")
    # For demonstration purposes in repo, we don't raise Exit
    root_files = []

all_dataframes = []

for i, filename in enumerate(root_files):
    try:
        with uproot.open(filename) as file:
            tree_name = "CollectionTree" if "CollectionTree" in file else list(file.keys())[0]
            tree = file[tree_name]
            keys = tree.keys()
            
            el_branches = find_branches(keys, possible_electron_names)
            mu_branches = find_branches(keys, possible_muon_names)
            jet_branches = find_branches(keys, possible_jet_names)

            if not jet_branches: continue 

            if "MET_Core_AnalysisMETAuxDyn.mpx" in keys:
                mpx_name, mpy_name = "MET_Core_AnalysisMETAuxDyn.mpx", "MET_Core_AnalysisMETAuxDyn.mpy"
                is_vector_met = True
            elif "met_et" in keys:
                mpx_name, mpy_name = "met_et", "met_phi"
                is_vector_met = False
            else: continue

            load_list = ["EventInfoAuxDyn.eventNumber" if "EventInfoAuxDyn.eventNumber" in keys else "eventNumber"]
            load_list += [mpx_name, mpy_name] if is_vector_met else [mpx_name, mpy_name]
            if el_branches: load_list += el_branches
            if mu_branches: load_list += mu_branches
            load_list += jet_branches

            data = tree.arrays(load_list, library="ak")

            # MET Calculation
            if is_vector_met:
                mpx = ak.fill_none(ak.firsts(data[mpx_name]), 0)
                mpy = ak.fill_none(ak.firsts(data[mpy_name]), 0)
                met_gev = np.sqrt(mpx**2 + mpy**2) / 1000.0
                met_phi = np.arctan2(mpy, mpx)
            else:
                raw_met = data[mpx_name]
                raw_phi = data[mpy_name]
                try:
                    met_gev = raw_met / 1000.0
                    met_phi = raw_phi
                except:
                    met_gev = ak.fill_none(ak.firsts(raw_met), 0) / 1000.0
                    met_phi = ak.fill_none(ak.firsts(raw_phi), 0)

            # Lepton Veto
            n_lep = (ak.sum(data[el_branches[0]]/1000.0 > 10, axis=1) if el_branches else 0) + \
                    (ak.sum(data[mu_branches[0]]/1000.0 > 10, axis=1) if mu_branches else 0)

            # Jet Kinematics
            jet_pt = data[jet_branches[0]] / 1000.0
            jet_phi_data = data[jet_branches[1]]
            
            lead_jet_pt = ak.fill_none(ak.firsts(jet_pt), 0)
            lead_jet_phi = ak.fill_none(ak.firsts(jet_phi_data), 0)
            
            dphi = calculate_delta_phi(met_phi, lead_jet_phi)
            dphi = ak.where(lead_jet_pt > 0, dphi, -1.0)
            
            # Transverse Mass (Mt)
            mt = np.sqrt(2 * met_gev * lead_jet_pt * (1 - np.cos(dphi)))

            all_dataframes.append(pd.DataFrame({
                "MET_GeV": ak.to_numpy(met_gev),
                "LeadJet_Pt": ak.to_numpy(lead_jet_pt),
                "N_Leptons": ak.to_numpy(n_lep),
                "DeltaPhi": ak.to_numpy(dphi),
                "Mt_GeV": ak.to_numpy(mt)
            }))
            
    except Exception as e:
        print(f"[SKIP] Error in file {filename}: {e}")

if all_dataframes:
    full_df = pd.concat(all_dataframes, ignore_index=True)
    
    # GOLDEN SELECTION
    golden = full_df[
        (full_df["MET_GeV"] > limit_high_met) & 
        (full_df["N_Leptons"] == 0) & 
        (full_df["DeltaPhi"] > 2.0)
    ].copy()
    
    golden["Ratio"] = golden["MET_GeV"] / golden["LeadJet_Pt"]
    
    print(f"Total Events Processed: {len(full_df)}")
    print(f"Golden Candidates Found: {len(golden)}")
    print(f"Mean Mass (Mt): {golden['Mt_GeV'].mean():.2f} GeV")
    
