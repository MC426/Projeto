import unittest
from utils.password_checker import PasswordChecker

class TestPasswordChecker(unittest.TestCase):
    def test_password_strength(self):
        strong_passwords =[
            "StrongPass123!",
            "YourName1",
        ]
        weak_passwords = [
            "weak",
            "Small12",
            "NoNumHAHAH",
            "noupper123"
        ]
        for strong_password in strong_passwords:
            self.assertTrue(PasswordChecker.is_strong_password(strong_password))
        for weak_password in weak_passwords:
            self.assertFalse(PasswordChecker.is_strong_password(weak_password))

if __name__ == "__main__":
    unittest.main()
