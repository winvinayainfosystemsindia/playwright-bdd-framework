"""
Report Helper Module
Provides utilities for Allure reporting and custom report generation
"""
import allure
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from config.config import config
from utils.logger import Logger


logger = Logger.get_logger(__name__)


class ReportHelper:
    """
    Report Helper class for Allure reporting utilities.
    Provides methods to enhance test reports with attachments and metadata.
    """
    
    @staticmethod
    def attach_text(text: str, name: str = "Text Attachment") -> None:
        """
        Attach text to Allure report.
        
        Args:
            text: Text content to attach
            name: Attachment name
        """
        try:
            allure.attach(
                text,
                name=name,
                attachment_type=allure.attachment_type.TEXT
            )
            logger.debug(f"Text attached to report: {name}")
        except Exception as e:
            logger.error(f"Failed to attach text: {str(e)}")
    
    @staticmethod
    def attach_json(data: Dict[str, Any], name: str = "JSON Data") -> None:
        """
        Attach JSON data to Allure report.
        
        Args:
            data: Dictionary to attach as JSON
            name: Attachment name
        """
        try:
            json_str = json.dumps(data, indent=2, ensure_ascii=False)
            allure.attach(
                json_str,
                name=name,
                attachment_type=allure.attachment_type.JSON
            )
            logger.debug(f"JSON attached to report: {name}")
        except Exception as e:
            logger.error(f"Failed to attach JSON: {str(e)}")
    
    @staticmethod
    def attach_html(html: str, name: str = "HTML Content") -> None:
        """
        Attach HTML content to Allure report.
        
        Args:
            html: HTML content
            name: Attachment name
        """
        try:
            allure.attach(
                html,
                name=name,
                attachment_type=allure.attachment_type.HTML
            )
            logger.debug(f"HTML attached to report: {name}")
        except Exception as e:
            logger.error(f"Failed to attach HTML: {str(e)}")
    
    @staticmethod
    def attach_file(file_path: str, name: Optional[str] = None) -> None:
        """
        Attach file to Allure report.
        
        Args:
            file_path: Path to file
            name: Attachment name (uses filename if not provided)
        """
        try:
            path = Path(file_path)
            if not path.exists():
                logger.error(f"File not found: {file_path}")
                return
            
            attachment_name = name or path.name
            
            with open(path, 'rb') as file:
                allure.attach(
                    file.read(),
                    name=attachment_name,
                    attachment_type=allure.attachment_type.TEXT
                )
            
            logger.debug(f"File attached to report: {attachment_name}")
        except Exception as e:
            logger.error(f"Failed to attach file: {str(e)}")
    
    @staticmethod
    def add_environment_info(env_info: Dict[str, str]) -> None:
        """
        Add environment information to Allure report.
        
        Args:
            env_info: Dictionary containing environment information
        """
        try:
            env_file = config.allure_results_dir / 'environment.properties'
            
            with open(env_file, 'w') as f:
                for key, value in env_info.items():
                    f.write(f"{key}={value}\n")
            
            logger.info("Environment information added to Allure report")
        except Exception as e:
            logger.error(f"Failed to add environment info: {str(e)}")
    
    @staticmethod
    def add_step(step_name: str) -> None:
        """
        Add a step to Allure report.
        
        Args:
            step_name: Name of the step
        """
        allure.dynamic.step(step_name)
    
    @staticmethod
    def add_description(description: str) -> None:
        """
        Add description to test in Allure report.
        
        Args:
            description: Test description
        """
        allure.dynamic.description(description)
    
    @staticmethod
    def add_title(title: str) -> None:
        """
        Add title to test in Allure report.
        
        Args:
            title: Test title
        """
        allure.dynamic.title(title)
    
    @staticmethod
    def add_severity(severity: str) -> None:
        """
        Add severity to test in Allure report.
        
        Args:
            severity: Severity level (blocker, critical, normal, minor, trivial)
        """
        allure.dynamic.severity(severity)
    
    @staticmethod
    def add_feature(feature: str) -> None:
        """
        Add feature label to test.
        
        Args:
            feature: Feature name
        """
        allure.dynamic.feature(feature)
    
    @staticmethod
    def add_story(story: str) -> None:
        """
        Add story label to test.
        
        Args:
            story: Story name
        """
        allure.dynamic.story(story)
    
    @staticmethod
    def add_link(url: str, name: Optional[str] = None) -> None:
        """
        Add link to test in Allure report.
        
        Args:
            url: URL to link
            name: Link name
        """
        allure.dynamic.link(url, name=name)

    @staticmethod
    def generate_csv_report(results: List[Dict[str, Any]]) -> str:
        """
        Generate a CSV report from test results.
        
        Args:
            results: List of dictionaries containing test results
            
        Returns:
            Path to the generated CSV file
        """
        import csv
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        csv_file = config.reports_dir / f"test_results_{timestamp}.csv"
        
        try:
            with open(csv_file, 'w', newline='', encoding='utf-8') as f:
                fieldnames = ['test_name', 'status', 'duration', 'error_message']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                
                writer.writeheader()
                for result in results:
                    writer.writerow({
                        'test_name': result.get('name', 'N/A'),
                        'status': result.get('status', 'N/A'),
                        'duration': f"{result.get('duration', 0):.2f}s",
                        'error_message': result.get('error', '').replace('\n', ' ')
                    })
            
            logger.info(f"CSV report generated: {csv_file}")
            return str(csv_file)
        except Exception as e:
            logger.error(f"Failed to generate CSV report: {str(e)}")
            return ""


def allure_step(step_name: str):
    """
    Decorator for marking functions as Allure steps.
    
    Args:
        step_name: Name of the step
        
    Returns:
        Decorated function
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            with allure.step(step_name):
                return func(*args, **kwargs)
        return wrapper
    return decorator


def allure_severity(severity: str):
    """
    Decorator for adding severity to tests.
    
    Args:
        severity: Severity level
        
    Returns:
        Decorated function
    """
    def decorator(func):
        return allure.severity(severity)(func)
    return decorator


def allure_feature(feature: str):
    """
    Decorator for adding feature label to tests.
    
    Args:
        feature: Feature name
        
    Returns:
        Decorated function
    """
    def decorator(func):
        return allure.feature(feature)(func)
    return decorator


def allure_story(story: str):
    """
    Decorator for adding story label to tests.
    
    Args:
        story: Story name
        
    Returns:
        Decorated function
    """
    def decorator(func):
        return allure.story(story)(func)
    return decorator


# Create singleton instance
report_helper = ReportHelper()
