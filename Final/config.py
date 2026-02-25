import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    client_id: str | None
    tenant_id: str | None
    client_secret: str | None
    drive_id: str | None
    plan_id: str | None
    folder_path: str
    folder_destination: str


def load_settings() -> Settings:
    load_dotenv()
    return Settings(
        client_id=os.getenv("CLIENT_ID_APPONLY"),
        tenant_id=os.getenv("TENANT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        drive_id=os.getenv("DRIVE_ID"),
        plan_id=os.getenv("PLN2_PLAN_ID"),
        folder_path="FINAL - Dev",
        folder_destination="FINAL - Dev/Procesados"
    )
