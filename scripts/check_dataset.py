import pandas as pd
import os
import sys

def analyze_dataset():
    data_dir = "/home/neeraj7388011/ids_analysis/data"
    
    # List available CSV files
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in data directory!")
        print("Please copy your CIC IDS 2018 CSV file to the data/ folder")
        return None
    
    print("📁 Available CSV files:")
    for i, file in enumerate(csv_files):
        file_path = os.path.join(data_dir, file)
        file_size = os.path.getsize(file_path) / (1024**3)  # Size in GB
        print(f"   {i+1}. {file} ({file_size:.2f} GB)")
    
    # Use first CSV file
    csv_file = csv_files[0]
    csv_path = os.path.join(data_dir, csv_file)
    
    print(f"\n🔍 Analyzing: {csv_file}")
    
    try:
        # Read just the first few rows to understand structure
        print("Reading first 10 rows...")
        df_sample = pd.read_csv(csv_path, nrows=10)
        
        print(f"📊 Dataset shape (sample): {df_sample.shape}")
        print(f"📝 Number of columns: {len(df_sample.columns)}")
        
        print("\n📋 First 3 rows:")
        print(df_sample.head(3))
        
        print("\n🏷️ Column names:")
        for i, col in enumerate(df_sample.columns):
            print(f"   {i+1:2d}. {col}")
            
        # Look for label/attack columns
        label_candidates = []
        for col in df_sample.columns:
            col_lower = col.lower()
            if any(keyword in col_lower for keyword in ['label', 'attack', 'type', 'class', 'category']):
                label_candidates.append(col)
        
        if label_candidates:
            print(f"\n🎯 Potential label columns found:")
            for col in label_candidates:
                try:
                    # Read more rows to see more unique values
                    df_col_sample = pd.read_csv(csv_path, usecols=[col], nrows=1000)
                    unique_vals = df_col_sample[col].unique()
                    print(f"   📌 '{col}': {len(unique_vals)} unique values")
                    print(f"      Sample values: {list(unique_vals[:5])}")
                except:
                    print(f"   📌 '{col}': Could not read values")
        else:
            print("\n❓ No obvious label columns found.")
            print("   You'll need to identify the target column manually from the list above.")
            
        return csv_path, df_sample.columns.tolist()
        
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        print("   The file might be too large, corrupted, or in a different format.")
        return None, None

if __name__ == "__main__":
    csv_path, columns = analyze_dataset()
    if csv_path:
        print(f"\n✅ Ready for analysis!")
        print(f"   File: {csv_path}")
        print(f"   Total columns: {len(columns)}")