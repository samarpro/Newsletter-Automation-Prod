"""
Newsletter builder - converts structured facts and articles into newsletters
"""

import json
import logging
from typing import List, Optional
from datetime import datetime
from email_service import NewsletterSender

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class NewsletterBuilder:
    """Builds newsletters from structured facts and articles"""

    def __init__(
        self,
        structured_facts_file: str = "structured_facts.json",
        scraped_content_file: str = "scraped_content.json",
    ):
        self.structured_facts_file = structured_facts_file
        self.scraped_content_file = scraped_content_file

    def load_structured_facts(self) -> List[dict]:
        """Load structured facts from JSON file"""
        try:
            with open(self.structured_facts_file, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            logger.warning(
                f"Structured facts file not found: {self.structured_facts_file}"
            )
            return []
        except Exception as e:
            logger.error(f"Error loading structured facts: {e}")
            return []

    def load_articles(self) -> List[dict]:
        """Load articles from scraped content"""
        try:
            with open(self.scraped_content_file, "r") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except FileNotFoundError:
            logger.warning(
                f"Scraped content file not found: {self.scraped_content_file}"
            )
            return []
        except Exception as e:
            logger.error(f"Error loading articles: {e}")
            return []

    def build_newsletter(
        self,
        articles: Optional[List[dict]] = None,
        structured_facts: Optional[List[dict]] = None,
    ) -> dict:
        """
        Build newsletter content from articles and facts

        Args:
            articles: List of article dicts (uses scraped_content.json if None)
            structured_facts: List of fact dicts (uses structured_facts.json if None)

        Returns:
            Dictionary with newsletter content
        """
        if articles is None:
            articles = self.load_articles()
        if structured_facts is None:
            structured_facts = self.load_structured_facts()

        newsletter = {
            "title": f"DSEC AI Newsletter - {datetime.now().strftime('%B %d, %Y')}",
            "generated_at": datetime.now().isoformat(),
            "articles": articles[:10],  # Top 10 articles
            "structured_facts": structured_facts,
            "article_count": len(articles),
            "facts_count": len(structured_facts),
        }

        return newsletter

    def save_newsletter(
        self, newsletter: dict, filename: str = "newsletter.json"
    ) -> bool:
        """Save newsletter to JSON file"""
        try:
            with open(filename, "w") as f:
                json.dump(newsletter, f, indent=2)
            logger.info(f"Newsletter saved to {filename}")
            return True
        except Exception as e:
            logger.error(f"Error saving newsletter: {e}")
            return False


def send_newsletter_to_subscribers(test_email: Optional[str] = None) -> dict:
    """
    Main function to build and send newsletter

    Args:
        test_email: If provided, sends only to this email for testing

    Returns:
        Dictionary with sending results
    """
    builder = NewsletterBuilder()
    sender = NewsletterSender()

    # Build newsletter
    newsletter = builder.build_newsletter()

    if not newsletter["articles"]:
        logger.warning("No articles found for newsletter")
        return {"error": "No articles found"}

    # Save newsletter
    builder.save_newsletter(newsletter)

    # Send to subscribers
    result = sender.send_newsletter(newsletter["articles"], test_email=test_email)

    return result


if __name__ == "__main__":
    # Example usage
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Test mode - send to specific email
        test_email = sys.argv[2] if len(sys.argv) > 2 else "test@example.com"
        print(f"Sending test newsletter to {test_email}...")
        result = send_newsletter_to_subscribers(test_email=test_email)
    else:
        # Production mode - send to all subscribers
        print("Sending newsletter to all subscribers...")
        result = send_newsletter_to_subscribers()

    print(json.dumps(result, indent=2))
