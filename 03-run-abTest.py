import pandas as pd
from scipy import stats
import os

# 1. Setup paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
clean_data_path = os.path.join(BASE_DIR, "data", "clean_ab_test_data.csv")

def run_significance_test():
    print("🔬 Loading clean dataset...")
    try:
        df = pd.read_csv(clean_data_path)
    except FileNotFoundError:
        print("❌ Cannot find clean data. Did you run the ETL script first?")
        return

    # 2. Separate the groups for comparison
    group_a = df[df['ab_group'] == 'A']['revenue_twd']
    group_b = df[df['ab_group'] == 'B']['revenue_twd']
    
    # 3. Calculate basic business metrics
    avg_a = group_a.mean()
    avg_b = group_b.mean()
    revenue_lift = avg_b - avg_a
    percentage_lift = (revenue_lift / avg_a) * 100

    print("\n" + "="*50)
    print("📊 MEDSHIFT A/B TEST RESULTS")
    print("="*50)
    print(f"Group A (Control) Average Revenue:  {avg_a:,.0f} TWD")
    print(f"Group B (Variant) Average Revenue:  {avg_b:,.0f} TWD")
    print("-" * 50)
    print(f"Observed Difference (Lift):         +{revenue_lift:,.0f} TWD per clinic")
    print(f"Percentage Growth:                  +{percentage_lift:.1f}%")
    print("="*50)

    # 4. The Moment of Truth: Run the SciPy T-Test
    # We use equal_var=False (Welch's t-test) because variance between hospitals is high
    t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)

    print("\n🧠 STATISTICAL SIGNIFICANCE CHECK")
    print(f"P-Value: {p_value:.4f}")
    
    # 5. Interpret the result for stakeholders
    if p_value < 0.05:
        print("\n✅ THE VERDICT: STATISTICALLY SIGNIFICANT")
        print("The new High-End marketing case study genuinely works.")
        print(f"There is less than a {(p_value * 100):.1f}% chance these results were a fluke.")
        print("Recommendation: Roll out the 'Group B' strategy company-wide immediately.")
    else:
        print("\n❌ THE VERDICT: INCONCLUSIVE (NOISE)")
        print("Although Group B performed differently, the math says it could just be random luck.")
        print(f"There is a {(p_value * 100):.1f}% chance these results occurred by chance.")
        print("Recommendation: Do not pivot strategy yet. Run the test longer or redesign the material.")

if __name__ == "__main__":
    run_significance_test()