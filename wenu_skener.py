import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyzuj_wenu(subor_csv):
    print(f"--- Začínam analýzu W \u2192 e\u03BD: {subor_csv} ---")
    
    try:
        # Načítanie dát
        df = pd.read_csv(subor_csv)
        df.columns = df.columns.str.strip()
        print(f"Súbor načítaný. Počet udalostí: {len(df)}")
        
        # Očakávané stĺpce pre W analýzu: pt, phi (elektrón) a MET, phiMET (neutríno)
        required = ['pt', 'phi', 'MET', 'phiMET']
        if not all(col in df.columns for col in required):
            print(f"Pozor: Nenašiel som všetky potrebné stĺpce. Nájdené: {list(df.columns)}")
            return

        # Fyzikálne filtre pre elektrónový kanál
        # pt > 25 GeV a často sa používa prísnejšia izolácia pre elektróny
        df_signal = df[(df['pt'] > 25)].copy()
        
        # Ak súbor obsahuje informáciu o kvalite (napr. HoverE alebo sigmaEtaEta), 
        # tu by sa dali pridať ďalšie filtre. Pre teraz použijeme základné:
        print(f"Počet udalostí po základnom pt filtri: {len(df_signal)}")

        # Výpočet Transverzálnej hmotnosti (Transverse Mass)
        # MT = sqrt( 2 * pt * MET * (1 - cos(phi - phiMET)) )
        print("Počítam transverzálnu hmotnosť M_T...")
        
        pt = df_signal['pt']
        met = df_signal['MET']
        d_phi = df_signal['phi'] - df_signal['phiMET']
        
        mt = np.sqrt(2 * pt * met * (1 - np.cos(d_phi)))
        df_signal['MT'] = mt
        
        # Vykreslenie histogramu
        plt.figure(figsize=(10, 6))
        
        # Jacobian peak pre W bozón (hmotnosť ~80.4 GeV)
        plt.hist(df_signal['MT'], bins=100, range=(0, 120), color='mediumseagreen', alpha=0.8, edgecolor='darkgreen', label='Dáta (W \u2192 e\u03BD)')
        
        plt.axvline(x=80.38, color='red', linestyle='--', linewidth=2, label='Tabuľková M_W (80.4 GeV)')
        
        plt.title('Transverzálna hmotnosť W \u2192 e\u03BD (CMS Open Data)', fontsize=15)
        plt.xlabel('Transverzálna hmotnosť M_T [GeV]', fontsize=12)
        plt.ylabel('Počet udalostí', fontsize=12)
        plt.legend()
        plt.grid(axis='y', alpha=0.3)
        
        # Štatistický box
        textstr = '\n'.join((
            f'Udalostí: {len(df_signal)}',
            f'Priemerná M_T: {df_signal["MT"].mean():.2f} GeV'))
        plt.text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
                 verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

        output_file = 'wenu_mass_histogram.png'
        plt.savefig(output_file, dpi=300)
        print(f"Graf bol úspešne uložený ako: {output_file}")

    except Exception as e:
        print(f"CHYBA: {str(e)}")

if __name__ == "__main__":
    analyzuj_wenu('Wenu.csv')