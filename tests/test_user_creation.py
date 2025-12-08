"""
Comprehensive Test Suite for User Creation
Tests all scenarios to ensure robust error handling and success flows
"""
import requests
import json
import sys
import random
import string

BASE_URL = "http://127.0.0.1:8000"

class UserCreationTestSuite:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.token = None
        self.created_users = []
        
    def login(self):
        """Login as superuser to get token"""
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
    
    def generate_unique_email(self):
        """Generate a unique email for testing"""
        random_str = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test.{random_str}@example.com"
    
    def run_all_tests(self):
        print("="*80)
        print("USER CREATION - COMPREHENSIVE TEST SUITE")
        print("="*80)
        
        # Login first
        if not self.login():
            print("❌ Cannot proceed without authentication")
            return False
        
        print("\n✅ Authentication successful\n")
        
        # Test Suite 1: Successful User Creation
        self.test_successful_creation()
        
        # Test Suite 2: Duplicate Email Handling
        self.test_duplicate_email()
        
        # Test Suite 3: Duplicate Username Handling
        self.test_duplicate_username()
        
        # Test Suite 4: Invalid Input Validation
        self.test_invalid_inputs()
        
        # Test Suite 5: Complete Flow (Create + Invite)
        self.test_complete_flow()
        
        # Test Suite 6: Different User Roles
        self.test_different_roles()
        
        # Test Suite 7: Edge Cases
        self.test_edge_cases()
        
        # Summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"Total: {self.passed + self.failed}")
        
        if self.failed == 0:
            print("\n🎉 ALL TESTS PASSED! User creation is working perfectly.")
        else:
            print(f"\n⚠️  {self.failed} test(s) failed. Review above for details.")
        
        print("="*80)
        
        return self.failed == 0
    
    def test_successful_creation(self):
        """Test Suite 1: Successful User Creation"""
        print("\n--- Test Suite 1: Successful User Creation ---")
        
        headers = self.get_headers()
        email = self.generate_unique_email()
        
        # Test 1.1: Create user with valid data
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
        
        self.test(
            "Create user with valid data",
            response.status_code == 200,
            f"Status: {response.status_code}"
        )
        
        if response.status_code == 200:
            user = response.json()
            self.created_users.append(user)
            
            # Test 1.2: Response has required fields
            self.test(
                "Response contains 'id' field",
                'id' in user,
                f"User ID: {user.get('id')}"
            )
            
            self.test(
                "Response contains 'username' field",
                'username' in user,
                f"Username: {user.get('username')}"
            )
            
            self.test(
                "Response contains 'email' field",
                'email' in user,
                f"Email: {user.get('email')}"
            )
            
            self.test(
                "Response contains 'user_role' field",
                'user_role' in user,
                f"Role: {user.get('user_role')}"
            )
            
            # Test 1.3: Username format is correct
            expected_username = "john.doe"
            self.test(
                "Username format is 'firstname.lastname'",
                user.get('username') == expected_username,
                f"Expected: {expected_username}, Got: {user.get('username')}"
            )
            
            # Test 1.4: User is inactive by default
            self.test(
                "New user is inactive by default",
                user.get('is_active') == False,
                f"is_active: {user.get('is_active')}"
            )
    
    def test_duplicate_email(self):
        """Test Suite 2: Duplicate Email Handling"""
        print("\n--- Test Suite 2: Duplicate Email Handling ---")
        
        headers = self.get_headers()
        
        # Create a user first
        email = self.generate_unique_email()
        response1 = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Alice",
                "lastname": "Smith",
                "email": email,
                "user_role": "user"
            }
        )
        
        # Test 2.1: Try to create another user with same email
        response2 = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Bob",
                "lastname": "Jones",
                "email": email,  # Same email
                "user_role": "admin"
            }
        )
        
        self.test(
            "Duplicate email returns 409 Conflict",
            response2.status_code == 409,
            f"Status: {response2.status_code}"
        )
        
        if response2.status_code == 409:
            error = response2.json()
            self.test(
                "Error message mentions duplicate email",
                "already exists" in error.get('detail', '').lower(),
                f"Message: {error.get('detail')}"
            )
    
    def test_duplicate_username(self):
        """Test Suite 3: Duplicate Username Handling"""
        print("\n--- Test Suite 3: Duplicate Username Handling ---")
        
        headers = self.get_headers()
        email1 = self.generate_unique_email()
        email2 = self.generate_unique_email()
        
        # Create first user
        response1 = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Charlie",
                "lastname": "Brown",
                "email": email1,
                "user_role": "user"
            }
        )
        
        # Test 3.1: Try to create user with same name but different email
        response2 = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Charlie",
                "lastname": "Brown",
                "email": email2,  # Different email
                "user_role": "user"
            }
        )
        
        self.test(
            "Duplicate username returns 409 Conflict",
            response2.status_code == 409,
            f"Status: {response2.status_code}"
        )
        
        if response2.status_code == 409:
            error = response2.json()
            self.test(
                "Error message mentions duplicate username",
                "username" in error.get('detail', '').lower(),
                f"Message: {error.get('detail')}"
            )
    
    def test_invalid_inputs(self):
        """Test Suite 4: Invalid Input Validation"""
        print("\n--- Test Suite 4: Invalid Input Validation ---")
        
        headers = self.get_headers()
        
        # Test 4.1: Invalid email format
        response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Invalid",
                "lastname": "Email",
                "email": "not-an-email",
                "user_role": "user"
            }
        )
        
        self.test(
            "Invalid email format rejected",
            response.status_code == 422,
            f"Status: {response.status_code}"
        )
        
        # Test 4.2: Missing required field
        response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Missing",
                "lastname": "Field",
                # email missing
                "user_role": "user"
            }
        )
        
        self.test(
            "Missing required field rejected",
            response.status_code == 422,
            f"Status: {response.status_code}"
        )
    
    def test_complete_flow(self):
        """Test Suite 5: Complete Flow (Create + Invite)"""
        print("\n--- Test Suite 5: Complete Flow (Create + Invite) ---")
        
        headers = self.get_headers()
        email = self.generate_unique_email()
        
        # Test 5.1: Create user
        print("\n   Step 1: Creating user...")
        create_response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Complete",
                "lastname": "Flow",
                "email": email,
                "user_role": "admin"
            }
        )
        
        self.test(
            "User creation successful",
            create_response.status_code == 200,
            f"Status: {create_response.status_code}"
        )
        
        if create_response.status_code == 200:
            user = create_response.json()
            
            # Test 5.2: Send invite
            print("   Step 2: Sending invite...")
            invite_response = requests.post(
                f"{BASE_URL}/users/send_invite",
                headers=headers,
                json={"email": user['email']}
            )
            
            self.test(
                "Invite sent successfully",
                invite_response.status_code == 200,
                f"Status: {invite_response.status_code}"
            )
            
            if invite_response.status_code == 200:
                invite_data = invite_response.json()
                self.test(
                    "Invite response contains success message",
                    'message' in invite_data,
                    f"Message: {invite_data.get('message')}"
                )
    
    def test_different_roles(self):
        """Test Suite 6: Different User Roles"""
        print("\n--- Test Suite 6: Different User Roles ---")
        
        headers = self.get_headers()
        roles = ['user', 'admin', 'manager']
        
        for role in roles:
            email = self.generate_unique_email()
            response = requests.post(
                f"{BASE_URL}/users/create",
                headers=headers,
                json={
                    "firstname": "Role",
                    "lastname": role.capitalize(),
                    "email": email,
                    "user_role": role
                }
            )
            
            self.test(
                f"Create user with role '{role}'",
                response.status_code == 200,
                f"Status: {response.status_code}"
            )
            
            if response.status_code == 200:
                user = response.json()
                self.test(
                    f"User has correct role '{role}'",
                    user.get('user_role') == role,
                    f"Role: {user.get('user_role')}"
                )
    
    def test_edge_cases(self):
        """Test Suite 7: Edge Cases"""
        print("\n--- Test Suite 7: Edge Cases ---")
        
        headers = self.get_headers()
        
        # Test 7.1: Very long names
        email = self.generate_unique_email()
        response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "VeryLongFirstName" * 5,
                "lastname": "VeryLongLastName" * 5,
                "email": email,
                "user_role": "user"
            }
        )
        
        self.test(
            "Handle very long names",
            response.status_code in [200, 422],  # Either accepts or rejects gracefully
            f"Status: {response.status_code}"
        )
        
        # Test 7.2: Names with special characters
        email = self.generate_unique_email()
        response = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "O'Brien",
                "lastname": "Smith-Jones",
                "email": email,
                "user_role": "user"
            }
        )
        
        self.test(
            "Handle names with special characters",
            response.status_code in [200, 422],
            f"Status: {response.status_code}"
        )
        
        # Test 7.3: Case sensitivity in email
        base_email = self.generate_unique_email()
        response1 = requests.post(
            f"{BASE_URL}/users/create",
            headers=headers,
            json={
                "firstname": "Case",
                "lastname": "Test1",
                "email": base_email.lower(),
                "user_role": "user"
            }
        )
        
        if response1.status_code == 200:
            response2 = requests.post(
                f"{BASE_URL}/users/create",
                headers=headers,
                json={
                    "firstname": "Case",
                    "lastname": "Test2",
                    "email": base_email.upper(),  # Same email, different case
                    "user_role": "user"
                }
            )
            
            self.test(
                "Email case sensitivity handled",
                response2.status_code == 409,  # Should detect as duplicate
                f"Status: {response2.status_code}"
            )

if __name__ == "__main__":
    print("\n" + "🧪" * 40)
    print("Starting User Creation Test Suite...")
    print("🧪" * 40 + "\n")
    
    suite = UserCreationTestSuite()
    success = suite.run_all_tests()
    
    if success:
        print("\n✅ All user creation tests passed!")
        print("   - Users can be created successfully")
        print("   - Invites are sent correctly")
        print("   - All errors are caught and handled gracefully")
        print("   - No crashes or unhandled exceptions")
        sys.exit(0)
    else:
        print("\n⚠️  Some tests failed. Review and fix before deployment.")
        sys.exit(1)
