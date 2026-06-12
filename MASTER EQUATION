import random
import math
from typing import Dict, List, Tuple, Optional

# Pure Python simulation of the described pathway
# ⊤ = [RdRp (NHC-TP ↔ CTP/UTP) τ → tautomer/H-bond (Lung→Brain)] 
# → α [ACE2 N-glyco ⊗ Spike sequons] 
# → GARD (CUB ⊗ Transformations) ⇑⇔ V_titer → fitness (Warburg · HIF-1α) 
# ⇔ (LN/APC/Tex = ⊤)

class VirusModel:
    def __init__(self, 
                 initial_mutagenic_rate: float = 0.01,
                 population_size: int = 1000,
                 lung_to_brain_hbond_factor: float = 1.2):
        self.population_size = population_size
        self.mutagenic_rate = initial_mutagenic_rate  # NHC-TP induced tautomer mutagenesis
        self.hbond_shift = lung_to_brain_hbond_factor  # Lung H-bond → Brain H-bond
        self.viral_titer = 1.0
        self.fitness = 1.0
        self.generation = 0
        
        # Spike sequons / glycosylation states (simplified)
        self.spike_sequons = {
            'ACE2_binding': 0.85,      # Base affinity
            'N_glyco_mod': 0.0,        # Glycosylation modification level
            'brain_tropism': 0.0
        }
        
        # Codon Usage Bias (CUB) proxy
        self.cub_bias = 1.0
        
        # Warburg/HIF-1α metabolic fitness multiplier
        self.warburg_hif = 1.0
    
    def rdRp_mutagenesis(self, sequence_length: int = 30000) -> int:
        """Simulate RdRp with NHC-TP tautomer incorporation leading to mutations."""
        # Tautomer/H-bond driven error rate
        base_error = self.mutagenic_rate
        tautomer_boost = random.uniform(1.0, 1.5)  # Tautomer effect (A<->G like pairing)
        hbond_boost = self.hbond_shift if random.random() < 0.3 else 1.0  # Lung to brain shift
        
        error_rate = base_error * tautomer_boost * hbond_boost
        mutations = int(sequence_length * error_rate)
        
        # Update brain tropism if H-bond shift
        if hbond_boost > 1.0:
            self.spike_sequons['brain_tropism'] = min(1.0, self.spike_sequons['brain_tropism'] + 0.05)
        
        return mutations
    
    def ace2_spike_interaction(self) -> float:
        """ACE2 N-glycosylation ⊗ Spike sequons binding probability."""
        glyco_effect = 1.0 - (0.4 * self.spike_sequons['N_glyco_mod'])  # Glycans can shield or enhance
        brain_bonus = 1.0 + (0.3 * self.spike_sequons['brain_tropism'])
        
        alpha = self.spike_sequons['ACE2_binding'] * glyco_effect * brain_bonus
        return max(0.1, min(1.0, alpha))
    
    def apply_gard_cub_transform(self, mutations: int):
        """GARD (recombination detection proxy) + Codon Usage Bias transformations."""
        # Simple CUB adaptation under selection
        if mutations > 50:  # High mutagenesis -> selection pressure
            self.cub_bias = max(0.6, self.cub_bias * 0.98)  # Bias shift
        
        # Transformations table proxy: random adaptive changes
        transform_prob = min(0.3, mutations / 500.0)
        if random.random() < transform_prob:
            self.spike_sequons['N_glyco_mod'] = min(1.0, self.spike_sequons['N_glyco_mod'] + random.uniform(0.05, 0.15))
            self.spike_sequons['ACE2_binding'] = min(1.0, self.spike_sequons['ACE2_binding'] + random.uniform(-0.1, 0.2))
    
    def update_fitness_warburg(self):
        """Fitness via Warburg effect + HIF-1α metabolic reprogramming."""
        # Higher titer + metabolic shift -> fitness
        titer_factor = math.log10(self.viral_titer + 1) * 0.5
        hif_factor = 1.0 + (0.4 * self.spike_sequons['brain_tropism'])  # Hypoxia-like in brain
        
        self.warburg_hif = 1.0 + titer_factor * hif_factor
        self.fitness = self.ace2_spike_interaction() * self.cub_bias * self.warburg_hif
    
    def update_titer(self):
        """Viral titer update based on current fitness and entry."""
        entry_prob = self.ace2_spike_interaction()
        replication_success = 1.0 - (self.mutagenic_rate * 20)  # Too much mutagenesis hurts
        
        self.viral_titer *= (entry_prob * replication_success * 1.8)  # Exponential growth factor
        self.viral_titer = max(0.01, min(1e6, self.viral_titer))  # Bounds
    
    def step(self):
        """One generation/step of the model."""
        self.generation += 1
        
        # 1. RdRp mutagenesis phase
        muts = self.rdRp_mutagenesis()
        
        # 2. GARD/CUB/Transformations
        self.apply_gard_cub_transform(muts)
        
        # 3. Update titer and fitness
        self.update_titer()
        self.update_fitness_warburg()
        
        # Adaptive feedback: high fitness reduces effective drug pressure
        if self.fitness > 1.5:
            self.mutagenic_rate *= 0.95
        
        return {
            'generation': self.generation,
            'mutations': muts,
            'titer': self.viral_titer,
            'fitness': self.fitness,
            'ace2_affinity': self.ace2_spike_interaction(),
            'brain_tropism': self.spike_sequons['brain_tropism'],
            'warburg_hif': self.warburg_hif
        }


# Example usage / simulation run
if __name__ == "__main__":
    model = VirusModel(initial_mutagenic_rate=0.015, population_size=5000)
    
    print("Starting simulation: RdRp(NHC-TP) → ACE2/Spike → GARD/CUB → Fitness (Warburg·HIF-1α)")
    print("=" * 80)
    
    for i in range(20):
        stats = model.step()
        if i % 5 == 0 or i < 5:
            print(f"Gen {stats['generation']:2d} | "
                  f"Mut: {stats['mutations']:3d} | "
                  f"Titer: {stats['titer']:8.1f} | "
                  f"Fitness: {stats['fitness']:.3f} | "
                  f"ACE2: {stats['ace2_affinity']:.3f} | "
                  f"Brain: {stats['brain_tropism']:.2f}")
    
    print("\nFinal state (LN/APC/Tex equilibrium proxy):")
    print(f"  Viral fitness (⊤): {model.fitness:.3f}")
    print(f"  Titer: {model.viral_titer:.1f}")
    print(f"  Brain tropism: {model.spike_sequons['brain_tropism']:.2f}")
