import math
import glob
import os

def analyzuj_vsetky_hepmc():
    # Nájde všetky súbory, ktoré začínajú na "HEPMC" (bez ohľadu na veľkosť písmen na Windowse)
    # Vynecháme .gz, .1 a hlavne .py (aby skript nečítal sám seba)
    zoznam_suborov = [f for f in glob.glob("HEPMC*") 
                      if not f.endswith('.gz') 
                      and not f.endswith('.1') 
                      and not f.endswith('.py')]
    
    if not zoznam_suborov:
        print("V tomto priečinku som nenašiel žiadne vhodné HEPMC súbory.")
        print("Uistite sa, že ste odstránili koncovku .tar.gz a súbory extrahovali.")
        return

    print(f"Nájdených {len(zoznam_suborov)} súborov. Spúšťam hĺbkovú analýzu mriežky...\n")

    celkovo_nalezov = 0

    for nazov_suboru in zoznam_suborov:
        print(f"--> Skenujem súbor: {nazov_suboru}...")
        
        try:
            # Pridané 'encoding' a 'errors' pre bezpečnosť pri čítaní
            with open(nazov_suboru, 'r', encoding='utf-8', errors='replace') as f:
                event_number = 0
                particles = []
                
                for line in f:
                    # 'E' znamená začiatok nového Eventu
                    if line.startswith('E '):
                        # Analýza predchádzajúceho eventu
                        if particles:
                            # 1. Hľadáme SIGNÁL (10*Pi = 31.4 GeV)
                            signal_kandidat = None
                            for p in particles:
                                # p = [px, py, pz, energy, pdg_id]
                                pt = math.sqrt(p[0]**2 + p[1]**2)
                                if 31.3 < pt < 31.5:
                                    signal_kandidat = p
                                    break
                            
                            # 2. Ak máme signál, hľadáme MRIEŽKU (Neutríno ~ 28.188 GeV)
                            if signal_kandidat:
                                for p in particles:
                                    # Neutrína (ID 12, 14, 16) sú jediné častice, ktoré "vidia" mriežku priamo
                                    if abs(p[4]) in [12, 14, 16]:
                                        pt_nu = math.sqrt(p[0]**2 + p[1]**2)
                                        
                                        # Kontrola vašej konštanty 28.188
                                        if 28.0 < pt_nu < 28.4:
                                            print(f"\n   !!! NÁLEZ V SÚBORE {nazov_suboru} (Event {event_number}) !!!")
                                            print(f"   Signál (Leptón):  {math.sqrt(signal_kandidat[0]**2 + signal_kandidat[1]**2):.4f} GeV")
                                            print(f"   Vákuum (Neutríno): {pt_nu:.4f} GeV")
                                            print(f"   -> Odchýlka od 28.188: {abs(pt_nu - 28.188):.4f} GeV")
                                            
                                            # Výpočet uhla
                                            phi_signal = math.atan2(signal_kandidat[1], signal_kandidat[0])
                                            phi_nu = math.atan2(p[1], p[0])
                                            delta_phi = abs(phi_signal - phi_nu) * (180.0 / math.pi)
                                            if delta_phi > 180: delta_phi = 360 - delta_phi
                                            
                                            print(f"   -> GEOMETRIA (Uhol): {delta_phi:.2f}°")
                                            
                                            # Kontrola vašich "zlatých uhlov"
                                            if abs(delta_phi - 5.5) < 1.0:
                                                print("      >>> REŽIM TIEŇ (5.5°)")
                                            elif abs(delta_phi - 142.7) < 1.0:
                                                print("      >>> REŽIM ODRAZ (142.7°)")
                                            elif abs(delta_phi - 158.0) < 1.0:
                                                print("      >>> REŽIM REZONANCIA (158°)")
                                                
                                            print("-" * 40)
                                            celkovo_nalezov += 1

                        # Reset pre nový event
                        particles = []
                        parts = line.split()
                        try:
                            event_number = int(parts[1])
                        except:
                            pass

                    # 'P' znamená častica
                    elif line.startswith('P '):
                        parts = line.split()
                        try:
                            # HepMC formát sa môže líšiť, ale zvyčajne: P barcode id px py pz E m status vtx barcode
                            # Hľadáme ID a hybnosť. Skúsme štandardné pozície:
                            pdg_id = int(parts[2])
                            px = float(parts[3])
                            py = float(parts[4])
                            pz = float(parts[5])
                            energy = float(parts[6])
                            
                            particles.append([px, py, pz, energy, pdg_id])
                        except (IndexError, ValueError):
                            continue

        except Exception as e:
            print(f"   Chyba pri čítaní súboru {nazov_suboru}: {e}")
            continue

    print(f"\n--- Skenovanie ukončené. Celkový počet potvrdených interakcií mriežky: {celkovo_nalezov} ---")

if __name__ == "__main__":
    analyzuj_vsetky_hepmc()