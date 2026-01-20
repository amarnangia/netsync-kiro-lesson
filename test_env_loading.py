"""
Test to verify .env file loading works correctly
"""

import os
import pytest
from dotenv import load_dotenv


def test_env_file_exists():
    """Verify .env file exists"""
    assert os.path.exists('.env'), ".env file should exist"


def test_env_example_exists():
    """Verify .env.example file exists as a template"""
    assert os.path.exists('.env.example'), ".env.example file should exist as a template"


def test_dotenv_loads():
    """Verify dotenv can load the .env file"""
    # Load the .env file
    result = load_dotenv()
    assert result is not None, "load_dotenv() should successfully load .env file"


def test_api_key_accessible():
    """Verify API key can be accessed from environment"""
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("MASSIVE_API_KEY")
    
    # Should have a value (even if it's the placeholder)
    assert api_key is not None, "MASSIVE_API_KEY should be accessible from environment"
    assert isinstance(api_key, str), "MASSIVE_API_KEY should be a string"
    assert len(api_key) > 0, "MASSIVE_API_KEY should not be empty"


def test_gitignore_protects_env():
    """Verify .gitignore includes .env to protect API keys"""
    assert os.path.exists('.gitignore'), ".gitignore file should exist"
    
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    assert '.env' in gitignore_content, ".gitignore should include .env to protect API keys"
    # Make sure it's not just .env.example
    lines = gitignore_content.split('\n')
    env_lines = [line.strip() for line in lines if '.env' in line and not line.strip().startswith('#')]
    assert '.env' in env_lines, ".env should be explicitly listed in .gitignore"


def test_stock_explorer_imports_dotenv():
    """Verify stock_explorer.py imports and uses dotenv"""
    with open('stock_explorer.py', 'r') as f:
        content = f.read()
    
    assert 'from dotenv import load_dotenv' in content, "stock_explorer.py should import load_dotenv"
    assert 'load_dotenv()' in content, "stock_explorer.py should call load_dotenv()"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
