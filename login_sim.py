import time
import secrets

class BoloUpProAuthSimulator:
    def _init_(self):
        # Simulating a backend user database
        self.registered_users = {
            "user@example.com": {"user_id": "992811", "status": "Active", "profile": "Pro_User"}
        }
        # In-memory storage for active verification tokens
        self.active_otps = {}

    def request_otp_link(self, email):
        """Step 1: User inputs email to request a passwordless token."""
        print(f"\n[System] Checking database for: {email}...")
        
        if email not in self.registered_users:
            print("[Error] Email address not registered on BoloUp Pro.")
            return False
            
        # Generate a secure 6-digit verification code
        otp_code = str(secrets.randbelow(900000) + 100000)
        # Set expiration timestamp (e.g., valid for 2 minutes)
        expiration = time.time() + 120 
        
        self.active_otps[email] = {"code": otp_code, "expires_at": expiration}
        
        print(f"[Email Server] Outgoing message sent to {email} successfully!")
        print(f"-------- EMAIL INBOX SIMULATION --------")
        print(f"Subject: Your BoloUp Pro Verification Code")
        print(f"Your secure one-time login code is: {otp_code}")
        print(f"----------------------------------------")
        return True

    def verify_login(self, email, input_code):
        """Step 2: User inputs the received code to finalize authentication."""
        if email not in self.active_otps:
            print("[Error] No login session initiated for this email.")
            return False
            
        auth_data = self.active_otps[email]
        
        # Check if token has expired
        if time.time() > auth_data["expires_at"]:
            print("[Error] Verification code has expired. Please request a new one.")
            del self.active_otps[email]
            return False
            
        # Validate input code
        if input_code == auth_data["code"]:
            user_info = self.registered_users[email]
            print("\n========================================")
            print("🎉 LOGIN SUCCESSFUL (No Password Used)")
            print(f"Welcome back! BoloUp ID: {user_info['user_id']}")
            print(f"Account Profile Type: {user_info['profile']}")
            print("========================================")
            # Clear used code from active memory
            del self.active_otps[email]
            return True
        else:
            print("[Error] Invalid verification code. Please check your spelling.")
            return False

# --- Running the Automation Flow ---
if _name_ == "_main_":
    auth_system = BoloUpProAuthSimulator()
    
    # 1. Provide your registered email address
    my_email = "user@example.com" 
    
    # 2. Trigger the code request sequence
    if auth_system.request_otp_link(my_email):
        
        # 3. Simulate user typing code directly from their email inbox
        user_otp_input = input("\nEnter the 6-digit code displayed in your email inbox above: ")
        
        # 4. Verify code integrity to gain system access
        auth_system.verify_login(my_email, user_otp_input)
