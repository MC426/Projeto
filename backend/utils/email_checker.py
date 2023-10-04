import re

class EmailChecker:
    @staticmethod
    def is_valid_email(email):
        '''
            Email checker. Uses the RFC5322-compliant Regular Expression
            to check if the email string corresponds to a valid email address
            Doesn't check if the email exists, only if it is valid
        '''
        regex = re.compile(r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
        if re.fullmatch(regex, email):
            return True
        else:
            return False
