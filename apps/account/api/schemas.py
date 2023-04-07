from fastapi.param_functions import Form


class OAuth2PasswordRequestForm:

    def __init__(
        self,
        username: str = Form(),
        password: str = Form(),
    ):
        self.grant_type = None
        self.username = username
        self.password = password
        self.scopes = ''.split()
        self.client_id = None
        self.client_secret = None
