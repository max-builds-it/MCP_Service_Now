from utils.config import ServerConfig, AuthType

class AuthManager:
    def __init__(self, config: ServerConfig):
        self.config = config

    def get_headers(self) -> dict:
        """Return the appropriate headers based on the authentication type."""
        if self.config.auth.type == AuthType.API_KEY:
            return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                self.config.auth.api_key.header_name: self.config.auth.api_key.api_key,
            }
        elif self.config.auth.type == AuthType.BASIC:
            import base64
            creds = f"{self.config.auth.basic.username}:{self.config.auth.basic.password}"
            b64_creds = base64.b64encode(creds.encode()).decode()
            return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Basic {b64_creds}",
            }
        elif self.config.auth.type == AuthType.OAUTH:
            token = self.get_oauth_token()
            return {
                "Accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            }
        else:
            raise ValueError(f"Unsupported authentication type: {self.config.auth.type}")