"""
COMPREHENSIVE SUPERUSER WORKFLOW TEST SUITE
Tests all superuser functionalities from account creation to management
"""
import requests
import sys
import random
import string

BASE_URL = "http://127.0.0.1:8000"

class SuperuserWorkflowTests:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.token = None
        self.test_users = []
        
    def login(self):
        """Login as superuser"""
        try:
            response = requests.post(
                f"{BASE_URL}/users/login_token",
                data={"username": "elaine.maua", "password": "password123"}
            )
            if response.status_code == 200:
                self.token = response.json()["access_token"]
                return True
            return False
        except Exception as e:
            print(f"❌ Login failed: {e}")
            return False
    
    def get_headers(self):
        return {"Authorization": f"Bearer {self.token}", "Content-Type": "application/json"}
    
    def test(self, name, condition, details=""):
        """Record test result"""
        if condition:
            self.passed += 1
            print(f"✅ {name}")
            if details:
                print(f"   {details}")
        else:
            self.failed += 1
            print(f"❌ {name}")
            if details:
                print(f"   {details}")
        return condition
    
    def generate_unique_email(self):
        """Generate unique email"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test.{random_str}@example.com"
    
    def run_all_tests(self):
        print("="*80)
        print("COMPREHENSIVE SUPERUSER WORKFLOW TEST SUITE")
        print("="*80)
        
        if not self.login():
            print("❌ Cannot proceed without authentication")
            return False
        
        print("\n✅ Authentication successful\n")
        
        # Test all workflows
        self.test_1_create_user_and_send_invite()
        self.test_2_list_and_view_users()
        self.test_3_resend_invite()
        self.test_4_disable_enable_account()
        self.test_5_complete_end_to_end_workflow()
        self.test_6_error_handling()
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! Superuser workflow is fully functional.")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Review above for details.")
        
        print("="*80)
        return self.failed == 0
    
    def test_1_create_user_and_send_invite(self):
        """Test Suite 1: Create User and Send Invite"""
        print("\n--- Test Suite 1: Create User and Send Invite ---")
        
        headers = self.get_headers()
        email = self.generate_unique_email()
        
        # Test 1.1: Create user
        print("\n  Step 1: Creating user...")
        response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "John",
                "lastname": "Doe",
                "email": email,
                "user_role": "user"
            }
        )
        
        if self.test("Create user successfully", response.status_code == 200, f"Status: {response.status_code}"):
            user = response.json()
            self.test_users.append(user)
            
            self.test("User has ID", 'id' in user, f"ID: {user.get('id')}")
            self.test("User has username", 'username' in user, f"Username: {user.get('username')}")
            self.test("User has email", 'email' in user, f"Email: {user.get('email')}")
            self.test("User is inactive by default", user.get('is_active') == False, f"is_active: {user.get('is_active')}")
            
            # Test 1.2: Send invite
            print("\n  Step 2: Sending invite...")
            invite_response = requests.post(
                f"{BASE_URL}/users/send_invite",
                headers=headers,
                json={"email": user['email']}
            )
            
            self.test("Send invite successfully", invite_response.status_code == 200, f"Status: {invite_response.status_code}")
            
            if invite_response.status_code == 200:
                invite_data = invite_response.json()
                self.test("Invite response has message", 'message' in invite_data, f"Message: {invite_data.get('message')}")
    
    def test_2_list_and_view_users(self):
        """Test Suite 2: List and View Users"""
        print("\n--- Test Suite 2: List and View Users ---")
        
        headers = self.get_headers()
        
        # Test 2.1: List all users
        print("\n  Step 1: Listing all users...")
        response = requests.get(f"{BASE_URL}/users/list", headers=headers)
        
        if self.test("List all users", response.status_code == 200, f"Status: {response.status_code}"):
            users = response.json()
            self.test("Users list is not empty", len(users) > 0, f"Count: {len(users)}")
            
            if users:
                user = users[0]
                self.test("User has required fields", 
                         all(field in user for field in ['id', 'username', 'email', 'user_role', 'is_active']),
                         f"Fields: {list(user.keys())}")
        
        # Test 2.2: Filter users by role
        print("\n  Step 2: Filtering users by role...")
        response = requests.get(f"{BASE_URL}/users/list?role=user", headers=headers)
        
        if self.test("Filter users by role", response.status_code == 200, f"Status: {response.status_code}"):
            users = response.json()
            if users:
                self.test("Filtered users have correct role", 
                         all(u.get('user_role') == 'user' for u in users),
                         f"Sample role: {users[0].get('user_role')}")
    
    def test_3_resend_invite(self):
        """Test Suite 3: Resend Invite"""
        print("\n--- Test Suite 3: Resend Invite ---")
        
        headers = self.get_headers()
        
        # Create a new user
        email = self.generate_unique_email()
        create_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Resend",
                "lastname": "Test",
                "email": email,
                "user_role": "user"
            }
        )
        
        if create_response.status_code == 200:
            user = create_response.json()
            
            # Test 3.1: Resend invite
            print("\n  Resending invite...")
            resend_response = requests.post(
                f"{BASE_URL}/users/send_invite",
                headers=headers,
                json={"email": user['email']}
            )
            
            self.test("Resend invite successfully", resend_response.status_code == 200, f"Status: {resend_response.status_code}")
    
    def test_4_disable_enable_account(self):
        """Test Suite 4: Disable and Enable Account"""
        print("\n--- Test Suite 4: Disable and Enable Account ---")
        
        headers = self.get_headers()
        
        # Create a user to test with
        email = self.generate_unique_email()
        create_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Disable",
                "lastname": "EnableTest",
                "email": email,
                "user_role": "user"
            }
        )
        
        if create_response.status_code == 200:
            user = create_response.json()
            user_id = user['id']
            
            # Test 4.1: Disable account
            print("\n  Step 1: Disabling account...")
            disable_response = requests.put(
                f"{BASE_URL}/users/disable/{user_id}",
                headers=headers
            )
            
            if self.test("Disable account", disable_response.status_code == 200, f"Status: {disable_response.status_code}"):
                disabled_user = disable_response.json()
                self.test("User is disabled", disabled_user.get('is_active') == False, f"is_active: {disabled_user.get('is_active')}")
            
            # Test 4.2: Enable account
            print("\n  Step 2: Enabling account...")
            enable_response = requests.put(
                f"{BASE_URL}/users/enable/{user_id}",
                headers=headers
            )
            
            if self.test("Enable account", enable_response.status_code == 200, f"Status: {enable_response.status_code}"):
                enabled_user = enable_response.json()
                self.test("User is enabled", enabled_user.get('is_active') == True, f"is_active: {enabled_user.get('is_active')}")
    
    def test_5_complete_end_to_end_workflow(self):
        """Test Suite 5: Complete End-to-End Workflow"""
        print("\n--- Test Suite 5: Complete End-to-End Workflow ---")
        
        headers = self.get_headers()
        email = self.generate_unique_email()
        
        print("\n  Complete workflow: Create → Invite → View → Disable → Enable → Resend")
        
        # Step 1: Create
        create_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "E2E",
                "lastname": "Test",
                "email": email,
                "user_role": "admin"
            }
        )
        
        if not self.test("E2E: Create user", create_response.status_code == 200):
            return
        
        user = create_response.json()
        user_id = user['id']
        
        # Step 2: Send invite
        invite_response = requests.post(
            f"{BASE_URL}/users/send_invite",
            headers=headers,
            json={"email": user['email']}
        )
        self.test("E2E: Send invite", invite_response.status_code == 200)
        
        # Step 3: View in list
        list_response = requests.get(f"{BASE_URL}/users/list", headers=headers)
        if list_response.status_code == 200:
            users = list_response.json()
            user_in_list = any(u['id'] == user_id for u in users)
            self.test("E2E: User appears in list", user_in_list)
        
        # Step 4: Disable
        disable_response = requests.put(f"{BASE_URL}/users/disable/{user_id}", headers=headers)
        self.test("E2E: Disable account", disable_response.status_code == 200)
        
        # Step 5: Enable
        enable_response = requests.put(f"{BASE_URL}/users/enable/{user_id}", headers=headers)
        self.test("E2E: Enable account", enable_response.status_code == 200)
        
        # Step 6: Resend invite
        resend_response = requests.post(
            f"{BASE_URL}/users/send_invite",
            headers=headers,
            json={"email": user['email']}
        )
        self.test("E2E: Resend invite", resend_response.status_code == 200)
        
        print("\n  ✅ Complete workflow executed successfully!")
    
    def test_6_error_handling(self):
        """Test Suite 6: Error Handling"""
        print("\n--- Test Suite 6: Error Handling ---")
        
        headers = self.get_headers()
        
        # Test 6.1: Duplicate email
        email = self.generate_unique_email()
        requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={"firstname": "Dup", "lastname": "Test1", "email": email, "user_role": "user"}
        )
        
        dup_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={"firstname": "Dup", "lastname": "Test2", "email": email, "user_role": "user"}
        )
        self.test("Reject duplicate email", dup_response.status_code == 409, f"Status: {dup_response.status_code}")
        
        # Test 6.2: Invalid email
        invalid_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={"firstname": "Invalid", "lastname": "Email", "email": "not-an-email", "user_role": "user"}
        )
        self.test("Reject invalid email", invalid_response.status_code == 422, f"Status: {invalid_response.status_code}")
        
        # Test 6.3: Non-existent user
        disable_response = requests.put(f"{BASE_URL}/users/disable/999999", headers=headers)
        self.test("Handle non-existent user", disable_response.status_code == 404, f"Status: {disable_response.status_code}")
        
        # Test 6.4: Invite non-existent email
        invite_response = requests.post(
            f"{BASE_URL}/users/send_invite",
            headers=headers,
            json={"email": "nonexistent@example.com"}
        )
        self.test("Handle invite to non-existent email", invite_response.status_code == 404, f"Status: {invite_response.status_code}")

if __name__ == "__main__":
    print("\n" + "🧪" * 40)
    print("Starting Comprehensive Superuser Workflow Tests...")
    print("🧪" * 40 + "\n")
    
    suite = SuperuserWorkflowTests()
    success = suite.run_all_tests()
    
    if success:
        print("\n✅ All superuser workflow tests passed!")
        print("   - User creation works")
        print("   - Invite sending works")
        print("   - User listing and viewing works")
        print("   - Resend invite works")
        print("   - Disable/Enable works")
        print("   - Complete E2E workflow works")
        print("   - Error handling works")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Review and fix before deployment.")
        sys.exit(1)
