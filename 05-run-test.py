import pandas as pd
from scipy import stats
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(BASE_DIR, "data", "ab_test_5000.csv")

def run_significance_test():
    print("🔬 Loading 5,000-row dataset...")
    df = pd.read_csv(data_path)

    group_a = df[df['ab_group'] == 'A']['revenue_twd']
    group_b = df[df['ab_group'] == 'B']['revenue_twd']
    
    avg_a = group_a.mean()
    avg_b = group_b.mean()
    revenue_lift = avg_b - avg_a
    percentage_lift = (revenue_lift / avg_a) * 100

    print("\n" + "="*50)
    print("📊 MEDSHIFT SCALED A/B TEST RESULTS")
    print("="*50)
    print(f"Group A (Control) Average:   {avg_a:,.0f} TWD")
    print(f"Group B (Variant) Average:   {avg_b:,.0f} TWD")
    print("-" * 50)
    print(f"Observed Lift:               +{revenue_lift:,.0f} TWD per clinic")
    print(f"Percentage Growth:           +{percentage_lift:.1f}%")
    print("="*50)

    t_stat, p_value = stats.ttest_ind(group_a, group_b, equal_var=False)

    print("\n🧠 STATISTICAL SIGNIFICANCE CHECK")
    print(f"P-Value: {p_value:.4f}")
    
    if p_value < 0.05:
        print("\n✅ THE VERDICT: STATISTICALLY SIGNIFICANT")
    else:
        print("\n❌ THE VERDICT: INCONCLUSIVE (NOISE)")
        print("Although Group B's average is higher, the variance in spending is too massive.")
        print(f"There is a {(p_value * 100):.1f}% chance this lift was just random luck.")
        print("Recommendation: Do NOT pivot the entire sales force yet.")

if __name__ == "__main__":
    run_significance_test()