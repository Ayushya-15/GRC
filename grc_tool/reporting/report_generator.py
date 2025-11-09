"""
Report Generation Module
Generates comprehensive security and compliance reports.
"""

import logging
import json
from typing import Dict, List
from datetime import datetime
import os

logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Comprehensive report generation system.
    Provides detailed, actionable reports - superior to Nessus reporting.
    """
    
    def __init__(self, output_dir: str = "./reports"):
        """
        Initialize Report Generator.
        
        Args:
            output_dir: Directory for saving reports
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"ReportGenerator initialized with output directory: {output_dir}")
    
    def generate_comprehensive_report(self, scan_data: Dict) -> Dict:
        """
        Generate comprehensive GRC compliance report.
        
        Args:
            scan_data: Complete scan and analysis data
            
        Returns:
            Report data
        """
        logger.info("Generating comprehensive report")
        
        report = {
            "report_metadata": self._create_metadata(),
            "executive_summary": self._create_executive_summary(scan_data),
            "scan_results": scan_data.get("scan_results", {}),
            "risk_assessment": scan_data.get("risk_assessment", {}),
            "threat_analysis": scan_data.get("threat_analysis", {}),
            "mitigation_plan": scan_data.get("mitigation_plan", {}),
            "remediation_plan": scan_data.get("remediation_plan", {}),
            "compliance_status": self._assess_compliance(scan_data),
            "recommendations": self._compile_recommendations(scan_data),
            "appendices": self._create_appendices(scan_data)
        }
        
        # Save report
        self._save_report(report)
        
        logger.info("Comprehensive report generated successfully")
        return report
    
    def _create_metadata(self) -> Dict:
        """Create report metadata."""
        return {
            "report_title": "GRC Compliance Assessment Report",
            "report_type": "ISO 31000 Risk Assessment",
            "generated_date": datetime.now().isoformat(),
            "tool_version": "1.0.0",
            "standards": ["ISO 31000:2018", "ISO/IEC 27001", "NIST CSF"],
            "report_format": "JSON"
        }
    
    def _create_executive_summary(self, scan_data: Dict) -> Dict:
        """
        Create executive summary.
        
        Args:
            scan_data: Scan data
            
        Returns:
            Executive summary
        """
        risk_assessment = scan_data.get("risk_assessment", {})
        vulnerabilities = scan_data.get("vulnerabilities", [])
        threats = scan_data.get("threats", [])
        
        # Calculate key metrics
        total_risks = len(risk_assessment.get("evaluated_risks", []))
        critical_risks = sum(
            1 for r in risk_assessment.get("evaluated_risks", [])
            if r.get("risk_level") == "EXTREME"
        )
        
        summary = {
            "assessment_scope": "Network infrastructure and end-user systems",
            "assessment_date": datetime.now().strftime("%Y-%m-%d"),
            "key_findings": {
                "total_hosts_scanned": len(scan_data.get("scan_results", {}).get("hosts", {})),
                "total_vulnerabilities": len(vulnerabilities),
                "total_risks_identified": total_risks,
                "critical_risks": critical_risks,
                "high_risks": sum(
                    1 for r in risk_assessment.get("evaluated_risks", [])
                    if r.get("risk_level") == "HIGH"
                ),
                "threats_detected": len(threats)
            },
            "overall_risk_rating": self._calculate_overall_risk(risk_assessment),
            "compliance_status": "PARTIAL" if critical_risks > 0 else "COMPLIANT",
            "immediate_actions_required": critical_risks,
            "key_recommendations": [
                "Address all critical risks within 24 hours",
                "Implement comprehensive patch management",
                "Enhance access control mechanisms",
                "Establish continuous monitoring",
                "Conduct regular security assessments"
            ]
        }
        
        return summary
    
    def _assess_compliance(self, scan_data: Dict) -> Dict:
        """
        Assess compliance with standards.
        
        Args:
            scan_data: Scan data
            
        Returns:
            Compliance assessment
        """
        risk_assessment = scan_data.get("risk_assessment", {})
        evaluated_risks = risk_assessment.get("evaluated_risks", [])
        
        iso31000_compliance = {
            "context_established": True,
            "risks_identified": len(evaluated_risks) > 0,
            "risks_analyzed": all(r.get("status") == "ANALYZED" for r in evaluated_risks),
            "risks_evaluated": all(r.get("status") in ["EVALUATED", "ANALYZED"] for r in evaluated_risks),
            "mitigation_planned": scan_data.get("mitigation_plan") is not None,
            "overall_compliance": "PARTIAL"
        }
        
        # Check if all steps completed
        all_steps_complete = all([
            iso31000_compliance["context_established"],
            iso31000_compliance["risks_identified"],
            iso31000_compliance["risks_analyzed"],
            iso31000_compliance["risks_evaluated"],
            iso31000_compliance["mitigation_planned"]
        ])
        
        if all_steps_complete:
            iso31000_compliance["overall_compliance"] = "COMPLIANT"
        
        return {
            "iso_31000": iso31000_compliance,
            "assessment_date": datetime.now().isoformat()
        }
    
    def _compile_recommendations(self, scan_data: Dict) -> List[Dict]:
        """
        Compile all recommendations.
        
        Args:
            scan_data: Scan data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        # From mitigation plan
        mitigation = scan_data.get("mitigation_plan", {})
        for action_type in ["immediate_actions", "urgent_actions"]:
            actions = mitigation.get(action_type, [])
            for action in actions:
                recommendations.append({
                    "priority": "CRITICAL" if action_type == "immediate_actions" else "HIGH",
                    "category": "Mitigation",
                    "recommendation": action.get("risk_type", "Unknown"),
                    "implementation": action.get("timeframe", ""),
                    "effort": action.get("estimated_effort", "")
                })
        
        # General recommendations
        recommendations.extend([
            {
                "priority": "HIGH",
                "category": "Process Improvement",
                "recommendation": "Establish regular vulnerability scanning schedule",
                "implementation": "Within 2 weeks",
                "effort": "Medium"
            },
            {
                "priority": "MEDIUM",
                "category": "Training",
                "recommendation": "Conduct security awareness training for all staff",
                "implementation": "Within 1 month",
                "effort": "Low"
            },
            {
                "priority": "HIGH",
                "category": "Monitoring",
                "recommendation": "Implement 24/7 security monitoring (SIEM)",
                "implementation": "Within 1 month",
                "effort": "High"
            }
        ])
        
        return recommendations
    
    def _create_appendices(self, scan_data: Dict) -> Dict:
        """
        Create report appendices.
        
        Args:
            scan_data: Scan data
            
        Returns:
            Appendices
        """
        return {
            "glossary": {
                "ISO 31000": "International standard for risk management",
                "CVSS": "Common Vulnerability Scoring System",
                "CVE": "Common Vulnerabilities and Exposures",
                "GRC": "Governance, Risk, and Compliance"
            },
            "references": [
                "ISO 31000:2018 - Risk management - Guidelines",
                "ISO/IEC 27001:2013 - Information security management",
                "NIST Cybersecurity Framework",
                "OWASP Top 10",
                "CIS Critical Security Controls"
            ],
            "methodology": "ML-based vulnerability detection with ISO 31000 risk assessment framework"
        }
    
    def _calculate_overall_risk(self, risk_assessment: Dict) -> str:
        """Calculate overall risk rating."""
        evaluated_risks = risk_assessment.get("evaluated_risks", [])
        
        if not evaluated_risks:
            return "LOW"
        
        extreme_count = sum(1 for r in evaluated_risks if r.get("risk_level") == "EXTREME")
        high_count = sum(1 for r in evaluated_risks if r.get("risk_level") == "HIGH")
        
        if extreme_count > 0:
            return "CRITICAL"
        elif high_count > 3:
            return "HIGH"
        elif high_count > 0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _save_report(self, report: Dict):
        """
        Save report to file.
        
        Args:
            report: Report data
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grc_report_{timestamp}.json"
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            with open(filepath, 'w') as f:
                json.dump(report, f, indent=2)
            logger.info(f"Report saved to {filepath}")
        except Exception as e:
            logger.error(f"Failed to save report: {str(e)}")
    
    def generate_summary_report(self, report: Dict) -> str:
        """
        Generate human-readable summary.
        
        Args:
            report: Full report data
            
        Returns:
            Summary text
        """
        exec_summary = report.get("executive_summary", {})
        key_findings = exec_summary.get("key_findings", {})
        
        summary = f"""
GRC COMPLIANCE ASSESSMENT SUMMARY
{'=' * 60}

Assessment Date: {exec_summary.get('assessment_date', 'N/A')}
Overall Risk Rating: {exec_summary.get('overall_risk_rating', 'N/A')}
Compliance Status: {exec_summary.get('compliance_status', 'N/A')}

KEY FINDINGS:
- Total Hosts Scanned: {key_findings.get('total_hosts_scanned', 0)}
- Total Vulnerabilities: {key_findings.get('total_vulnerabilities', 0)}
- Total Risks Identified: {key_findings.get('total_risks_identified', 0)}
- Critical Risks: {key_findings.get('critical_risks', 0)}
- High Risks: {key_findings.get('high_risks', 0)}
- Threats Detected: {key_findings.get('threats_detected', 0)}

IMMEDIATE ACTIONS REQUIRED: {exec_summary.get('immediate_actions_required', 0)}

TOP RECOMMENDATIONS:
"""
        for i, rec in enumerate(exec_summary.get('key_recommendations', []), 1):
            summary += f"{i}. {rec}\n"
        
        summary += f"\n{'=' * 60}\n"
        summary += "Full report available in JSON format.\n"
        
        return summary
