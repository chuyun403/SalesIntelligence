import pandas as pd
import glob
import os

# 1. Setup Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raw_data_folder = os.path.join(BASE_DIR, "data", "raw_ab_test")
clean_data_path = os.path.join(BASE_DIR, "data", "clean_ab_test_data.csv")

def clean_regional_data():
    # Find all Excel files in the raw data folder
    all_files = glob.glob(os.path.join(raw_data_folder, "*.xlsx"))
    
    if not all_files:
        print("❌ No raw data found. Did you run the messy data generator?")
        return

    clean_dataframes = []
    print("🧹 Starting ETL Pipeline...\n")

    for file in all_files:
        region_name = os.path.basename(file)
        print(f"Processing: {region_name}")
        
        # Read the messy Excel file
        df = pd.read_excel(file)
        
        # A. Drop completely blank "ghost" rows
        df = df.dropna(how='all')
        
        # B. Standardize Headers dynamically (lowercase, strip spaces)
        df.columns = [str(c).strip().lower() for c in df.columns]
        
        # Create a mapping dictionary to catch all the regional variations
        column_mapping = {
            "hospital name": "hospital",
            "client": "hospital",
            "test_group": "ab_group",
            "group": "ab_group",
            "ab_cohort": "ab_group",
            "date_logged": "date",
            "logdate": "date",
            "high_end_purchased": "purchased_premium",
            "bought_premium?": "purchased_premium",
            "purchased": "purchased_premium",
            "total_rev": "revenue_twd",
            "rev(twd)": "revenue_twd",
            "revenue": "revenue_twd"
        }
        df = df.rename(columns=column_mapping)
        
        # C. Clean the actual data values
        if 'hospital' in df.columns:
            df['hospital'] = df['hospital'].astype(str).str.strip()
            
        if 'ab_group' in df.columns:
            # Fixes 'a', 'b ', ' A ' -> 'A', 'B'
            df['ab_group'] = df['ab_group'].astype(str).str.strip().str.upper()
            
        if 'purchased_premium' in df.columns:
            # Standardize Yes/No, True/False, 1/0 into strict 1 and 0
            df['purchased_premium'] = df['purchased_premium'].replace({'Yes': 1, 'No': 0, True: 1, False: 0})
            
        if 'revenue_twd' in df.columns:
            # Handle missing revenue (NaN) by filling with 0, then convert to integer
            df['revenue_twd'] = df['revenue_twd'].fillna(0).astype(int)
            
        # D. Standardize Dates using Pandas magic datetime parser
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], format='mixed').dt.strftime('%Y-%m-%d')
            
        clean_dataframes.append(df)

    # 3. Combine everything into one master dataset
    master_df = pd.concat(clean_dataframes, ignore_index=True)
    
    # Save to a clean CSV
    master_df.to_csv(clean_data_path, index=False)
    print("\n" + "="*50)
    print(f"✅ ETL Complete! {len(master_df)} clean rows saved to:")
    print(f"   {clean_data_path}")
    print("="*50)

if __name__ == "__main__":
    clean_regional_data()