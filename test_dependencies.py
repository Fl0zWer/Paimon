#!/usr/bin/env python3
"""
Test script to verify that aiofiles and other critical dependencies can be imported.
This addresses the "No module named 'aiofiles'" error reported in the Dashboard.
"""

import sys
import importlib

def test_import(module_name, description=""):
    """Test if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✅ {module_name} - {description}")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - {description}: {e}")
        return False

def main():
    print("Testing Paimon Discord Bot Dependencies")
    print("=" * 50)
    
    # Test critical dependencies
    tests = [
        ("aiofiles", "Async file operations (main missing dependency)"),
        ("discord", "Discord.py library"),
        ("aiohttp", "Async HTTP client"),
        ("asyncio", "Built-in async support"),
        ("json", "Built-in JSON support"),
        ("sqlite3", "Built-in SQLite support"),
        ("os", "Built-in OS operations"),
        ("sys", "Built-in system operations"),
    ]
    
    # Optional dependencies
    optional_tests = [
        ("pyttsx3", "Text-to-speech engine"),
        ("dotenv", "Environment variables support"),
    ]
    
    print("\nCore Dependencies:")
    core_passed = 0
    for module, desc in tests:
        if test_import(module, desc):
            core_passed += 1
    
    print(f"\nOptional Dependencies:")
    optional_passed = 0
    for module, desc in optional_tests:
        if test_import(module, desc):
            optional_passed += 1
    
    print("\n" + "=" * 50)
    print(f"Core Dependencies: {core_passed}/{len(tests)} passed")
    print(f"Optional Dependencies: {optional_passed}/{len(optional_tests)} passed")
    
    if core_passed == len(tests):
        print("\n✅ All core dependencies are available! The 'aiofiles' issue should be resolved.")
        return 0
    else:
        print(f"\n❌ {len(tests) - core_passed} core dependencies are missing. Please run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())