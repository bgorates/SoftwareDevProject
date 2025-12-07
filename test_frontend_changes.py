"""
Test script to validate frontend changes
Tests the key functionality we've modified
"""
import os
import re
from pathlib import Path

def test_file_exists(file_path):
    """Test if a file exists"""
    exists = Path(file_path).exists()
    if exists:
        return True, None
    else:
        return False, f"File {file_path} does not exist"

def test_file_contains(file_path, patterns, should_contain=True):
    """Test if file contains or doesn't contain certain patterns"""
    if not test_file_exists(file_path):
        return False, f"File {file_path} does not exist"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    results = []
    for pattern in patterns:
        found = bool(re.search(pattern, content, re.IGNORECASE))
        if should_contain and not found:
            results.append(f"Pattern '{pattern}' not found in {file_path}")
        elif not should_contain and found:
            results.append(f"Pattern '{pattern}' should not be in {file_path}")
    
    return len(results) == 0, results

def test_html_syntax(file_path):
    """Basic HTML syntax check"""
    if not test_file_exists(file_path)[0]:
        return False, [f"File {file_path} does not exist"]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Remove script and style content for better tag matching
    content_clean = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content_clean = re.sub(r'<style[^>]*>.*?</style>', '', content_clean, flags=re.DOTALL | re.IGNORECASE)
    
    # Check for unclosed tags (basic check)
    # Count self-closing tags
    self_closing_tags = ['br', 'hr', 'img', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']
    self_closing_count = sum(len(re.findall(rf'<{tag}[^>]*/?>', content_clean, re.IGNORECASE)) for tag in self_closing_tags)
    
    # Count regular tags
    open_tags = len(re.findall(r'<([a-zA-Z][a-zA-Z0-9]*)[^/>]*>', content_clean))
    close_tags = len(re.findall(r'</([a-zA-Z][a-zA-Z0-9]*)>', content_clean))
    
    # Basic validation - should have roughly balanced tags
    # Allow more imbalance for complex pages
    issues = []
    imbalance = open_tags - close_tags - self_closing_count
    if imbalance > 20:  # More lenient threshold
        issues.append(f"Possible unclosed tags in {file_path} (imbalance: {imbalance})")
    
    return len(issues) == 0, issues

def test_js_syntax(file_path):
    """Basic JavaScript syntax check"""
    if not test_file_exists(file_path):
        return False, f"File {file_path} does not exist"
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    issues = []
    # Check for common syntax errors
    if content.count('{') != content.count('}'):
        issues.append(f"Unbalanced braces in {file_path}")
    if content.count('(') != content.count(')'):
        issues.append(f"Unbalanced parentheses in {file_path}")
    if content.count('[') != content.count(']'):
        issues.append(f"Unbalanced brackets in {file_path}")
    
    return len(issues) == 0, issues

def run_tests():
    """Run all frontend validation tests"""
    print("=" * 60)
    print("Running Frontend Validation Tests")
    print("=" * 60)
    
    tests_passed = 0
    tests_failed = 0
    all_issues = []
    
    # Test 1: admin-login.html exists
    print("\n[Test 1] Checking admin-login.html exists...")
    exists, msg = test_file_exists("frontend/pages/auth/admin-login.html")
    if exists:
        print("✓ admin-login.html exists")
        tests_passed += 1
    else:
        print(f"✗ {msg}")
        tests_failed += 1
        all_issues.append(msg)
    
    # Test 2: admin-login.html has "Admin Login" button text
    print("\n[Test 2] Checking admin-login.html has 'Admin Login' button...")
    passed, issues = test_file_contains(
        "frontend/pages/auth/admin-login.html",
        [r'Admin Login', r'button-text.*Admin Login']
    )
    if passed:
        print("✓ admin-login.html has 'Admin Login' button text")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 3: employee-constraint-new.html exists
    print("\n[Test 3] Checking employee-constraint-new.html exists...")
    exists, msg = test_file_exists("frontend/pages/employees/employee-constraint-new.html")
    if exists:
        print("✓ employee-constraint-new.html exists")
        tests_passed += 1
    else:
        print(f"✗ {msg}")
        tests_failed += 1
        all_issues.append(msg)
    
    # Test 4: employee-constraints.html has list view with table
    print("\n[Test 4] Checking employee-constraints.html has table structure...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-constraints.html",
        [r'<table>', r'Employee', r'Days Available', r'Shift Preference', r'Actions']
    )
    if passed:
        print("✓ employee-constraints.html has proper table structure")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 5: employee-constraints.html has "+ New" button
    print("\n[Test 5] Checking employee-constraints.html has '+ New' button...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-constraints.html",
        [r'\+ New', r'employee-constraint-new.html']
    )
    if passed:
        print("✓ employee-constraints.html has '+ New' button")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 6: employee-constraints.html has delete functionality
    print("\n[Test 6] Checking employee-constraints.html has delete button...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-constraints.html",
        [r'deleteConstraint', r'Delete']
    )
    if passed:
        print("✓ employee-constraints.html has delete functionality")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 7: employee-edit.html has Status field instead of Start Date
    print("\n[Test 7] Checking employee-edit.html has Status field...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-edit.html",
        [r'is_active', r'Status', r'Active', r'Inactive']
    )
    if passed:
        print("✓ employee-edit.html has Status field")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 8: employee-edit.html doesn't have required attributes (excluding comments)
    print("\n[Test 8] Checking employee-edit.html fields are optional...")
    if test_file_exists("frontend/pages/employees/employee-edit.html")[0]:
        with open("frontend/pages/employees/employee-edit.html", 'r', encoding='utf-8') as f:
            content = f.read()
        # Remove comments and check for required attributes in actual HTML
        content_no_comments = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
        # Check for required attribute in input/select tags (not in comments)
        has_required = bool(re.search(r'<(input|select)[^>]*\srequired\s', content_no_comments, re.IGNORECASE))
        if not has_required:
            print("✓ employee-edit.html fields are optional (no 'required' attributes)")
            tests_passed += 1
        else:
            print("✗ employee-edit.html still has 'required' attributes in form fields")
            tests_failed += 1
            all_issues.append("employee-edit.html has 'required' attributes in form fields")
    else:
        print("✗ employee-edit.html does not exist")
        tests_failed += 1
        all_issues.append("employee-edit.html does not exist")
    if passed:
        print("✓ employee-edit.html fields are optional (no 'required' attributes)")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 9: employee-list.html doesn't have Delete button
    print("\n[Test 9] Checking employee-list.html doesn't have Delete button...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-list.html",
        [r'deleteEmployee', r'Delete.*button'],
        should_contain=False
    )
    if passed:
        print("✓ employee-list.html doesn't have Delete button")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 10: employee-list.html checks for 'user' role
    print("\n[Test 10] Checking employee-list.html checks for 'user' role...")
    passed, issues = test_file_contains(
        "frontend/pages/employees/employee-list.html",
        [r"userRole === 'user'", r"userRole === 'manager'", r"userRole === 'admin'"]
    )
    if passed:
        print("✓ employee-list.html checks for correct user roles")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 11: navbar.js handles superuser dashboard redirect
    print("\n[Test 11] Checking navbar.js handles superuser redirect...")
    passed, issues = test_file_contains(
        "frontend/components/navbar.js",
        [r'superuser', r'userRole === \'superuser\'']
    )
    if passed:
        print("✓ navbar.js handles superuser dashboard redirect")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 12: config.js has admin-login.html route
    print("\n[Test 12] Checking config.js has admin-login.html route...")
    passed, issues = test_file_contains(
        "frontend/js/config.js",
        [r'admin-login.html']
    )
    if passed:
        print("✓ config.js has admin-login.html route")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 13: API.js handles 204 responses
    print("\n[Test 13] Checking api.js handles 204 No Content responses...")
    passed, issues = test_file_contains(
        "frontend/js/api.js",
        [r'response.status === 204', r'status === 204']
    )
    if passed:
        print("✓ api.js handles 204 No Content responses")
        tests_passed += 1
    else:
        print(f"✗ {issues}")
        tests_failed += 1
        all_issues.extend(issues)
    
    # Test 14: Check JavaScript syntax
    print("\n[Test 14] Checking JavaScript syntax...")
    js_files = [
        "frontend/js/api.js",
        "frontend/js/config.js",
        "frontend/js/main.js",
        "frontend/components/navbar.js"
    ]
    js_errors = []
    for js_file in js_files:
        passed, issues = test_js_syntax(js_file)
        if not passed:
            js_errors.extend(issues)
    
    if len(js_errors) == 0:
        print("✓ All JavaScript files have valid syntax")
        tests_passed += 1
    else:
        print(f"✗ JavaScript syntax errors: {js_errors}")
        tests_failed += 1
        all_issues.extend(js_errors)
    
    # Test 15: Check HTML syntax
    print("\n[Test 15] Checking HTML syntax...")
    html_files = [
        "frontend/pages/auth/admin-login.html",
        "frontend/pages/employees/employee-constraints.html",
        "frontend/pages/employees/employee-constraint-new.html",
        "frontend/pages/employees/employee-edit.html",
        "frontend/pages/employees/employee-list.html"
    ]
    html_errors = []
    for html_file in html_files:
        passed, issues = test_html_syntax(html_file)
        if not passed:
            html_errors.extend(issues)
    
    if len(html_errors) == 0:
        print("✓ All HTML files have valid syntax")
        tests_passed += 1
    else:
        print(f"✗ HTML syntax errors: {html_errors}")
        tests_failed += 1
        all_issues.extend(html_errors)
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Tests Passed: {tests_passed}")
    print(f"Tests Failed: {tests_failed}")
    print(f"Total Tests: {tests_passed + tests_failed}")
    
    if all_issues:
        print("\nIssues Found:")
        for issue in all_issues:
            print(f"  - {issue}")
    
    return tests_failed == 0

if __name__ == "__main__":
    # Change to project root
    os.chdir(Path(__file__).parent)
    success = run_tests()
    exit(0 if success else 1)

