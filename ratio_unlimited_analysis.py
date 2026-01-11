import glob

import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import uproot

# --- 1. KONFIGURÁCIA ---
limit_high_met = 50.0

# Názvy premenných pre ATLAS PHYSLITE / Open Data
possible_electron_names = [["AnalysisElectronsAuxDyn.pt", "AnalysisElectronsAuxDyn.eta"], ["el_pt", "el_eta"]]
possible_muon_names = [["AnalysisMuonsAuxDyn.pt", "AnalysisMuonAuxDyn.eta"], ["mu_pt", "mu_eta"]]
possible_jet_names = [["AnalysisJetsAuxDyn.pt", "AnalysisJetsAuxDyn.phi"], ["jet_pt", "jet_phi"]]


def find_branches(tree_keys, candidates):
    for variant in candidates:
        if all(col in tree_keys for col in variant):
            return variant
    return None


def calculate_delta_phi(phi1, phi2):
    dphi = np.abs(phi1 - phi2)
    dphi = np.where(dphi > np.pi, 2 * np.pi - dphi, dphi)
    return dphi


print("--- KRITICKÁ ANALÝZA: TEST BARIÉRY R=2.0 ---")
root_files = glob.glob("*.root*")
if not root_files: raise SystemExit("Žiadne súbory.")

all_dataframes = []

for filename in root_files:
    try:
        with uproot.open(filename) as file:
            tree_name = "CollectionTree" if "CollectionTree" in file else list(file.keys())[0]
            tree = file[tree_name]
            keys = tree.keys()

            el_branches = find_branches(keys, possible_electron_names)
            mu_branches = find_branches(keys, possible_muon_names)
            jet_branches = find_branches(keys, possible_jet_names)

            if not jet_branches: continue

            mpx_name, mpy_name = "MET_Core_AnalysisMETAuxDyn.mpx", "MET_Core_AnalysisMETAuxDyn.mpy"
            is_vector_met = mpx_name in keys

            load_list = ["EventInfoAuxDyn.eventNumber" if "EventInfoAuxDyn.eventNumber" in keys else "eventNumber"]
            load_list += [mpx_name, mpy_name] if is_vector_met else ["met_et", "met_phi"]
            if el_branches: load_list += el_branches
            if mu_branches: load_list += mu_branches
            load_list += jet_branches

            data = tree.arrays(load_list, library="ak")

            # --- FYZIKA ---
            if is_vector_met:
                # Safely get mpx and mpy, defaulting to 0 if the ListArray is empty
                mpx = ak.fill_none(ak.firsts(ak.pad_none(data[mpx_name], 1, clip=True)), 0)
                mpy = ak.fill_none(ak.firsts(ak.pad_none(data[mpy_name], 1, clip=True)), 0)
                met_gev = np.sqrt(mpx ** 2 + mpy ** 2) / 1000.0
                met_phi = np.arctan2(mpy, mpx)
            else:
                met_gev, met_phi = data["met_et"] / 1000.0, data["met_phi"]

            n_lep = (ak.sum(data[el_branches[0]] / 1000.0 > 10, axis=1) if el_branches else 0) + \
                    (ak.sum(data[mu_branches[0]] / 1000.0 > 10, axis=1) if mu_branches else 0)

            jet_pt_raw = data[jet_branches[0]] / 1000.0
            jet_phi_raw = data[jet_branches[1]]

            # Safely get leading jet pt and phi, defaulting to 0 if no jets
            lead_jet_pt = ak.fill_none(ak.firsts(ak.pad_none(jet_pt_raw, 1, clip=True)), 0)
            lead_jet_phi = ak.fill_none(ak.firsts(ak.pad_none(jet_phi_raw, 1, clip=True)), 0)
            dphi = calculate_delta_phi(met_phi, lead_jet_phi)

            all_dataframes.append(pd.DataFrame({
                "MET_GeV": ak.to_numpy(met_gev),
                "LeadJet_Pt": ak.to_numpy(lead_jet_pt),
                "N_Leptons": ak.to_numpy(n_lep),
                "DeltaPhi": ak.to_numpy(dphi)
            }))
    except Exception as e:
        print(f"Warning: Could not process file {filename} due to error: {e}")
        continue  # Skip to the next file

# Check if any dataframes were successfully processed
if not all_dataframes: raise SystemExit("No dataframes were successfully loaded from any ROOT files.")

full_df = pd.concat(all_dataframes, ignore_index=True)
golden = full_df[
    (full_df["MET_GeV"] > limit_high_met) & (full_df["N_Leptons"] == 0) & (full_df["DeltaPhi"] > 2.0)].copy()

# VÝPOČET POMERU BEZ OBMEDZENÍ
golden["Ratio"] = golden["MET_GeV"] / golden["LeadJet_Pt"]

# --- ŠTATISTICKÝ PRIESKUM ---
over_two = golden[golden["Ratio"] > 2.0]
print(f"Celkový počet kandidátov: {len(golden)}")
print(f"Počet udalostí s R > 2.0: {len(over_two)} ({len(over_two) / len(golden) * 100:.2f}%)")

# GRAF S ROZŠÍRENÝM ROZSAHOM
plt.figure(figsize=(10, 6))
# Zmenili sme range z (0, 2.0) na automatický (alebo širší), aby sme videli 'chvost'
plt.hist(golden["Ratio"], bins=50, color='teal', alpha=0.7, edgecolor='black')
plt.axvline(x=2.0, color='red', linestyle='--', label='Teoretická bariéra R=2')
plt.title("Distribúcia pomeru MET / Jet pT (Bez umelých limitov)")
plt.xlabel("Pomer R")
plt.ylabel("Počet udalostí")
plt.legend()
plt.grid(alpha=0.3)
plt.savefig("ratio_unlimited_analysis.png")
plt.show()

