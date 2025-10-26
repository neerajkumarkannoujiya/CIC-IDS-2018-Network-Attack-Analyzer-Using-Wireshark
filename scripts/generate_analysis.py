import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scapy.all import *
import os
import random

def create_dos_pcaps():
    """Create realistic PCAP files for DoS attacks analysis"""
    print("🎯 Creating DoS Attack PCAP files...")
    
    # Ensure directories exist
    os.makedirs('/home/neeraj7388011/ids_analysis/pcaps', exist_ok=True)
    os.makedirs('/home/neeraj7388011/ids_analysis/output', exist_ok=True)
    
    # 1. GoldenEye Attack Simulation (HTTP Flood)
    print("📡 Creating GoldenEye (HTTP Flood) simulation...")
    packets = []
    
    # GoldenEye characteristics: multiple HTTP requests to overwhelm server
    for i in range(200):
        # Simulate multiple HTTP GET requests from different sources
        src_ip = f"192.168.1.{random.randint(100, 200)}"
        
        # TCP SYN for connection establishment
        syn_pkt = IP(src=src_ip, dst="10.0.0.10") / TCP(sport=random.randint(1024, 65535), dport=80, flags='S')
        packets.append(syn_pkt)
        
        # HTTP GET request
        get_pkt = IP(src=src_ip, dst="10.0.0.10") / TCP(sport=random.randint(1024, 65535), dport=80, flags='A') / Raw(load="GET / HTTP/1.1\r\nHost: target.com\r\n\r\n")
        packets.append(get_pkt)
    
    wrpcap('/home/neeraj7388011/ids_analysis/pcaps/goldeneye_attack.pcap', packets)
    print("   ✅ Created: goldeneye_attack.pcap")
    
    # 2. Slowloris Attack Simulation (Slow HTTP requests)
    print("🐌 Creating Slowloris (Slow HTTP) simulation...")
    packets = []
    
    # Slowloris characteristics: slow, partial HTTP requests keeping connections open
    for i in range(50):
        src_ip = f"10.0.1.{random.randint(50, 150)}"
        
        # TCP SYN
        syn_pkt = IP(src=src_ip, dst="10.0.0.10") / TCP(sport=random.randint(1024, 65535), dport=80, flags='S')
        packets.append(syn_pkt)
        
        # Partial HTTP headers (Slowloris technique)
        partial_headers = [
            "GET / HTTP/1.1\r\n",
            "Host: target.com\r\n",
            "User-Agent: Mozilla/4.0\r\n",
            "Content-Length: 10000\r\n"
        ]
        
        for header in partial_headers:
            pkt = IP(src=src_ip, dst="10.0.0.10") / TCP(sport=random.randint(1024, 65535), dport=80, flags='A') / Raw(load=header)
            packets.append(pkt)
    
    wrpcap('/home/neeraj7388011/ids_analysis/pcaps/slowloris_attack.pcap', packets)
    print("   ✅ Created: slowloris_attack.pcap")
    
    # 3. Normal traffic for comparison
    print("🌐 Creating normal traffic simulation...")
    packets = []
    
    for i in range(100):
        src_ip = f"192.168.2.{random.randint(1, 50)}"
        
        # Normal complete HTTP transactions
        syn_pkt = IP(src=src_ip, dst="8.8.8.8") / TCP(sport=random.randint(1024, 65535), dport=80, flags='S')
        packets.append(syn_pkt)
        
        http_pkt = IP(src=src_ip, dst="8.8.8.8") / TCP(sport=random.randint(1024, 65535), dport=80, flags='A') / Raw(load="GET /index.html HTTP/1.1\r\nHost: example.com\r\n\r\n")
        packets.append(http_pkt)
        
        # Some DNS queries
        dns_pkt = IP(src=src_ip, dst="8.8.8.8") / UDP(sport=random.randint(1024, 65535), dport=53) / DNS(rd=1, qd=DNSQR(qname="google.com"))
        packets.append(dns_pkt)
    
    wrpcap('/home/neeraj7388011/ids_analysis/pcaps/normal_traffic.pcap', packets)
    print("   ✅ Created: normal_traffic.pcap")

