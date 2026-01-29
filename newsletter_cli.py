#!/usr/bin/env python3
"""
CLI tool for managing newsletter operations
Usage:
  python newsletter_cli.py send          # Send to all subscribers
  python newsletter_cli.py test EMAIL    # Send test to specific email
  python newsletter_cli.py add EMAIL [NAME]  # Add subscriber
  python newsletter_cli.py remove EMAIL  # Remove subscriber
  python newsletter_cli.py list          # List all subscribers
"""

import sys
import os
import json
from dotenv import load_dotenv
from email_service import SubscriberManager, NewsletterSender
from newsletter_builder import NewsletterBuilder


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{'=' * 60}")
    print(f"  {text}")
    print(f"{'=' * 60}\n")


def cmd_send():
    """Send newsletter to all subscribers"""
    print_header("Sending Newsletter to All Subscribers")

    builder = NewsletterBuilder()
    sender = NewsletterSender()

    articles = builder.load_articles()
    if not articles:
        print("❌ No articles found!")
        return False

    print(f"📰 Found {len(articles)} articles")

    newsletter = builder.build_newsletter(articles=articles)
    builder.save_newsletter(newsletter)
    print(f"✅ Newsletter saved to newsletter.json")

    result = sender.send_newsletter(articles)
    print(f"\n📧 Newsletter Sending Results:")
    print(f"   Success: {result['success']}")
    print(f"   Failed: {result['failed']}")
    print(f"   Total: {result['total']}")
    print(f"   Timestamp: {result['timestamp']}")

    return result["success"] > 0


def cmd_test(test_email: str):
    """Send test newsletter to specific email"""
    print_header(f"Sending Test Newsletter to {test_email}")

    if not "@" in test_email or "." not in test_email:
        print("❌ Invalid email address!")
        return False

    builder = NewsletterBuilder()
    sender = NewsletterSender()

    articles = builder.load_articles()
    if not articles:
        print("❌ No articles found!")
        return False

    print(f"📰 Found {len(articles)} articles")
    result = sender.send_newsletter(articles, test_email=test_email)

    print(f"\n📧 Test Email Result:")
    print(f"   Sent to: {test_email}")
    print(f"   Status: {'✅ Success' if result['success'] > 0 else '❌ Failed'}")

    return result["success"] > 0


def cmd_add(email: str, name: str = ""):
    """Add subscriber"""
    print_header(f"Adding Subscriber")

    if not "@" in email or "." not in email:
        print("❌ Invalid email address!")
        return False

    manager = SubscriberManager()
    success = manager.add_subscriber(email, name)

    if success:
        print(f"✅ Successfully added: {email}")
        if name:
            print(f"   Name: {name}")
    else:
        print(f"❌ Failed to add subscriber (may already exist)")

    return success


def cmd_remove(email: str):
    """Remove subscriber"""
    print_header(f"Removing Subscriber")

    manager = SubscriberManager()
    success = manager.remove_subscriber(email)

    if success:
        print(f"✅ Successfully removed: {email}")
    else:
        print(f"❌ Failed to remove subscriber")

    return success


def cmd_list():
    """List all subscribers"""
    print_header("Active Subscribers")

    manager = SubscriberManager()
    subscribers = manager.load_subscribers()

    if not subscribers:
        print("No active subscribers found.")
        return True

    print(f"Total: {len(subscribers)} subscriber(s)\n")
    for i, sub in enumerate(subscribers, 1):
        name = sub.get("name", "N/A")
        email = sub["email"]
        date = sub.get("subscribed_at", "N/A")[:10]
        print(f"{i}. {email}")
        print(f"   Name: {name}")
        print(f"   Added: {date}\n")

    return True


def cmd_stats():
    """Show newsletter statistics"""
    print_header("Newsletter Statistics")

    manager = SubscriberManager()
    builder = NewsletterBuilder()

    subscribers = manager.load_subscribers()
    articles = builder.load_articles()
    structured_facts = builder.load_structured_facts()

    print(f"📊 Statistics:")
    print(f"   Active Subscribers: {len(subscribers)}")
    print(f"   Available Articles: {len(articles)}")
    print(f"   Structured Facts: {len(structured_facts)}")

    if os.path.exists("newsletter.json"):
        with open("newsletter.json", "r") as f:
            last_newsletter = json.load(f)
        print(f"\n📋 Last Newsletter:")
        print(f"   Generated: {last_newsletter.get('generated_at', 'N/A')}")
        print(f"   Articles: {last_newsletter.get('article_count', 0)}")

    return True


def print_help():
    """Print help message"""
    print("""
DSEC AI Newsletter CLI
======================

Commands:
  send                Send newsletter to all subscribers
  test EMAIL          Send test newsletter to specific email
  add EMAIL [NAME]    Add new subscriber
  remove EMAIL        Remove subscriber
  list                List all active subscribers
  stats               Show newsletter statistics
  help                Show this help message

Examples:
  python newsletter_cli.py send
  python newsletter_cli.py test user@example.com
  python newsletter_cli.py add john@example.com "John Doe"
  python newsletter_cli.py remove john@example.com
  python newsletter_cli.py list
  python newsletter_cli.py stats
""")


def main():
    """Main CLI entry point"""
    load_dotenv()

    if len(sys.argv) < 2:
        print_help()
        return 1

    command = sys.argv[1].lower()

    try:
        if command == "send":
            success = cmd_send()
        elif command == "test":
            if len(sys.argv) < 3:
                print("❌ Please provide an email address for test")
                print("   Usage: python newsletter_cli.py test EMAIL")
                return 1
            success = cmd_test(sys.argv[2])
        elif command == "add":
            if len(sys.argv) < 3:
                print("❌ Please provide an email address")
                print("   Usage: python newsletter_cli.py add EMAIL [NAME]")
                return 1
            name = sys.argv[3] if len(sys.argv) > 3 else ""
            success = cmd_add(sys.argv[2], name)
        elif command == "remove":
            if len(sys.argv) < 3:
                print("❌ Please provide an email address")
                print("   Usage: python newsletter_cli.py remove EMAIL")
                return 1
            success = cmd_remove(sys.argv[2])
        elif command == "list":
            success = cmd_list()
        elif command == "stats":
            success = cmd_stats()
        elif command == "help":
            print_help()
            return 0
        else:
            print(f"❌ Unknown command: {command}")
            print("Use 'help' to see available commands")
            return 1

        return 0 if success else 1

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
