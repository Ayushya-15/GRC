# Quick Start Guide

Get up and running with the GRC Compliance Tool in minutes.

## Prerequisites

- Python 3.8 or higher
- pip package manager
- nmap installed on your system
- Basic knowledge of network security
- **Authorization** to scan your target networks

## Installation

### Step 1: Install nmap

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install nmap -y
```

**macOS:**
```bash
brew install nmap
```

**Windows:**
Download and install from [nmap.org](https://nmap.org/download.html)

### Step 2: Clone the Repository

```bash
git clone https://github.com/Ayushya-15/GRC.git
cd GRC
```

### Step 3: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install the Tool

```bash
pip install -e .
```

Verify installation:
```bash
grc-scan --help
```

## Basic Usage

### Your First Scan

**Scan localhost (safe for testing):**
```bash
grc-scan --target 127.0.0.1 --quick
```

This will:
1. Scan common ports on localhost
2. Identify services
3. Detect vulnerabilities
4. Analyze risks using ISO 31000
5. Generate mitigation recommendations
6. Create a comprehensive report

### Understanding the Output

The scan will show 9 phases:

```
[1/9] Network Scanning...
✓ Found 1 hosts

[2/9] Vulnerability Scanning...
✓ Identified 5 vulnerabilities

[3/9] ML-based Threat Detection...
✓ Detected 1 potential threats

[4/9] Anomaly Detection...
✓ Found 0 anomalies

[5/9] ISO 31000 Risk Assessment...
✓ Assessed 5 risks per ISO 31000

[6/9] Detailed Risk Analysis...
✓ Risk analysis completed

[7/9] Risk Prediction (ML)...
✓ Future risk predictions generated

[8/9] Generating Mitigation Strategies...
✓ Mitigation strategies generated

[9/9] Generating Report...
✓ Report generated successfully
```

### Scan Results

After the scan completes, you'll see a summary:

```
======================================================================
GRC COMPLIANCE SCAN SUMMARY
======================================================================

Overall Risk Rating: MEDIUM
Compliance Status: PARTIAL

Key Findings:
  • Hosts Scanned: 1
  • Vulnerabilities: 5
  • Risks Identified: 5
  • Critical Risks: 0
  • High Risks: 2
  • Threats Detected: 1

Top Recommendations:
  1. Address all critical risks within 24 hours
  2. Implement comprehensive patch management
  3. Enhance access control mechanisms
  4. Establish continuous monitoring
  5. Conduct regular security assessments

======================================================================

Full report saved to: ./reports
```

### Finding Your Reports

Reports are saved in the `./reports` directory:

```bash
ls -lh reports/
# Output: grc_report_20250109_140830.json
```

## Common Scanning Scenarios

### Scenario 1: Quick Network Assessment

**Scan a single server:**
```bash
grc-scan --target 192.168.1.100 --quick
```

**What it does:**
- Scans only common ports (faster)
- Identifies critical services
- Quick vulnerability check
- Basic risk assessment

**Time**: ~2-5 minutes

### Scenario 2: Comprehensive Assessment

**Full port scan:**
```bash
grc-scan --target 192.168.1.100
```

**What it does:**
- Scans all 65,535 ports
- Deep service analysis
- Complete vulnerability assessment
- Full ISO 31000 risk management

**Time**: ~15-30 minutes

### Scenario 3: Network Range Scan

**Scan multiple hosts:**
```bash
grc-scan --target 192.168.1.0/24 --quick
```

**What it does:**
- Discovers active hosts
- Scans each host
- Aggregates risks
- Network-wide risk assessment

**Time**: Varies with network size

### Scenario 4: Custom Configuration

**Create config file:**
```bash
cat > my_config.yaml <<EOF
scanning:
  timeout: 60
  threads: 20

risk_assessment:
  risk_appetite: 6.0

reporting:
  output_dir: ./my_reports

logging:
  level: DEBUG
EOF
```

**Run with config:**
```bash
grc-scan --target 192.168.1.100 --config my_config.yaml
```

## Using Python API

### Basic Script

Create `my_scan.py`:

```python
#!/usr/bin/env python3
from grc_tool import GRCScanner

# Initialize scanner
scanner = GRCScanner()

# Perform scan
results = scanner.scan("127.0.0.1", quick=True)

# Access results
print(f"Vulnerabilities found: {len(results['vulnerabilities'])}")
print(f"Risks identified: {len(results['risk_assessment']['evaluated_risks'])}")

# Check for critical risks
risks = results['risk_assessment']['evaluated_risks']
critical = [r for r in risks if r.get('risk_level') == 'EXTREME']
print(f"Critical risks: {len(critical)}")

