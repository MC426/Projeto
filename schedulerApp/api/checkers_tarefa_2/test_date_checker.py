import unittest
from utils.date_checker import DateChecker
import datetime



class TestDateChecker(unittest.TestCase):

    def test_date_validation(self):
        """
            Tests to see if the appointment_date_check function of the DateChecker class provides the correct answers when someone is trying to make a medical appointment .

            It is important to remember that this function is testing dates in September 2023. Therefore, future tests with the same valid dates may yield different results or encounter errors,
            as those dates may no longer be valid in the future.
        """
        valid_dates = [
            "2024-09-10 14:30:00", # Monday
            "2023-12-21 10:10:10", # Thursday
            "2024-01-19 17:59:20"  # Friday
        ]

        invalid_dates = [
            "2023-09-10 08:08:08", # Past
            "2023-12-25 14:14:14", # National Holiday
            "2023-11-15 10:10:10", # Brazilian Holiday
            "2023-12-10 13:13:13", # Weekend
            "2023-09-10 19:19:19", # Outside Comercial Time
            "2025-02-14 11:11:11", # More than 2 years
        ]
        
        # --------- VALID DATES -------
        for date in valid_dates:
            self.assertTrue(DateChecker.appointment_date_check(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")), "Valid Date: This is valid for a medical appointment")
        
        # --------- INVALID DATES -------
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[0], "%Y-%m-%d %H:%M:%S")), "Invalid Date: This date has already passed.")
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[1], "%Y-%m-%d %H:%M:%S")), "Invalid Date: Medical appointments cannot be scheduled on National Holidays.")
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[2], "%Y-%m-%d %H:%M:%S")), "Invalid Date: Medical appointments cannot be scheduled on Brazilian Holidays.")
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[3], "%Y-%m-%d %H:%M:%S")), "Invalid Date: Medical appointments cannot be scheduled outside comercial time (Monday to Friday, 8 am to 6 pm).")
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[4], "%Y-%m-%d %H:%M:%S")), "Invalid Date: Medical appointments cannot be scheduled outside comercial time (Monday to Friday, 8 am to 6 pm).")
        self.assertFalse(DateChecker.appointment_date_check(datetime.datetime.strptime(invalid_dates[5], "%Y-%m-%d %H:%M:%S")), "Invalid Date: Medical appointments can only be scheduled for this year or the next.")
        
        
       

if __name__ == "__main__":
    unittest.main()