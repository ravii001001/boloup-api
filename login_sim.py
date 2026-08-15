import time
import secrets

# 1. This is your simulated user database
database = {
    "test@gmail.com": {"user_id": "992811", "status": "Active"},
    "admin@gmail.com": {"user_id": "000001", "status": "Active"}
}

active_otps = {}

print("\n==========================================")
print("     BoloUp Pro Passwordless Login Flow   ")
print("==========================================\n")

# 2. The script will now explicitly ask you to type your email
user_email = input("Step 1: Enter your email address to log in: ").strip()

# 3. Check if the email exists in our simulation database
if user_email not in database:
    print(f"\n[Error] '{user_email}' is not found in the database.")
    print("-> Tip: Try logging in with 'test@gmail.com' to see it work!")
else:
    # 4. Generate a secure 6-digit login token
    generated_code = str(secrets.randbelow(900000) + 100000)
    active_otps[user_email] = generated_code
    
    print(f"\n[System] Checking email records for {user_email}...")
    print(f"[Email Server] Verification token sent successfully!")
    print(f"------------ EMAIL INBOX SIMULATION ------------")
    print(f"Subject: Your BoloUp Pro Verification Code")
    print(f"Your secure one-time login code is: {generated_code}")
    print(f"------------------------------------------------")

    # 5. The script pauses here and waits for your input
    user_input_code = input("\nStep 2: Enter the 6-digit code displayed above: ").strip()

    # 6. Verify if the code matches
    if user_input_code == active_otps[user_email]:
        account_details = database[user_email]
        print("\n========================================")
        print("🎉 LOGIN SUCCESSFUL (No Password Used)")
        print(f"Welcome back! BoloUp ID: {account_details['user_id']}")
        print(f"Account Status: {account_details['status']}")
        print("========================================")
    else:
        print("\n[Error] Invalid verification code. Login failed.")
