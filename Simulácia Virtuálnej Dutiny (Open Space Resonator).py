import numpy as np
import matplotlib.pyplot as plt


def simulate_interference():
    # Rozmery priestoru (v metroch pred loďou)
    x = np.linspace(-10, 10, 500)
    y = np.linspace(0, 20, 500)  # Loď je na Y=0, Tunel chceme smerom Y+
    X, Y = np.meshgrid(x, y)

    # Pozície vysielačov na lodi (Phased Array)
    # Rozostavenie do polkruhu na prednej časti lode
    emitters = [
        (-2, 0), (-1, 0), (1, 0), (2, 0)
    ]

    # Vlnová dĺžka (škálovaná pre vizualizáciu)
    wavelength = 1.0
    k = 2 * np.pi / wavelength

    # Cieľový bod (Focus Point) - Kde chceme otvoriť tunel
    focus_point = (0, 10)

    # Výpočet poľa
    Z = np.zeros_like(X)

    for ex, ey in emitters:
        # Vzdialenosť od vysielača k bodu v priestore
        dist_grid = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)

        # Vzdialenosť od vysielača k cieľovému bodu (pre fázovanie)
        dist_focus = np.sqrt((focus_point[0] - ex) ** 2 + (focus_point[1] - ey) ** 2)

        # Fázový posun: Nastavíme tak, aby v cieľovom bode bola DEŠTRUKTÍVNA interferencia
        # Chceme, aby súčet v bode (0,10) bol NULA (Ticho)
        # Toto je zjednodušený model "Dark Spot" generácie
        phase_shift = -k * dist_focus + np.pi  # +PI zabezpečí inverziu

        # Sčítanie vĺn
        Z += np.sin(k * dist_grid + phase_shift)

    # Energia poľa (Amplitúda na druhú)
    Energy = Z ** 2

    # --- VIZUALIZÁCIA ---
    plt.figure(figsize=(8, 10))

    # Mapa energie
    # Červená = Vysoká energia (Rozbúrené vákuum)
    # Modrá/Biela = Nulová energia (Upokojené vákuum / Tunel)
    plt.pcolormesh(X, Y, Energy, cmap='RdBu_r', shading='auto')

    # Vysielače
    for ex, ey in emitters:
        plt.plot(ex, ey, 'ko', markersize=10, label='Vysielač' if ex == -2 else "")

    # Cieľový tunel
    plt.plot(focus_point[0], focus_point[1], 'g*', markersize=20, label='Otvorený Tunel (Cold Spot)')

    # Loď
    plt.fill_between([-3, 3], -1, 0, color='gray', alpha=0.5)
    plt.text(0, -0.5, "LOĎ", ha='center', fontweight='bold')

    plt.title("Holografický Rezonátor: Vytvorenie 'Ticha' v Otvorenom Priestore", fontsize=14)
    plt.xlabel("X [m]")
    plt.ylabel("Vzdialenosť pred loďou [m]")
    plt.colorbar(label="Intenzita vibrácií mriežky")
    plt.legend(loc='lower right')

    plt.savefig("open_space_tunnel_sim.png")
    print("[OK] Simulácia interferencie uložená.")
    plt.show()


simulate_interference()