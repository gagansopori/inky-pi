class UserProfile:
    def __init__(self):
        self._username: str = None
        self._user_type: int = None
        self._messages: str = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, uname):
        self._username = uname

    @property
    def user_type(self):
        return self._user_type

    @user_type.setter
    def user_type(self, utype):
        self._user_type = utype

    @property
    def messages(self):
        return self._messages

    @messages.setter
    def messages(self, msg):
        self._messages = msg
