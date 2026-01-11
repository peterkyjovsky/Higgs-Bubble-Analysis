import math

def analyzuj_event(pt_namerane, pt_teoria):
    # W bozon hmotnost (standard)
    w_mass_standard = 80.385
    
    # Uhly (v CERNe su casto protilahle, delta_phi = pi)
    delta_phi = math.pi 
    
    # Vzorec pre Transverse Mass: sqrt(2 * pt1 * pt2 * (1 - cos(delta_phi)))
    # Ak su protilahle, (1 - cos(pi)) = 2. Vzorec sa zjednodusi na: 2 * sqrt(pt1 * pt2)
    m_t = math.sqrt(2 * pt_namerane * pt_teoria * (1 - math.cos(delta_phi)))
    
    print(f"--- ANAL›ZA EVENTU ---")
    print(f"NameranÈ pT: {pt_namerane} GeV")
    print(f"Vaöa teÛria: {pt_teoria} GeV")
    print(f"VypoËÌtan· hmotnosù systÈmu: {m_t:.4f} GeV")
    print(f"Rozdiel oproti W bozÛnu: {m_t - w_mass_standard:.4f} GeV")

# Hodnoty, ktorÈ hæad·me
analyzuj_event(31.4, 28.18829)