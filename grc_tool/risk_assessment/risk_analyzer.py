"""
Risk Analysis Module
Provides detailed risk analysis capabilities.
"""

import logging
from typing import Dict, List
import numpy as np

logger = logging.getLogger(__name__)


class RiskAnalyzer:
    """
    Advanced risk analysis with quantitative and qualitative methods.
    """
    
    def __init__(self):
        """Initialize Risk Analyzer."""
        logger.info("RiskAnalyzer initialized")
    
    def perform_quantitative_analysis(self, risks: List[Dict]) -> Dict:
        """
        Perform quantitative risk analysis.
        
        Args:
            risks: List of risks
            
        Returns:
            Quantitative analysis results
        """
        logger.info("Performing quantitative risk analysis")
        
        if not risks:
            return {"total_risk_exposure": 0, "average_risk": 0}
        
        # Calculate metrics
        cvss_scores = [r.get("cvss_score", 0) for r in risks]
        total_exposure = sum(cvss_scores)
        average_risk = np.mean(cvss_scores)
        max_risk = max(cvss_scores)
        min_risk = min(cvss_scores)
        std_dev = np.std(cvss_scores)
        
        # Risk distribution
        critical_count = sum(1 for s in cvss_scores if s >= 9.0)
        high_count = sum(1 for s in cvss_scores if 7.0 <= s < 9.0)
        medium_count = sum(1 for s in cvss_scores if 4.0 <= s < 7.0)
        low_count = sum(1 for s in cvss_scores if s < 4.0)
        
        return {
            "total_risk_exposure": round(total_exposure, 2),
            "average_risk": round(average_risk, 2),
            "maximum_risk": round(max_risk, 2),
            "minimum_risk": round(min_risk, 2),
            "standard_deviation": round(std_dev, 2),
            "risk_distribution": {
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "total_risks": len(risks)
        }
    
    def perform_qualitative_analysis(self, risks: List[Dict]) -> Dict:
        """
        Perform qualitative risk analysis.
        
        Args:
            risks: List of risks
            
        Returns:
            Qualitative analysis results
        """
        logger.info("Performing qualitative risk analysis")
        
        # Categorize by type
        risk_categories = {}
        for risk in risks:
            risk_type = risk.get("event", "Unknown")
            if risk_type not in risk_categories:
                risk_categories[risk_type] = []
            risk_categories[risk_type].append(risk)
        
        # Analyze each category
        category_analysis = {}
        for category, cat_risks in risk_categories.items():
            category_analysis[category] = {
                "count": len(cat_risks),
                "severity_breakdown": self._analyze_severity(cat_risks),
                "common_causes": self._identify_common_causes(cat_risks),
                "affected_systems": self._count_affected_systems(cat_risks)
            }
        
        return {
            "risk_categories": category_analysis,
            "total_categories": len(risk_categories),
            "most_common_risk": max(risk_categories.items(), key=lambda x: len(x[1]))[0] if risk_categories else "None"
        }
    
    def calculate_residual_risk(self, initial_risk: float, control_effectiveness: float) -> float:
        """
        Calculate residual risk after controls.
        
        Args:
            initial_risk: Initial risk score
            control_effectiveness: Control effectiveness (0-1)
            
        Returns:
            Residual risk score
        """
        residual = initial_risk * (1 - control_effectiveness)
        return round(residual, 2)
    
    def assess_risk_aggregation(self, risks: List[Dict]) -> Dict:
        """
        Assess cumulative and aggregated risks.
        
        Args:
            risks: List of risks
            
        Returns:
            Risk aggregation assessment
        """
        logger.info("Assessing risk aggregation")
        
        # Group by affected assets
        asset_risks = {}
        for risk in risks:
            assets = risk.get("affected_assets", ["Unknown"])
            for asset in assets:
                if asset not in asset_risks:
                    asset_risks[asset] = []
                asset_risks[asset].append(risk)
        
        # Calculate cumulative risk per asset
        asset_risk_scores = {}
        for asset, asset_risk_list in asset_risks.items():
            cumulative_score = sum(r.get("cvss_score", 0) for r in asset_risk_list)
            asset_risk_scores[asset] = {
                "cumulative_risk": round(cumulative_score, 2),
                "risk_count": len(asset_risk_list),
                "highest_risk": max(r.get("cvss_score", 0) for r in asset_risk_list)
            }
        
        # Identify high-risk assets
        high_risk_assets = {
            asset: score for asset, score in asset_risk_scores.items()
            if score["cumulative_risk"] > 15.0
        }
        
        return {
            "total_assets_at_risk": len(asset_risks),
            "asset_risk_scores": asset_risk_scores,
            "high_risk_assets": high_risk_assets,
            "most_vulnerable_asset": max(asset_risk_scores.items(), key=lambda x: x[1]["cumulative_risk"])[0] if asset_risk_scores else "None"
        }
    
    def _analyze_severity(self, risks: List[Dict]) -> Dict:
        """Analyze severity distribution."""
        severities = [r.get("risk_level", "LOW") for r in risks]
        return {
            "EXTREME": severities.count("EXTREME"),
            "HIGH": severities.count("HIGH"),
            "MEDIUM": severities.count("MEDIUM"),
            "LOW": severities.count("LOW")
        }
    
    def _identify_common_causes(self, risks: List[Dict]) -> List[str]:
        """Identify common root causes."""
        causes = [r.get("cause", "") for r in risks]
        unique_causes = list(set(causes))
        return unique_causes[:3]  # Top 3
    
    def _count_affected_systems(self, risks: List[Dict]) -> int:
        """Count unique affected systems."""
        all_assets = []
        for risk in risks:
            all_assets.extend(risk.get("affected_assets", []))
        return len(set(all_assets))
