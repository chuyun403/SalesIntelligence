import pandas as pd
import numpy as np
import random
import os

# Setup Folder
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
raw_data_folder = os.path.join(BASE_DIR, "data", "raw_ab_test")
os.makedirs(raw_data_folder, exist_ok=True)

# Shared Variables
hospitals = ["台大", "長庚", "榮總", "馬偕", "慈濟", "秀傳", "成大", "奇美", "高醫", "中山"]

# --- Region 1: The "Mostly Clean but Weird Dates" Region (North) ---
def generate_north_data(n=200):
    data = []
    for _ in range(n):
        group = random.choice(['A', 'B'])
        # Group B (Variant) has a slightly higher chance of buying High-End
        bought_high_end = random.choices([1, 0], weights=[0.6 if group == 'B' else 0.4, 0.4 if group == 'B' else 0.6])[0]
        revenue = random.randint(15000, 80000) if bought_high_end else random.randint(1000, 10000)
        
        data.append({
            "Hospital Name": random.choice(hospitals) + " ", # Sneaky trailing space
            "Test_Group": group,
            "Date_Logged": f"2025/{random.randint(4,6):02d}/{random.randint(1,28):02d}", # YYYY/MM/DD
            "High_End_Purchased": bought_high_end,
            "Total_Rev": revenue
        })
    df = pd.DataFrame(data)
    # Inject a blank row
    df.loc[50] = np.nan
    df.to_excel(os.path.join(raw_data_folder, "North_Region_AB_Results.xlsx"), index=False)

# --- Region 2: The "Terrible Typo" Region (South) ---
def generate_south_data(n=180):
    data = []
    for _ in range(n):
        group = random.choice(['a', 'b ', 'B', ' A ']) # Messy group labels
        # Group B performs slightly better here too
        clean_group = group.strip().upper()
        bought = random.choices(["Yes", "No"], weights=[0.55 if clean_group == 'B' else 0.35, 0.45 if clean_group == 'B' else 0.65])[0]
        revenue = random.randint(15000, 75000) if bought == "Yes" else random.randint(1000, 9000)
        
        data.append({
            "hospital": random.choice(hospitals),
            "Group": group,
            "LogDate": f"{random.randint(1,28):02d}-{random.randint(4,6):02d}-2025", # DD-MM-YYYY
            "Bought_Premium?": bought, # Different column name and data type (Yes/No vs 1/0)
            "Rev(TWD)": revenue
        })
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(raw_data_folder, "south_ab_data_FINAL.xlsx"), index=False)

# --- Region 3: The "Incomplete Data" Region (Central) ---
def generate_central_data(n=150):
    data = []
    for _ in range(n):
        group = random.choice(['A', 'B'])
        bought = random.choices([True, False], weights=[0.6 if group == 'B' else 0.4, 0.4 if group == 'B' else 0.6])[0]
        
        # Sometimes they forget to log revenue
        revenue = random.randint(15000, 85000) if bought else random.randint(1000, 11000)
        if random.random() < 0.1: # 10% chance revenue is missing
            revenue = np.nan
            
        data.append({
            "Client": random.choice(hospitals), # Yet another column name for hospital
            "AB_Cohort": group,
            "Date": f"{random.randint(4,6):02d}/{random.randint(1,28):02d}/2025", # MM/DD/YYYY
            "Purchased": bought, # Boolean type
            "Revenue": revenue
        })
    df = pd.DataFrame(data)
    df.to_excel(os.path.join(raw_data_folder, "Central-Test-Results.xlsx"), index=False)

# Execute
print("🧨 Generating chaotic raw data files...")
generate_north_data()
generate_south_data()
generate_central_data()
print(f"✅ Three horribly formatted regional Excel files generated in: {raw_data_folder}")