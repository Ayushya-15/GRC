#!/usr/bin/env python3
"""
Basic Usage Example for GRC Compliance Tool

This script demonstrates how to use the GRC tool programmatically.
"""

from grc_tool import GRCScanner
from grc_tool.utils import Config, setup_logging
import json


def example_basic_scan():
    """Example: Basic network scan"""
    print("Example 1: Basic Network Scan")
    print("-" * 50)
    
    # Initialize scanner with default configuration
    scanner = GRCScanner()
    
    # Perform scan on a target
    # NOTE: Replace with your actual target
    target = "127.0.0.1"  # localhost for testing
    
    print(f"Scanning target: {target}")
    results = scanner.scan(target, quick=True)
    
    # Access results
    print(f"\nHosts found: {len(results['scan_results']['hosts'])}")
    print(f"Vulnerabilities: {len(results['vulnerabilities'])}")
    print(f"Risks identified: {len(results['risk_assessment']['evaluated_risks'])}")
    
    return results


def example_custom_config():
    """Example: Using custom configuration"""
    print("\nExample 2: Custom Configuration")
    print("-" * 50)
    
    # Create custom configuration
    config = Config()
    
    # Customize settings
    config.set("scanning.timeout", 60)
    config.set("scanning.threads", 20)
    config.set("risk_assessment.risk_appetite", 6.0)
    config.set("reporting.output_dir", "./custom_reports")
    config.set("logging.level", "DEBUG")
    
    # Initialize scanner with custom config
    scanner = GRCScanner(config)
    
    # Perform scan
    target = "127.0.0.1"
    results = scanner.scan(target, quick=True)
    
    print(f"Scan completed with custom configuration")
    
    return results


def example_analyze_results():
    """Example: Analyzing scan results"""
    print("\nExample 3: Analyzing Results")
    print("-" * 50)
    
    scanner = GRCScanner()
    target = "127.0.0.1"
    results = scanner.scan(target, quick=True)
    
    # Analyze vulnerabilities
    vulnerabilities = results['vulnerabilities']
    critical = [v for v in vulnerabilities if v.get('severity') == 'CRITICAL']
    high = [v for v in vulnerabilities if v.get('severity') == 'HIGH']
    
    print(f"\nVulnerability Analysis:")
    print(f"  Critical: {len(critical)}")
    print(f"  High: {len(high)}")
    
    # Analyze risks
    risks = results['risk_assessment']['evaluated_risks']
    extreme_risks = [r for r in risks if r.get('risk_level') == 'EXTREME']
    
    print(f"\nRisk Analysis:")
    print(f"  Extreme risks: {len(extreme_risks)}")
    
    if extreme_risks:
        print("\n  Extreme Risk Details:")
        for risk in extreme_risks[:3]:  # Show first 3
            print(f"    - {risk.get('event')}")
            print(f"      Cause: {risk.get('cause')}")
            print(f"      CVSS: {risk.get('cvss_score')}")
    
    # Analyze mitigation plan
    mitigation = results['mitigation_plan']
    immediate_actions = mitigation.get('immediate_actions', [])
    
    print(f"\nMitigation Plan:")
    print(f"  Immediate actions: {len(immediate_actions)}")
    
    if immediate_actions:
        print("\n  First Immediate Action:")
        action = immediate_actions[0]
        print(f"    Risk: {action.get('risk_type')}")
        print(f"    Timeframe: {action.get('timeframe')}")
        print(f"    Effort: {action.get('estimated_effort')}")
    
    return results


def example_access_ml_predictions():
    """Example: Accessing ML predictions"""
    print("\nExample 4: ML Predictions")
    print("-" * 50)
    
    scanner = GRCScanner()
    target = "127.0.0.1"
    results = scanner.scan(target, quick=True)
    
    # Access threat detection results
    threats = results['threats']
    print(f"\nThreats detected by ML: {len(threats)}")
    
    if threats:
        print("\n  Threat Details:")
        for threat in threats[:3]:  # Show first 3
            print(f"    - Host: {threat.get('host')}")
            print(f"      Level: {threat.get('threat_level')}")
            print(f"      Type: {threat.get('threat_type')}")
            print(f"      Score: {threat.get('threat_score'):.2f}")
            print(f"      Confidence: {threat.get('confidence'):.2%}")
    
    # Access anomaly detection results
    anomalies = results['anomalies']
    print(f"\nAnomalies detected: {len(anomalies)}")
    
    # Access risk predictions
    predictions = results['risk_predictions']
    print(f"\nRisk Predictions:")
    print(f"  Trend: {predictions.get('risk_trend', {}).get('trend')}")
    print(f"  Overall risk level: {predictions.get('overall_risk_level')}")
    
    exploitation = predictions.get('exploitation_risk', {})
    high_likelihood = exploitation.get('high_likelihood_exploits', [])
    print(f"  High likelihood exploits: {len(high_likelihood)}")
    
    return results


def example_save_results():
    """Example: Saving results to file"""
    print("\nExample 5: Saving Results")
    print("-" * 50)
    
    scanner = GRCScanner()
    target = "127.0.0.1"
    results = scanner.scan(target, quick=True)
    
    # Save complete results to JSON
    output_file = "scan_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Results saved to: {output_file}")
    
    # Save specific sections
    risks_file = "risks_only.json"
    with open(risks_file, 'w') as f:
        json.dump(results['risk_assessment']['evaluated_risks'], f, indent=2)
    
    print(f"Risks saved to: {risks_file}")
    
    return results


def example_network_range_scan():
    """Example: Scanning a network range"""
    print("\nExample 6: Network Range Scan")
    print("-" * 50)
    
    # NOTE: This requires appropriate permissions
    # Replace with your actual network range
    network = "192.168.1.0/29"  # Small range for testing
    
    print(f"WARNING: This will scan multiple hosts in {network}")
    print("Make sure you have authorization!")
    
    # Uncomment to run:
    # scanner = GRCScanner()
    # results = scanner.scan(network, quick=True)
    # print(f"Scanned {len(results['scan_results']['hosts'])} hosts")
    
    print("(Skipped in example)")


def main():
    """Run all examples"""
    print("=" * 70)
    print("GRC Compliance Tool - Usage Examples")
    print("=" * 70)
    
    try:
        # Run examples
        example_basic_scan()
        example_custom_config()
        example_analyze_results()
        example_access_ml_predictions()
        example_save_results()
        example_network_range_scan()
        
        print("\n" + "=" * 70)
        print("All examples completed successfully!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\nError running examples: {str(e)}")
        print("Make sure you have appropriate permissions and nmap installed.")


if __name__ == "__main__":
    main()
