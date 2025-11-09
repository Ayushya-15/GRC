"""
Risk Evaluation Module
Evaluates risks against organizational criteria.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class RiskEvaluator:
    """
    Risk evaluation and prioritization per ISO 31000.
    """
    
    def __init__(self, risk_appetite: float = 5.0):
        """
        Initialize Risk Evaluator.
        
        Args:
            risk_appetite: Organization's risk appetite threshold
        """
        self.risk_appetite = risk_appetite
        logger.info(f"RiskEvaluator initialized with risk appetite: {risk_appetite}")
    
    def evaluate_against_criteria(self, risks: List[Dict]) -> Dict:
        """
        Evaluate risks against organizational criteria.
        
        Args:
            risks: List of analyzed risks
            
        Returns:
            Evaluation results
        """
        logger.info("Evaluating risks against criteria")
        
        acceptable_risks = []
        unacceptable_risks = []
        
        for risk in risks:
            cvss_score = risk.get("cvss_score", 0)
            risk_level = risk.get("risk_level", "LOW")
            
            if self._is_acceptable(cvss_score, risk_level):
                acceptable_risks.append(risk)
            else:
                unacceptable_risks.append(risk)
        
        return {
            "acceptable_risks": acceptable_risks,
            "unacceptable_risks": unacceptable_risks,
            "acceptance_rate": len(acceptable_risks) / max(len(risks), 1),
            "requires_treatment": len(unacceptable_risks),
            "evaluation_summary": self._generate_summary(risks, acceptable_risks, unacceptable_risks)
        }
    
    def prioritize_risks(self, risks: List[Dict]) -> List[Dict]:
        """
        Prioritize risks for treatment.
        
        Args:
            risks: List of evaluated risks
            
        Returns:
            Prioritized list of risks
        """
        logger.info("Prioritizing risks for treatment")
        
        # Score each risk for prioritization
        scored_risks = []
        for risk in risks:
            priority_score = self._calculate_priority_score(risk)
            scored_risk = {**risk, "priority_score": priority_score}
            scored_risks.append(scored_risk)
        
        # Sort by priority score (descending)
        prioritized = sorted(scored_risks, key=lambda x: x["priority_score"], reverse=True)
        
        return prioritized
    
    def recommend_risk_response(self, risk: Dict) -> str:
        """
        Recommend risk response strategy.
        
        Args:
            risk: Risk to evaluate
            
        Returns:
            Recommended response strategy
        """
        cvss_score = risk.get("cvss_score", 0)
        risk_level = risk.get("risk_level", "LOW")
        
        if risk_level == "EXTREME" or cvss_score >= 9.0:
            return "TREAT_IMMEDIATELY"
        elif risk_level == "HIGH" or cvss_score >= 7.0:
            return "TREAT_PRIORITY"
        elif risk_level == "MEDIUM":
            return "TREAT_SCHEDULED"
        else:
            return "ACCEPT_WITH_MONITORING"
    
    def _is_acceptable(self, cvss_score: float, risk_level: str) -> bool:
        """
        Determine if risk is acceptable.
        
        Args:
            cvss_score: CVSS score
            risk_level: Risk level
            
        Returns:
            True if acceptable
        """
        return cvss_score < self.risk_appetite and risk_level in ["LOW", "MEDIUM"]
    
    def _calculate_priority_score(self, risk: Dict) -> float:
        """
        Calculate priority score for risk.
        
        Args:
            risk: Risk data
            
        Returns:
            Priority score
        """
        cvss_score = risk.get("cvss_score", 0)
        risk_level = risk.get("risk_level", "LOW")
        affected_assets = len(risk.get("affected_assets", []))
        
        # Weight factors
        cvss_weight = 1.0
        level_weight = self._get_level_weight(risk_level)
        asset_weight = min(affected_assets * 0.1, 2.0)
        
        priority = (cvss_score * cvss_weight) + level_weight + asset_weight
        
        return round(priority, 2)
    
    def _get_level_weight(self, risk_level: str) -> float:
        """Get weight for risk level."""
        weights = {
            "EXTREME": 5.0,
            "HIGH": 3.0,
            "MEDIUM": 1.5,
            "LOW": 0.5
        }
        return weights.get(risk_level, 0.0)
    
    def _generate_summary(self, all_risks: List[Dict], acceptable: List[Dict], unacceptable: List[Dict]) -> Dict:
        """Generate evaluation summary."""
        return {
            "total_risks_evaluated": len(all_risks),
            "acceptable_count": len(acceptable),
            "unacceptable_count": len(unacceptable),
            "immediate_action_required": sum(1 for r in unacceptable if r.get("risk_level") == "EXTREME"),
            "recommendation": self._get_overall_recommendation(unacceptable)
        }
    
    def _get_overall_recommendation(self, unacceptable_risks: List[Dict]) -> str:
        """Get overall recommendation."""
        if not unacceptable_risks:
            return "Risk posture is acceptable. Continue monitoring."
        
        extreme_count = sum(1 for r in unacceptable_risks if r.get("risk_level") == "EXTREME")
        
        if extreme_count > 0:
            return f"URGENT: {extreme_count} extreme risks require immediate treatment"
        elif len(unacceptable_risks) > 10:
            return "Multiple risks require treatment. Implement systematic remediation."
        else:
            return f"{len(unacceptable_risks)} risks require treatment per schedule."
