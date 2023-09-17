import unittest
from utils.email_checker import EmailChecker


class TestEmailChecker(unittest.TestCase):

    def test_email_validation(self):
        """
            Tests to see if an email is valid or not. Does not check if an email exists or not.
        """
        valid_emails = [
            "abcd@gmail.com",
            "lk123A@hotmail.com",
            "john.pd@dom.org"  
        ]

        invalid_emails = [
            "gha@@dac.unicamp.br",
            "try@gmail.",
            "ops@domain.prt%"
        ]
        
        # --------- VALID EMAILS -------
        for valid_email in valid_emails:
            self.assertTrue(EmailChecker.is_valid_email(valid_email))
        
        # --------- INVALID EMAILS -------
        for invalid_email in invalid_emails:
            self.assertFalse(EmailChecker.is_valid_email(invalid_email))
        
        
       

if __name__ == "__main__":
    unittest.main()