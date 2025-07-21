# quick_test_auth.py

from services.auth_service import AuthService

if __name__ == "__main__":
    svc = AuthService()
    user = svc.login("admin", "adminpass")
    print("Login result:", user)
