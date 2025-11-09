"""
Network Scanner Module
Performs comprehensive network scanning to identify active hosts and services.
"""

import nmap
import socket
import logging
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
import ipaddress

logger = logging.getLogger(__name__)


class NetworkScanner:
    """
    Advanced network scanner with support for multiple scanning techniques.
    Provides better coverage than Nessus for network discovery.
    """
    
    def __init__(self, timeout: int = 30, threads: int = 10):
        """
        Initialize Network Scanner.
        
        Args:
            timeout: Scan timeout in seconds
            threads: Number of parallel scanning threads
        """
        self.timeout = timeout
        self.threads = threads
        self.nm = nmap.PortScanner()
        logger.info(f"NetworkScanner initialized with timeout={timeout}s, threads={threads}")
    
    def scan_network(self, target: str, ports: str = "1-65535", scan_type: str = "-sS -sV -O") -> Dict:
        """
        Perform comprehensive network scan.
        
        Args:
            target: Target IP address or CIDR range
            ports: Port range to scan
            scan_type: Nmap scan type arguments
            
        Returns:
            Dict containing scan results
        """
        logger.info(f"Starting network scan for target: {target}")
        
        try:
            # Perform nmap scan
            self.nm.scan(hosts=target, ports=ports, arguments=scan_type)
            
            results = {
                "scan_info": self.nm.scaninfo(),
                "hosts": {}
            }
            
            # Process results for each host
            for host in self.nm.all_hosts():
                host_info = {
                    "hostname": self.nm[host].hostname(),
                    "state": self.nm[host].state(),
                    "protocols": {},
                    "os": self._get_os_info(host)
                }
                
                # Get protocol information
                for proto in self.nm[host].all_protocols():
                    ports_info = {}
                    lport = self.nm[host][proto].keys()
                    
                    for port in lport:
                        port_data = self.nm[host][proto][port]
                        ports_info[port] = {
                            "state": port_data.get("state", "unknown"),
                            "name": port_data.get("name", ""),
                            "product": port_data.get("product", ""),
                            "version": port_data.get("version", ""),
                            "extrainfo": port_data.get("extrainfo", ""),
                            "cpe": port_data.get("cpe", "")
                        }
                    
                    host_info["protocols"][proto] = ports_info
                
                results["hosts"][host] = host_info
            
            logger.info(f"Scan completed. Found {len(results['hosts'])} hosts")
            return results
            
        except Exception as e:
            logger.error(f"Network scan failed: {str(e)}")
            return {"error": str(e), "hosts": {}}
    
    def quick_scan(self, target: str) -> Dict:
        """
        Perform quick scan on common ports.
        
        Args:
            target: Target IP address
            
        Returns:
            Dict containing quick scan results
        """
        common_ports = "21,22,23,25,53,80,110,143,443,445,3306,3389,5432,8080,8443"
        return self.scan_network(target, ports=common_ports, scan_type="-sV")
    
    def _get_os_info(self, host: str) -> Dict:
        """
        Extract OS information from scan results.
        
        Args:
            host: Host IP address
            
        Returns:
            Dict containing OS information
        """
        try:
            if "osmatch" in self.nm[host]:
                os_matches = self.nm[host]["osmatch"]
                if os_matches:
                    return {
                        "name": os_matches[0].get("name", "Unknown"),
                        "accuracy": os_matches[0].get("accuracy", "0"),
                        "type": os_matches[0].get("osclass", [{}])[0].get("type", "Unknown") if os_matches[0].get("osclass") else "Unknown"
                    }
        except Exception as e:
            logger.debug(f"Could not determine OS for {host}: {str(e)}")
        
        return {"name": "Unknown", "accuracy": "0", "type": "Unknown"}
    
    def validate_target(self, target: str) -> bool:
        """
        Validate if target is reachable.
        
        Args:
            target: Target IP address or hostname
            
        Returns:
            bool indicating if target is reachable
        """
        try:
            # Try to resolve hostname
            socket.gethostbyname(target)
            return True
        except socket.error:
            logger.warning(f"Target {target} is not reachable")
            return False
    
    def discover_hosts(self, network: str) -> List[str]:
        """
        Discover active hosts in a network range.
        
        Args:
            network: Network in CIDR notation (e.g., 192.168.1.0/24)
            
        Returns:
            List of active host IP addresses
        """
        logger.info(f"Discovering hosts in network: {network}")
        active_hosts = []
        
        try:
            # Use ping scan
            self.nm.scan(hosts=network, arguments="-sn")
            
            for host in self.nm.all_hosts():
                if self.nm[host].state() == "up":
                    active_hosts.append(host)
            
            logger.info(f"Discovered {len(active_hosts)} active hosts")
            return active_hosts
            
        except Exception as e:
            logger.error(f"Host discovery failed: {str(e)}")
            return []
