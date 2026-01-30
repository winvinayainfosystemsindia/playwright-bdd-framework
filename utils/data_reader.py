"""
Data Reader Module
Provides utilities for reading test data from various sources
"""
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
from faker import Faker
from utils.logger import Logger


logger = Logger.get_logger(__name__)
fake = Faker()


class DataReader:
    """
    Data Reader class for loading test data from files.
    Supports YAML and JSON formats.
    """
    
    @staticmethod
    def read_yaml(file_path: str) -> Dict[str, Any]:
        """
        Read data from YAML file.
        
        Args:
            file_path: Path to YAML file
            
        Returns:
            Dict containing YAML data
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"YAML file not found: {file_path}")
                return {}
            
            with open(path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                logger.info(f"Successfully loaded YAML file: {file_path}")
                return data or {}
                
        except Exception as e:
            logger.error(f"Failed to read YAML file {file_path}: {str(e)}")
            return {}
    
    @staticmethod
    def read_json(file_path: str) -> Dict[str, Any]:
        """
        Read data from JSON file.
        
        Args:
            file_path: Path to JSON file
            
        Returns:
            Dict containing JSON data
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"JSON file not found: {file_path}")
                return {}
            
            with open(path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Successfully loaded JSON file: {file_path}")
                return data
                
        except Exception as e:
            logger.error(f"Failed to read JSON file {file_path}: {str(e)}")
            return {}
    
    @staticmethod
    def write_yaml(file_path: str, data: Dict[str, Any]) -> bool:
        """
        Write data to YAML file.
        
        Args:
            file_path: Path to YAML file
            data: Data to write
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                yaml.dump(data, file, default_flow_style=False, allow_unicode=True)
                logger.info(f"Successfully wrote YAML file: {file_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to write YAML file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def write_json(file_path: str, data: Dict[str, Any], indent: int = 2) -> bool:
        """
        Write data to JSON file.
        
        Args:
            file_path: Path to JSON file
            data: Data to write
            indent: JSON indentation level
            
        Returns:
            True if successful, False otherwise
        """
        try:
            path = Path(file_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=indent, ensure_ascii=False)
                logger.info(f"Successfully wrote JSON file: {file_path}")
                return True
                
        except Exception as e:
            logger.error(f"Failed to write JSON file {file_path}: {str(e)}")
            return False


class FakeDataGenerator:
    """
    Fake Data Generator using Faker library.
    Provides methods to generate realistic test data.
    """
    
    def __init__(self, locale: str = 'en_US'):
        """
        Initialize Fake Data Generator.
        
        Args:
            locale: Locale for generated data
        """
        self.fake = Faker(locale)
    
    def generate_user(self) -> Dict[str, str]:
        """
        Generate fake user data.
        
        Returns:
            Dict containing user information
        """
        return {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name(),
            'email': self.fake.email(),
            'password': self.fake.password(length=12, special_chars=True, digits=True, upper_case=True),
            'phone': self.fake.phone_number(),
            'address': self.fake.address(),
            'city': self.fake.city(),
            'country': self.fake.country(),
            'zipcode': self.fake.zipcode()
        }
    
    def generate_email(self) -> str:
        """Generate fake email address."""
        return self.fake.email()
    
    def generate_password(self, length: int = 12) -> str:
        """
        Generate fake password.
        
        Args:
            length: Password length
            
        Returns:
            Generated password
        """
        return self.fake.password(length=length, special_chars=True, digits=True, upper_case=True)
    
    def generate_name(self) -> Dict[str, str]:
        """
        Generate fake name.
        
        Returns:
            Dict with first_name and last_name
        """
        return {
            'first_name': self.fake.first_name(),
            'last_name': self.fake.last_name()
        }
    
    def generate_phone(self) -> str:
        """Generate fake phone number."""
        return self.fake.phone_number()
    
    def generate_address(self) -> Dict[str, str]:
        """
        Generate fake address.
        
        Returns:
            Dict containing address information
        """
        return {
            'street': self.fake.street_address(),
            'city': self.fake.city(),
            'state': self.fake.state(),
            'country': self.fake.country(),
            'zipcode': self.fake.zipcode()
        }
    
    def generate_company(self) -> str:
        """Generate fake company name."""
        return self.fake.company()
    
    def generate_text(self, max_chars: int = 200) -> str:
        """
        Generate fake text.
        
        Args:
            max_chars: Maximum number of characters
            
        Returns:
            Generated text
        """
        return self.fake.text(max_nb_chars=max_chars)


# Create singleton instances
data_reader = DataReader()
fake_data_generator = FakeDataGenerator()
