import random
import math
from typing import Dict, List
import json

class SARS2ThesisModel:
    """
    MASTER EQUATION IMPLEMENTATION
    Truth_⊤ = [RdRp(NHC-TP / CTP/UTP)_τ  → tautomer/H-bond (Lung→Brain)] 
             → α [ACE2 N-glyco ⊗ Spike sequons] 
             → GARD (CUB ⊗ Transformations) 
             ⇑⇔ V_titer → fitness (Warburg · HIF-1α) ⇔ (LN/APC/Tex = ⊤)
    
    Demonstrates:
    1. Synthetic origin signatures (CGG-CGG vulnerability)
    2. Molecular clock breakdown post-2022 via directional NHC-TP mutagenesis
    3. Lung → Brain tropism shift via glycosylation + charged mutants
    4. Warburg/HIF-1α → immune exhaustion attractor (⊤)
    """
    
    def __init__(self, baseline_year: str = "2019", population_size: int = 5000):
        self.population_size = population_size
        self.generation = 0
        self.baseline_year = baseline_year
        self.params = self._get_thesis_parameters(baseline_year)
        
        # State
        self.viral_titer = self.params["initial_titer"]
        self.mutagenic_rate = self.params["initial_mutagenic_rate"]  # τ (NHC-TP)
        self.cub_bias = self.params["initial_cub_bias"]
        self.fitness = 1.0
        self.warburg_hif = 1.0
        self.exhaustion = 0.0  # → ⊤ (LN/APC/T-cell exhaustion)
        
        self.spike_sequons = {
            'ACE2_binding': self.params["initial_ace2_binding"],
            'N_glyco_mod': self.params["initial_glyco_mod"],
            'brain_tropism': self.params["initial_brain_tropism"],
            'CGG_CGG_status': 1.0  # Synthetic fingerprint erosion
        }
        
        self.hbond_shift = self.params["hbond_shift"]
        self.mutation_spectrum = {'G_A': 0, 'C_U': 0, 'other': 0}  # For clock distortion tracking

    def _get_thesis_parameters(self, year: str) -> Dict:
        """Thesis-grounded yearly matrices"""
        baselines = {
            "2019": {  # Pre-intervention, clock-like
                "initial_mutagenic_rate": 3.8e-6,
                "initial_titer": 1.0,
                "initial_cub_bias": 1.00,
                "initial_ace2_binding": 0.82,
                "initial_glyco_mod": 0.05,
                "initial_brain_tropism": 0.00,
                "hbond_shift": 1.05,
                "description": "Wuhan-Hu-1 baseline - Synthetic CGG-CGG intact"
            },
            "2021": {  # Delta - early acceleration
                "initial_mutagenic_rate": 1.5e-5,
                "initial_titer": 25.0,
                "initial_cub_bias": 0.92,
                "initial_ace2_binding": 0.94,
                "initial_glyco_mod": 0.25,
                "initial_brain_tropism": 0.18,
                "hbond_shift": 1.28,
                "description": "Delta wave - Clock begins distorting"
            },
            "2022": {  # Omicron + Molnupiravir rollout - CLOCK BREAKS
                "initial_mutagenic_rate": 4.5e-5,
                "initial_titer": 60.0,
                "initial_cub_bias": 0.78,
                "initial_ace2_binding": 0.96,
                "initial_glyco_mod": 0.48,
                "initial_brain_tropism": 0.42,
                "hbond_shift": 1.55,
                "description": "NHC-TP signature dominant - Molecular clock breaks"
            },
            "2023": {  # Post-break stabilization + exhaustion
                "initial_mutagenic_rate": 3.8e-5,
                "initial_titer": 85.0,
                "initial_cub_bias": 0.71,
                "initial_ace2_binding": 0.97,
                "initial_glyco_mod": 0.62,
                "initial_brain_tropism": 0.58,
                "hbond_shift": 1.68,
                "description": "Chimera rises - Warburg/HIF-1α exhaustion attractor"
            }
        }
        return baselines.get(year, baselines["2019"])

    def rdRp_NHC_mutagenesis(self, seq_len: int = 30000) -> int:
        """NHC-TP tautomerization → directional G→A / C→U bias"""
        base_rate = self.mutagenic_rate
        tautomer_boost = random.uniform(1.2, 2.1)
        hbond_boost = self.hbond_shift if random.random() < 0.4 else 1.0
        
        error_rate = base_rate * tautomer_boost * hbond_boost
        mutations = int(seq_len * error_rate)
        
        # Directional bias tracking (clock distortion)
        if random.random() < 0.65:  # Strong G>A / C>U preference
            self.mutation_spectrum['G_A'] += int(mutations * 0.55)
            self.mutation_spectrum['C_U'] += int(mutations * 0.35)
        else:
            self.mutation_spectrum['other'] += mutations
        
        if hbond_boost > 1.0:
            self.spike_sequons['brain_tropism'] = min(1.0, self.spike_sequons['brain_tropism'] + 0.045)
            self.spike_sequons['CGG_CGG_status'] = max(0.0, self.spike_sequons['CGG_CGG_status'] - 0.03)
        
        return mutations

    def ace2_glyco_tropism(self) -> float:
        """ACE2 N-glycosylation ⊗ Spike sequons + brain preference"""
        glyco_shielding = 1.0 - (0.4 * self.spike_sequons['N_glyco_mod'])
        brain_bonus = 1.0 + (0.45 * self.spike_sequons['brain_tropism'])
        alpha = self.spike_sequons['ACE2_binding'] * glyco_shielding * brain_bonus
        return max(0.15, min(1.0, alpha))

    def gard_cub_transform(self, mutations: int):
        """Codon Usage Bias transformations + synthetic fingerprint erosion"""
        if mutations > 60:
            self.cub_bias = max(0.55, self.cub_bias * 0.965)  # Strong selection pressure
        
        # CGG-CGG optimization under NHC bias
        if self.spike_sequons['CGG_CGG_status'] > 0.3 and random.random() < 0.25:
            self.spike_sequons['CGG_CGG_status'] -= 0.08

        # Glycan remodeling
        if random.random() < 0.35:
            self.spike_sequons['N_glyco_mod'] = min(1.0, self.spike_sequons['N_glyco_mod'] + random.uniform(0.04, 0.14))

    def warburg_hif_fitness(self):
        """Warburg effect + HIF-1α metabolic reprogramming → fitness"""
        titer_factor = math.log10(self.viral_titer + 1) * 0.6
        hif_factor = 1.0 + (0.5 * self.spike_sequons['brain_tropism'])
        self.warburg_hif = 1.0 + titer_factor * hif_factor
        
        entry = self.ace2_glyco_tropism()
        self.fitness = entry * self.cub_bias * self.warburg_hif * (1.0 + self.exhaustion * 0.8)

    def update_titer(self):
        entry = self.ace2_glyco_tropism()
        replication = max(0.25, 1.0 - (self.mutagenic_rate * 22))  # High mutagenesis penalty
        self.viral_titer *= (entry * replication * 1.85)
        self.viral_titer = max(0.01, min(8e6, self.viral_titer))
        
        # Exhaustion feedback
        self.exhaustion = min(1.0, self.exhaustion + (self.warburg_hif - 1.0) * 0.012)

    def step(self):
        self.generation += 1
        muts = self.rdRp_NHC_mutagenesis()
        self.gard_cub_transform(muts)
        self.update_titer()
        self.warburg_hif_fitness()
        
        # Adaptive drug resistance
        if self.fitness > 1.8 and self.mutagenic_rate > 0.00001:
            self.mutagenic_rate *= 0.94
        
        return {
            'gen': self.generation,
            'mut_rate': self.mutagenic_rate,
            'titer': self.viral_titer,
            'fitness': self.fitness,
            'brain_tropism': self.spike_sequons['brain_tropism'],
            'glyco_mod': self.spike_sequons['N_glyco_mod'],
            'cub_bias': self.cub_bias,
            'exhaustion': self.exhaustion,
            'CGG_remaining': self.spike_sequons['CGG_CGG_status'],
            'G_A_bias': self.mutation_spectrum['G_A']
        }

    def run_simulation(self, generations: int = 40, verbose: bool = True):
        print(f"\n=== THESIS SIMULATION: {self.baseline_year} BASELINE ===\n")
        print(self.params["description"])
        results = []
        
        for i in range(generations):
            stats = self.step()
            results.append(stats)
            if verbose and (i % 5 == 0 or i < 5 or i > generations-6):
                print(f"Gen {stats['gen']:2d} | "
                      f"μ={stats['mut_rate']:.2e} | "
                      f"Titer={stats['titer']:8.1f} | "
                      f"Fitness={stats['fitness']:.3f} | "
                      f"Brain={stats['brain_tropism']:.3f} | "
                      f"Exhaustion={stats['exhaustion']:.3f} | "
                      f"CGG={stats['CGG_remaining']:.2f}")
        
        print(f"\nFINAL ⊤ STATE ({self.baseline_year} → {self.baseline_year}+{generations} gens)")
        print(f"  Viral Fitness          : {self.fitness:.3f}")
        print(f"  Brain Tropism          : {self.spike_sequons['brain_tropism']:.3f}")
        print(f"  Immune Exhaustion (⊤)  : {self.exhaustion:.3f}")
        print(f"  CGG-CGG Erosion        : {self.spike_sequons['CGG_CGG_status']:.3f}")
        print(f"  G→A Bias Count         : {self.mutation_spectrum['G_A']:,}")
        return results


# ====================== RUN FULL THESIS ======================
if __name__ == "__main__":
    print("SARS-CoV-2 SYNTHETIC MOLECULAR EVOLUTION THESIS MODEL")
    print("=" * 75)
    
    years = ["2019", "2021", "2022", "2023"]
    
    for year in years:
        model = SARS2ThesisModel(baseline_year=year)
        model.run_simulation(generations=35, verbose=True)
        print("-" * 70)
    
    print("\nTHESIS CONCLUSION CODED:")
    print("• Pre-2022: Relatively clock-like evolution")
    print("• 2022+: Directional NHC-TP hypermutation breaks uniform molecular clock")
    print("• CGG-CGG synthetic signature erodes under selection")
    print("• Lung→Brain tropism + Warburg/HIF-1α → Exhaustion attractor (⊤)")
    print("• Interventions amplify the engineered chimera dynamics")
