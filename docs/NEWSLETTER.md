# Newsletter Feature Documentation

## Overview

The newsletter feature allows you to automatically generate and send newsletters from structured facts and scraped articles to a list of email subscribers.

## Architecture

The newsletter system consists of three main components:

### 1. **Email Service** (`email_service.py`)
- **EmailConfig**: Manages SMTP configuration from environment variables
- **SubscriberManager**: Handles subscriber management (add, remove, list)
- **NewsletterSender**: Sends HTML emails via SMTP

### 2. **Newsletter Builder** (`newsletter_builder.py`)
- Loads articles from `scraped_content.json`
- Loads structured facts from `structured_facts.json`
- Generates newsletter content
- Saves newsletter to JSON for archival

### 3. **CLI Tool** (`newsletter_cli.py`)
- User-friendly command-line interface
- Subscriber management
- Newsletter sending with testing capabilities

## Configuration

### Environment Variables

Add these to your `.env` file:

```bash
# Email Configuration
SMTP_SERVER="smtp.gmail.com"          # SMTP server address
SMTP_PORT="587"                        # SMTP port (587 for TLS, 465 for SSL)
SENDER_EMAIL="your-email@gmail.com"   # Sender email address
SENDER_PASSWORD="your-app-password"   # App-specific password
SENDER_NAME="DSEC AI Newsletter"       # Display name
```

### Gmail Setup (Recommended)

For Gmail:
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer" (or your device)
   - Copy the generated 16-character password
3. Use this password as `SENDER_PASSWORD` in `.env`

### Other Email Providers

- **Outlook**: Use `smtp-mail.outlook.com:587`
- **SendGrid**: Use `smtp.sendgrid.net:587` (use `apikey` as username)
- **AWS SES**: Use `email-smtp.[region].amazonaws.com:587`

## Usage

### Command Line Interface

```bash
# View help
python newsletter_cli.py help

# Send newsletter to all subscribers
python newsletter_cli.py send

# Send test newsletter to specific email
python newsletter_cli.py test user@example.com

# Add subscriber
python newsletter_cli.py add john@example.com "John Doe"

# Remove subscriber
python newsletter_cli.py remove john@example.com

# List all subscribers
python newsletter_cli.py list

# Show statistics
python newsletter_cli.py stats
```

### Python API

```python
from main import send_newsletter, add_subscriber, remove_subscriber, list_subscribers

# Send to all subscribers
result = send_newsletter()

# Send test newsletter
result = send_newsletter(test_email="user@example.com")

# Manage subscribers
add_subscriber("john@example.com", "John Doe")
remove_subscriber("john@example.com")
list_subscribers()
```

Or use directly from modules:

```python
from email_service import SubscriberManager, NewsletterSender
from newsletter_builder import NewsletterBuilder

# Manage subscribers
manager = SubscriberManager()
subscribers = manager.load_subscribers()
manager.add_subscriber("email@example.com", "Name")

# Build and send newsletter
builder = NewsletterBuilder()
newsletter = builder.build_newsletter()

sender = NewsletterSender()
result = sender.send_newsletter(newsletter['articles'])
```

## Data Files

### subscribers.json
Stores the list of newsletter subscribers:

```json
{
  "subscribers": [
    {
      "email": "user@example.com",
      "name": "User Name",
      "subscribed_at": "2026-01-29T12:00:00",
      "active": true
    }
  ]
}
```

### newsletter.json
Archive of the last generated newsletter:

```json
{
  "title": "DSEC AI Newsletter - January 29, 2026",
  "generated_at": "2026-01-29T12:00:00",
  "articles": [...],
  "structured_facts": [...],
  "article_count": 42,
  "facts_count": 0
}
```

## Newsletter Template

The newsletter HTML template includes:

- **Header**: Newsletter title and description
- **Articles**: Up to 10 articles with:
  - Title (clickable link)
  - Categories
  - Publication date
  - Summary snippet (200 chars)
  - Read more link
- **Footer**: Unsubscribe information

The template is responsive and styled for modern email clients.

## Error Handling

The system includes comprehensive error handling:

- **Missing Configuration**: Logs warning if SMTP credentials are not configured
- **Connection Failures**: Returns error message if SMTP connection fails
- **Invalid Email**: Checks email format before sending
- **Duplicate Subscribers**: Prevents adding duplicate email addresses
- **File I/O Errors**: Catches and logs all file operation errors

## Workflow Integration

### Full Pipeline

```bash
# 1. Scrape articles and generate content
python main.py

# 2. Add subscribers (one-time setup)
python newsletter_cli.py add subscriber1@example.com "Name 1"
python newsletter_cli.py add subscriber2@example.com "Name 2"

# 3. Send test newsletter
python newsletter_cli.py test youraddress@example.com

# 4. Send to all subscribers
python newsletter_cli.py send
```

### Automatic Integration

Integrate into your main workflow:

```python
from main import main, send_newsletter

# Run scraper
main()

# Send newsletter after scraping
send_newsletter()
```

## Logging

The system logs all operations:

- Subscriber additions/removals
- Newsletter sending attempts
- SMTP connection issues
- File I/O errors

Enable debug logging in modules:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Troubleshooting

### "SMTP credentials not configured"
- Add `SENDER_EMAIL` and `SENDER_PASSWORD` to `.env`
- Reload environment with `dotenv.load_dotenv()`

### "Failed to connect to SMTP server"
- Check `SMTP_SERVER` and `SMTP_PORT` in `.env`
- Verify internet connection
- For Gmail, use App Password (not account password)

### "No recipients to send newsletter to"
- Add subscribers using `python newsletter_cli.py add EMAIL`
- Check `subscribers.json` file exists and is valid JSON

### "No articles found for newsletter"
- Run `python main.py` to scrape articles first
- Check `scraped_content.json` is not empty

## Best Practices

1. **Test First**: Always test with `python newsletter_cli.py test YOUR_EMAIL` before sending to all
2. **Monitor Results**: Check the sending statistics returned
3. **Backup Subscribers**: Keep backups of `subscribers.json`
4. **Use App Passwords**: For Gmail, use App Password not your account password
5. **Rate Limiting**: Space out newsletter sends to avoid SMTP rate limits
6. **Content Fresh**: Ensure `scraped_content.json` is updated before sending

## Advanced Configuration

### Custom SMTP Server

For self-hosted SMTP or custom providers:

```bash
SMTP_SERVER="mail.yourdomain.com"
SMTP_PORT="587"  # or 465 for SSL
SENDER_EMAIL="newsletter@yourdomain.com"
SENDER_PASSWORD="your-password"
```

### Sender Customization

Customize sender name:

```bash
SENDER_NAME="Your Newsletter Name"
```

This appears in the "From:" field as:
```
Your Newsletter Name <sender@email.com>
```

## Future Enhancements

Potential improvements:

- [ ] Database support (SQLite, PostgreSQL)
- [ ] Subscriber preferences (frequency, categories)
- [ ] Scheduled sending (cron integration)
- [ ] Email templates with user customization
- [ ] Delivery tracking and analytics
- [ ] Unsubscribe link functionality
- [ ] SPF/DKIM configuration guide
- [ ] Attachment support
- [ ] Multi-language support
- [ ] A/B testing

## License

Part of DSEC AI Newsletter project.
