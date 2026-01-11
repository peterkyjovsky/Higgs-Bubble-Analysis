import matplotlib.pyplot as plt
import numpy as np


def simulate_standard_model_background(n_events=100000):
    """
    Simuluje proces Z(->nu nu) + Jet v Standardnom modeli.
    Cieľom je zistiť, aké je prirodzené rozdelenie pomeru R = MET / Jet_pT.
    """
    print(f"--- Spúšťam simuláciu Standard Model Background ({n_events} udalostí) ---")

    # 1. Generovanie SKUTOČNEJ hybnosti (True pT)
    # V hadrónových zrážkach (LHC) počet udalostí klesá exponenciálne s energiou.
    # Generujeme pT jetov od 40 GeV do 1000 GeV.
    true_jet_pt = np.random.exponential(scale=100, size=n_events) + 40

    # 2. Fyzika Standardného Modelu (Zachovanie hybnosti)
    # V procese Z + Jet sú tieto dva objekty "back-to-back".
    # Ideálne platí: True MET = True Jet pT
    true_met = true_jet_pt.copy()

    # 3. Simulácia DETEKTORA (Smearing / Resolution)
    # Detektory nie sú dokonalé. Energia jetov má rozlíšenie cca 10-15%.
    # Energia MET má tiež svoje rozlíšenie.
    jet_resolution = 0.15  # 15% chyba merania jetu
    met_resolution = 0.15  # 15% chyba merania MET

    # Aplikujeme Gaussovský šum na merania
    measured_jet_pt = np.random.normal(true_jet_pt, true_jet_pt * jet_resolution)
    measured_met = np.random.normal(true_met, true_met * met_resolution)

    # Ošetríme záporné hodnoty (fyzikálne nemožné, ale matematika ich môže vyrobiť)
    measured_jet_pt = np.maximum(measured_jet_pt, 0.1)
    measured_met = np.maximum(measured_met, 0.1)

    # 4. Aplikácia TVOJICH FILTROV (Cuts)
    # Tvoj report uvádza: MET > 50 GeV
    mask = (measured_met > 50)

    # Filtrované dáta
    final_met = measured_met[mask]
    final_jet_pt = measured_jet_pt[mask]

    print(f"Počet udalostí po reze MET > 50 GeV: {len(final_met)}")

    # 5. Výpočet POMERU R
    ratios = final_met / final_jet_pt

    # 6. Štatistika
    mean_ratio = np.mean(ratios)
    events_above_2 = np.sum(ratios > 2.0)
    percent_above_2 = (events_above_2 / len(ratios)) * 100

    print(f"\n--- VÝSLEDKY STANDARD MODELU ---")
    print(f"Priemerný pomer R (MET/Jet): {mean_ratio:.4f}")
    print(f"Štandardná odchýlka: {np.std(ratios):.4f}")
    print(f"Počet udalostí s R > 2.0: {events_above_2} z {len(ratios)}")
    print(f"Percento udalostí s R > 2.0: {percent_above_2:.2f}%")
    print("-" * 30)

    # 7. Vizualizácia
    plt.figure(figsize=(10, 6))

    # Histogram simulovaných dát
    plt.hist(ratios, bins=100, range=(0, 5), density=True, alpha=0.6, color='gray', label='Standard Model (Simulácia)')

    # Zvýraznenie oblasti R > 2.0
    plt.axvline(x=2.0, color='red', linestyle='--', linewidth=2, label='Hranica R=2.0')

    # Pridanie textu s výsledkami do grafu
    plt.text(2.1, 0.5, f'SM Predpoveď:\nLen {percent_above_2:.1f}% > 2.0', color='red', fontweight='bold')

    plt.title('Očakávaná distribúcia pre Standard Model (Z->vv + Jet)')
    plt.xlabel('Pomer R = MET / Jet_pT')
    plt.ylabel('Pravdepodobnosť')
    plt.legend()
    plt.grid(alpha=0.3)

    # Uloženie a zobrazenie
    plt.tight_layout()
    plt.show()


# Spustenie funkcie
if __name__ == "__main__":
    simulate_standard_model_background()
