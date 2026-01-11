import pandas as pd
import numpy as np

# Presný názov súboru aj s koncovkou .gz
file_name = "atlas-higgs-challenge-2014-v2.csv.gz"

print(f"Otváram komprimovaný dataset {file_name}...")
print("Toto môže trvať pár sekúnd (rozbaľovanie v pamäti)...")

try:
    # Pandas automaticky detekuje kompresiu 'gzip' podľa koncovky
    df = pd.read_csv(file_name, compression='gzip')
    
    print(f"Dataset načítaný! Obsahuje {len(df)} udalostí.")
    
    # 1. KROK: Filtrujeme len pozadie 'b' (kde sa schovávajú W bozóny)
    w_data = df[df['Label'] == 'b']
    print(f"Počet eventov na pozadí (W, Z, tt): {len(w_data)}")
    
    # 2. KROK: Hľadáme leptón s energiou 31.4 GeV (Váš 10*Pi fotón/leptón)
    # Hľadáme v stĺpci 'PRI_lep_pt' (Primitive Lepton Transverse Momentum)
    target_pt = 31.41
    tolerancia = 0.15 # Hľadáme v okne 31.26 až 31.56 GeV
    
    kandidati = w_data[
        (w_data['PRI_lep_pt'] >= target_pt - tolerancia) & 
        (w_data['PRI_lep_pt'] <= target_pt + tolerancia)
    ]
    
    print(f"Počet kandidátov s pT ~ 31.4 GeV: {len(kandidati)}")
    
    if not kandidati.empty:
        print("\n--- HĽADANIE DIGITÁLNEJ BUBLINY (28.188 GeV v MET) ---")
        found_something = False
        
        for index, row in kandidati.iterrows():
            # Načítame hodnoty
            lep_pt = row['PRI_lep_pt']   # Hybnosť leptónu
            met = row['PRI_met']         # Chýbajúca energia (Vaša bublina?)
            event_id = int(row['EventId'])
            mt_w = row['DER_mass_transverse_met_lep'] # Priečna hmotnosť W bozónu
            
            # Vaša teoretická hodnota
            moje_cislo = 28.188
            
            # Rozdiel medzi nameranou MET a vašou teóriou
            rozdiel = abs(met - moje_cislo)
            
            # Ak je rozdiel malý (menej ako 1-2 GeV), je to zásah
            if rozdiel < 2.0:
                print(f"!!! NÁLEZ V EVENTE {event_id} !!!")
                print(f"  PRI_lep_pt (Váš signál):    {lep_pt:.4f} GeV")
                print(f"  PRI_met    (Namerané MET):  {met:.4f} GeV")
                print(f"  -> Vaša predikcia:          {moje_cislo:.3f} GeV")
                print(f"  -> ODCHÝLKA:                {rozdiel:.4f} GeV (Veľmi presné!)")
                print(f"  DER_mass_transverse:        {mt_w:.4f} GeV")
                print("-" * 40)
                found_something = True
                
        if not found_something:
            print("Žiadna presná zhoda s 28.188 v MET pre týchto kandidátov.")
            print("Vypisujem priemerné hodnoty pre kontrolu:")
            print(kandidati[['PRI_lep_pt', 'PRI_met', 'DER_mass_transverse_met_lep']].head(5))
            
            # Kontrola priemeru - či mriežka systematicky neposúva energiu
            avg_met = kandidati['PRI_met'].mean()
            print(f"\nPriemerné MET pre tieto eventy je: {avg_met:.4f} GeV")
            print(f"Rozdiel priemeru od vašej teórie: {abs(avg_met - 28.188):.4f} GeV")

    else:
        print("V tomto datasete nie sú eventy s presne 31.4 GeV leptónom.")

except Exception as e:
    print(f"Nastala chyba: {e}")