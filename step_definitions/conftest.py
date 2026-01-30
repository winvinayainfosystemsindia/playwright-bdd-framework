"""
Step Definitions Conftest
Configuration and fixtures for step definitions
"""
import pytest
from pytest_bdd import given, when, then, parsers
from typing import Dict, Any


# Shared context for scenarios
@pytest.fixture
def context() -> Dict[str, Any]:
    """
    Shared context dictionary for storing data between steps.
    
    Returns:
        Empty dictionary for context
    """
    return {}
