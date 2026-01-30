"""
Email service module for sending newsletters via SMTP
"""

import smtplib
import json
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from typing import List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EmailConfig:
    """Configuration for email sending"""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.sender_name = os.getenv("SENDER_NAME", "DSEC AI Newsletter")

        if not self.sender_email or not self.sender_password:
            logger.warning("SMTP credentials not configured in .env file")


class SubscriberManager:
    """Manages newsletter subscribers"""

    def __init__(self, subscribers_file: str = "output/subscribers.json"):
        self.subscribers_file = subscribers_file
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create subscribers file if it doesn't exist"""
        if not os.path.exists(self.subscribers_file):
            with open(self.subscribers_file, "w") as f:
                json.dump({"subscribers": []}, f, indent=2)

    def load_subscribers(self) -> List[dict]:
        """Load all active subscribers"""
        try:
            with open(self.subscribers_file, "r") as f:
                data = json.load(f)
                return [s for s in data.get("subscribers", []) if s.get("active", True)]
        except Exception as e:
            logger.error(f"Error loading subscribers: {e}")
            return []

    def add_subscriber(self, email: str, name: str = "") -> bool:
        """Add a new subscriber"""
        try:
            with open(self.subscribers_file, "r") as f:
                data = json.load(f)

            # Check if already subscribed
            if any(s["email"] == email for s in data["subscribers"]):
                logger.warning(f"Email {email} already subscribed")
                return False

            data["subscribers"].append(
                {
                    "email": email,
                    "name": name,
                    "subscribed_at": datetime.now().isoformat(),
                    "active": True,
                }
            )

            with open(self.subscribers_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info(f"Added subscriber: {email}")
            return True
        except Exception as e:
            logger.error(f"Error adding subscriber: {e}")
            return False

    def remove_subscriber(self, email: str) -> bool:
        """Remove a subscriber"""
        try:
            with open(self.subscribers_file, "r") as f:
                data = json.load(f)

            for subscriber in data["subscribers"]:
                if subscriber["email"] == email:
                    subscriber["active"] = False

            with open(self.subscribers_file, "w") as f:
                json.dump(data, f, indent=2)

            logger.info(f"Removed subscriber: {email}")
            return True
        except Exception as e:
            logger.error(f"Error removing subscriber: {e}")
            return False


class NewsletterSender:
    """Sends newsletter emails"""

    def __init__(self):
        self.config = EmailConfig()
        self.subscriber_manager = SubscriberManager()

    def _create_connection(self):
        """Create SMTP connection"""
        try:
            server = smtplib.SMTP(self.config.smtp_server, self.config.smtp_port)
            server.starttls()
            if self.config.sender_email and self.config.sender_password:
                server.login(self.config.sender_email, self.config.sender_password)
            return server
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            return None

    def create_html_template(
        self, articles: List[dict], title: str = "DSEC AI Newsletter"
    ) -> str:
        """Create HTML template for newsletter"""
        articles_html = ""

        for i, article in enumerate(articles[:10], 1):  # Limit to 10 articles
            categories = ", ".join(article.get("Category", [])[:3])
            summary = article.get("summary", "No summary available")[:200] + "..."

            articles_html += f"""
            <div style="margin: 20px 0; padding: 15px; border-left: 4px solid #0066cc;">
                <h3 style="margin-top: 0; color: #333;">
                    <a href="{article.get("link", "#")}" style="color: #0066cc; text-decoration: none;">
                        {article.get("title", "Untitled")}
                    </a>
                </h3>
                <p style="color: #666; font-size: 14px; margin: 5px 0;">
                    <strong>Categories:</strong> {categories}
                </p>
                <p style="color: #888; font-size: 13px; margin: 5px 0;">
                    <strong>Published:</strong> {article.get("published", "N/A")}
                </p>
                <p style="color: #555; line-height: 1.6;">
                    {summary}
                </p>
                <a href="{article.get("link", "#")}" style="color: #0066cc; text-decoration: none; font-weight: bold;">
                    Read Full Article →
                </a>
            </div>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 700px; margin: 0 auto; }}
                .header {{ background-color: #0066cc; color: white; padding: 20px; text-align: center; }}
                .container {{ padding: 20px; }}
                .footer {{ background-color: #f5f5f5; padding: 15px; text-align: center; font-size: 12px; color: #666; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{title}</h1>
                <p>Your daily digest of AI and tech news</p>
            </div>
            
            <div class="container">
                <p>Hi there!</p>
                <p>Here are today's top stories in AI and technology:</p>
                {articles_html}
            </div>
            
            <div class="footer">
                <p>You're receiving this because you're subscribed to DSEC AI Newsletter.</p>
                <p><a href="{{unsubscribe_link}}" style="color: #0066cc;">Unsubscribe</a></p>
            </div>
        </body>
        </html>
        """

        return html_content

    def send_newsletter(
        self, articles: List[dict], test_email: Optional[str] = None
    ) -> dict:
        """
        Send newsletter to subscribers

        Args:
            articles: List of article dictionaries to include in newsletter
            test_email: If provided, send only to this email address (for testing)

        Returns:
            Dictionary with send statistics
        """
        if not self.config.sender_email or not self.config.sender_password:
            logger.error("SMTP credentials not configured")
            return {
                "success": 0,
                "failed": 0,
                "error": "SMTP credentials not configured",
            }

        recipients = (
            [test_email]
            if test_email
            else [s["email"] for s in self.subscriber_manager.load_subscribers()]
        )

        if not recipients:
            logger.warning("No recipients to send newsletter to")
            return {"success": 0, "failed": 0, "error": "No recipients"}

        html_content = self.create_html_template(articles)
        success_count = 0
        failed_count = 0

        server = self._create_connection()
        if not server:
            return {
                "success": 0,
                "failed": len(recipients),
                "error": "Failed to connect to SMTP",
            }

        try:
            for email in recipients:
                try:
                    msg = MIMEMultipart("alternative")
                    msg["Subject"] = (
                        f"DSEC AI Newsletter - {datetime.now().strftime('%B %d, %Y')}"
                    )
                    msg["From"] = (
                        f"{self.config.sender_name} <{self.config.sender_email}>"
                    )
                    msg["To"] = email

                    # Attach HTML
                    msg.attach(MIMEText(html_content, "html"))

                    server.send_message(msg)
                    logger.info(f"Newsletter sent to {email}")
                    success_count += 1
                except Exception as e:
                    logger.error(f"Failed to send to {email}: {e}")
                    failed_count += 1
        finally:
            server.quit()

        result = {
            "success": success_count,
            "failed": failed_count,
            "total": len(recipients),
            "timestamp": datetime.now().isoformat(),
        }

        logger.info(f"Newsletter sending complete: {result}")
        return result
