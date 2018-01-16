import bcrypt
from user.models import User


class Validator:
    def __init__(self, data):
        self.data = data

    def email_exists(self):
        if User.objects.filter(email=self.data["email"]).first():
            raise Exception("email already exists", 409)
        return False

    def username_exists(self):
        if User.objects.filter(username=self.data["username"]).first():
            raise Exception("username already exists", 409)
        return False

    def is_unique(self):
        self.email_exists()
        self.username_exists()
        return True

    def is_email(self):
        parts = self.data["email"].split('@')
        if len(parts) != 2 or len(parts[1].split('.')) != 2:
            raise Exception("email is not valid", 422)
        return True

    def is_all_valid(self):
        self.data["email"] and self.is_email()
        self.is_valid_password()
        self.is_unique()
        return True

    def is_password(self, password):
        if bcrypt.hashpw(self.data["password"], password) == password:
            return True
        raise Exception("credentials do not match", 401)

    def is_valid_password(self):
        if len(self.data['password']) < 8:
            raise Exception("password must be at least 8 characters long", 422)
        return True

    def is_present(self, *args):
        for field in args:
            if field not in self.data:
                raise Exception("%s is required" % field, 422)
        return True
