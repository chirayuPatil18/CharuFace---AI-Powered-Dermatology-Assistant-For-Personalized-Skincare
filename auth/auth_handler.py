import json
import os

USER_FILE = "auth/users.json"


def load_users():
    if not os.path.exists(USER_FILE):
        return {}

    with open(USER_FILE, "r") as f:
        return json.load(f)


def save_users(users):
    os.makedirs("auth", exist_ok=True)
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)


# VERIFY EMAIL (PERSISTENT)
def mark_email_verified(email):
    users = load_users()

    # if user not created yet → create temp entry
    if email not in users:
        users[email] = {}

    users[email]["verified"] = True
    save_users(users)


def is_email_verified(email):
    users = load_users()

    return users.get(email, {}).get("verified", False)

# SIGNUP
def signup(name, email, password):
    users = load_users()

    # already exists + already signed up
    if email in users and "password" in users[email]:
        return False, "User already exists"

    # BLOCK if not verified
    if not is_email_verified(email):
        return False, "Email not verified"

    users[email] = {
        "name": name,
        "password": password,
        "verified": True
    }

    save_users(users)
    return True, "Signup successful"

# LOGIN
def login(email, password):
    users = load_users()

    if email not in users:
        return False, "User not found"

    if users[email].get("password") != password:
        return False, "Incorrect password"

    return True, "Login successful"