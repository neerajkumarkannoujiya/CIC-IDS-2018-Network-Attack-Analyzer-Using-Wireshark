# CIC-IDS-2018 Network Attack Analyzer

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Wireshark](https://img.shields.io/badge/Wireshark-Network%20Analysis-green)
![Dataset](https://img.shields.io/badge/Dataset-CIC%20IDS%202018-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A comprehensive network security analysis toolkit for processing and analyzing the CIC IDS 2018 dataset. This project enables statistical analysis of network attacks using Python and deep packet inspection using Wireshark.

## 📖 Overview

The **CIC-IDS-2018 Network Attack Analyzer** provides a complete environment for:
- **Statistical analysis** of network intrusion detection datasets
- **Comparative attack analysis** between different attack types
- **Automated PCAP generation** for hands-on network forensics
- **Comprehensive reporting** with visualizations and findings

### 🎯 Key Features

- 🔍 **Dataset Analysis**: Process and analyze CIC IDS 2018 CSV files
- 📊 **Attack Comparison**: Compare distinctive features between attack types
- 🌐 **PCAP Generation**: Create realistic attack simulations for Wireshark analysis
- 📈 **Visual Reporting**: Generate comprehensive reports with charts and findings
- 🛠️ **Modular Design**: Easy to extend for additional attack types and datasets

## 🚀 Quick Start

### Prerequisites

- Ubuntu 18.04+ or similar Linux distribution
- Python 3.8+
- 10GB+ free disk space

### Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/CIC-IDS-2018-Network-Analyzer.git
cd CIC-IDS-2018-Network-Analyzer

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Download CIC IDS 2018 dataset
# Place CSV files in the data/ directory
# Download from: https://www.unb.ca/cic/datasets/ids-2018.html
```

### Basic Usage

```bash
# Activate virtual environment
source env/bin/activate

# Run complete analysis workflow
python3 scripts/check_dataset.py
python3 scripts/analyze_attacks.py
python3 scripts/generate_analysis.py
```

## 📁 Project Structure

```
CIC-IDS-2018-Network-Analyzer/
├── data/                   # CIC IDS 2018 dataset files
│   ├── 02-14-2018.csv
│   ├── 02-15-2018.csv
│   └── ...
├── scripts/               # Analysis scripts
│   ├── check_dataset.py   # Dataset verification
│   ├── analyze_attacks.py # Main analysis engine
│   └── generate_analysis.py # PCAP & report generation
├── output/                # Generated reports & visualizations
│   ├── attack_analysis_report.txt
│   ├── detailed_analysis.png
│   └── ...
├── pcaps/                 # Network capture files
│   ├── goldeneye_attack.pcap
│   ├── slowloris_attack.pcap
│   └── normal_traffic.pcap
├── env/                   # Python virtual environment
├── docs/                  # Documentation
└── README.md
```

## 🔧 Detailed Setup Guide

### Step 1: System Preparation

```bash
# Update system and install base packages
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv python3-full git curl wget

# Install Wireshark for packet analysis
sudo apt install wireshark tshark tcpdump -y

# Configure Wireshark permissions
sudo dpkg-reconfigure wireshark-common
# Select "Yes" when prompted

sudo usermod -aG wireshark $USER
# LOGOUT AND LOGIN AFTER THIS COMMAND
```

### Step 2: Project Setup

```bash
# Create project structure
mkdir -p ~/ids_analysis/{data,scripts,output,pcaps,backup}
cd ~/ids_analysis
```

### Step 3: Python Environment

```bash
# Create and activate virtual environment
python3 -m venv env
source env/bin/activate

# Install required packages
pip install --upgrade pip
pip install pandas numpy matplotlib seaborn scikit-learn jupyter pyshark scapy
```

### Step 4: Dataset Preparation

Download CIC IDS 2018 CSV files from:
- [Official Source](https://www.unb.ca/cic/datasets/ids-2018.html)
- [Kaggle Dataset](https://www.kaggle.com/datasets/solarmainframe/ids-intrusion-csv)

Place the downloaded CSV files in the `data/` directory.

## 📊 Usage Examples

### Basic Analysis

```bash
# Check dataset structure
python3 scripts/check_dataset.py

# Analyze attack distribution and compare attacks
python3 scripts/analyze_attacks.py

# Generate PCAP files and reports
python3 scripts/generate_analysis.py
```

### Sample Output

```
🎯 Attack Distribution:
--------------------------------------------------
   DoS attacks-GoldenEye:  28507 samples (95.02%)
   DoS attacks-Slowloris:   1353 samples (4.51%)
   Benign:                   140 samples (0.47%)

📊 Top distinctive features:
1. Flow Duration (Distinctiveness: 2.14)
   - GoldenEye: mean=9852493.15, std=14227371.55
   - Slowloris: mean=73056165.41, std=44973865.30
```

### Wireshark Analysis

```bash
# Analyze generated attack simulations
wireshark pcaps/goldeneye_attack.pcap
wireshark pcaps/slowloris_attack.pcap

# Command-line analysis
tshark -r pcaps/goldeneye_attack.pcap -Y "http.request.method == GET" -c 10
```

## 🔍 Analysis Features

### Supported Attack Types

- **DoS Attacks**: GoldenEye, Slowloris, Hulk, etc.
- **DDoS Attacks**: LOIT, PortScan
- **Brute Force Attacks**: FTP-Patator, SSH-Patator
- **Web Attacks**: Brute Force, XSS, SQL Injection
- **Infiltration Attacks**: Dropbox download

### Key Analysis Metrics

- **Flow Duration**: Connection lifetime analysis
- **Packet Statistics**: Size, count, and timing patterns
- **Protocol Analysis**: TCP/UDP behavior and flags
- **Traffic Patterns**: Source/destination analysis
- **Anomaly Detection**: Statistical outlier identification

## 🛠️ Script Documentation

### `check_dataset.py`
- Verifies dataset integrity and structure
- Identifies label columns and attack types
- Provides dataset statistics and sample data

### `analyze_attacks.py`
- Performs statistical analysis of attack patterns
- Compares distinctive features between attack types
- Generates attack distribution visualizations

### `generate_analysis.py`
- Creates realistic PCAP simulations of attacks
- Generates comprehensive analysis reports
- Produces comparative visualizations

## 📈 Outputs Generated

### Reports (`output/` directory)
- `attack_analysis_report.txt`: Comprehensive findings
- `detailed_analysis.png`: Comparative visualizations
- `attack_distribution.png`: Attack type distribution

### Network Captures (`pcaps/` directory)
- `goldeneye_attack.pcap`: HTTP flood simulation
- `slowloris_attack.pcap`: Slow HTTP attack simulation
- `normal_traffic.pcap`: Baseline normal traffic

## 🎯 Use Cases

### Academic Research
- Network security coursework and assignments
- Intrusion detection system development
- Attack pattern analysis and classification

### Professional Training
- Security analyst skill development
- Network forensics practice
- Incident response training

### Research & Development
- IDS signature development
- Machine learning feature engineering
- Security tool validation

## 🔧 Advanced Configuration

### Customizing Analysis Parameters

Modify `scripts/analyze_attacks.py`:

```python
# Adjust sample size for large datasets
analyzer.load_data_sample(50000)  # Change as needed

# Customize attack selection
attack1 = "DDoS attacks-LOIT"
attack2 = "Brute Force-Web"
```

### Extending for New Attacks

Add new attack analysis in `scripts/generate_analysis.py`:

```python
def create_custom_attack_simulation():
    # Add custom attack simulation logic
    pass
```

## 🐛 Troubleshooting

### Common Issues

**Wireshark Permission Denied**
```bash
sudo usermod -aG wireshark $USER
# Logout and login again
```

**Python Packages Not Found**
```bash
source env/bin/activate
pip install --force-reinstall pandas scapy
```

**Dataset Too Large**
```python
# Reduce sample size in analyze_attacks.py
analyzer.load_data_sample(10000)
```

**PCAP Generation Fails**
```bash
pip install scapy
python3 -c "import scapy; print('Scapy installed successfully')"
```

### Debug Mode

Enable verbose output by modifying scripts:

```python
# Add to any script for debugging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/CONTRIBUTING.md) for details.

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/yourusername/CIC-IDS-2018-Network-Analyzer.git
cd CIC-IDS-2018-Network-Analyzer

# Create feature branch
git checkout -b feature/amazing-feature

# Commit changes
git commit -m 'Add some amazing feature'

# Push to branch
git push origin feature/amazing-feature

# Open Pull Request
```

## 📊 Results Interpretation

### Understanding Distinctiveness Scores

- **Score > 2.0**: Highly distinctive feature
- **Score 1.0-2.0**: Moderately distinctive feature  
- **Score < 1.0**: Less distinctive feature

### Key Attack Indicators

**GoldenEye DoS**
- Short flow duration
- High packet size variability
- Multiple concurrent connections

**Slowloris DoS**
- Long flow duration
- Consistent small packet sizes
- Incomplete HTTP requests

## 📚 Learning Resources

- [CIC IDS 2018 Dataset Paper](https://www.unb.ca/cic/datasets/ids-2018.html)
- [Wireshark Documentation](https://www.wireshark.org/docs/)
- [Network Forensics Guide](https://tools.ietf.org/html/rfc3227)
- [Python for Security Analysis](https://github.com/topics/security-tools)

## 🏆 Featured Analyses

### DoS Attack Comparison
- **GoldenEye**: Rapid HTTP requests from multiple sources
- **Slowloris**: Slow, partial requests keeping connections open
- **Hulk**: HTTP-based attack with unique patterns

### DDoS Analysis
- **LOIT**: Layer 7 application attack
- **PortScan**: Network reconnaissance patterns

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- University of New Brunswick for the CIC IDS 2018 dataset
- Wireshark team for network analysis capabilities
- Python community for data analysis libraries

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Search existing [GitHub Issues](https://github.com/yourusername/CIC-IDS-2018-Network-Analyzer/issues)
3. Create a new issue with detailed information

## 🚀 Future Enhancements

- [ ] Real-time network monitoring integration
- [ ] Machine learning-based attack classification
- [ ] Cloud deployment support
- [ ] Additional dataset compatibility
- [ ] Web-based dashboard interface

---

<div align="center">

**Happy Analyzing! 🚀🔍**

</div>
