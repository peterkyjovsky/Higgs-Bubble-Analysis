import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyzuj_zee(subor_csv):
    print(f"--- Začínam analýzu súboru: {subor_csv} ---")
    
    try:
        # Načítanie dát
        df = pd.read_csv(subor_csv)
        print("Súbor úspešne načítaný.")
        
        # 1. Vyčistenie názvov stĺpcov
        df.columns = df.columns.str.strip()
        
        # 2. Výpočet Invariantnej Hmotnosti
        # Vzorec: M = sqrt( 2*pt1*pt2 * (cosh(eta1-eta2) - cos(phi1-phi2)) )
        print("Počítam invariantnú hmotnosť...")
        
        pt1 = df['pt1']
        pt2 = df['pt2']
        d_eta = df['eta1'] - df['eta2']
        d_phi = df['phi1'] - df['phi2']
        
        M = np.sqrt(2 * pt1 * pt2 * (np.cosh(d_eta) - np.cos(d_phi)))
        df['M'] = M
        
        # 3. Výpis základnej štatistiky
        print(f"Priemerná hmotnosť (celková): {df['M'].mean():.4f} GeV")
        
        # 4. Vykreslenie histogramu
        print("Vytváram histogram...")
        plt.figure(figsize=(10, 6))
        
        # Vykreslíme histogram pre rozsah 60-120 GeV, kde očakávame Z bozón
        # bins=100 znamená, že rozsah rozdelíme na 100 malých stĺpcov
        plt.hist(df['M'], bins=100, range=(60, 120), color='royalblue', alpha=0.7, edgecolor='black')
        
        plt.title('Invariantná hmotnosť Z bozónu (Zee)', fontsize=15)
        plt.xlabel('Invariantná hmotnosť [GeV]', fontsize=12)
        plt.ylabel('Počet udalostí', fontsize=12)
        plt.grid(True, alpha=0.3)
        
        # Pridanie textu s očakávanou hmotnosťou
        plt.axvline(x=91.1876, color='red', linestyle='--', label='Z mass (91.2 GeV)')
        plt.legend()
        
        # Uloženie grafu
        output_file = 'z_mass_histogram.png'
        plt.savefig(output_file)
        print(f"Graf bol úspešne uložený do súboru: {output_file}")
        
        # Ak bežíte lokálne (nie na serveri), môžete odkomentovať:
        # plt.show()

    except FileNotFoundError:
        print(f"CHYBA: Súbor '{subor_csv}' nebol nájdený.")
    except Exception as e:
        print(f"CHYBA: {str(e)}")

if __name__ == "__main__":
    analyzuj_zee('Zee.csv')