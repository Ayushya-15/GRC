# GRC Compliance Tool - GUI Usage Guide

## Overview

The GRC Compliance Tool now includes a user-friendly graphical interface that makes security scanning and report generation accessible to both technical and non-technical users.

## Launching the GUI

### Command Line
```bash
grc-gui
```

### From Python
```python
from grc_tool.gui import launch_gui
launch_gui()
```

## GUI Features

### 1. Main Window

The GUI provides an intuitive interface with the following components:

#### Scan Configuration Section
- **Target Input**: Enter IP address, hostname, or CIDR range (e.g., `192.168.1.0/24`)
- **Quick Scan Option**: Checkbox to enable quick scanning (common ports only)
- **Output Directory**: Choose where to save reports with a file browser

#### Action Buttons
- **Start Scan**: Begin the security assessment
- **Stop Scan**: Interrupt a running scan
- **Export PDF**: Generate professional PDF report
- **Export JSON**: Export raw data in JSON format
- **Export HTML**: Create web-based report

#### Progress Monitoring
- **Progress Bar**: Visual indication of scan progress
- **Status Label**: Current operation status

#### Output Tabs
- **Console Output**: Real-time logging and progress messages
- **Scan Results**: Formatted summary of findings

### 2. Scan Workflow

#### Step 1: Configure Scan
1. Enter target IP address or network range
2. Choose Quick Scan or Full Scan mode
3. Select output directory for reports

#### Step 2: Execute Scan
1. Click "Start Scan" button
2. Monitor progress in the console tab
3. Wait for scan completion notification

#### Step 3: Review Results
1. Switch to "Scan Results" tab
2. Review summary statistics:
   - Hosts scanned
   - Vulnerabilities found
   - Risks identified
   - Threat analysis
3. Check risk breakdown by severity

#### Step 4: Export Reports
1. Click desired export format button:
   - **PDF**: Professional formatted report
   - **JSON**: Raw data for further analysis
   - **HTML**: Web-based shareable report
2. Reports saved to configured output directory
3. Success dialog shows file location

## Export Formats

### PDF Reports

Professional PDF reports include:

- **Title Page**
  - Report metadata
  - Overall risk rating
  - Generation date

- **Executive Summary**
  - Key findings table
  - Risk statistics
  - Immediate actions required
  - Top recommendations

- **Risk Assessment**
  - Risk distribution by severity
  - Top 10 risks with details
  - CVSS scores and likelihood

- **Vulnerability Details**
  - Grouped by severity
  - CVE identifiers
  - Service and port information

- **Mitigation Plan**
  - Immediate actions (24 hours)
  - Urgent actions
  - Remediation timeline

- **Compliance Status**
  - ISO 31000:2018 compliance checklist
  - Overall compliance rating

### JSON Export

Raw JSON export includes all scan data:
- Complete scan results
- Vulnerability details
- Risk assessment data
- ML predictions
- Threat analysis
- Mitigation recommendations

Perfect for:
- Integration with other tools
- Custom analysis scripts
- Data archival

### HTML Export

Web-based report with:
- Responsive design
- Interactive tables
- Color-coded risk levels
- Easy sharing via email or web

## Example Usage Scenarios

### Scenario 1: Quick Network Assessment

```
1. Launch GUI: grc-gui
2. Enter target: 192.168.1.0/24
3. Enable "Quick Scan"
4. Click "Start Scan"
5. Wait ~5 minutes
6. Export PDF for management review
```

### Scenario 2: Detailed Security Audit

```
1. Launch GUI: grc-gui
2. Enter target: production-server.company.com
3. Disable "Quick Scan" for full assessment
4. Set output to: /reports/production-audit
5. Click "Start Scan"
6. Wait ~30 minutes
7. Export all formats:
   - PDF for executives
   - JSON for security team
   - HTML for documentation
```

### Scenario 3: Compliance Check

```
1. Launch GUI: grc-gui
2. Enter target: compliance-zone network
3. Run scan with default settings
4. Review compliance status in results
5. Export PDF with compliance section
6. Share with auditors
```

## GUI Best Practices

### Security Considerations

1. **Authorization**: Always obtain proper authorization before scanning
2. **Network Impact**: Use Quick Scan on production networks
3. **Output Security**: Store reports in secure locations
4. **Access Control**: Limit GUI access to authorized personnel

### Performance Tips

1. **Quick Scan**: Use for faster results on large networks
2. **Targeted Scans**: Scan specific hosts when possible
3. **Off-Peak Hours**: Schedule full scans during maintenance windows
4. **Report Management**: Regularly archive old reports

### Troubleshooting

#### GUI Won't Launch
```bash
# Check dependencies
pip install -r requirements.txt

# Verify tkinter installation
python3 -c "import tkinter"

# On Ubuntu/Debian, install tkinter if missing
sudo apt-get install python3-tk
```

#### Scan Fails to Start
- Verify target is reachable
- Check network permissions
- Ensure nmap is installed
- Review console output for errors

#### Export Fails
- Check output directory permissions
- Ensure disk space is available
- Verify reportlab is installed for PDF

## Keyboard Shortcuts

- **Ctrl+Q**: Quit application
- **F5**: Refresh results view
- **Ctrl+S**: Quick save to default format

## Configuration

The GUI uses the same configuration as the CLI tool. Settings can be customized in `config.yaml`:

```yaml
reporting:
  output_dir: "./reports"
  format: "json"

scanning:
  timeout: 30
  threads: 10
  
risk_assessment:
  risk_appetite: 5.0
```

## Support

For issues or questions:
- GitHub Issues: https://github.com/Ayushya-15/GRC/issues
- Check console output for detailed error messages
- Enable debug logging in config.yaml

## See Also

- [Main README](../README.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [API Reference](API.md)
