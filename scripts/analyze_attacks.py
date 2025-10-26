import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

class IDSAnalyzer:
    def __init__(self, csv_path, label_column='Label'):
        self.csv_path = csv_path
        self.label_column = label_column
        self.df = None
        
    def load_data_sample(self, sample_size=50000):
        """Load a sample of the data for analysis"""
        print(f"📥 Loading {sample_size} samples from dataset...")
        
        try:
            # Get total rows
            with open(self.csv_path, 'r') as f:
                total_rows = sum(1 for line in f) - 1  # minus header
            
            print(f"   Total rows in dataset: {total_rows:,}")
            
            if total_rows > sample_size:
                # Read sample using chunks to handle memory
                chunks = []
                for chunk in pd.read_csv(self.csv_path, chunksize=10000, nrows=sample_size):
                    chunks.append(chunk)
                self.df = pd.concat(chunks, ignore_index=True)
                print(f"   Loaded {len(self.df)} samples")
            else:
                self.df = pd.read_csv(self.csv_path)
                print(f"   Loaded all {len(self.df)} rows")
                
            print(f"   Dataset shape: {self.df.shape}")
            return True
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            return False
    
    def analyze_attack_distribution(self):
        """Analyze the distribution of different attacks"""
        if self.label_column not in self.df.columns:
            print(f"❌ Label column '{self.label_column}' not found!")
            print("   Available columns:", self.df.columns.tolist())
            return None
            
        attack_counts = self.df[self.label_column].value_counts()
        
        print(f"\n🎯 Attack Distribution:")
        print("-" * 50)
        total_samples = len(self.df)
        for attack, count in attack_counts.items():
            percentage = (count / total_samples) * 100
            print(f"   {attack:<20}: {count:>6} samples ({percentage:>6.2f}%)")
            
        return attack_counts
    
    def compare_two_attacks(self, attack1, attack2):
        """Compare two specific attack types"""
        print(f"\n🔍 Comparing: {attack1} vs {attack2}")
        print("-" * 50)
        
        attack1_data = self.df[self.df[self.label_column] == attack1]
        attack2_data = self.df[self.df[self.label_column] == attack2]
        
        print(f"   {attack1}: {len(attack1_data)} samples")
        print(f"   {attack2}: {len(attack2_data)} samples")
        
        # Get numeric features for comparison
        numeric_features = self.df.select_dtypes(include=[np.number]).columns.tolist()
        if self.label_column in numeric_features:
            numeric_features.remove(self.label_column)
        
        print(f"\n   Analyzing {len(numeric_features)} numeric features...")
        
        # Find most distinctive features
        distinctive_features = []
        for feature in numeric_features[:15]:  # Limit for performance
            try:
                mean1 = attack1_data[feature].mean()
                mean2 = attack2_data[feature].mean()
                std1 = attack1_data[feature].std()
                std2 = attack2_data[feature].std()
                
                if std1 > 0 and std2 > 0:
                    distinctiveness = abs(mean1 - mean2) / ((std1 + std2) / 2)
                    distinctive_features.append((feature, distinctiveness, mean1, mean2, std1, std2))
            except:
                continue
        
        # Sort by distinctiveness
        distinctive_features.sort(key=lambda x: x[1], reverse=True)
        
        print(f"\n📊 Top 5 most distinctive features:")
        for i, (feature, dist, mean1, mean2, std1, std2) in enumerate(distinctive_features[:5]):
            print(f"   {i+1}. {feature}:")
            print(f"      {attack1}: mean={mean1:.2f}, std={std1:.2f}")
            print(f"      {attack2}: mean={mean2:.2f}, std={std2:.2f}")
            print(f"      Distinctiveness: {dist:.2f}")
            
        return attack1_data, attack2_data, distinctive_features

def main():
    # Find CSV file
    data_dir = "/home/neeraj7388011/ids_analysis/data"
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found! Please add your CSV file to the data directory.")
        return
    
    csv_file = csv_files[0]
    csv_path = os.path.join(data_dir, csv_file)
    
    print(f"🎯 Analyzing: {csv_file}")
    
    # You might need to change this based on your dataset
    LABEL_COLUMN = "Label"  # Common column names: "Label", "Attack", "Category"
    
    analyzer = IDSAnalyzer(csv_path, LABEL_COLUMN)
    
    if analyzer.load_data_sample(30000):
        attack_dist = analyzer.analyze_attack_distribution()
        
        if attack_dist is not None and len(attack_dist) >= 2:
            attacks = attack_dist.index.tolist()
            print(f"\n🔄 Available attacks: {attacks}")
            
            # Select first two non-BENIGN attacks if available
            non_benign = [a for a in attacks if 'benign' not in str(a).lower() and 'normal' not in str(a).lower()]
            
            if len(non_benign) >= 2:
                attack1, attack2 = non_benign[0], non_benign[1]
            else:
                attack1, attack2 = attacks[0], attacks[1]
            
            print(f"\n🎯 Selected for analysis: '{attack1}' and '{attack2}'")
            
            # Compare the attacks
            attack1_data, attack2_data, distinctive_features = analyzer.compare_two_attacks(attack1, attack2)
            
            print(f"\n✅ Analysis complete!")
            print(f"📋 Next steps:")
            print(f"   1. Use Wireshark to analyze network patterns for these attacks")
            print(f"   2. Focus on the distinctive features identified above")
            print(f"   3. Look for protocol anomalies and traffic patterns")
            
        else:
            print("❌ Not enough attack types found for comparison.")

if __name__ == "__main__":
    main()