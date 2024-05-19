from requests import session

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0"
API_BASE = "https://quack.duckduckgo.com/api"
OTP = "/auth/loginlink" #?user=user ; GET ; always returns {}
LOGIN = "/auth/login" #?otp=abc&user=user ; POST ; returns {"status": "authenticated", "token": "[...]", "user": "user"}
DASHBOARD = "/email/dashboard" # GET ; returns {"invites":[],"stats":{"addresses_generated":12},"user":{"access_token":"[...]","cohort":"[..]","email":"real_email","username":"user"}}
GEN_EMAIL = "/email/addresses" # POST ; returns {"address":"1234abcd"}


class Client:
    def __init__(self, username: str, token: str | None = None,
                 access_token: str | None = None)  ->  None:
        self.username = username
        self.token = token
        self.access_token = access_token
        self.generated_addresses: int | None = None # will be None if not logged in
        self.real_email: str | None = None # will be None if not logged in
        self.logged_in = all((token, access_token))
        self.session = session()
        self.headers = {"Origin": "https://duckduckgo.com",
                        "Referer": "https://duckduckgo.com",
                        "User-Agent": USER_AGENT}

    def otp(self, username: str | None = None) -> bool:
        """Will use `self.username` if `username` not given"""
        params = {"user": username or self.username}
        req = self.session.get(f"{API_BASE}{OTP}", params=params, headers=self.headers)
        req.raise_for_status()
        return True

    def login(self, otp: str, username: str | None = None) -> dict:
        """Will use `self.username` if `username` not given
        otp can be either the phrase or url
        returns {"status": "authenticated", "token": "[...]", "user": "user"}"""
        if "https://" in otp:
            otp = otp.split('otp=')[-1].split('&')[0]
        else:
            otp = otp.replace(' ', '-')
        params = {"user": username or self.username, "otp": otp}
        req = self.session.get(f"{API_BASE}{LOGIN}", params=params, headers=self.headers)
        req.raise_for_status()
        d = req.json()
        return d['token']

    def dashboard(self) -> dict:
        """returns `{"invites":[],"stats":{"addresses_generated":12},"user":{"access_token":"[...]","cohort":"[..]","email":"real_email","username":"user"}}`"""
        headers = {**self.headers, "Authorization": f"Bearer {self.token}"}
        req = self.session.get(f"{API_BASE}{DASHBOARD}", headers=headers)
        req.raise_for_status()
        d = req.json()
        return d

    def full_login(self, otp: str, username: str | None = None):
        token = self.login(otp, username)
        self.token = token
        res = self.dashboard()
        self.access_token = res['user']['access_token']
        self.real_email = res['user']['email']
        self.generated_addresses = res['stats']['addresses_generated']
        self.logged_in = True
        return True

    def generate_alias(self) -> str:
        headers = {**self.headers, "Authorization": f"Bearer {self.access_token}"}
        req = self.session.post(f"{API_BASE}{GEN_EMAIL}", headers=headers)
        req.raise_for_status()
        d = req.json()
        return d['address']
