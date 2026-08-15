#!/usr/bin/env python3
"""
BoloUp Tool
- Username OR Email le login
- Coin Generator
- 24 Hour Online Keeper
"""

import requests
import time
import sys
from datetime import datetime, timedelta

# ====================== CONFIG ======================
API_BASE = "http://localhost:8000"      # change if needed
TOKEN_REFRESH_MINUTES = 50
ONLINE_HOURS = 24
# ====================================================

class BoloUpClient:
    def __init__(self):
        self.token = None
        self.user_id = "4123538"
        self.username = "rabin246808644@gmail.com"
        self.login_id = None          # username or email
        self.password = None

    def login(self, login_id: str, password: str) -> bool:
        """Username OR Email le login"""
        url = f"{API_BASE}/auth/login"
        data = {
            "username": login_id,     # email hale pani yahi field ma pathaune
            "password": password
        }

        try:
            r = requests.post(url, data=data, timeout=12)
            if r.status_code == 200:
                self.token = r.json()["access_token"]
                self.login_id = login_id
                self.password = password
                self._get_me()
                print(f"✅ Login successful!")
                print(f"   User ID  : {self.user_id}")
                print(f"   Username : {self.username}")
                return True
            else:
                print(f"❌ Login failed: {r.text}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    def _get_me(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            r = requests.get(f"{API_BASE}/users/me", headers=headers, timeout=10)
            if r.status_code == 200:
                data = r.json()
                self.user_id = data["id"]
                self.username = data["username"]
                print(f"💰 Current coins: {data.get('coins', 0)}")
        except Exception as e:
            print(f"⚠️ Could not fetch profile: {e}")

    def add_coins(self, amount: float, target_user_id: int = None):
        if not self.token:
            print("❌ Please login first")
            return

        if target_user_id is None:
            target_user_id = self.user_id

        url = f"{API_BASE}/users/add-coins"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        payload = {
            "user_id": target_user_id,
            "amount": amount
        }

        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                print("✅", r.json())
            else:
                print(f"❌ Failed ({r.status_code}): {r.text}")
        except Exception as e:
            print(f"❌ Error: {e}")

    def keep_online(self, hours: int = 24):
        if not self.token:
            print("❌ Please login first")
            return

        end_time = datetime.now() + timedelta(hours=hours)
        print(f"\n🟢 Online mode started")
        print(f"   Will stay online until: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("   Press Ctrl+C to stop\n")

        try:
            while datetime.now() < end_time:
                success = self.login(self.login_id, self.password)
                if not success:
                    print("⚠️ Refresh failed. Retrying in 30 seconds...")
                    time.sleep(30)
                    continue

                remaining = end_time - datetime.now()
                hrs = remaining.seconds // 3600
                mins = (remaining.seconds % 3600) // 60
                print(f"🔄 Token refreshed | Remaining: {remaining.days}d {hrs}h {mins}m")
                time.sleep(TOKEN_REFRESH_MINUTES * 60)

            print("\n⏰ 24 hours completed.")
        except KeyboardInterrupt:
            print("\n🛑 Stopped by user.")

    def run(self):
        print("=" * 52)
        print("     BoloUp Tool - Coin Generator + 24h Online")
        print("=" * 52)

        login_id = input("Username or Email: ").strip()
        password = input("Password: ").strip()

        if not self.login(login_id, password):
            sys.exit(1)

        while True:
            print("\n" + "-" * 40)
            print("1. Add Coins (Coin Generator)")
            print("2. Keep Online for 24 Hours")
            print("3. Check My Balance")
            print("4. Exit")
            print("-" * 40)

            choice = input("Choose (1-4): ").strip()

            if choice == "1":
                try:
                    amount = float(input("Coins amount: "))
                    target = input("Target User ID (Enter = myself): ").strip()
                    target_id = int(target) if target else None
                    self.add_coins(amount, target_id)
                except ValueError:
                    print("❌ Invalid number")

            elif choice == "2":
                self.keep_online(ONLINE_HOURS)

            elif choice == "3":
                self._get_me()

            elif choice == "4":
                print("Bye 👋")
                break
            else:
                print("Invalid choice")

if __name__ == "__main__":
    client = BoloUpClient()
    client.run()
