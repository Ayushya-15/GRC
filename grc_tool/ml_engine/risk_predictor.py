"""
Risk Prediction Module
Predicts future security risks using ML techniques.
"""

import logging
import numpy as np
from typing import Dict, List
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class RiskPredictor:
    """
    ML-based risk prediction for proactive security management.
    Provides predictive capabilities beyond Nessus.
    """
    
    def __init__(self):
        """Initialize Risk Predictor."""
        self.risk_history = []
        logger.info("RiskPredictor initialized")
    
    def predict_future_risks(self, current_risks: List[Dict], historical_data: List[Dict] = None) -> Dict:
        """
        Predict future security risks.
        
        Args:
            current_risks: Current identified risks
            historical_data: Historical risk data
            
        Returns:
            Dict containing risk predictions
        """
        logger.info("Predicting future security risks")
        
        # Calculate risk trends
        risk_trend = self._analyze_risk_trend(current_risks, historical_data)
        
        # Predict likelihood of exploitation
        exploitation_risk = self._predict_exploitation_likelihood(current_risks)
        
        # Identify emerging threats
        emerging_threats = self._identify_emerging_threats(current_risks)
        
        # Calculate time-to-exploit predictions
        tte_predictions = self._predict_time_to_exploit(current_risks)
        
        prediction = {
            "prediction_date": datetime.now().isoformat(),
            "risk_trend": risk_trend,
            "exploitation_risk": exploitation_risk,
            "emerging_threats": emerging_threats,
            "time_to_exploit": tte_predictions,
            "overall_risk_level": self._calculate_overall_risk(current_risks),
            "recommendations": self._generate_predictive_recommendations(current_risks, risk_trend)
        }
        
        logger.info("Risk prediction completed")
        return prediction
    
    def _analyze_risk_trend(self, current_risks: List[Dict], historical_data: List[Dict] = None) -> Dict:
        """
        Analyze risk trends over time.
        
        Args:
            current_risks: Current risks
            historical_data: Historical risk data
            
        Returns:
            Risk trend analysis
        """
        current_score = self._calculate_aggregate_risk_score(current_risks)
        
        if historical_data and len(historical_data) > 0:
            historical_scores = [self._calculate_aggregate_risk_score(h.get("risks", [])) for h in historical_data]
            avg_historical = np.mean(historical_scores)
            
            if current_score > avg_historical * 1.2:
                trend = "INCREASING"
            elif current_score < avg_historical * 0.8:
                trend = "DECREASING"
            else:
                trend = "STABLE"
        else:
            trend = "UNKNOWN"
        
        return {
            "trend": trend,
            "current_score": current_score,
            "change_rate": self._calculate_change_rate(current_risks, historical_data)
        }
    
    def _predict_exploitation_likelihood(self, risks: List[Dict]) -> Dict:
        """
        Predict likelihood of vulnerability exploitation.
        
        Args:
            risks: List of identified risks
            
        Returns:
            Exploitation likelihood prediction
        """
        high_likelihood = []
        medium_likelihood = []
        low_likelihood = []
        
        for risk in risks:
            severity = risk.get("severity", "LOW")
            cvss_score = risk.get("cvss_score", 0)
            
            # Calculate likelihood based on severity and CVSS
            if severity == "CRITICAL" or cvss_score >= 9.0:
                likelihood = "HIGH"
                time_window = "24-48 hours"
                high_likelihood.append({
                    "risk": risk.get("type", "Unknown"),
                    "likelihood": likelihood,
                    "expected_timeframe": time_window
                })
            elif severity == "HIGH" or cvss_score >= 7.0:
                likelihood = "MEDIUM"
                time_window = "1-7 days"
                medium_likelihood.append({
                    "risk": risk.get("type", "Unknown"),
                    "likelihood": likelihood,
                    "expected_timeframe": time_window
                })
            else:
                likelihood = "LOW"
                time_window = "30+ days"
                low_likelihood.append({
                    "risk": risk.get("type", "Unknown"),
                    "likelihood": likelihood,
                    "expected_timeframe": time_window
                })
        
        return {
            "high_likelihood_exploits": high_likelihood,
            "medium_likelihood_exploits": medium_likelihood,
            "low_likelihood_exploits": low_likelihood,
            "total_at_risk": len(risks)
        }
    
    def _identify_emerging_threats(self, risks: List[Dict]) -> List[Dict]:
        """
        Identify emerging threat patterns.
        
        Args:
            risks: Current risks
            
        Returns:
            List of emerging threats
        """
        emerging = []
        
        # Analyze risk patterns
        risk_types = {}
        for risk in risks:
            risk_type = risk.get("type", "Unknown")
            risk_types[risk_type] = risk_types.get(risk_type, 0) + 1
        
        # Identify clusters of similar risks
        for risk_type, count in risk_types.items():
            if count >= 3:  # Threshold for emerging threat
                emerging.append({
                    "threat_type": risk_type,
                    "occurrence_count": count,
                    "severity": "HIGH",
                    "description": f"Multiple instances of {risk_type} detected across network"
                })
        
        return emerging
    
    def _predict_time_to_exploit(self, risks: List[Dict]) -> Dict:
        """
        Predict time until potential exploitation.
        
        Args:
            risks: List of risks
            
        Returns:
            Time-to-exploit predictions
        """
        predictions = {}
        
        for risk in risks:
            severity = risk.get("severity", "LOW")
            risk_id = risk.get("type", "Unknown")
            
            # Estimate time based on severity
            if severity == "CRITICAL":
                tte = "< 24 hours"
                priority = 1
            elif severity == "HIGH":
                tte = "1-7 days"
                priority = 2
            elif severity == "MEDIUM":
                tte = "7-30 days"
                priority = 3
            else:
                tte = "30+ days"
                priority = 4
            
            predictions[risk_id] = {
                "time_to_exploit": tte,
                "priority": priority,
                "confidence": 0.75
            }
        
        return predictions
    
    def _calculate_aggregate_risk_score(self, risks: List[Dict]) -> float:
        """
        Calculate aggregate risk score.
        
        Args:
            risks: List of risks
            
        Returns:
            Aggregate score
        """
        if not risks:
            return 0.0
        
        total = sum(risk.get("cvss_score", 5.0) for risk in risks)
        return total / len(risks)
    
    def _calculate_change_rate(self, current_risks: List[Dict], historical_data: List[Dict] = None) -> str:
        """
        Calculate rate of change in risks.
        
        Args:
            current_risks: Current risks
            historical_data: Historical data
            
        Returns:
            Change rate description
        """
        if not historical_data:
            return "N/A"
        
        current_count = len(current_risks)
        historical_avg = np.mean([len(h.get("risks", [])) for h in historical_data])
        
        change_pct = ((current_count - historical_avg) / max(historical_avg, 1)) * 100
        
        if abs(change_pct) < 10:
            return "Minimal change"
        elif change_pct > 0:
            return f"Increased by {change_pct:.1f}%"
        else:
            return f"Decreased by {abs(change_pct):.1f}%"
    
    def _calculate_overall_risk(self, risks: List[Dict]) -> str:
        """
        Calculate overall risk level.
        
        Args:
            risks: List of risks
            
        Returns:
            Overall risk level
        """
        if not risks:
            return "LOW"
        
        critical_count = sum(1 for r in risks if r.get("severity") == "CRITICAL")
        high_count = sum(1 for r in risks if r.get("severity") == "HIGH")
        
        if critical_count > 0:
            return "CRITICAL"
        elif high_count > 2:
            return "HIGH"
        elif high_count > 0 or len(risks) > 5:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _generate_predictive_recommendations(self, risks: List[Dict], trend: Dict) -> List[str]:
        """
        Generate recommendations based on predictions.
        
        Args:
            risks: Current risks
            trend: Risk trend data
            
        Returns:
            List of recommendations
        """
        recommendations = []
        
        if trend.get("trend") == "INCREASING":
            recommendations.append("Risk levels are increasing - immediate action required")
            recommendations.append("Schedule emergency security review within 24 hours")
        
        critical_risks = [r for r in risks if r.get("severity") == "CRITICAL"]
        if critical_risks:
            recommendations.append(f"Address {len(critical_risks)} critical risks immediately")
        
        if len(risks) > 10:
            recommendations.append("High volume of risks detected - consider systematic remediation approach")
        
        recommendations.append("Implement continuous monitoring and automated patching")
        recommendations.append("Conduct regular vulnerability assessments")
        
        return recommendations
