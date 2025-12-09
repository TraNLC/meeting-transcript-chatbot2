"""
Batch Test Runner
Runs tests from test_history_page_comprehensive.py in specific ranges.

Usage: python tests/run_batch.py <start_id> <end_id>
Example: python tests/run_batch.py 1 10
"""

import sys
import os
sys.path.append(os.getcwd())
import unittest
# Import directly from the file assuming we run from root
from tests.test_history_page_comprehensive import TestHistoryPageEasy, TestHistoryPageMedium, TestHistoryPageHard

def run_batch(start_id, end_id):
    print("\n" + "="*70)
    print(f"RUNNING BATCH TESTS: {start_id} to {end_id}")
    print("="*70 + "\n")

    test_classes = [TestHistoryPageEasy, TestHistoryPageMedium, TestHistoryPageHard]
    
    passed = 0
    failed = 0
    total_run = 0

    for test_id in range(start_id, end_id + 1):
        # Format test ID (e.g., 1 -> "test_01")
        test_prefix = f"test_{test_id:02d}_"
        
        found = False
        for cls in test_classes:
            # Find method strictly starting with the prefix
            methods = [m for m in dir(cls) if m.startswith(test_prefix)]
            if methods:
                method_name = methods[0]
                instance = cls()
                try:
                    # Run the test method
                    getattr(instance, method_name)()
                    passed += 1
                except Exception as e:
                    print(f"✗ Test {test_id} FAILED: {e}")
                    failed += 1
                found = True
                total_run += 1
                break
        
        if not found:
            print(f"⚠ Test {test_id} NOT FOUND")

    print("\n" + "-"*70)
    print(f"BATCH SUMMARY: {passed} Passed, {failed} Failed (Total: {total_run})")
    print("-"*70 + "\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python tests/run_batch.py <start> <end>")
    else:
        run_batch(int(sys.argv[1]), int(sys.argv[2]))
