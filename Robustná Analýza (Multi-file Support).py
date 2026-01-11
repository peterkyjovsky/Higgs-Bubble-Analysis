import uproot
import awkward as ak
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

# --- 1. KONFIGURÁCIA ---
limit_high_met = 50.0

# Názvy premenných (rozšírená kompatibilita)
possible_electron_names = [["AnalysisElectronsAuxDyn.pt", "AnalysisElectronsAuxDyn.eta"], ["el_pt", "el_eta"]]
possible_muon_names = [["AnalysisMuonsAuxDyn.pt", "AnalysisMuonsAuxDyn.eta"], ["mu_pt", "mu_eta"]]
possible_jet_names = [["AnalysisJetsAuxDyn.pt", "AnalysisJetsAuxDyn.phi"], ["jet_pt", "jet_phi"]]


def find_branches(tree_keys, candidates):
    for variant in candidates:
        if all(col in tree_keys for col in variant): return variant
    return None


def calculate_delta_phi(phi1, phi2):
    dphi = np.abs(phi1 - phi2)
    dphi = np.where(dphi > np.pi, 2 * np.pi - dphi, dphi)
    return dphi


print("--- UPDATE: HROMADNÉ SPRACOVANIE (SAFE MODE) ---")
root_files = glob.glob("*.root*")
if not root_files: raise SystemExit("Žiadne súbory. Nahrajte ich do priečinka.")

print(f"[INFO] Detekovaných súborov: {len(root_files)}")
all_dataframes = []

# --- 2. SPRACOVANIE SÚBOROV ---
for i, filename in enumerate(root_files):
    try:
        with uproot.open(filename) as file:
            # Smart Tree Detection
            tree_name = "CollectionTree" if "CollectionTree" in file else list(file.keys())[0]
            tree = file[tree_name]
            keys = tree.keys()

            # Branches
            el_branches = find_branches(keys, possible_electron_names)
            mu_branches = find_branches(keys, possible_muon_names)
            jet_branches = find_branches(keys, possible_jet_names)

            if not jet_branches: continue

            # MET logic
            if "MET_Core_AnalysisMETAuxDyn.mpx" in keys:
                mpx_name, mpy_name = "MET_Core_AnalysisMETAuxDyn.mpx", "MET_Core_AnalysisMETAuxDyn.mpy"
                is_vector_met = True
            elif "met_et" in keys:
                mpx_name, mpy_name = "met_et", "met_phi"
                is_vector_met = False
            else:
                continue

            # Load
            load_list = ["EventInfoAuxDyn.eventNumber" if "EventInfoAuxDyn.eventNumber" in keys else "eventNumber"]
            load_list += [mpx_name, mpy_name] if is_vector_met else [mpx_name, mpy_name]
            if el_branches: load_list += el_branches
            if mu_branches: load_list += mu_branches
            load_list += jet_branches

            data = tree.arrays(load_list, library="ak")

            # Calc MET (Safe Access)
            if is_vector_met:
                # Používame ak.firsts pre bezpečný prístup aj k prázdnym poliam
                mpx = ak.fill_none(ak.firsts(data[mpx_name]), 0)
                mpy = ak.fill_none(ak.firsts(data[mpy_name]), 0)
                met_gev = np.sqrt(mpx ** 2 + mpy ** 2) / 1000.0
                met_phi = np.arctan2(mpy, mpx)
            else:
                raw_met = data[mpx_name]
                raw_phi = data[mpy_name]
                # Kontrola či je to pole (jagged) alebo číslo
                try:
                    met_gev = raw_met / 1000.0
                    met_phi = raw_phi
                except:
                    met_gev = ak.fill_none(ak.firsts(raw_met), 0) / 1000.0
                    met_phi = ak.fill_none(ak.firsts(raw_phi), 0)

            # Calc Leptons
            n_lep = (ak.sum(data[el_branches[0]] / 1000.0 > 10, axis=1) if el_branches else 0) + \
                    (ak.sum(data[mu_branches[0]] / 1000.0 > 10, axis=1) if mu_branches else 0)

            # Calc Jets (Safe Access - FIX PRE CHYBU)
            jet_pt = data[jet_branches[0]] / 1000.0
            jet_phi_data = data[jet_branches[1]]

            # ak.firsts vráti None ak je zoznam prázdny, ak.fill_none to nahradí nulou
            lead_jet_pt = ak.fill_none(ak.firsts(jet_pt), 0)
            lead_jet_phi = ak.fill_none(ak.firsts(jet_phi_data), 0)

            dphi = calculate_delta_phi(met_phi, lead_jet_phi)
            # Ak nemáme jet (pt=0), dphi nedáva zmysel, nastavíme na -1
            dphi = ak.where(lead_jet_pt > 0, dphi, -1.0)

            # Mt Calc
            mt = np.sqrt(2 * met_gev * lead_jet_pt * (1 - np.cos(dphi)))

            all_dataframes.append(pd.DataFrame({
                "MET_GeV": ak.to_numpy(met_gev),
                "LeadJet_Pt": ak.to_numpy(lead_jet_pt),
                "N_Leptons": ak.to_numpy(n_lep),
                "DeltaPhi": ak.to_numpy(dphi),
                "Mt_GeV": ak.to_numpy(mt)
            }))

    except Exception as e:
        print(f"[SKIP] Chyba v súbore {filename}: {e}")

# --- 3. VÝSLEDKY ---
if not all_dataframes: raise SystemExit("Žiadne dáta.")
full_df = pd.concat(all_dataframes, ignore_index=True)

# CUTS
golden = full_df[
    (full_df["MET_GeV"] > limit_high_met) &
    (full_df["N_Leptons"] == 0) &
    (full_df["DeltaPhi"] > 2.0)
    ].copy()

# RATIO
golden["Ratio"] = golden["MET_GeV"] / golden["LeadJet_Pt"]

print("-" * 40)
print(f"CELKOVO SPRACOVANÝCH: {len(full_df)} udalostí")
print(f"POČET 'GOLDEN' KANDIDÁTOV: {len(golden)}")
print("-" * 40)

# CHECK R=2.0 BARRIER
over_barrier = golden[golden["Ratio"] > 2.0]
at_barrier = golden[(golden["Ratio"] >= 1.9) & (golden["Ratio"] <= 2.0)]

print(f"Kandidáti s R > 2.0 (Porušenie bariéry): {len(over_barrier)}")
print(f"Kandidáti na hranici (1.9 <= R <= 2.0):  {len(at_barrier)}")

# MT STATS
print("-" * 40)
print(f"Priemerná Hmotnosť (Mt): {golden['Mt_GeV'].mean():.2f} GeV")
print("-" * 40)

# GRAF
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.hist(golden["Ratio"], bins=60, range=(0, 3.0), color='crimson', alpha=0.7, edgecolor='black')
plt.axvline(x=2.0, color='black', linestyle='--', linewidth=2, label='Limit c (R=2)')
plt.title("Test Bariéry R=2.0 (Všetky súbory)")
plt.xlabel("Pomer MET/Jet")
plt.legend()

plt.subplot(1, 2, 2)
plt.hist(golden["Mt_GeV"], bins=40, color='orange', alpha=0.7, edgecolor='black')
plt.title(f"Hmotnosť (Priemer: {golden['Mt_GeV'].mean():.1f} GeV)")
plt.xlabel("Mt [GeV]")

plt.tight_layout()
plt.savefig("updated_analysis_results.png")
print("[OK] Grafy aktualizované: updated_analysis_results.png")
plt.show()