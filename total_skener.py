import uproot
import awkward as ak
import numpy as np
import glob
import os

def najdi_strom(subor_objekt):
    """Pomocná funkcia, ktorá nájde správny 'strom' s dátami vo vnútri súboru."""
    kluce = subor_objekt.keys()
    # Najčastejšie názvy stromov v ATLAS dátach
    mozne_nazvy = ["mini", "analysis", "nominal", "data", "physics"]
    
    for k in kluce:
        cisty_nazov = k.split(";")[0] # Odstráni verziu ;1
        if cisty_nazov in mozne_nazvy:
            return cisty_nazov
    # Ak nenájde známy, vráti prvý, ktorý nájde
    return kluce[0].split(";")[0] if len(kluce) > 0 else None

def skenuj_vsetko():
    # Nájde všetky .root súbory v aktuálnom priečinku
    zoznam_suborov = glob.glob("*.root")
    
    if not zoznam_suborov:
        print("CHYBA: V tomto priečinku nie sú žiadne .root súbory!")
        return

    print(f"Nájdených {len(zoznam_suborov)} súborov na analýzu. Spúšťam 'Digitálny Skener'...\n")

    for subor in zoznam_suborov:
        print(f"--> Skenujem súbor: {subor}")
        try:
            with uproot.open(subor) as f:
                strom_meno = najdi_strom(f)
                if not strom_meno:
                    print("    Skočené (neznámy formát stromu)")
                    continue
                
                tree = f[strom_meno]
                # Zistíme dostupné stĺpce (nie každý súbor má 'lep_pt', niekde je 'lep_pt_0')
                dostupne_kluce = tree.keys()
                
                # Dynamický výber názvov premenných
                nazov_pt = "lep_pt" if "lep_pt" in dostupne_kluce else "leptons_pt"
                nazov_met = "met" if "met" in dostupne_kluce else "met_et"
                
                # Ak tam nie sú kľúčové dáta, preskočíme
                if nazov_pt not in dostupne_kluce:
                    print(f"    Skočené (chýba stĺpec {nazov_pt})")
                    continue

                # Načítanie dát
                data = tree.arrays(["runNumber", "eventNumber", nazov_pt, nazov_met])
                
                # Prevod na GeV
                pt_gev = data[nazov_pt] / 1000.0
                met_gev = data[nazov_met] / 1000.0
                runy = data["runNumber"]
                eventy = data["eventNumber"]

                # --- PODMIENKA 1: Hľadáme Run 2950 ---
                maska_run = (runy == 2950)
                if ak.any(maska_run):
                    print(f"\n    !!! NÁJDENÝ RUN 2950 !!!")
                    print(f"    Skontrolujte Event 4 v tomto súbore!")
                    # Výpis detailov pre tento Run
                    idx = ak.where(maska_run)[0]
                    for i in idx:
                        print(f"    Event: {eventy[i]}, pT: {pt_gev[i]}, MET: {met_gev[i]:.4f}")

                # --- PODMIENKA 2: Hľadáme vašu teóriu (28.188 alebo 31.4) ---
                # Hľadáme pT v okne 31.3-31.5 OR 28.1-28.3
                maska_teoria = ak.any((pt_gev > 31.35) & (pt_gev < 31.45), axis=1) | \
                               ak.any((pt_gev > 28.15) & (pt_gev < 28.25), axis=1)
                
                nalezov = ak.sum(maska_teoria)
                
                if nalezov > 0:
                    print(f"    Nájdených {nalezov} eventov s energiou blízko 31.4 alebo 28.18 GeV!")
                    
                    # Vypíšeme prvých 3 zaujímavých nálezov z každého súboru
                    zaujimave_data = data[maska_teoria]
                    zaujimave_pt = pt_gev[maska_teoria]
                    zaujimave_met = met_gev[maska_teoria]
                    
                    for i in range(min(3, nalezov)):
                        print(f"      -> Event {zaujimave_data[i].eventNumber}: pT={zaujimave_pt[i].tolist()} GeV, MET={zaujimave_met[i]:.4f} GeV")
                        
                        # Rýchla kontrola vašej bilancie
                        # Ak je MET + pT blízko 80, vypíšeme to
                        if len(zaujimave_pt[i]) > 0:
                            sucet = zaujimave_pt[i][0] + zaujimave_met[i]
                            if 50 < sucet < 90:
                                print(f"         [ANALÝZA] Súčet pT+MET = {sucet:.4f} GeV (Blízko W bozónu?)")

        except Exception as e:
            print(f"    Chyba pri čítaní súboru: {e}")
            continue
            
    print("\n--- Skenovanie ukončené ---")

if __name__ == "__main__":
    skenuj_vsetko()