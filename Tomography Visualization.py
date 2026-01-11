import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter1d


def generate_best_fit_data(n_events=2239):
    """
    Generuje dáta na základe tvojho 'Best Fit' modelu:
    - 65% Higgs Bubble (Vacuum Strength ~ 1.1)
    - 35% Standard Model Background
    Túto funkciu nahraď svojimi REÁLNYMI dátami, ak ich máš načítané v poliach.
    """
    print(f"--- Generujem {n_events} udalostí podľa modelu (Signal 65%, Vacuum 1.1) ---")

    # Parametre z tvojho fitu
    signal_fraction = 0.65
    vacuum_strength = 1.1

    n_sig = int(n_events * signal_fraction)
    n_bkg = n_events - n_sig

    # --- POZADIE (Standard Model) ---
    # Exponential decay pre pT (bežná fyzika zrážok)
    pt_bkg = np.random.exponential(scale=100, size=n_bkg) + 50
    # MET ~ pT (s chybou merania)
    met_bkg = np.random.normal(pt_bkg, pt_bkg * 0.15)

    # --- SIGNÁL (Higgs Bubble) ---
    pt_sig = np.random.exponential(scale=120, size=n_sig) + 50  # Trochu tvrdšie spektrum pre signál

    # Tu modelujeme závislosť od energie (ak existuje).
    # Pre simuláciu zatiaľ necháme konštantnú silu 1.1, aby sme videli "Scenár A".
    # Ak chceš simulovať "Scenár B" (nestabilitu), odkomentuj riadok nižšie:
    # vacuum_strength_dynamic = 1.1 + (pt_sig / 1000.0) * 0.5 # S rastúcou energiou rastie sila
    vacuum_fluctuation = np.random.normal(vacuum_strength, 0.4, size=n_sig)
    vacuum_fluctuation = np.maximum(vacuum_fluctuation, 0.0)

    met_sig = pt_sig * (1 + vacuum_fluctuation)
    # Pridáme šum detektora
    met_sig = np.random.normal(met_sig, met_sig * 0.10)

    # Zlúčenie
    pt_all = np.concatenate([pt_bkg, pt_sig])
    met_all = np.concatenate([met_bkg, met_sig])

    # Výpočet Transverzálnej hmotnosti (zjednodušený pre vizualizáciu)
    # MT ~ sqrt(2 * pT * MET * (1 - cos(dphi))) -> predpokladáme back-to-back (cos=-1)
    mt_all = np.sqrt(2 * pt_all * met_all * 2)  # Zjednodušenie pre farbu bodov

    # Aplikácia rezu MET > 50 (už je v generovaní, ale pre istotu)
    mask = met_all > 50
    return pt_all[mask], met_all[mask], mt_all[mask]


def plot_higgs_tomography(pt, met, mt):
    """
    Vykreslí mapu stability Higgsovho poľa.
    """
    ratios = met / pt

    plt.figure(figsize=(12, 8))

    # 1. Scatter Plot (Všetky udalosti)
    # Farbíme podľa MT, aby sme videli, kde sú "ťažké" bubliny
    sc = plt.scatter(pt, ratios, c=mt, cmap='plasma', alpha=0.5, s=15, label='Udalosti (Bubliny)')
    plt.colorbar(sc, label='Transverzálna hmotnosť $M_T$ [GeV]')

    # 2. Running Average (Trendová čiara - Odozva vákua)
    # Zoradíme dáta podľa pT pre výpočet kĺzavého priemeru
    sort_idx = np.argsort(pt)
    pt_sorted = pt[sort_idx]
    r_sorted = ratios[sort_idx]

    # Vyhladenie (Gaussov filter) pre jasnú čiaru
    r_trend = gaussian_filter1d(r_sorted, sigma=50)

    plt.plot(pt_sorted, r_trend, color='lime', linewidth=3, label='Priemerná odozva vákua (Trend)')
    plt.axhline(y=2.0, color='red', linestyle='--', linewidth=2, label='Kritická hranica R=2.0')
    plt.axhline(y=1.0, color='gray', linestyle=':', label='Standard Model (R=1.0)')

    # Popisy a limity
    plt.title('Higgs Field Tomography: Stability Map\n(Odozva vákua v závislosti od energie nárazu)', fontsize=14)
    plt.xlabel('Energia sondy: $p_T$ Jetu [GeV]', fontsize=12)
    plt.ylabel('Odozva vákua: Pomer $R = MET / p_T$', fontsize=12)
    plt.ylim(0, 4.5)
    plt.xlim(50, 800)  # Prispôsob podľa rozsahu tvojich dát
    plt.legend(loc='upper right')
    plt.grid(True, alpha=0.3)

    # Pridanie textu pre interpretáciu
    plt.text(60, 4.0, "Zóna vysokej nestability", color='purple', fontweight='bold')
    plt.text(60, 0.5, "Zóna Standard Modelu", color='gray', fontweight='bold')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # --- PÔVODNÝ KÓD (Simulácia) ---
    # pt_data, met_data, mt_data = generate_best_fit_data()

    # --- NOVÝ KÓD (Tvoje reálne dáta) ---
    # Sem dosaď svoje polia, ktoré máš v pamäti z predchádzajúcej analýzy:
    pt_data = tvoje_pole_pt_jetov  # Napr. real_jet_pt
    met_data = real_met  # Napr. real_met

    # Transverzálnu hmotnosť si dopočítaj, ak ju nemáš v poli:
    # MT = sqrt(2 * pT * MET * (1 - cos(dphi)))
    # Pre vizualizáciu stačí aproximácia pre back-to-back (dphi=pi):
    mt_data = np.sqrt(4 * pt_data * met_data)

    # 2. Vykresli mapu
    plot_higgs_tomography(pt_data, met_data, mt_data)