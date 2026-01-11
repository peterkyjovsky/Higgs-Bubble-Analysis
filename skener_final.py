import uproot
import awkward as ak
import numpy as np

file_name = "ODEO_FEB2025_v0_2to4lep_data15_periodF.2to4lep.root"

with uproot.open(file_name + ":analysis") as tree:
    # Načítame dáta (uproot ich načíta ako polia, pretože v 1 evente môže byť viac leptónov)
    data = tree.arrays(["runNumber", "eventNumber", "lep_pt", "met", "lep_eta", "lep_phi"])
    
    # Prevod z MeV na GeV (CERN dáta sú v MeV)
    lep_pt_gev = data["lep_pt"] / 1000.0
    met_gev = data["met"] / 1000.0
    
    # Definujeme vaše "okno" záujmu
    # Hľadáme čokoľvek okolo 28.188 a 31.4
    maska_teoria = ak.any((lep_pt_gev > 28.1) & (lep_pt_gev < 28.3), axis=1)
    maska_cern = ak.any((lep_pt_gev > 31.3) & (lep_pt_gev < 31.5), axis=1)
    
    # Spoločná maska: hľadáme eventy, kde je aspoň jedna z týchto hodnôt
    finalna_maska = maska_teoria | maska_cern
    maska_met = (met_gev > 28.13) & (met_gev < 28.23)
    vysledky = data[finalna_maska]
    pt_vysledky = lep_pt_gev[finalna_maska]
    met_vysledky = met_gev[finalna_maska]

    print(f"Prehľadaných eventov: {len(data)}")
    print(f"Nájdených zaujímavých udalostí: {len(vysledky)}\n")

    for i in range(len(vysledky)):
        print(f"Run: {vysledky[i]['runNumber']}, Event: {vysledky[i]['eventNumber']}")
        print(f"  Leptón pT [GeV]: {pt_vysledky[i].tolist()}")
        print(f"  Missing ET (met) [GeV]: {met_vysledky[i]:.4f}")
        print(f"  Uhly (eta): {vysledky[i]['lep_eta'].tolist()}")
        print("-" * 30)