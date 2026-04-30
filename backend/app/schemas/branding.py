from typing import Optional
from pydantic import BaseModel


class BrandingSettings(BaseModel):
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: str = "#1976d2"
    secondary_color: str = "#dc004e"
    platform_name: str = "CC Video"
    custom_domain: Optional[str] = None
    email_header: Optional[str] = None
    email_footer: Optional[str] = None


class BrandingUpdate(BaseModel):
    logo_url: Optional[str] = None
    favicon_url: Optional[str] = None
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    platform_name: Optional[str] = None
    custom_domain: Optional[str] = None
    email_header: Optional[str] = None
    email_footer: Optional[str] = None
