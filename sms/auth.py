import hashlib
import json
from pathlib import Path

from sms.exceptions import AuthenticationError


class AdminAuth:
    """Handle admin authentication using a JSON configuration file."""

    def __init__(self, auth_file: Path) -> None:
        self.auth_file = auth_file
        self._ensure_default_admin()

    def _ensure_default_admin(self) -> None:
        self.auth_file.parent.mkdir(parents=True, exist_ok=True)
        if self.auth_file.exists():
            return

        default_data = {
            "username": "admin",
            "password_hash": self._hash_password("admin123"),
        }
        self.auth_file.write_text(json.dumps(default_data, indent=4), encoding="utf-8")

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def login(self, username: str, password: str) -> bool:
        data = json.loads(self.auth_file.read_text(encoding="utf-8"))
        hashed_password = self._hash_password(password)

        if data["username"] == username and data["password_hash"] == hashed_password:
            return True
        raise AuthenticationError("Invalid admin username or password.")
