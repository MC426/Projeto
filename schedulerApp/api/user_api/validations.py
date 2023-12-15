from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    ##
    if not email or UserModel.objects.filter(email=email).exists():
        raise ValidationError('choose another email')
    ##
    if not password or len(password) < 8:
        raise ValidationError('choose another password, min 8 characters')
    ##
    if not username:
        raise ValidationError('choose another username')
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
        raise ValidationError('an email is needed')
    return True

def validate_username(data):
    username = data['username'].strip()
    if not username:
        raise ValidationError('choose another username')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
        raise ValidationError('a password is needed')
    return True

class EmailValidator:
    def validate(self, email):

        if '@' not in email:
            raise ValidationError('Email must contain "@"')
                
        username, domain = email.split('@', 1)

        if '.' not in domain :
            raise ValidationError('Invalid email domain')
        
        before_dot, after_dot = domain.split('.',1)
        
        if not username or not domain:
            raise ValidationError('Invalid email format. It not contains a username or a domain')
        
        
        if not before_dot or not after_dot:
             raise ValidationError('Invalid email format. It not contains a username or a domain')
        
        
        return True
