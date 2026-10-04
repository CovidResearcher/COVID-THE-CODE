import math
import matplotlib.pyplot as plt  # optional for plotting (remove if not needed)

def sars_unified_pure_python(days=30, dt=0.1, alpha=0.6, tau=0.4, beta=1.2, gamma=0.8, delta=0.7, epsilon=0.7):
    """
    Unified SARS-CoV-2 Pathobiology Model
    From your thesis: RdRp-NHCTP → Tautomerization → ACE2 Glycosylation → Codon Evolution → Titer → Warburg/HIF-1α → Exhaustion (⊤)
    """
    
    # Initial conditions
    V = 5.0          # Viral titer
    Glyco_eff = 0.70 # ACE2/Spike glycosylation efficiency
    Mut_load = 0.10  # Mutation load from NHCTP tautomerization
    HIF = 0.20       # HIF-1α level
    Exhaust = 0.10   # Immune exhaustion (LN/APC/T-cell)
    Titer_eff = 0.60 # Effective infectious titer (codon fitness)

    history = {
        'time': [], 'V': [], 'Glyco_eff': [], 'Mut_load': [],
        'HIF': [], 'Exhaust': [], 'Titer_eff': []
    }

    n_steps = int(days / dt)
    
    for step in range(n_steps):
        t = step * dt
        
        # Record state
        history['time'].append(t)
        history['V'].append(V)
        history['Glyco_eff'].append(Glyco_eff)
        history['Mut_load'].append(Mut_load)
        history['HIF'].append(HIF)
        history['Exhaust'].append(Exhaust)
        history['Titer_eff'].append(Titer_eff)
        
        # Core ODEs (Euler integration)
        dV         = beta * Glyco_eff * Titer_eff * (1 - V/100) - gamma * Mut_load * V
        dGlyco     = alpha * (0.8 - Glyco_eff) - 0.05 * HIF
        dMut       = tau * V - delta * Mut_load
        dHIF       = 0.1 * V + 0.2 * Exhaust - 0.15 * HIF
        dExhaust   = epsilon * HIF * (1 - Exhaust) * V - 0.08 * Exhaust
        dTiter_eff = 0.05 * Glyco_eff * (1 - Mut_load) - 0.03 * Titer_eff
        
        # Update states
        V         += dV * dt
        Glyco_eff += dGlyco * dt
        Mut_load  += dMut * dt
        HIF       += dHIF * dt
        Exhaust   += dExhaust * dt
        Titer_eff += dTiter_eff * dt
        
        # Bounds
        V = max(0.0, min(V, 100.0))
        Glyco_eff = max(0.0, min(Glyco_eff, 1.0))
        Mut_load = max(0.0, Mut_load)
        HIF = max(0.0, HIF)
        Exhaust = max(0.0, min(Exhaust, 1.0))
        Titer_eff = max(0.0, min(Titer_eff, 1.0))
    
    # Final state summary
    print("=== FINAL STATE (t = {} days) ===".format(days))
    print(f"Viral Titer (V)       : {V:.3f}")
    print(f"Glyco Efficiency     : {Glyco_eff:.3f}")
    print(f"Mutation Load        : {Mut_load:.3f}")
    print(f"HIF-1α               : {HIF:.3f}")
    print(f"Immune Exhaustion    : {Exhaust:.3f}  ← Fixed Point ⊤")
    print(f"Effective Titer      : {Titer_eff:.3f}")
    
    return history


# ===================== RUN BASELINE =====================
if __name__ == "__main__":
    history = sars_unified_pure_python(days=30, dt=0.05)
    
    # Simple plotting (matplotlib is optional)
    try:
        plt.figure(figsize=(12, 8))
        plt.suptitle("SARS-CoV-2 Unified Framework Simulation\n(RdRp-NHCTP → Glycosylation → Codon Bias → Warburg/Exhaustion ⊤)", fontsize=14)
        
        vars_list = ['V', 'Glyco_eff', 'Mut_load', 'HIF', 'Exhaust', 'Titer_eff']
        titles = ['Viral Titer (V)', 'Glyco Efficiency', 'Mutation Load', 
                 'HIF-1α', 'Exhaustion (⊤)', 'Effective Titer']
        
        for i, var in enumerate(vars_list, 1):
            plt.subplot(2, 3, i)
            plt.plot(history['time'], history[var])
            plt.title(titles[i-1])
            plt.xlabel('Time (days)')
            plt.grid(True)
        
        plt.tight_layout()
        plt.show()
    except:
        print("Plotting skipped (matplotlib not available)")
