"""Recreate the complete SE4095 submission from a clean workspace.

Run: python run_all_parts.py
The scripts write only to their own part_*_output folders.
"""
import random
import numpy as np

MASTER_SEED = 4095

def main():
    random.seed(MASTER_SEED)
    np.random.seed(MASTER_SEED)
    import part_a_analysis, part_b_analysis, part_c_analysis, part_d_analysis, part_e_analysis
    part_a_analysis.main()       # loading, cleaning, graph profile, basic figures
    part_b_analysis.main()       # selected centralities and rankings
    part_c_analysis.main()       # targeted and random removal experiment
    part_d_analysis.main()       # five-seed Louvain detection and visualization
    part_e_analysis.main()       # post-detection pairwise evaluation

if __name__ == '__main__':
    main()
