#!/usr/bin/env python3
"""
Test script to verify that aiofiles and other critical dependencies can be imported.
This addresses the "No module named 'aiofiles'" error reported in the Dashboard.

Improvements:
- Better structured test organization
- More informative output
- Cleaner code with helper functions
"""

import sys
import importlib
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DependencyTester:
    """Manages testing of Python dependencies."""
    
    def __init__(self):
        self.results = {
            'core': {'passed': 0, 'failed': 0, 'tests': []},
            'optional': {'passed': 0, 'failed': 0, 'tests': []}
        }
    
    def test_import(self, module_name: str, description: str = "") -> bool:
        """
        Test if a module can be imported.
        
        Args:
            module_name: Name of the module to import
            description: Human-readable description
            
        Returns:
            bool: True if import successful, False otherwise
        """
        try:
            importlib.import_module(module_name)
            print(f"✅ {module_name:20s} - {description}")
            return True
        except ImportError as e:
            print(f"❌ {module_name:20s} - {description}: {e}")
            return False
    
    def run_core_tests(self):
        """Run tests for core dependencies."""
        print("\n" + "=" * 60)
        print("Core Dependencies:")
        print("=" * 60)
        
        core_tests = [
            ("aiofiles", "Async file operations (main missing dependency)"),
            ("discord", "Discord.py library"),
            ("aiohttp", "Async HTTP client"),
            ("asyncio", "Built-in async support"),
            ("json", "Built-in JSON support"),
            ("sqlite3", "Built-in SQLite support"),
            ("os", "Built-in OS operations"),
            ("sys", "Built-in system operations"),
        ]
        
        for module, desc in core_tests:
            result = self.test_import(module, desc)
            self.results['core']['tests'].append((module, desc, result))
            if result:
                self.results['core']['passed'] += 1
            else:
                self.results['core']['failed'] += 1
    
    def run_optional_tests(self):
        """Run tests for optional dependencies."""
        print("\n" + "=" * 60)
        print("Optional Dependencies:")
        print("=" * 60)
        
        optional_tests = [
            ("pyttsx3", "Text-to-speech engine"),
            ("dotenv", "Environment variables support"),
            ("sqlalchemy", "Database ORM"),
            ("flask", "Web framework"),
        ]
        
        for module, desc in optional_tests:
            result = self.test_import(module, desc)
            self.results['optional']['tests'].append((module, desc, result))
            if result:
                self.results['optional']['passed'] += 1
            else:
                self.results['optional']['failed'] += 1
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        
        core_total = self.results['core']['passed'] + self.results['core']['failed']
        optional_total = self.results['optional']['passed'] + self.results['optional']['failed']
        
        print(f"Core Dependencies:     {self.results['core']['passed']}/{core_total} passed")
        print(f"Optional Dependencies: {self.results['optional']['passed']}/{optional_total} passed")
        
        if self.results['core']['failed'] == 0:
            print("\n✅ All core dependencies are available!")
            print("   The 'aiofiles' issue should be resolved.")
            return True
        else:
            print(f"\n❌ {self.results['core']['failed']} core dependencies are missing.")
            print("   Please run: pip install -r requirements.txt")
            return False


def main() -> int:
    """
    Main entry point for dependency testing.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("=" * 60)
    print("Testing Paimon Discord Bot Dependencies")
    print("=" * 60)
    
    tester = DependencyTester()
    
    # Run tests
    tester.run_core_tests()
    tester.run_optional_tests()
    
    # Print summary
    success = tester.print_summary()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())