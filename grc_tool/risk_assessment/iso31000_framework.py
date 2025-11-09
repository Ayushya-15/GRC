"""
ISO 31000:2018 Risk Management Framework Implementation
Provides comprehensive risk management aligned with international standards.
"""

import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class ISO31000Framework:
    """
    Complete implementation of ISO 31000:2018 Risk Management Framework.
    Superior to Nessus by providing structured, standards-compliant risk management.
    
    ISO 31000 Principles:
    1. Integrated
    2. Structured and comprehensive
    3. Customized
    4. Inclusive
    5. Dynamic
    6. Best available information
    7. Human and cultural factors
    8. Continual improvement
    """
    
    def __init__(self):
        """Initialize ISO 31000 Framework."""
        self.context = {}
        self.risk_criteria = {}
        self.risks = []
        logger.info("ISO31000Framework initialized")
    
    def establish_context(self, organization_context: Dict) -> Dict:
        """
        Step 1: Establish the Context (ISO 31000 Clause 5.3)
        Define internal and external context for risk management.
        
        Args:
            organization_context: Organization-specific context information
            
        Returns:
            Context definition
        """
        logger.info("Establishing risk management context")
        
        self.context = {
            "external_context": {
                "regulatory_requirements": organization_context.get("regulatory", []),
                "industry_standards": ["ISO 31000:2018", "ISO/IEC 27001", "NIST Cybersecurity Framework"],
                "threat_landscape": organization_context.get("threats", []),
                "stakeholder_expectations": organization_context.get("stakeholders", [])
            },
            "internal_context": {
                "organization_structure": organization_context.get("structure", ""),
                "governance": organization_context.get("governance", ""),
                "capabilities": organization_context.get("capabilities", []),
                "information_systems": organization_context.get("systems", [])
            },
            "risk_management_context": {
                "scope": "Network infrastructure and end-user systems",
                "objectives": [
                    "Identify and eliminate security risks",
                    "Ensure compliance with ISO 31000",
                    "Protect confidentiality, integrity, and availability",
                    "Enable business continuity"
                ],
                "resources": organization_context.get("resources", {}),
                "accountability": organization_context.get("accountability", {})
            }
        }
        
        return self.context
    
    def define_risk_criteria(self) -> Dict:
        """
        Step 2: Define Risk Criteria (ISO 31000 Clause 5.3.5)
        Establish criteria for evaluating significance of risk.
        
        Returns:
            Risk criteria definition
        """
        logger.info("Defining risk criteria")
        
        self.risk_criteria = {
            "risk_appetite": {
                "description": "Maximum risk organization is willing to accept",
                "level": "LOW",
                "threshold": 5.0  # CVSS score threshold
            },
            "risk_tolerance": {
                "description": "Acceptable deviation from risk appetite",
                "variation": 1.0
            },
            "likelihood_criteria": {
                "VERY_HIGH": {"probability": "> 90%", "description": "Expected to occur"},
                "HIGH": {"probability": "70-90%", "description": "Likely to occur"},
                "MEDIUM": {"probability": "30-70%", "description": "May occur"},
                "LOW": {"probability": "10-30%", "description": "Unlikely to occur"},
                "VERY_LOW": {"probability": "< 10%", "description": "Rare occurrence"}
            },
            "consequence_criteria": {
                "CATASTROPHIC": {
                    "impact": "Complete system failure, data loss, regulatory penalties",
                    "recovery_time": "> 30 days",
                    "financial_impact": "> $1M"
                },
                "MAJOR": {
                    "impact": "Significant disruption, partial data loss",
                    "recovery_time": "7-30 days",
                    "financial_impact": "$100K - $1M"
                },
                "MODERATE": {
                    "impact": "Moderate disruption, limited data exposure",
                    "recovery_time": "1-7 days",
                    "financial_impact": "$10K - $100K"
                },
                "MINOR": {
                    "impact": "Minor disruption, no data loss",
                    "recovery_time": "< 24 hours",
                    "financial_impact": "$1K - $10K"
                },
                "NEGLIGIBLE": {
                    "impact": "Minimal impact",
                    "recovery_time": "< 4 hours",
                    "financial_impact": "< $1K"
                }
            },
            "risk_matrix": self._create_risk_matrix()
        }
        
        return self.risk_criteria
    
    def _create_risk_matrix(self) -> Dict:
        """
        Create risk matrix for risk level determination.
        
        Returns:
            Risk matrix
        """
        return {
            "VERY_HIGH_LIKELIHOOD": {
                "CATASTROPHIC": "EXTREME",
                "MAJOR": "EXTREME",
                "MODERATE": "HIGH",
                "MINOR": "MEDIUM",
                "NEGLIGIBLE": "LOW"
            },
            "HIGH_LIKELIHOOD": {
                "CATASTROPHIC": "EXTREME",
                "MAJOR": "HIGH",
                "MODERATE": "HIGH",
                "MINOR": "MEDIUM",
                "NEGLIGIBLE": "LOW"
            },
            "MEDIUM_LIKELIHOOD": {
                "CATASTROPHIC": "EXTREME",
                "MAJOR": "HIGH",
                "MODERATE": "MEDIUM",
                "MINOR": "MEDIUM",
                "NEGLIGIBLE": "LOW"
            },
            "LOW_LIKELIHOOD": {
                "CATASTROPHIC": "HIGH",
                "MAJOR": "MEDIUM",
                "MODERATE": "MEDIUM",
                "MINOR": "LOW",
                "NEGLIGIBLE": "LOW"
            },
            "VERY_LOW_LIKELIHOOD": {
                "CATASTROPHIC": "MEDIUM",
                "MAJOR": "MEDIUM",
                "MODERATE": "LOW",
                "MINOR": "LOW",
                "NEGLIGIBLE": "LOW"
            }
        }
    
    def identify_risks(self, scan_results: Dict, vulnerabilities: List[Dict]) -> List[Dict]:
        """
        Step 3: Risk Identification (ISO 31000 Clause 6.4.2)
        Identify sources of risk, events, and consequences.
        
        Args:
            scan_results: Network scan results
            vulnerabilities: Identified vulnerabilities
            
        Returns:
            List of identified risks
        """
        logger.info("Identifying risks per ISO 31000")
        
        identified_risks = []
        
        for vuln in vulnerabilities:
            risk = {
                "risk_id": self._generate_risk_id(),
                "identification_date": datetime.now().isoformat(),
                "source": vuln.get("service", "Unknown"),
                "event": vuln.get("type", "Unknown"),
                "cause": self._identify_cause(vuln),
                "consequence": self._identify_consequence(vuln),
                "affected_assets": self._identify_affected_assets(vuln, scan_results),
                "vulnerability_ref": vuln,
                "status": "IDENTIFIED"
            }
            identified_risks.append(risk)
        
        self.risks.extend(identified_risks)
        logger.info(f"Identified {len(identified_risks)} risks")
        
        return identified_risks
    
    def analyze_risks(self, risks: List[Dict]) -> List[Dict]:
        """
        Step 4: Risk Analysis (ISO 31000 Clause 6.4.3)
        Understand nature and determine level of risk.
        
        Args:
            risks: Identified risks
            
        Returns:
            Analyzed risks with likelihood and consequence
        """
        logger.info("Analyzing risks per ISO 31000")
        
        analyzed_risks = []
        
        for risk in risks:
            vuln = risk.get("vulnerability_ref", {})
            
            # Determine likelihood
            likelihood = self._determine_likelihood(vuln)
            
            # Determine consequence
            consequence = self._determine_consequence(vuln)
            
            # Calculate risk level
            risk_level = self._calculate_risk_level(likelihood, consequence)
            
            analyzed_risk = {
                **risk,
                "likelihood": likelihood,
                "consequence": consequence,
                "risk_level": risk_level,
                "cvss_score": vuln.get("cvss_score", 0),
                "analysis_method": "Quantitative and Qualitative",
                "analysis_date": datetime.now().isoformat(),
                "status": "ANALYZED"
            }
            
            analyzed_risks.append(analyzed_risk)
        
        logger.info(f"Analyzed {len(analyzed_risks)} risks")
        return analyzed_risks
    
    def evaluate_risks(self, analyzed_risks: List[Dict]) -> List[Dict]:
        """
        Step 5: Risk Evaluation (ISO 31000 Clause 6.4.4)
        Compare analysis results with risk criteria.
        
        Args:
            analyzed_risks: Analyzed risks
            
        Returns:
            Evaluated risks with treatment decisions
        """
        logger.info("Evaluating risks per ISO 31000")
        
        evaluated_risks = []
        risk_threshold = self.risk_criteria.get("risk_appetite", {}).get("threshold", 5.0)
        
        for risk in analyzed_risks:
            cvss_score = risk.get("cvss_score", 0)
            risk_level = risk.get("risk_level", "LOW")
            
            # Determine if risk is acceptable
            is_acceptable = cvss_score < risk_threshold and risk_level in ["LOW", "MEDIUM"]
            
            # Determine treatment priority
            priority = self._determine_treatment_priority(risk)
            
            evaluated_risk = {
                **risk,
                "is_acceptable": is_acceptable,
                "exceeds_criteria": not is_acceptable,
                "treatment_priority": priority,
                "treatment_required": not is_acceptable,
                "evaluation_date": datetime.now().isoformat(),
                "status": "EVALUATED"
            }
            
            evaluated_risks.append(evaluated_risk)
        
        logger.info(f"Evaluated {len(evaluated_risks)} risks")
        return evaluated_risks
    
    def _generate_risk_id(self) -> str:
        """Generate unique risk identifier."""
        import uuid
        return f"RISK-{uuid.uuid4().hex[:8].upper()}"
    
    def _identify_cause(self, vulnerability: Dict) -> str:
        """Identify root cause of risk."""
        vuln_type = vulnerability.get("type", "Unknown")
        
        causes = {
            "Outdated Software": "Failure to apply security patches",
            "Default Credentials": "Inadequate access control",
            "SSL/TLS Configuration": "Weak cryptographic configuration",
            "Weak Cipher Suites": "Outdated security standards",
            "Missing Security Patches": "Inadequate patch management"
        }
        
        return causes.get(vuln_type, "Security misconfiguration or vulnerability")
    
    def _identify_consequence(self, vulnerability: Dict) -> str:
        """Identify potential consequences."""
        severity = vulnerability.get("severity", "LOW")
        
        consequences = {
            "CRITICAL": "Complete system compromise, data breach, service disruption",
            "HIGH": "Unauthorized access, data exposure, system exploitation",
            "MEDIUM": "Limited unauthorized access, potential data exposure",
            "LOW": "Minor security weakness, limited impact"
        }
        
        return consequences.get(severity, "Potential security incident")
    
    def _identify_affected_assets(self, vulnerability: Dict, scan_results: Dict) -> List[str]:
        """Identify affected assets."""
        assets = []
        service = vulnerability.get("service", "")
        
        for host, host_data in scan_results.get("hosts", {}).items():
            for proto, ports in host_data.get("protocols", {}).items():
                for port, info in ports.items():
                    if service in info.get("name", ""):
                        assets.append(f"{host}:{port}")
        
        return assets if assets else ["Network infrastructure"]
    
    def _determine_likelihood(self, vulnerability: Dict) -> str:
        """Determine likelihood of risk occurrence."""
        severity = vulnerability.get("severity", "LOW")
        
        likelihood_map = {
            "CRITICAL": "VERY_HIGH",
            "HIGH": "HIGH",
            "MEDIUM": "MEDIUM",
            "LOW": "LOW"
        }
        
        return likelihood_map.get(severity, "LOW")
    
    def _determine_consequence(self, vulnerability: Dict) -> str:
        """Determine consequence severity."""
        cvss_score = vulnerability.get("cvss_score", 0)
        
        if cvss_score >= 9.0:
            return "CATASTROPHIC"
        elif cvss_score >= 7.0:
            return "MAJOR"
        elif cvss_score >= 5.0:
            return "MODERATE"
        elif cvss_score >= 3.0:
            return "MINOR"
        else:
            return "NEGLIGIBLE"
    
    def _calculate_risk_level(self, likelihood: str, consequence: str) -> str:
        """Calculate risk level using risk matrix."""
        matrix = self.risk_criteria.get("risk_matrix", {})
        return matrix.get(likelihood, {}).get(consequence, "MEDIUM")
    
    def _determine_treatment_priority(self, risk: Dict) -> int:
        """Determine priority for risk treatment (1=highest)."""
        risk_level = risk.get("risk_level", "LOW")
        
        priority_map = {
            "EXTREME": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4
        }
        
        return priority_map.get(risk_level, 4)
