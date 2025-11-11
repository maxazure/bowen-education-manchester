"""
Request validation schemas using Pydantic
"""
from pydantic import BaseModel, EmailStr, Field, validator


class ContactFormRequest(BaseModel):
    """Contact form submission validation"""

    name: str = Field(..., min_length=1, max_length=100, description="Contact name")
    email: EmailStr = Field(..., description="Email address")
    phone: str = Field(default="", max_length=20, description="Phone number (optional)")
    subject: str = Field(
        ..., min_length=1, max_length=200, description="Message subject"
    )
    message: str = Field(
        ..., min_length=1, max_length=2000, description="Message content"
    )

    @validator("name")
    def name_must_not_be_empty(cls, v):
        """Validate name is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError("Name cannot be empty")
        return v.strip()

    @validator("subject")
    def subject_must_not_be_empty(cls, v):
        """Validate subject is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError("Subject cannot be empty")
        return v.strip()

    @validator("message")
    def message_must_not_be_empty(cls, v):
        """Validate message is not empty or whitespace"""
        if not v or not v.strip():
            raise ValueError("Message cannot be empty")
        return v.strip()

    @validator("phone")
    def phone_format(cls, v):
        """Validate phone format if provided"""
        if v and v.strip():
            # Remove common separators
            cleaned = v.strip().replace("-", "").replace(" ", "").replace("(", "").replace(")", "")
            # Check if it contains only digits and +
            if not all(c.isdigit() or c == "+" for c in cleaned):
                raise ValueError("Phone number can only contain digits, spaces, hyphens, and + symbol")
        return v.strip() if v else ""

    class Config:
        str_strip_whitespace = True
