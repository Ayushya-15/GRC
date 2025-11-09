"""
Main GRC Scanner Module
Orchestrates the complete GRC compliance scanning and risk assessment process.
"""

import logging
import argparse
from typing import Dict, Optional
from colorama import init, Fore, Style

from .scanner import NetworkScanner, VulnerabilityScanner, ServiceDetector
from .ml_engine import ThreatDetector, AnomalyDetector, RiskPredictor
from .risk_assessment import ISO31000Framework, RiskAnalyzer, RiskEvaluator
from .mitigation import MitigationEngine, RemediationPlanner
from .reporting import ReportGenerator
from .utils import setup_logging, Config

init(autoreset=True)  # Initialize colorama

logger = logging.getLogger(__name__)


class GRCScanner:
    """
    Main GRC Compliance Scanner
    
    Comprehensive security assessment tool implementing ISO 31000 risk management
    with ML-based threat detection and automated mitigation recommendations.
    """
    
    def __init__(self, config: Config = None):
        """
        Initialize GRC Scanner.
        
        Args:
            config: Configuration object
        """
        self.config = config or Config()
        
        # Setup logging
        log_level = self.config.get("logging.level", "INFO")
        log_file = self.config.get("logging.file")
        setup_logging(level=log_level, log_file=log_file)
        
        # Initialize components
        self.network_scanner = NetworkScanner(
            timeout=self.config.get("scanning.timeout", 30),
            threads=self.config.get("scanning.threads", 10)
        )
        self.vulnerability_scanner = VulnerabilityScanner()
        self.service_detector = ServiceDetector()
        self.threat_detector = ThreatDetector()
        self.anomaly_detector = AnomalyDetector()
        self.risk_predictor = RiskPredictor()
        self.iso31000 = ISO31000Framework()
        self.risk_analyzer = RiskAnalyzer()
        self.risk_evaluator = RiskEvaluator(
            risk_appetite=self.config.get("risk_assessment.risk_appetite", 5.0)
        )
        self.mitigation_engine = MitigationEngine()
        self.remediation_planner = RemediationPlanner()
        self.report_generator = ReportGenerator(
            output_dir=self.config.get("reporting.output_dir", "./reports")
        )
        
        logger.info("GRCScanner initialized successfully")
    
    def scan(self, target: str, quick: bool = False) -> Dict:
        """
        Perform complete GRC compliance scan.
        
        Args:
            target: Target IP address or network range
            quick: Perform quick scan on common ports
            
        Returns:
            Complete scan results
        """
        logger.info(f"{Fore.GREEN}Starting GRC compliance scan for target: {target}{Style.RESET_ALL}")
        
        # Step 1: Network Scanning
        print(f"\n{Fore.CYAN}[1/9] Network Scanning...{Style.RESET_ALL}")
        if quick:
            scan_results = self.network_scanner.quick_scan(target)
        else:
            scan_results = self.network_scanner.scan_network(target)
        
        if not scan_results.get("hosts"):
            logger.error("No hosts found. Scan failed.")
            return {"error": "No hosts discovered"}
        
        print(f"{Fore.GREEN}✓ Found {len(scan_results['hosts'])} hosts{Style.RESET_ALL}")
        
        # Step 2: Vulnerability Scanning
        print(f"\n{Fore.CYAN}[2/9] Vulnerability Scanning...{Style.RESET_ALL}")
        all_vulnerabilities = []
        for host, host_data in scan_results["hosts"].items():
            services = host_data.get("protocols", {})
            vulns = self.vulnerability_scanner.scan_host(host, services)
            all_vulnerabilities.extend(vulns)
        
        print(f"{Fore.GREEN}✓ Identified {len(all_vulnerabilities)} vulnerabilities{Style.RESET_ALL}")
        
        # Step 3: Threat Detection (ML)
        print(f"\n{Fore.CYAN}[3/9] ML-based Threat Detection...{Style.RESET_ALL}")
        threats = self.threat_detector.detect_threats(scan_results)
        print(f"{Fore.GREEN}✓ Detected {len(threats)} potential threats{Style.RESET_ALL}")
        
        # Step 4: Anomaly Detection
        print(f"\n{Fore.CYAN}[4/9] Anomaly Detection...{Style.RESET_ALL}")
        anomalies = self.anomaly_detector.detect_anomalies(scan_results)
        print(f"{Fore.GREEN}✓ Found {len(anomalies)} anomalies{Style.RESET_ALL}")
        
        # Step 5: ISO 31000 Risk Assessment
        print(f"\n{Fore.CYAN}[5/9] ISO 31000 Risk Assessment...{Style.RESET_ALL}")
        
        # Establish context
        context = self.iso31000.establish_context({})
        
        # Define risk criteria
        criteria = self.iso31000.define_risk_criteria()
        
        # Identify risks
        identified_risks = self.iso31000.identify_risks(scan_results, all_vulnerabilities)
        
        # Analyze risks
        analyzed_risks = self.iso31000.analyze_risks(identified_risks)
        
        # Evaluate risks
        evaluated_risks = self.iso31000.evaluate_risks(analyzed_risks)
        
        print(f"{Fore.GREEN}✓ Assessed {len(evaluated_risks)} risks per ISO 31000{Style.RESET_ALL}")
        
        # Step 6: Risk Analysis
        print(f"\n{Fore.CYAN}[6/9] Detailed Risk Analysis...{Style.RESET_ALL}")
        quantitative_analysis = self.risk_analyzer.perform_quantitative_analysis(evaluated_risks)
        qualitative_analysis = self.risk_analyzer.perform_qualitative_analysis(evaluated_risks)
        risk_aggregation = self.risk_analyzer.assess_risk_aggregation(evaluated_risks)
        
        print(f"{Fore.GREEN}✓ Risk analysis completed{Style.RESET_ALL}")
        
        # Step 7: Risk Prediction
        print(f"\n{Fore.CYAN}[7/9] Risk Prediction (ML)...{Style.RESET_ALL}")
        risk_predictions = self.risk_predictor.predict_future_risks(evaluated_risks)
        print(f"{Fore.GREEN}✓ Future risk predictions generated{Style.RESET_ALL}")
        
        # Step 8: Mitigation Planning
        print(f"\n{Fore.CYAN}[8/9] Generating Mitigation Strategies...{Style.RESET_ALL}")
        evaluation_results = self.risk_evaluator.evaluate_against_criteria(evaluated_risks)
        prioritized_risks = self.risk_evaluator.prioritize_risks(evaluation_results["unacceptable_risks"])
        
        mitigation_plan = self.mitigation_engine.generate_mitigations(prioritized_risks)
        remediation_plan = self.remediation_planner.create_remediation_plan(mitigation_plan)
        
        print(f"{Fore.GREEN}✓ Mitigation strategies generated{Style.RESET_ALL}")
        
        # Step 9: Report Generation
        print(f"\n{Fore.CYAN}[9/9] Generating Report...{Style.RESET_ALL}")
        
        complete_data = {
            "scan_results": scan_results,
            "vulnerabilities": all_vulnerabilities,
            "threats": threats,
            "anomalies": anomalies,
            "risk_assessment": {
                "context": context,
                "criteria": criteria,
                "identified_risks": identified_risks,
                "analyzed_risks": analyzed_risks,
                "evaluated_risks": evaluated_risks,
                "quantitative_analysis": quantitative_analysis,
                "qualitative_analysis": qualitative_analysis,
                "risk_aggregation": risk_aggregation
            },
            "risk_predictions": risk_predictions,
            "threat_analysis": {
                "threats": threats,
                "anomalies": anomalies
            },
            "mitigation_plan": mitigation_plan,
            "remediation_plan": remediation_plan
        }
        
        report = self.report_generator.generate_comprehensive_report(complete_data)
        
        print(f"{Fore.GREEN}✓ Report generated successfully{Style.RESET_ALL}")
        
        # Display summary
        self._display_summary(report)
        
        logger.info("GRC compliance scan completed successfully")
        return complete_data
    
    def _display_summary(self, report: Dict):
        """
        Display scan summary to console.
        
        Args:
            report: Generated report
        """
        print(f"\n{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}GRC COMPLIANCE SCAN SUMMARY{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
        
        exec_summary = report.get("executive_summary", {})
        key_findings = exec_summary.get("key_findings", {})
        
        print(f"\n{Fore.CYAN}Overall Risk Rating:{Style.RESET_ALL} {exec_summary.get('overall_risk_rating', 'N/A')}")
        print(f"{Fore.CYAN}Compliance Status:{Style.RESET_ALL} {exec_summary.get('compliance_status', 'N/A')}")
        
        print(f"\n{Fore.CYAN}Key Findings:{Style.RESET_ALL}")
        print(f"  • Hosts Scanned: {key_findings.get('total_hosts_scanned', 0)}")
        print(f"  • Vulnerabilities: {key_findings.get('total_vulnerabilities', 0)}")
        print(f"  • Risks Identified: {key_findings.get('total_risks_identified', 0)}")
        print(f"  • {Fore.RED}Critical Risks: {key_findings.get('critical_risks', 0)}{Style.RESET_ALL}")
        print(f"  • {Fore.YELLOW}High Risks: {key_findings.get('high_risks', 0)}{Style.RESET_ALL}")
        print(f"  • Threats Detected: {key_findings.get('threats_detected', 0)}")
        
        if exec_summary.get('immediate_actions_required', 0) > 0:
            print(f"\n{Fore.RED}⚠ IMMEDIATE ACTIONS REQUIRED: {exec_summary.get('immediate_actions_required', 0)}{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}Top Recommendations:{Style.RESET_ALL}")
        for i, rec in enumerate(exec_summary.get('key_recommendations', [])[:5], 1):
            print(f"  {i}. {rec}")
        
        print(f"\n{Fore.YELLOW}{'=' * 70}{Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Full report saved to: {self.report_generator.output_dir}{Style.RESET_ALL}\n")


def main():
    """Main entry point for CLI."""
    parser = argparse.ArgumentParser(
        description="GRC Compliance Tool - ISO 31000 Risk Assessment with ML-based Threat Detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  grc-scan --target 192.168.1.1
  grc-scan --target 192.168.1.0/24 --quick
  grc-scan --target example.com --config config.yaml
  
For more information, visit: https://github.com/Ayushya-15/GRC
        """
    )
    
    parser.add_argument(
        "--target",
        required=True,
        help="Target IP address, hostname, or CIDR range"
    )
    
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Perform quick scan on common ports only"
    )
    
    parser.add_argument(
        "--config",
        help="Path to configuration file (YAML or JSON)"
    )
    
    parser.add_argument(
        "--output",
        help="Output directory for reports (default: ./reports)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.config) if args.config else Config()
    
    # Override config with CLI arguments
    if args.output:
        config.set("reporting.output_dir", args.output)
    
    if args.log_level:
        config.set("logging.level", args.log_level)
    
    # Initialize and run scanner
    try:
        scanner = GRCScanner(config)
        results = scanner.scan(args.target, quick=args.quick)
        
        if "error" in results:
            print(f"{Fore.RED}Scan failed: {results['error']}{Style.RESET_ALL}")
            return 1
        
        return 0
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Scan interrupted by user{Style.RESET_ALL}")
        return 130
    
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        logger.exception("Scan failed with exception")
        return 1


if __name__ == "__main__":
    exit(main())
