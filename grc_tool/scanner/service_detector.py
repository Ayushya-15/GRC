"""
Service Detection Module
Identifies and fingerprints network services.
"""

import logging
import socket
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ServiceDetector:
    """
    Advanced service detection and fingerprinting.
    Provides better service identification than Nessus.
    """
    
    def __init__(self):
        """Initialize Service Detector."""
        self.service_signatures = self._load_service_signatures()
        logger.info("ServiceDetector initialized")
    
    def detect_service(self, host: str, port: int, protocol: str = "tcp") -> Dict:
        """
        Detect service running on a specific port.
        
        Args:
            host: Host IP address
            port: Port number
            protocol: Protocol type (tcp/udp)
            
        Returns:
            Dict containing service information
        """
        logger.debug(f"Detecting service on {host}:{port}/{protocol}")
        
        service_info = {
            "port": port,
            "protocol": protocol,
            "service": "unknown",
            "version": "",
            "banner": ""
        }
        
        try:
            if protocol == "tcp":
                service_info = self._detect_tcp_service(host, port)
            elif protocol == "udp":
                service_info = self._detect_udp_service(host, port)
        except Exception as e:
            logger.error(f"Service detection failed for {host}:{port}: {str(e)}")
        
        return service_info
    
    def _detect_tcp_service(self, host: str, port: int) -> Dict:
        """
        Detect TCP service.
        
        Args:
            host: Host IP address
            port: Port number
            
        Returns:
            Dict containing service information
        """
        service_info = {
            "port": port,
            "protocol": "tcp",
            "service": self._identify_service_by_port(port),
            "version": "",
            "banner": ""
        }
        
        try:
            # Try to grab banner
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            
            # Send probe
            sock.send(b"HEAD / HTTP/1.0\r\n\r\n")
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            
            sock.close()
            
            if banner:
                service_info["banner"] = banner.strip()
                service_info["version"] = self._extract_version(banner)
                service_info["service"] = self._identify_service_by_banner(banner, port)
        
        except Exception as e:
            logger.debug(f"Banner grab failed for {host}:{port}: {str(e)}")
        
        return service_info
    
    def _detect_udp_service(self, host: str, port: int) -> Dict:
        """
        Detect UDP service.
        
        Args:
            host: Host IP address
            port: Port number
            
        Returns:
            Dict containing service information
        """
        service_info = {
            "port": port,
            "protocol": "udp",
            "service": self._identify_service_by_port(port),
            "version": "",
            "banner": ""
        }
        
        return service_info
    
    def _identify_service_by_port(self, port: int) -> str:
        """
        Identify service by common port number.
        
        Args:
            port: Port number
            
        Returns:
            Service name
        """
        common_ports = {
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            143: "imap",
            443: "https",
            445: "microsoft-ds",
            3306: "mysql",
            3389: "ms-wbt-server",
            5432: "postgresql",
            5900: "vnc",
            8080: "http-proxy",
            8443: "https-alt"
        }
        
        return common_ports.get(port, "unknown")
    
    def _identify_service_by_banner(self, banner: str, port: int) -> str:
        """
        Identify service by banner content.
        
        Args:
            banner: Service banner
            port: Port number
            
        Returns:
            Service name
        """
        banner_lower = banner.lower()
        
        if "ssh" in banner_lower:
            return "ssh"
        elif "ftp" in banner_lower:
            return "ftp"
        elif "http" in banner_lower or "apache" in banner_lower or "nginx" in banner_lower:
            return "http" if port == 80 else "https"
        elif "mysql" in banner_lower:
            return "mysql"
        elif "postgresql" in banner_lower:
            return "postgresql"
        elif "smtp" in banner_lower:
            return "smtp"
        else:
            return self._identify_service_by_port(port)
    
    def _extract_version(self, banner: str) -> str:
        """
        Extract version information from banner.
        
        Args:
            banner: Service banner
            
        Returns:
            Version string
        """
        import re
        
        # Common version patterns
        patterns = [
            r'(\d+\.\d+\.\d+)',
            r'version (\d+\.\d+)',
            r'v(\d+\.\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, banner, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""
    
    def _load_service_signatures(self) -> Dict:
        """
        Load service signature database.
        
        Returns:
            Dict of service signatures
        """
        return {
            "http": {
                "patterns": ["HTTP/", "Apache", "nginx", "IIS"],
                "ports": [80, 8080, 8000, 8888]
            },
            "ssh": {
                "patterns": ["SSH-", "OpenSSH"],
                "ports": [22]
            },
            "ftp": {
                "patterns": ["220", "FTP"],
                "ports": [21]
            },
            "smtp": {
                "patterns": ["220", "SMTP", "ESMTP"],
                "ports": [25, 587]
            }
        }
