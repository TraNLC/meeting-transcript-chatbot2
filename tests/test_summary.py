"""
Test Summary Generator
Generates statistics and summary of all test cases
"""

import yaml
from pathlib import Path
from collections import defaultdict


def analyze_test_cases():
    """Analyze all YAML test cases and generate summary."""
    test_cases_dir = Path(__file__).parent / "test_cases"
    
    total_tests = 0
    tests_by_file_type = defaultdict(int)
    tests_by_category = defaultdict(int)
    tests_by_priority = defaultdict(int)
    file_type_details = {}
    
    yaml_files = list(test_cases_dir.glob("upload_*_tests.yaml"))
    
    print("=" * 80)
    print("TEST SUITE SUMMARY")
    print("=" * 80)
    print()
    
    for yaml_file in sorted(yaml_files):
        with open(yaml_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        test_suite = data.get('test_suite', {})
        test_cases = data.get('test_cases', [])
        
        suite_name = test_suite.get('name', yaml_file.stem)
        file_type = yaml_file.stem.replace('upload_', '').replace('_tests', '').upper()
        
        num_tests = len(test_cases)
        total_tests += num_tests
        tests_by_file_type[file_type] = num_tests
        
        # Collect categories and priorities
        categories = set()
        priorities = defaultdict(int)
        
        for test_case in test_cases:
            category = test_case.get('category', 'general')
            priority = test_case.get('priority', 'medium')
            
            categories.add(category)
            tests_by_category[category] += 1
            priorities[priority] += 1
            tests_by_priority[priority] += 1
        
        file_type_details[file_type] = {
            'name': suite_name,
            'num_tests': num_tests,
            'categories': sorted(categories),
            'priorities': dict(priorities),
            'description': test_suite.get('description', '')
        }
    
    # Print summary by file type
    print("📊 TESTS BY FILE TYPE")
    print("-" * 80)
    print(f"{'File Type':<15} {'Tests':<10} {'Description'}")
    print("-" * 80)
    
    for file_type in sorted(tests_by_file_type.keys()):
        details = file_type_details[file_type]
        print(f"{file_type:<15} {details['num_tests']:<10} {details['description'][:50]}")
    
    print("-" * 80)
    print(f"{'TOTAL':<15} {total_tests:<10}")
    print()
    
    # Print summary by priority
    print("🎯 TESTS BY PRIORITY")
    print("-" * 80)
    for priority in ['critical', 'high', 'medium', 'low']:
        count = tests_by_priority.get(priority, 0)
        percentage = (count / total_tests * 100) if total_tests > 0 else 0
        print(f"{priority.upper():<15} {count:<10} ({percentage:.1f}%)")
    print()
    
    # Print summary by category
    print("📁 TESTS BY CATEGORY")
    print("-" * 80)
    for category, count in sorted(tests_by_category.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_tests * 100) if total_tests > 0 else 0
        print(f"{category:<30} {count:<10} ({percentage:.1f}%)")
    print()
    
    # Print detailed breakdown
    print("📋 DETAILED BREAKDOWN")
    print("=" * 80)
    
    for file_type in sorted(tests_by_file_type.keys()):
        details = file_type_details[file_type]
        print(f"\n{file_type} - {details['name']}")
        print("-" * 80)
        print(f"Total Tests: {details['num_tests']}")
        print(f"Description: {details['description']}")
        print(f"\nPriorities:")
        for priority, count in sorted(details['priorities'].items()):
            print(f"  - {priority}: {count}")
        print(f"\nCategories:")
        for category in details['categories']:
            print(f"  - {category}")
    
    print()
    print("=" * 80)
    print(f"TOTAL TEST CASES: {total_tests}")
    print("=" * 80)
    
    # Generate markdown table
    print("\n\n📝 MARKDOWN TABLE FOR README")
    print("-" * 80)
    print("| File Type | Test Cases | Focus Areas |")
    print("|-----------|-----------|-------------|")
    
    for file_type in sorted(tests_by_file_type.keys()):
        details = file_type_details[file_type]
        focus = ", ".join(details['categories'][:3])
        print(f"| {file_type} | {details['num_tests']} | {focus} |")
    
    print(f"| **Total** | **{total_tests}** | **Comprehensive coverage** |")
    print()


if __name__ == "__main__":
    analyze_test_cases()
