import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST", "")
        self.smtp_port = int(os.getenv("SMTP_PORT", "25"))
        self.smtp_user = os.getenv("SMTP_USER", "")
        self.smtp_password = os.getenv("SMTP_PASSWORD", "")
        self.smtp_from = os.getenv("SMTP_FROM", "noreply@example.com")

    def send_password_reset_email(self, email: str, reset_token: str, reset_url: str) -> bool:
        """
        Send password reset email to user.
        In development mode (no SMTP_HOST), logs the email instead of sending.
        """
        subject = "Password Reset Request"
        body = f"""
You have requested to reset your password.

Click the following link to reset your password:
{reset_url}?token={reset_token}

This link will expire in 1 hour.

If you did not request this password reset, please ignore this email.
"""

        # Development mode: log instead of sending
        if not self.smtp_host:
            logger.info(f"""
[DEV MODE] Password reset email for {email}
Reset URL: {reset_url}?token={reset_token}
Token: {reset_token}
""")
            return True

        # Production mode: send actual email
        try:
            msg = MIMEMultipart()
            msg['From'] = self.smtp_from
            msg['To'] = email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.smtp_user and self.smtp_password:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_password)
                server.sendmail(self.smtp_from, email, msg.as_string())

            logger.info(f"Password reset email sent to {email}")
            return True
        except Exception as e:
            logger.error(f"Failed to send password reset email to {email}: {e}")
            return False


email_service = EmailService()
