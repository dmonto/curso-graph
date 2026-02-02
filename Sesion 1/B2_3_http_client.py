import requests

class HttpClient:
    def __init__(self, base_url: str, default_timeout: int = 10):
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")
        self.default_timeout = default_timeout
        self.session.headers.update({"User-Agent": "curso-msgraph/1.0"})

    def get(self, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        timeout = kwargs.pop("timeout", self.default_timeout)
        return self.session.get(url, timeout=timeout, **kwargs)

    def post(self, path: str, **kwargs):
        url = f"{self.base_url}/{path.lstrip('/')}"
        timeout = kwargs.pop("timeout", self.default_timeout)
        return self.session.post(url, timeout=timeout, **kwargs)