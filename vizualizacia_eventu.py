import pandas as pd
import numpy as np
import plotly.graph_objects as go

# Názov súboru
file_name = "atlas-higgs-challenge-2014-v2.csv.gz"
TARGET_EVENT_ID = 637112  # Náš zlatý kandidát

print(f"Hľadám dáta pre Event {TARGET_EVENT_ID}...")

try:
    df = pd.read_csv(file_name, compression='gzip')
    event_data = df[df['EventId'] == TARGET_EVENT_ID]
    
    if event_data.empty:
        print("Chyba: Event sa nenašiel.")
    else:
        row = event_data.iloc[0]
        print("Dáta načítané. Počítam 3D geometriu...")
        
        # --- 1. Získanie sférických súradní ---
        pt_lep = row['PRI_lep_pt']
        phi_lep = row['PRI_lep_phi']
        eta_lep = row['PRI_lep_eta']
        
        met = row['PRI_met']
        phi_met = row['PRI_met_phi']
        
        # --- 2. Prevod na Kartézske súradnice (X, Y, Z) ---
        # Leptón (Váš signál 31.4 GeV)
        lep_x = pt_lep * np.cos(phi_lep)
        lep_y = pt_lep * np.sin(phi_lep)
        lep_z = pt_lep * np.sinh(eta_lep) # Z-os sa počíta z pseudorapidity
        
        # MET (Vaša bublina 28.188 GeV)
        # MET je len v priečnej rovine (nemá Z zložku, resp. ju nepoznáme), kreslíme v rovine XY
        met_x = met * np.cos(phi_met)
        met_y = met * np.sin(phi_met)
        met_z = 0 
        
        # --- 3. Výpočet uhlov ---
        # Rozdiel uhlov v rovine (Delta Phi)
        delta_phi = abs(phi_lep - phi_met)
        if delta_phi > np.pi:
            delta_phi = 2*np.pi - delta_phi
            
        angle_deg = delta_phi * (180 / np.pi)
        
        print(f"\n--- GEOMETRIA DIGITÁLNEHO POĽA ---")
        print(f"Energia Leptónu: {pt_lep:.3f} GeV")
        print(f"Energia Bubliny: {met:.3f} GeV")
        print(f"Uhol medzi nimi (Delta Phi): {angle_deg:.4f} stupňov")
        
        target_angle = 28.188
        print(f"Odchýlka od 28.18°: {abs(angle_deg - target_angle):.4f}°")
        print(f"Odchýlka od (180° - 28.18°): {abs(angle_deg - (180 - target_angle)):.4f}°")

        # --- 4. 3D Vizualizácia ---
        fig = go.Figure()
        
        # Bod zrážky
        fig.add_trace(go.Scatter3d(x=[0], y=[0], z=[0], mode='markers', marker=dict(size=5, color='yellow'), name='Zrážka'))
        
        # Vektor Leptónu (Červená)
        fig.add_trace(go.Scatter3d(
            x=[0, lep_x], y=[0, lep_y], z=[0, lep_z],
            mode='lines+markers', line=dict(color='red', width=5), name=f'Leptón ({pt_lep:.2f} GeV)'
        ))
        
        # Vektor MET / Bubliny (Modrá)
        fig.add_trace(go.Scatter3d(
            x=[0, met_x], y=[0, met_y], z=[0, met_z],
            mode='lines+markers', line=dict(color='cyan', width=5, dash='dash'), name=f'Vákuum ({met:.2f} GeV)'
        ))
        
        # Pridanie mriežky detektora (pre orientáciu)
        r = 40
        theta = np.linspace(0, 2*np.pi, 100)
        fig.add_trace(go.Scatter3d(x=r*np.cos(theta), y=r*np.sin(theta), z=np.zeros_like(theta), mode='lines', line=dict(color='gray'), name='Detektor ring'))

        fig.update_layout(
            title=f"Rekonštrukcia Eventu {TARGET_EVENT_ID}<br>Uhol: {angle_deg:.2f}°",
            scene=dict(
                xaxis_title='X [GeV]',
                yaxis_title='Y [GeV]',
                zaxis_title='Z [GeV] (Smer lúča)',
                bgcolor='black'
            ),
            template="plotly_dark"
        )
        
        fig.show()

except Exception as e:
    print(f"Chyba: {e}")