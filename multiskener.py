import uproot
import awkward as ak
import os

def hromadny_skener():
    cielovy_run = 2950
    cielovy_event = 4
    nasiel_sa = False

    # Prejde všetky súbory v priečinku
    for subor in os.listdir("."):
        if subor.endswith(".root"):
            print(f"Skenujem: {subor}...")
            try:
                with uproot.open(subor) as f:
                    # Zistíme názov stromu (často 'mini' alebo 'nominal')
                    kluce = f.keys()
                    strom_meno = kluce[0].split(';')[0]
                    tree = f[strom_meno]
                    
                    # Načítame len identifikátory
                    data = tree.arrays(["runNumber", "eventNumber"])
                    
                    maska = (data["runNumber"] == cielovy_run) & (data["eventNumber"] == cielovy_event)
                    
                    if ak.any(maska):
                        print(f"\n!!! NAŠIEL SOM HO !!!")
                        print(f"Súbor: {subor}")
                        
                        # Teraz vytiahneme energie pre tento nález
                        detaily = tree.arrays(["lep_pt", "met"], entry_start=ak.where(maska)[0][0], entry_stop=ak.where(maska)[0][0]+1)
                        pt = detaily["lep_pt"][0][0] / 1000.0 if len(detaily["lep_pt"][0]) > 0 else 0
                        met = detaily["met"][0] / 1000.0
                        
                        print(f"Namerané pT: {pt:.4f} GeV")
                        print(f"Missing ET: {met:.4f} GeV")
                        nasiel_sa = True
                        break
            except Exception as e:
                continue

    if not nasiel_sa:
        print("\nRun 2950_E4 sa v aktuálnych súboroch nenašiel.")

hromadny_skener()