from datetime import datetime
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_data , is_confirmed=False, confirmed_on=None):
        self.id = str(user_data['_id'])
        self.username = user_data.get('username', '')
        self.email = user_data.get('email')
        self.created_on = datetime.now()
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on
        self.user_data = user_data

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<email {self.email}>"



