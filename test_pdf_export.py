#!/usr/bin/env python3
"""
Test script for PDF export functionality.
Tests PDF generation with sample data without requiring full scanner dependencies.
"""

import sys
import os
from datetime import datetime

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import PDF exporter directly without going through grc_tool.__init__
import importlib.util
spec = importlib.util.spec_from_file_location(
    "pdf_exporter",
    os.path.join(os.path.dirname(__file__), "grc_tool/reporting/pdf_exporter.py")
)
pdf_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pdf_module)
PDFExporter = pdf_module.PDFExporter


def create_sample_report_data():
    """Create sample report data for testing."""
    return {
        "report_metadata": {
            "report_title": "GRC Compliance Assessment Report",
            "report_type": "ISO 31000 Risk Assessment",
            "generated_date": datetime.now().isoformat(),
            "tool_version": "1.0.0",
            "standards": ["ISO 31000:2018", "ISO/IEC 27001", "NIST CSF"],
            "report_format": "PDF"
        },
        "executive_summary": {
            "assessment_scope": "Network infrastructure and end-user systems",
            "assessment_date": datetime.now().strftime("%Y-%m-%d"),
            "key_findings": {
                "total_hosts_scanned": 5,
                "total_vulnerabilities": 12,
                "total_risks_identified": 8,
                "critical_risks": 2,
                "high_risks": 3,
                "threats_detected": 4
            },
            "overall_risk_rating": "HIGH",
            "compliance_status": "PARTIAL",
            "immediate_actions_required": 2,
            "key_recommendations": [
                "Address all critical risks within 24 hours",
                "Implement comprehensive patch management",
                "Enhance access control mechanisms",
                "Establish continuous monitoring",
                "Conduct regular security assessments"
            ]
        },
        "scan_results": {
            "hosts": {
                "192.168.1.100": {"status": "up"},
                "192.168.1.101": {"status": "up"}
            }
        },
        "vulnerabilities": [
            {
                "cve_id": "CVE-2023-1234",
                "severity": "CRITICAL",
                "service": "Apache",
                "port": 80,
                "cvss_score": 9.8
            },
            {
                "cve_id": "CVE-2023-5678",
                "severity": "HIGH",
                "service": "OpenSSH",
                "port": 22,
                "cvss_score": 7.5
            }
        ],
        "risk_assessment": {
            "context": {},
            "criteria": {},
            "identified_risks": [],
            "analyzed_risks": [],
            "evaluated_risks": [
                {
                    "event": "Unauthorized access to web server",
                    "risk_level": "EXTREME",
                    "cvss_score": 9.8,
                    "likelihood": 0.9,
                    "cause": "Outdated Apache version with known vulnerabilities",
                    "status": "EVALUATED"
                },
                {
                    "event": "SSH brute force attack",
                    "risk_level": "HIGH",
                    "cvss_score": 7.5,
                    "likelihood": 0.7,
                    "cause": "Weak SSH configuration",
                    "status": "EVALUATED"
                },
                {
                    "event": "Data exfiltration via open port",
                    "risk_level": "HIGH",
                    "cvss_score": 7.0,
                    "likelihood": 0.6,
                    "cause": "Unnecessary open ports",
                    "status": "EVALUATED"
                },
                {
                    "event": "Denial of service attack",
                    "risk_level": "MEDIUM",
                    "cvss_score": 5.5,
                    "likelihood": 0.5,
                    "cause": "Missing rate limiting",
                    "status": "EVALUATED"
                }
            ]
        },
        "threats": [
            {"host": "192.168.1.100", "threat_level": "HIGH", "threat_type": "Known exploit"}
        ],
        "anomalies": [
            {"host": "192.168.1.101", "anomaly_type": "Unusual port configuration"}
        ],
        "mitigation_plan": {
            "immediate_actions": [
                {
                    "risk_type": "Critical vulnerability in Apache",
                    "timeframe": "Within 24 hours",
                    "estimated_effort": "2-4 hours"
                },
                {
                    "risk_type": "SSH hardening required",
                    "timeframe": "Within 48 hours",
                    "estimated_effort": "1-2 hours"
                }
            ],
            "urgent_actions": []
        },
        "remediation_plan": {
            "project_plan": {
                "total_duration": "2 weeks",
                "total_cost_estimate": "$5,000-$10,000",
                "resources_required": "2 security engineers"
            }
        },
        "compliance_status": {
            "iso_31000": {
                "context_established": True,
                "risks_identified": True,
                "risks_analyzed": True,
                "risks_evaluated": True,
                "mitigation_planned": True,
                "overall_compliance": "COMPLIANT"
            },
            "assessment_date": datetime.now().isoformat()
        }
    }


