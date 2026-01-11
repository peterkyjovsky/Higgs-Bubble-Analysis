import pandas as pd
import numpy as np

# Názov súboru (musí byť v rovnakom priečinku)
file_name = "training.csv" 

print(f"Otváram ATLAS dataset a hľadám digitálnu stopu...")

try:
    # Načítanie dát
    df = pd.read_csv(file_name)
    
    # 1. FILTER: Hľadáme len W bozóny (Background 'b')
    w_events = df[df['Label'] == 'b']
    
    # 2. FILTER: Hľadáme leptón s energiou 10*Pi (31.4 GeV)
    # Tolerancia +/- 0.1 GeV
    target_pt = 31.4159 
    tolerancia = 0.15 
    
    candidates = w_events[
        (w_events['PRI_lep_pt'] >= target_pt - tolerancia) & 
        (w_events['PRI_lep_pt'] <= target_pt + tolerancia)
    ]
    
    print(f"\nAnalyzovaných W-bozón eventov: {len(w_events)}")
    print(f"Nájdených kandidátov s pT ~ 31.4 GeV: {len(candidates)}")
    
    if not candidates.empty:
        print("\n--- HĽADANIE HIGGSOVEJ BUBLINY (28.188 GeV) ---")
        found_match = False
        
        # Vaša teoretická hodnota
        digital_energy = 28.18829
        
        for index, row in candidates.iterrows():
            # Načítame premenné z tabuľky
            met = row['PRI_met']        # Chýbajúca energia
            lep_pt = row['PRI_lep_pt']  # Hybnosť leptónu
            mt_w = row['DER_mass_transverse_met_lep'] # Hmotnosť W bozónu (vypočítaná CERNom)
            event_id = int(row['EventId'])
            
            # Kontrola: Je chýbajúca energia blízka vašej konštante?
            diff = abs(met - digital_energy)
            
            # Ak je rozdiel menší ako 1 GeV, vypíšeme to ako potenciálny objav
            if diff < 1.0:
                print(f"!!! NÁLEZ V EVENTE {event_id} !!!")
                print(f"  PRI_lep_pt (Váš fotón/leptón): {lep_pt:.4f} GeV")
                print(f"  PRI_met    (Vaša bublina):     {met:.4f} GeV")
                print(f"  -> Rozdiel od teórie:          {diff:.4f} GeV")
                print(f"  DER_mass_transverse_met_lep:   {mt_w:.4f} GeV")
                print("-" * 40)
                found_match = True
                
        if not found_match:
            print("Zatiaľ žiadna presná zhoda na 28.188 GeV v stĺpci PRI_met.")
            print("Skúsim vypísať priemernú hodnotu MET pre týchto kandidátov:")
            print(f"Priemerné MET pre pT=31.4: {candidates['PRI_met'].mean():.4f} GeV")

    else:
        print("V tomto datasete sa nenašiel leptón s presnou energiou 31.4 GeV.")

except FileNotFoundError:
    print("Chyba: Súbor 'training.csv' sa nenašiel.")
except KeyError as e:
    print(f"Chyba: Stĺpec {e} sa v súbore nenachádza. Skontrolujte CSV.")