if critical:
    print("\nCritical Risk Details:")
    for risk in critical:
        print(f"  - {risk['event']}")
        print(f"    CVSS: {risk['cvss_score']}")
        print(f"    Consequence: {risk['consequence']}")
```

Run it:
```bash
python3 my_scan.py
```

## Working with Reports

### View Report Summary

```bash
# Install jq for JSON parsing
sudo apt-get install jq

# View executive summary
jq '.executive_summary' reports/grc_report_*.json
```

### Extract Specific Information

**Get all critical vulnerabilities:**
```bash
jq '.vulnerabilities[] | select(.severity == "CRITICAL")' reports/grc_report_*.json
```

**Get mitigation plan:**
```bash
jq '.mitigation_plan.immediate_actions' reports/grc_report_*.json
```

**Get risk predictions:**
```bash
jq '.risk_predictions' reports/grc_report_*.json
```

## Best Practices

### 1. Always Get Authorization

⚠️ **CRITICAL**: Only scan systems you own or have explicit permission to scan.

```bash
# Good: Your own server
grc-scan --target your-server.com

# Bad: Someone else's server without permission
grc-scan --target someone-else.com  # ILLEGAL!
```

### 2. Start with Quick Scans

```bash
# First, do a quick scan
grc-scan --target 192.168.1.100 --quick

# If issues found, do full scan
grc-scan --target 192.168.1.100
```

### 3. Schedule Regular Scans

Create a cron job:
```bash
# Edit crontab
crontab -e

# Add weekly scan (every Sunday at 2 AM)
0 2 * * 0 /usr/local/bin/grc-scan --target 192.168.1.0/24 --quick
```

### 4. Keep Reports Organized

```bash
# Use timestamped directories
grc-scan --target 192.168.1.100 --output ./reports/$(date +%Y%m%d)
```

### 5. Review Mitigation Plans

After scanning:
1. Review the executive summary
2. Prioritize critical and high risks
3. Follow the mitigation steps
4. Re-scan to verify fixes

## Troubleshooting

### Problem: "Command not found: grc-scan"

**Solution:**
```bash
# Reinstall
pip install -e .

# Or use full path
python3 -m grc_tool.main --target 127.0.0.1
```

### Problem: "No module named 'nmap'"

**Solution:**
```bash
pip install python-nmap
```

### Problem: "Permission denied"

**Solution:**
```bash
# Some scans require sudo (OS detection)
sudo grc-scan --target 192.168.1.100
```

### Problem: "No hosts found"

**Possible causes:**
1. Target is down or unreachable
2. Firewall blocking scans
3. Wrong IP address/range

**Solution:**
```bash
# Test connectivity first
ping 192.168.1.100

# Check firewall
sudo iptables -L

# Try quick scan first
grc-scan --target 192.168.1.100 --quick
```

### Problem: Scan is too slow

**Solution:**
```bash
# Use quick scan
grc-scan --target 192.168.1.100 --quick

# Or reduce timeout in config
cat > fast_config.yaml <<EOF
scanning:
  timeout: 10
  threads: 20
EOF

grc-scan --target 192.168.1.100 --config fast_config.yaml
```

## Next Steps

Now that you've completed a basic scan:

1. **Learn More**: Read the [full documentation](../README.md)
2. **Understand ISO 31000**: Review [ISO31000Framework](./ARCHITECTURE.md)
3. **Compare with Nessus**: See [comparison document](./COMPARISON_WITH_NESSUS.md)
4. **Review Research**: Check [research references](./RESEARCH_REFERENCES.md)
5. **Advanced Usage**: Try the [example scripts](../examples/)

## Common Commands Reference

```bash
# Basic scan
grc-scan --target <IP>

# Quick scan (common ports only)
grc-scan --target <IP> --quick

# Network range
grc-scan --target <CIDR>

# Custom config
grc-scan --target <IP> --config config.yaml

# Custom output directory
grc-scan --target <IP> --output /path/to/reports

# Debug mode
grc-scan --target <IP> --log-level DEBUG

# Get help
grc-scan --help
```

## Getting Help

- **GitHub Issues**: https://github.com/Ayushya-15/GRC/issues
- **Documentation**: Check the `docs/` directory
- **Examples**: See `examples/` for code samples

## Safety Reminder

⚠️ **IMPORTANT SECURITY NOTES**:

1. **Authorization Required**: Always get written permission before scanning
2. **Legal Implications**: Unauthorized scanning can be illegal
3. **Network Impact**: Scans can generate significant network traffic
4. **False Positives**: Not all identified issues may be exploitable
5. **Responsible Disclosure**: Report vulnerabilities responsibly

## Success!

You've successfully installed and run the GRC Compliance Tool! 🎉

For advanced features and customization, check out the full documentation.

---

**Need Help?** Open an issue on GitHub or consult the documentation.

**Happy Scanning!** 🔒🛡️
