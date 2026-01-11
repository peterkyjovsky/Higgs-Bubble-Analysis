import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


def draw_gate_cooling_system():
    fig, ax = plt.subplots(figsize=(12, 12))
    ax.set_xlim(-12, 12)
    ax.set_ylim(-12, 12)
    ax.axis('off')

    # --- 1. VONKAJŠÍ PLÁŠŤ (Vákuová izolácia) ---
    # Masívny oceľový kruh, ktorý drží vákuum okolo chladných častí
    outer_shell = patches.Circle((0, 0), 10, color='#e0e0e0', ec='black', lw=3, label='Vonkajší Plášť (Vákuová komora)')
    ax.add_patch(outer_shell)
    inner_void = patches.Circle((0, 0), 8, color='white', ec='black', lw=2)  # Priestor pre loď
    ax.add_patch(inner_void)

    # --- 2. TEPELNÝ ŠTÍT (Thermal Shield - 80K) ---
    # Chladený tekutým dusíkom, odráža sálavé teplo
    shield = patches.Circle((0, 0), 9.5, color='none', ec='orange', lw=4, linestyle='--',
                            label='Tepelný Štít (LN2 - 80K)')
    ax.add_patch(shield)

    # --- 3. KRYOGÉNNE POTRUBIE (Helium Supply) ---
    # Červená = Hélium prívod (2K), Modrá = Hélium návrat
    # Kreslíme ako prstenec vo vnútri
    helium_ring = patches.Circle((0, 0), 9.0, color='none', ec='blue', lw=5, label='Hélium (LHe - 2K)')
    ax.add_patch(helium_ring)

    # --- 4. SUPRAVODIVÉ VYSIELAČE (SRF Modules) ---
    # Umiestnené po obvode, ponorené v héliu
    n_modules = 12
    radius = 9.0
    for i in range(n_modules):
        angle = np.deg2rad(i * (360 / n_modules))
        x = radius * np.cos(angle)
        y = radius * np.sin(angle)

        # Modul (SRF Cavity)
        cavity = patches.Circle((x, y), 0.6, color='gold', ec='black', zorder=10)
        ax.add_patch(cavity)

        # Vlnovod (Smerom do stredu)
        # Znázorňuje vyžarovanie energie
        ax.arrow(x, y, -1.5 * np.cos(angle), -1.5 * np.sin(angle),
                 head_width=0.3, head_length=0.4, fc='red', ec='red', zorder=5)

    # --- 5. INFRAŠTRUKTÚRA (Popis) ---

    # Kryo-Stanica (External Plant)
    draw_box = patches.Rectangle((-11, -11), 4, 3, color='gray', alpha=0.3)
    ax.add_patch(draw_box)
    ax.text(-9, -9.5, "KRYO-STANICA\n(Kompresory He)", ha='center', fontsize=9, fontweight='bold')

    # Potrubie k rámu
    ax.plot([-9, -7], [-8, -6], color='blue', lw=3)

    # Popisky
    ax.text(0, 10.5, "VONKAJŠÍ VÁKUOVÝ PLÁŠŤ (300K)", ha='center', fontweight='bold')
    ax.text(0, 8.2, "LETOROVÝ KORIDOR (Pre loď)", ha='center', color='green', fontweight='bold')

    # Detail vysielača
    ax.text(6, 9, "SRF VYSIELAČ\n(Ponorený v 2K Héliu)", color='darkgoldenrod', fontweight='bold')
    ax.plot([6, 5.5], [8.8, 4.5], color='black', lw=1)  # Ukazovadlo

    plt.title("Technická Architektúra: Chladená Odletová Brána (Stargate)", fontsize=14)
    plt.legend(loc='lower right')

    plt.savefig("gate_cooling_system.png")
    print("[OK] Schéma chladenia brány uložená.")
    plt.show()


draw_gate_cooling_system()