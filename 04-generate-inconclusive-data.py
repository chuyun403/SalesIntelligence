import pandas as pd
import numpy as np
import random
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ensure data folder exists
os.makedirs(os.path.join(BASE_DIR, "data"), exist_ok=True)
data_path = os.path.join(BASE_DIR, "data", "ab_test_5000.csv")

def generate_large_dataset(n=5000):
    print(f"🧨 Generating {n} rows of highly-variant clinical data...")
    
    # We use numpy for faster, more realistic distributions
    np.random.seed(42) # Keeps the random generation consistent
    
    # Half the clinics get A, Half get B
    groups = ['A'] * (n // 2) + ['B'] * (n // 2)
    random.shuffle(groups)
    
    data = []
    for i, group in enumerate(groups):
        # The Secret Sauce: Massive Variance
        # Most clinics buy low-end (Mean ~8,000)
        # But a few massive hospitals skew the data with huge purchases (150,000+)
        
        # Group B is technically slightly better...
        if group == 'B':
            base_revenue = np.random.lognormal(mean=9.1, sigma=1.2) # Skewed distribution
        else:
            base_revenue = np.random.lognormal(mean=9.05, sigma=1.2)
            
        # Add some random noise to simulate real-world chaos
        noise = random.uniform(0.8, 1.2)
        final_revenue = int(base_revenue * noise)
        
        # Cap outliers to keep it somewhat realistic for a medical supplier
        if final_revenue > 250000:
            final_revenue = random.randint(180000, 220000)
            
        data.append({
            "clinic_id": f"CLINIC_{i:04d}",
            "ab_group": group,
            "revenue_twd": final_revenue
        })

    df = pd.DataFrame(data)
    df.to_csv(data_path, index=False)
    print(f"✅ Generated and saved to: {data_path}")

if __name__ == "__main__":
    generate_large_dataset()