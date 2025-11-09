"""
Configuration Management Module
"""

import yaml
import json
import os
from typing import Dict, Any


class Config:
    """
    Configuration management for GRC tool.
    """
    
    def __init__(self, config_file: str = None):
        """
        Initialize configuration.
        
        Args:
            config_file: Path to configuration file
        """
        self.config = self._load_default_config()
        
        if config_file and os.path.exists(config_file):
            self._load_config_file(config_file)
    
    def _load_default_config(self) -> Dict[str, Any]:
        """
        Load default configuration.
        
        Returns:
            Default configuration dict
        """
        return {
            "scanning": {
                "timeout": 30,
                "threads": 10,
                "port_range": "1-65535",
                "scan_type": "-sV -sC"
            },
            "ml_engine": {
                "model_path": None,
                "contamination": 0.1,
                "confidence_threshold": 0.7
            },
            "risk_assessment": {
                "risk_appetite": 5.0,
                "framework": "ISO 31000:2018"
            },
            "reporting": {
                "output_dir": "./reports",
                "format": "json",
                "include_raw_data": False
            },
            "logging": {
                "level": "INFO",
                "file": "./logs/grc_tool.log"
            }
        }
    
    def _load_config_file(self, config_file: str):
        """
        Load configuration from file.
        
        Args:
            config_file: Path to config file
        """
        try:
            with open(config_file, 'r') as f:
                if config_file.endswith('.yaml') or config_file.endswith('.yml'):
                    file_config = yaml.safe_load(f)
                elif config_file.endswith('.json'):
                    file_config = json.load(f)
                else:
                    raise ValueError("Unsupported config file format")
                
                # Merge with default config
                self._merge_config(file_config)
        
        except Exception as e:
            print(f"Warning: Failed to load config file: {str(e)}")
    
    def _merge_config(self, file_config: Dict):
        """
        Merge file configuration with defaults.
        
        Args:
            file_config: Configuration from file
        """
        for key, value in file_config.items():
            if key in self.config and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def save(self, filepath: str):
        """
        Save configuration to file.
        
        Args:
            filepath: Path to save configuration
        """
        try:
            with open(filepath, 'w') as f:
                if filepath.endswith('.yaml') or filepath.endswith('.yml'):
                    yaml.dump(self.config, f, default_flow_style=False)
                else:
                    json.dump(self.config, f, indent=2)
        except Exception as e:
            print(f"Error saving configuration: {str(e)}")