def test_pdf_export():
    """Test PDF export functionality."""
    print("=" * 80)
    print("Testing PDF Export Functionality")
    print("=" * 80)
    
    # Create output directory
    output_dir = "./test_reports"
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize PDF exporter
    print("\n1. Initializing PDF Exporter...")
    pdf_exporter = PDFExporter(output_dir=output_dir)
    print("   ✓ PDF Exporter initialized")
    
    # Create sample data
    print("\n2. Creating sample report data...")
    report_data = create_sample_report_data()
    print("   ✓ Sample data created")
    
    # Export to PDF
    print("\n3. Generating PDF report...")
    try:
        pdf_path = pdf_exporter.export_to_pdf(report_data, filename="test_report.pdf")
        print(f"   ✓ PDF report generated successfully!")
        print(f"   Location: {pdf_path}")
        
        # Check if file exists and has content
        if os.path.exists(pdf_path):
            file_size = os.path.getsize(pdf_path)
            print(f"   File size: {file_size:,} bytes")
            
            if file_size > 1000:
                print("\n" + "=" * 80)
                print("✓ PDF EXPORT TEST PASSED")
                print("=" * 80)
                print(f"\nGenerated PDF report can be found at: {pdf_path}")
                print("You can open this file to verify the formatting and content.")
                return True
            else:
                print("\n✗ PDF file is too small, may be incomplete")
                return False
        else:
            print("\n✗ PDF file was not created")
            return False
            
    except Exception as e:
        print(f"\n✗ PDF generation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_multiple_formats():
    """Test generating multiple PDF reports."""
    print("\n" + "=" * 80)
    print("Testing Multiple Report Formats")
    print("=" * 80)
    
    output_dir = "./test_reports"
    pdf_exporter = PDFExporter(output_dir=output_dir)
    report_data = create_sample_report_data()
    
    test_cases = [
        ("minimal_risks", "Minimal risks scenario"),
        ("high_severity", "High severity scenario"),
        ("compliance_check", "Compliance check")
    ]
    
    results = []
    for filename, description in test_cases:
        print(f"\nGenerating: {description}...")
        try:
            pdf_path = pdf_exporter.export_to_pdf(report_data, filename=f"{filename}.pdf")
            print(f"   ✓ {filename}.pdf created")
            results.append(True)
        except Exception as e:
            print(f"   ✗ Failed: {str(e)}")
            results.append(False)
    
    if all(results):
        print("\n✓ All PDF formats generated successfully")
        return True
    else:
        print(f"\n⚠ Some formats failed: {sum(results)}/{len(results)} succeeded")
        return False


if __name__ == "__main__":
    print("GRC Tool - PDF Export Test\n")
    
    # Run tests
    test1 = test_pdf_export()
    test2 = test_multiple_formats()
    
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Basic PDF Export: {'PASSED' if test1 else 'FAILED'}")
    print(f"Multiple Formats: {'PASSED' if test2 else 'FAILED'}")
    
    if test1 and test2:
        print("\n✓ All tests passed!")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed")
        sys.exit(1)
