import numpy as np
import matplotlib.pyplot as plt


def simulate_ring_gate():
    # Rozmery priestoru (Prierez tunelom)
    # Rám má polomer 5 metrov
    side = 8  # Zobrazíme 8x8 metrov
    x = np.linspace(-side, side, 400)
    y = np.linspace(-side, side, 400)
    X, Y = np.meshgrid(x, y)

    # Parametre Kruhového Rámu
    radius = 5.0  # Polomer brány
    n_emitters = 36  # Počet vysielačov po obvode (každých 10 stupňov)

    # Generovanie pozícií vysielačov
    angles = np.linspace(0, 2 * np.pi, n_emitters, endpoint=False)
    emitters = []
    for ang in angles:
        emitters.append((radius * np.cos(ang), radius * np.sin(ang)))

    # Vlnová dĺžka (škálovaná)
    wavelength = 1.0
    k = 2 * np.pi / wavelength

    # Výpočet poľa (Superpozícia)
    Z = np.zeros_like(X)

    for ex, ey in emitters:
        # Vzdialenosť od vysielača k bodu v priestore
        dist = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)

        # Fázovanie:
        # Chceme DEŠTRUKTÍVNU interferenciu v strede (0,0)
        # Vzdialenosť do stredu je 'radius'
        # Fáza musí byť nastavená tak, aby sin(k*radius + phi) = 0
        # Alebo presnejšie, aby sa sumárne vyrušili.
        # Pri kruhovej symetrii, ak všetci vysielajú rovnako, v strede vznikne buď pík alebo nula.
        # My chceme "ticho" (low energy) v strede a "hluk" na okraji.
        # Použijeme Besselov mód J0 (tlmenie v strede vyžaduje špecifický posun)

        phase_shift = np.pi  # Inverzia fázy pre vytvorenie "diery"

        Z += np.sin(k * dist + phase_shift)

    # Energia (Intenzita)
    # Logaritmická škála pre lepšiu viditeľnosť tunela
    Energy = Z ** 2

    # --- VIZUALIZÁCIA ---
    plt.figure(figsize=(10, 8))

    # Mapa energie
    plt.pcolormesh(X, Y, Energy, cmap='RdBu_r', shading='auto')

    # Vykreslenie Rámu
    circle = plt.Circle((0, 0), radius, color='black', fill=False, linewidth=3, linestyle='--')
    plt.gca().add_patch(circle)

    # Vysielače
    for ex, ey in emitters:
        plt.plot(ex, ey, 'ko', markersize=5)

    # Loď (v strede)
    ship_circle = plt.Circle((0, 0), 1.5, color='green', alpha=0.4, label='Loď (V tuneli)')
    plt.gca().add_patch(ship_circle)

    plt.text(0, 0, "SLIPSTREAM\n(Zero Inertia)", ha='center', va='center', fontweight='bold', color='white')
    plt.text(0, -radius - 1, "Kruhový Rám Brány", ha='center', fontweight='bold')

    plt.title("Simulácia Odletovej Haly: Kruhový Fázový Generátor", fontsize=14)
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.axis('equal')
    plt.colorbar(label="Intenzita vibrácií Higgsovej mriežky")

    plt.savefig("ring_gate_simulation.png")
    print("[OK] Simulácia kruhovej brány uložená.")
    plt.show()


simulate_ring_gate()