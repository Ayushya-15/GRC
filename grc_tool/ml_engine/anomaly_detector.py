"""
Anomaly Detection Module
Detects abnormal patterns and behaviors in network traffic and system activities.
"""

import logging
import numpy as np
from typing import Dict, List
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

logger = logging.getLogger(__name__)


class AnomalyDetector:
    """
    ML-based anomaly detection for identifying unusual patterns.
    Provides proactive threat detection beyond Nessus capabilities.
    """
    
    def __init__(self, contamination: float = 0.1):
        """
        Initialize Anomaly Detector.
        
        Args:
            contamination: Expected proportion of anomalies
        """
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.baseline_established = False
        logger.info("AnomalyDetector initialized")
    
    def detect_anomalies(self, scan_results: Dict, baseline: Dict = None) -> List[Dict]:
        """
        Detect anomalies in scan results.
        
        Args:
            scan_results: Current scan results
            baseline: Baseline scan for comparison
            
        Returns:
            List of detected anomalies
        """
        logger.info("Detecting anomalies in scan results")
        anomalies = []
        
        for host, host_data in scan_results.get("hosts", {}).items():
            # Extract features
            features = self._extract_anomaly_features(host_data)
            
            # Detect anomaly
            is_anomaly, score = self._is_anomalous(features)
            
            if is_anomaly:
                anomaly_info = {
                    "host": host,
                    "anomaly_score": score,
                    "severity": self._get_anomaly_severity(score),
                    "description": self._describe_anomaly(host_data, features),
                    "type": "Network Anomaly"
                }
                anomalies.append(anomaly_info)
        
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    
    def _extract_anomaly_features(self, host_data: Dict) -> np.ndarray:
        """
        Extract features for anomaly detection.
        
        Args:
            host_data: Host scan data
            
        Returns:
            Feature vector
        """
        features = []
        
        # Port count features
        total_ports = 0
        tcp_ports = 0
        udp_ports = 0
        
        for proto, ports in host_data.get("protocols", {}).items():
            port_count = len(ports)
            total_ports += port_count
            if proto == "tcp":
                tcp_ports = port_count
            elif proto == "udp":
                udp_ports = port_count
        
        features.extend([total_ports, tcp_ports, udp_ports])
        
        # Service diversity
        unique_services = set()
        for proto, ports in host_data.get("protocols", {}).items():
            for port, info in ports.items():
                service = info.get("name", "unknown")
                unique_services.add(service)
        
        features.append(len(unique_services))
        
        # High port usage (ports > 1024)
        high_ports = 0
        low_ports = 0
        for proto, ports in host_data.get("protocols", {}).items():
            for port in ports.keys():
                if port > 1024:
                    high_ports += 1
                else:
                    low_ports += 1
        
        features.extend([high_ports, low_ports])
        
        # Unknown services ratio
        unknown_count = 0
        total_services = 0
        for proto, ports in host_data.get("protocols", {}).items():
            for port, info in ports.items():
                total_services += 1
                if info.get("name", "unknown") == "unknown":
                    unknown_count += 1
        
        unknown_ratio = unknown_count / max(total_services, 1)
        features.append(unknown_ratio)
        
        return np.array(features).reshape(1, -1)
    
    def _is_anomalous(self, features: np.ndarray) -> tuple:
        """
        Check if features represent an anomaly.
        
        Args:
            features: Feature vector
            
        Returns:
            Tuple of (is_anomaly, score)
        """
        # Simple threshold-based detection if model not trained
        if not self.baseline_established:
            score = self._calculate_simple_anomaly_score(features[0])
            is_anomaly = score > 0.6
            return is_anomaly, score
        
        # Use trained model
        prediction = self.model.predict(features)
        score = -self.model.score_samples(features)[0]
        
        return prediction[0] == -1, score
    
    def _calculate_simple_anomaly_score(self, features: np.ndarray) -> float:
        """
        Calculate anomaly score without trained model.
        
        Args:
            features: Feature vector
            
        Returns:
            Anomaly score (0-1)
        """
        # Normalize and score
        total_ports = features[0]
        high_ports = features[4]
        unknown_ratio = features[6]
        
        score = 0.0
        
        # Too many open ports
        if total_ports > 50:
            score += 0.3
        elif total_ports > 20:
            score += 0.2
        
        # Too many high ports
        if high_ports > 30:
            score += 0.2
        
        # High unknown service ratio
        if unknown_ratio > 0.5:
            score += 0.3
        elif unknown_ratio > 0.3:
            score += 0.2
        
        return min(score, 1.0)
    
    def _get_anomaly_severity(self, score: float) -> str:
        """
        Get severity level from anomaly score.
        
        Args:
            score: Anomaly score
            
        Returns:
            Severity level
        """
        if score > 0.8:
            return "CRITICAL"
        elif score > 0.6:
            return "HIGH"
        elif score > 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _describe_anomaly(self, host_data: Dict, features: np.ndarray) -> str:
        """
        Generate description of detected anomaly.
        
        Args:
            host_data: Host data
            features: Feature vector
            
        Returns:
            Anomaly description
        """
        descriptions = []
        
        if features[0][0] > 50:
            descriptions.append(f"Unusually high number of open ports ({int(features[0][0])})")
        
        if features[0][4] > 30:
            descriptions.append(f"Excessive high port usage ({int(features[0][4])} ports)")
        
        if features[0][6] > 0.5:
            descriptions.append(f"High ratio of unknown services ({features[0][6]:.1%})")
        
        if not descriptions:
            descriptions.append("Abnormal network behavior pattern detected")
        
        return "; ".join(descriptions)
    
    def establish_baseline(self, baseline_scans: List[Dict]):
        """
        Establish baseline from normal network scans.
        
        Args:
            baseline_scans: List of baseline scan results
        """
        logger.info("Establishing baseline for anomaly detection")
        
        features_list = []
        for scan in baseline_scans:
            for host, host_data in scan.get("hosts", {}).items():
                features = self._extract_anomaly_features(host_data)
                features_list.append(features[0])
        
        if features_list:
            X = np.array(features_list)
            X_scaled = self.scaler.fit_transform(X)
            self.model.fit(X_scaled)
            self.baseline_established = True
            logger.info("Baseline established successfully")
        else:
            logger.warning("No data available for baseline establishment")