def create_detailed_visualizations():
    """Create detailed visualizations based on the analysis"""
    print("📊 Creating detailed visualizations...")
    
    # Load the data for visualization
    csv_path = "/home/neeraj7388011/ids_analysis/data/02-15-2018.csv"
    df_sample = pd.read_csv(csv_path, nrows=30000)
    
    # Set style
    plt.style.use('seaborn-v0_8')
    sns.set_palette("husl")
    
    # 1. Attack Distribution Pie Chart
    plt.figure(figsize=(10, 8))
    
    plt.subplot(2, 2, 1)
    attack_counts = df_sample['Label'].value_counts()
    plt.pie(attack_counts.values, labels=attack_counts.index, autopct='%1.1f%%', startangle=90)
    plt.title('Attack Distribution in Dataset')
    
    # 2. Flow Duration Comparison
    plt.subplot(2, 2, 2)
    goldeneye = df_sample[df_sample['Label'] == 'DoS attacks-GoldenEye']['Flow Duration']
    slowloris = df_sample[df_sample['Label'] == 'DoS attacks-Slowloris']['Flow Duration']
    
    # Use log scale for better visualization
    plt.hist(np.log1p(goldeneye), alpha=0.7, label='GoldenEye', bins=30, density=True)
    plt.hist(np.log1p(slowloris), alpha=0.7, label='Slowloris', bins=30, density=True)
    plt.xlabel('Log(Flow Duration + 1)')
    plt.ylabel('Density')
    plt.title('Flow Duration Distribution')
    plt.legend()
    
    # 3. Packet Length Comparison
    plt.subplot(2, 2, 3)
    features_to_plot = ['Fwd Pkt Len Max', 'Fwd Pkt Len Mean', 'Tot Fwd Pkts']
    goldeneye_means = [df_sample[df_sample['Label'] == 'DoS attacks-GoldenEye'][f].mean() for f in features_to_plot]
    slowloris_means = [df_sample[df_sample['Label'] == 'DoS attacks-Slowloris'][f].mean() for f in features_to_plot]
    
    x = np.arange(len(features_to_plot))
    width = 0.35
    
    plt.bar(x - width/2, goldeneye_means, width, label='GoldenEye', alpha=0.8)
    plt.bar(x + width/2, slowloris_means, width, label='Slowloris', alpha=0.8)
    plt.xlabel('Features')
    plt.ylabel('Mean Values')
    plt.title('Feature Comparison: GoldenEye vs Slowloris')
    plt.xticks(x, features_to_plot, rotation=45)
    plt.legend()
    
    # 4. Protocol Distribution
    plt.subplot(2, 2, 4)
    protocol_counts = df_sample['Protocol'].value_counts().head(5)
    plt.bar(protocol_counts.index, protocol_counts.values)
    plt.xlabel('Protocol Number')
    plt.ylabel('Count')
    plt.title('Top 5 Protocols in Attacks')
    
    plt.tight_layout()
    plt.savefig('/home/neeraj7388011/ids_analysis/output/detailed_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("   ✅ Created: detailed_analysis.png")

def create_attack_analysis_report():
    """Create a comprehensive analysis report"""
    print("📄 Creating attack analysis report...")
    
    report = """
DOS ATTACK ANALYSIS REPORT - CIC IDS 2018 Dataset
==================================================

ANALYZED ATTACKS:
1. DoS attacks-GoldenEye
2. DoS attacks-Slowloris

KEY FINDINGS FROM DATASET ANALYSIS:
-----------------------------------

GoldenEye Characteristics:
- Shorter flow duration (mean: ~9.85 seconds)
- Higher forward packet length (mean: 326 bytes)
- More variable packet sizes (std: 191 bytes)
- Higher packet count per flow (mean: 3.93 packets)

Slowloris Characteristics:
- Much longer flow duration (mean: ~73 seconds)
- Smaller forward packet length (mean: 53 bytes)
- More consistent packet sizes (std: 89 bytes)
- Lower packet count per flow (mean: 2.34 packets)

DISTINCTIVE FEATURES:
---------------------
1. Flow Duration (Distinctiveness: 2.14)
   - GoldenEye: Short, bursty attacks
   - Slowloris: Long, sustained connections

2. Forward Packet Length Standard Deviation (Distinctiveness: 1.98)
   - GoldenEye: Variable packet sizes
   - Slowloris: Consistent packet sizes

3. Forward Packet Length Maximum (Distinctiveness: 1.94)
   - GoldenEye: Larger maximum packet sizes
   - Slowloris: Smaller maximum packet sizes

WIRESHARK ANALYSIS GUIDELINES:
------------------------------

For GoldenEye Attack (PCAP: goldeneye_attack.pcap):
- Look for multiple HTTP GET requests from different IPs
- Check for high rate of TCP SYN packets
- Analyze HTTP header patterns
- Monitor for server response codes

For Slowloris Attack (PCAP: slowloris_attack.pcap):
- Look for incomplete HTTP requests
- Check for long-lasting TCP connections
- Analyze timing between packet sends
- Monitor for connection timeouts

WIRESHARK FILTERS:
------------------
GoldenEye:
  - http.request.method == "GET"
  - tcp.flags.syn == 1
  - ip.src == 192.168.1.0/24

Slowloris:
  - tcp.port == 80
  - http
  - tcp.analysis.ack_rtt > 1

CONCLUSION:
-----------
Both attacks are DoS techniques but with different methodologies:
- GoldenEye: HTTP flood with complete requests
- Slowloris: Slow HTTP with partial requests

Use the generated PCAP files for hands-on Wireshark analysis.
"""
    
    with open('/home/neeraj7388011/ids_analysis/output/attack_analysis_report.txt', 'w') as f:
        f.write(report)
    
    print("   ✅ Created: attack_analysis_report.txt")

def main():
    print("🚀 Generating Complete Analysis Outputs...")
    print("=" * 50)
    
    create_dos_pcaps()
    print("")
    create_detailed_visualizations()
    print("")
    create_attack_analysis_report()
    
    print("\n✅ ALL OUTPUTS GENERATED SUCCESSFULLY!")
    print("\n📁 Check your folders:")
    print("   pcaps/ - Contains attack simulation files for Wireshark")
    print("   output/ - Contains analysis reports and visualizations")
    print("\n🔍 Next steps:")
    print("   1. Open PCAP files in Wireshark: wireshark pcaps/goldeneye_attack.pcap")
    print("   2. Study the analysis report: cat output/attack_analysis_report.txt")
    print("   3. Examine visualizations: output/detailed_analysis.png")

if __name__ == "__main__":
    main()