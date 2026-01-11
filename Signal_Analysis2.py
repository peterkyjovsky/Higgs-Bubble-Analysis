import numpy as np
import matplotlib.pyplot as plt


def find_best_fit_parameters(target_percent=40.2, tolerance=1.0):
    """
    Automaticky hľadá parametre (Sila vákua, Podiel signálu),
    ktoré najlepšie vysvetľujú tvoje namerané dáta (40.2% > 2.0).
    """
    print(f"--- HĽADÁM NAJLEPŠÍ FIT PRE CIEĽ: {target_percent}% ---")

    best_diff = 100.0
    best_params = (0, 0)
    best_result = 0

    # Skúšame rôzne kombinácie sily vákua a podielu signálu
    # Vacuum strength: od 1.0 do 1.8 (krok 0.1)
    # Signal fraction: od 0.3 do 0.7 (krok 0.05)

    vacuum_range = np.arange(1.0, 1.9, 0.1)
    fraction_range = np.arange(0.30, 0.75, 0.05)

    n_events = 50000  # Menšia vzorka pre rýchle hľadanie

    for v_strength in vacuum_range:
        for s_frac in fraction_range:
            # Rýchla simulácia
            percent = run_simulation_core(n_events, v_strength, s_frac)
            diff = abs(percent - target_percent)

            if diff < best_diff:
                best_diff = diff
                best_params = (v_strength, s_frac)
                best_result = percent
                print(f" -> Nový kandidát: Vacuum={v_strength:.1f}, Signal={s_frac:.2f} => {percent:.2f}%")

    print(f"\n--- VÍŤAZNÉ PARAMETRE ---")
    print(f"Sila vákua: {best_params[0]:.1f}")
    print(f"Podiel signálu: {best_params[1]:.2f}")
    print(f"Výsledné percento: {best_result:.2f}% (Odchýlka: {best_diff:.2f})")

    # Spustíme finálnu detailnú simuláciu s víťaznými parametrami
    simulate_higgs_bubble_signal(vacuum_strength=best_params[0], signal_fraction=best_params[1])


def run_simulation_core(n_events, vacuum_strength, signal_fraction):
    """Pomocná funkcia pre rýchly výpočet"""
    n_sig = int(n_events * signal_fraction)
    n_bkg = n_events - n_sig

    # Pozadie
    pt_bkg = np.random.exponential(scale=100, size=n_bkg) + 40
    met_bkg = np.random.normal(pt_bkg, pt_bkg * 0.15)

    # Signál
    pt_sig = np.random.exponential(scale=100, size=n_sig) + 40
    vacuum_fluctuation = np.random.normal(vacuum_strength, 0.4, size=n_sig)
    vacuum_fluctuation = np.maximum(vacuum_fluctuation, 0.0)
    met_sig = np.random.normal(pt_sig * (1 + vacuum_fluctuation), pt_sig * 0.15)

    # Merge
    all_met = np.concatenate([met_bkg, met_sig])
    all_pt = np.concatenate([pt_bkg, pt_sig])

    # Cut > 50
    mask = all_met > 50
    ratios = all_met[mask] / all_pt[mask]

    if len(ratios) == 0: return 0
    return np.sum(ratios > 2.0) / len(ratios) * 100


def simulate_higgs_bubble_signal(n_events=100000, vacuum_strength=1.0, signal_fraction=0.40):
    """
    Finálna vizualizácia s najlepšími parametrami
    """
    print(f"\n--- GENERUJEM FINÁLNY GRAF ---")

    n_sig = int(n_events * signal_fraction)
    n_bkg = int(n_events * (1 - signal_fraction))

    pt_bkg = np.random.exponential(scale=100, size=n_bkg) + 40
    met_bkg = np.random.normal(pt_bkg, pt_bkg * 0.15)

    pt_sig = np.random.exponential(scale=100, size=n_sig) + 40
    vacuum_fluctuation = np.random.normal(vacuum_strength, 0.4, size=n_sig)
    vacuum_fluctuation = np.maximum(vacuum_fluctuation, 0.0)
    met_sig_true = pt_sig * (1 + vacuum_fluctuation)
    met_sig = np.random.normal(met_sig_true, met_sig_true * 0.15)

    all_met = np.concatenate([met_bkg, met_sig])
    all_pt = np.concatenate([pt_bkg, pt_sig])

    mask = all_met > 50
    final_met = all_met[mask]
    final_pt = all_pt[mask]
    ratios = final_met / final_pt

    plt.figure(figsize=(12, 7))
    plt.hist(ratios, bins=100, range=(0, 5), density=True, color='black', histtype='step', linewidth=2,
             label='Model Fit')
    plt.hist(met_bkg / pt_bkg, bins=100, range=(0, 5), density=True, color='gray', alpha=0.3, label='Standard Model',
             weights=np.full(n_bkg, 1 - signal_fraction))
    plt.hist(met_sig / pt_sig, bins=100, range=(0, 5), density=True, color='cyan', alpha=0.3, label='Higgs Bubble',
             weights=np.full(n_sig, signal_fraction))

    plt.axvline(x=2.0, color='red', linestyle='--', label='R=2.0')
    plt.title(f'Best Fit: Vacuum={vacuum_strength:.1f}, Signal={signal_fraction * 100:.0f}%')
    plt.xlabel('Pomer R')
    plt.ylabel('Hustota')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    find_best_fit_parameters()
