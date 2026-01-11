import uproot
import pandas as pd
import numpy as np

# Sem napíšte presný názov súboru, ktorý vidíte v priečinku Data
# Pravdepodobne to bude: 'data_A.Wenu.root' alebo podobne
file_name = "data_A.Wenu.root" 

def analyzuj():
    print(f"Prehľadávam súbor {file_name}...")
    try:
        # Otvoríme strom 'mini', ktorý obsahuje surové dáta zrážok
        with uproot.open(file_name + ":mini") as tree:
            # Načítame len dôležité stĺpce pre Run 2950
            # Premenné: runNumber, eventNumber, lep_pt (hybnosť), met_et (neutríno)
            df = tree.arrays(["runNumber", "eventNumber", "lep_pt", "met_et", "lep_eta"], library="pd")
            
            # Filter pre váš konkrétny event
            moj_event = df[(df.runNumber == 2950) & (df.eventNumber == 4)]
            
            if not moj_event.empty:
                # CERN ukladá dáta v MeV, my chceme GeV (preto delíme 1000)
                pt = moj_event.iloc[0]['lep_pt'] / 1000.0
                met = moj_event.iloc[0]['met_et'] / 1000.0
                eta = moj_event.iloc[0]['lep_eta']
                
                print("\n--- NÁJDENÝ EVENT 2950_E4 ---")
                print(f"Namerané pT (Fotón/Leptón): {pt:.4f} GeV")
                print(f"Missing ET (Neutríno): {met:.4f} GeV")
                print(f"Uhol výletu (eta): {eta:.4f}")
                
                # Výpočet vašej bilancie
                moje_cislo = 28.18829
                rozdiel = pt - moje_cislo
                print(f"\nVaša predikcia: {moje_cislo} GeV")
                print(f"Odchýlka od nameraného pT: {rozdiel:.4f} GeV")
                
            else:
                print("\nV tomto súbore sa Run 2950_E4 nenachádza.")
                print("Skúste zmeniť 'data_A' na 'data_B', 'data_C' alebo 'data_D'.")
                
    except Exception as e:
        print(f"Chyba: {e}")

if __name__ == "__main__":
    analyzuj()
