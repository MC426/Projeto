class PasswordChecker:
    @staticmethod
    def is_strong_password(password):
        '''
            Single password strengh checker. It tests if:
            - lengh is >= 8
            - has at least 1 UpperCase
            - has at least 1 number
        '''
        strongSize = len(password) >= 8
        hasUpper = sum(1 for c in password if c.isupper())
        hasNumber = sum(1 for c in password if c>='0' and c<='9')
        return strongSize and hasUpper and hasNumber
