import numpy as np
import matplotlib.pyplot as plt


def simulate_higgs_bubble_signal(n_events=100000, vacuum_strength=1.0, signal_fraction=0.40):
    """
    Simuluje zmes Standard Model pozadia a Higgs Bubble signálu.
    Cieľom je reprodukovať tvoj výsledok (40% udalostí s R > 2.0).

    Parametre:
    - vacuum_strength: Koľko extra energie z vákua sa uvoľní (násobok pT jetu).
      Ak vacuum_strength = 1.0, potom MET ~ 2 * Jet_pT.
    - signal_fraction: Akú časť dát tvorí Bublina (vs. bežné Z bozóny).
      Tvoj odhad je cca 40%.
    """
    print(f"--- Spúšťam simuláciu Higgsovej Bubliny ---")
    print(f"Podiel signálu: {signal_fraction * 100}%")
    print(f"Sila vákua (Model parameter): {vacuum_strength}")

    # --- 1. GENERUJEME POZADIE (Standard Model) ---
    n_bkg = int(n_events * (1 - signal_fraction))
    pt_bkg = np.random.exponential(scale=100, size=n_bkg) + 40
    # SM: MET = Jet pT (plus šum detektora)
    met_bkg = np.random.normal(pt_bkg, pt_bkg * 0.15)

    # --- 2. GENERUJEME SIGNÁL (Higgs Bubble) ---
    # Hypotéza: Bublina pri kolapse uvoľní energiu jetu + energiu vákua.
    # MET_signal = pT + (pT * vacuum_factor)
    # Kde vacuum_factor nie je konštanta, ale má určité rozdelenie (kvantová fluktuácia).

    n_sig = int(n_events * signal_fraction)
    pt_sig = np.random.exponential(scale=100, size=n_sig) + 40

    # Modelujeme fluktuáciu vákuovej energie.
    # Predpokladáme, že bublina niekedy "nasaje" viac, niekedy menej.
    # Použijeme Landau rozdelenie alebo Gaussovu distribúciu posunutú o vacuum_strength.
    vacuum_fluctuation = np.random.normal(vacuum_strength, 0.4, size=n_sig)
    # Orezanie, aby vákuum nebralo energiu (negatívna energia)
    vacuum_fluctuation = np.maximum(vacuum_fluctuation, 0.0)

    # Kľúčová rovnica tvojej teórie:
    # MET = pT (odraz) + pT * vacuum_fluctuation (kolaps bubliny)
    met_sig_true = pt_sig * (1 + vacuum_fluctuation)

    # Pridáme šum detektora
    met_sig = np.random.normal(met_sig_true, met_sig_true * 0.15)

    # --- 3. SPOJENIE DÁT A ANALÝZA ---
    all_met = np.concatenate([met_bkg, met_sig])
    all_pt = np.concatenate([pt_bkg, pt_sig])

    # Aplikujeme cut MET > 50 GeV (ako v tvojej analýze)
    mask = all_met > 50
    final_met = all_met[mask]
    final_pt = all_pt[mask]

    ratios = final_met / final_pt

    percent_above_2 = np.sum(ratios > 2.0) / len(ratios) * 100

    print(f"\n--- VÝSLEDOK SIMULÁCIE ---")
    print(f"Percento R > 2.0: {percent_above_2:.2f}% (Cieľ: ~40.2%)")

    # --- 4. VIZUALIZÁCIA ---
    plt.figure(figsize=(12, 7))

    # Celkový histogram
    plt.hist(ratios, bins=100, range=(0, 5), density=True,
             color='black', histtype='step', linewidth=2, label='Simulované dáta (Mix)')

    # Komponent Pozadia (SM)
    # Pre vizualizáciu musíme prepočítať váhy, aby sedeli na celkový počet
    plt.hist(met_bkg / pt_bkg, bins=100, range=(0, 5), density=True,
             color='gray', alpha=0.3, label='Standard Model (Pozadie)', weights=np.full(n_bkg, 1 - signal_fraction))

    # Komponent Signálu (Bubble)
    plt.hist(met_sig / pt_sig, bins=100, range=(0, 5), density=True,
             color='cyan', alpha=0.3, label='Higgs Bubble (Signál)', weights=np.full(n_sig, signal_fraction))

    plt.axvline(x=2.0, color='red', linestyle='--', label='Tvoja hranica R=2.0')

    plt.title(f'Higgs Bubble Model: Signal ({signal_fraction * 100}%) + SM Background')
    plt.xlabel('Pomer R = MET / Jet_pT')
    plt.ylabel('Hustota pravdepodobnosti')
    plt.legend()
    plt.grid(alpha=0.3)

    plt.show()


# Spustenie
if __name__ == "__main__":
    # Experimentuj s týmito číslami, aby si dostal svojich 40.20%
    # Skús vacuum_strength okolo 0.8 až 1.2
    simulate_higgs_bubble_signal(vacuum_strength=1.1, signal_fraction=0.45)
