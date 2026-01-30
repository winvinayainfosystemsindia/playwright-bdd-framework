"""
Configuration Management Module
Implements Singleton pattern for centralized configuration management
"""
import os
import yaml
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """
    Singleton Configuration class for managing application settings.
    Loads environment variables and YAML configuration files.
    """
    _instance: Optional['Config'] = None
    _initialized: bool = False

    def __new__(cls) -> 'Config':
        """Implement Singleton pattern."""
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration only once."""
        if not Config._initialized:
            # Load environment variables from .env file
            env_path = Path(__file__).parent.parent / '.env'
            load_dotenv(dotenv_path=env_path)
            
            # Load basic configuration
            self.environment = os.getenv('ENVIRONMENT', 'dev')
            self.browser = os.getenv('BROWSER', 'chromium')
            self.headless = os.getenv('HEADLESS', 'false').lower() == 'true'
            self.base_url = os.getenv('BASE_URL', 'https://example.com')
            self.timeout = int(os.getenv('TIMEOUT', '30000'))
            self.slow_mo = int(os.getenv('SLOW_MO', '0'))
            self.video = os.getenv('VIDEO', 'on_failure')
            self.screenshot = os.getenv('SCREENSHOT', 'only-on-failure')
            self.log_level = os.getenv('LOG_LEVEL', 'INFO')
            
            # Load environment-specific configuration
            self.env_config = self._load_environment_config()
            
            # Load test data
            self.test_data = self._load_test_data()
            
            # Set paths
            self.root_dir = Path(__file__).parent.parent
            self.reports_dir = self.root_dir / 'reports'
            self.screenshots_dir = self.reports_dir / 'screenshots'
            self.videos_dir = self.reports_dir / 'videos'
            self.allure_results_dir = self.reports_dir / 'allure-results'
            
            # Create necessary directories
            self._create_directories()
            
            Config._initialized = True

    def _load_environment_config(self) -> Dict[str, Any]:
        """
        Load environment-specific configuration from YAML file.
        
        Returns:
            Dict containing environment configuration
        """
        config_path = Path(__file__).parent / 'environments' / f'{self.environment}.yml'
        if config_path.exists():
            with open(config_path, 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def _load_test_data(self) -> Dict[str, Any]:
        """
        Load test data from YAML file.
        
        Returns:
            Dict containing test data
        """
        test_data_path = Path(__file__).parent / 'test_data' / 'users.yml'
        if test_data_path.exists():
            with open(test_data_path, 'r') as file:
                return yaml.safe_load(file) or {}
        return {}

    def _create_directories(self) -> None:
        """Create necessary directories if they don't exist."""
        directories = [
            self.reports_dir,
            self.screenshots_dir,
            self.videos_dir,
            self.allure_results_dir
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)

    def get_base_url(self) -> str:
        """
        Get base URL for the application.
        
        Returns:
            Base URL string
        """
        return self.env_config.get('base_url', self.base_url)

    def get_timeout(self) -> int:
        """
        Get default timeout value.
        
        Returns:
            Timeout in milliseconds
        """
        return self.env_config.get('timeout', self.timeout)

    def get_browser_settings(self) -> Dict[str, Any]:
        """
        Get browser configuration settings.
        
        Returns:
            Dict containing browser settings
        """
        return {
            'browser': self.browser,
            'headless': self.headless,
            'slow_mo': self.slow_mo,
            'timeout': self.get_timeout(),
            'video': self.video,
            'screenshot': self.screenshot
        }

    def get_logging_config(self) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Dict containing logging settings
        """
        return {
            'level': self.log_level,
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }

    def get_test_user(self, user_type: str = 'valid') -> Dict[str, str]:
        """
        Get test user data.
        
        Args:
            user_type: Type of user (valid, invalid, etc.)
            
        Returns:
            Dict containing user data
        """
        return self.test_data.get('users', {}).get(user_type, {})

    def get_env_value(self, key: str, default: Any = None) -> Any:
        """
        Get environment-specific configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.env_config.get(key, default)


# Create a singleton instance
config = Config()
