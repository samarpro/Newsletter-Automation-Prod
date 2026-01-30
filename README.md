# DSEC AI Newsletter

## Overview

DSEC AI Newsletter is an automated system that scrapes AI/tech articles from RSS feeds, extracts content using Playwright, and distributes newsletters via email. The project uses a density-based content extraction algorithm to find main article text.

## Project Structure

```
DSEC-AI-newsletter/
├── src/                    # Python source code
│   ├── main.py             # Main entry point, RSS discovery, CLI commands
│   ├── imports.py          # Centralized imports, defines Article TypedDict
│   ├── scraper.py          # Playwright scraper with density-based content detection
│   ├── email_service.py    # SMTP sending, subscriber management
│   ├── newsletter_builder.py # Newsletter composition
│   ├── newsletter_cli.py   # Full CLI tool for newsletter operations
│   └── rss.py             # RSS utilities
│
├── config/                 # Configuration files
│   ├── publishers.yaml     # Publisher URLs for RSS discovery
│   ├── rss_urls.yaml       # Direct RSS feed URLs
│   └── articles_urls.yaml # Generated article URLs
│
├── output/                 # Generated outputs
│   ├── newsletter.json     # Latest newsletter
│   ├── scraped_content.json # Extracted articles with content
│   ├── structured_facts.json # AI-structured facts
│   └── subscribers.json   # Subscriber database
│
├── docs/                   # Documentation
│   ├── NEWSLETTER.md       # Newsletter feature documentation
│   ├── NEWSLETTER_QUICKSTART.md # Quick start guide
│   └── GEMINI.md          # Gemini integration notes
│
├── notebooks/              # Jupyter notebooks
│   ├── main.ipynb         # Main development notebook
│   └── trial.ipynb        # Experiment notebook
│
├── .env                    # Environment variables (not tracked)
├── README.md               # This file
├── pyproject.toml          # Python project configuration
├── requirements.txt        # Dependencies
└── uv.lock               # Dependency lock file
```

## Architecture

### 1. **RSS Discovery & Parsing** (main.py)
- `get_rss_urls()` → discovers RSS from publisher HTML
- `get_articles_urls()` → parses RSS, filters by category

### 2. **Content Extraction** (scraper.py)
- `Scraper.scrape()` → Playwright-based content extraction
- `find_content_by_density()` → density algorithm to find main content

### 3. **Newsletter Building** (newsletter_builder.py)
- Loads scraped_content.json + structured_facts.json
- Builds newsletter object, saves to newsletter.json

### 4. **Email Distribution** (email_service.py)
- `EmailConfig` → SMTP settings from .env
- `SubscriberManager` → manages subscribers.json
- `NewsletterSender` → generates HTML, sends via SMTP

## Installation & Setup

### Prerequisites
- Python 3.8+
- Gmail account (for email sending)

### Quick Setup
```bash
# Clone and setup
git clone <repository>
cd DSEC-AI-newsletter

# Install dependencies
source .venv/bin/activate
uv sync

# Install Playwright browsers
playwright install chromium

# Configure environment
cp .env.example .env
# Edit .env with your credentials

# Run the scraper
python src/main.py

# Send test email
python src/main.py test your@email.com
```

### Environment Configuration
```bash
# Create .env file with:
GROQ_API_KEY="your-groq-api-key"
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
SENDER_EMAIL="your-email@gmail.com"
SENDER_PASSWORD="xxxx xxxx xxxx xxxx"  # Gmail App Password
SENDER_NAME="DSEC AI Newsletter"
```

## Usage

### Command Line Interface
```bash
# Run scraper (fetch RSS feeds, scrape articles)
python src/main.py

# Full pipeline: scrape articles then send newsletter
python src/main.py send

# Send test email to verify setup
python src/main.py test your@email.com

# CLI for newsletter operations
python src/newsletter_cli.py help
python src/newsletter_cli.py send          # Send to all subscribers
python src/newsletter_cli.py test EMAIL    # Test send
python src/newsletter_cli.py add EMAIL     # Add subscriber
python src/newsletter_cli.py list          # List subscribers
python src/newsletter_cli.py stats         # Show statistics
```

### Category Filtering
Articles are filtered by category keywords including:
- AI, Machine Learning, Deep Learning
- Major tech companies (Nvidia, Google, Microsoft, OpenAI, Meta)
- AI application domains
- Technology, Innovation, Research

## Content Extraction Algorithm

The scraper uses a density-based algorithm that:
1. Removes noise tags (script, style, nav, footer, ads)
2. Filters elements with blacklisted class names
3. Traverses DOM layer-by-layer, finding child with highest word count
4. Stops when text is evenly distributed (no child has >60% of parent's text)

## Development

### Running Tests
```bash
# Lint code
ruff check src/

# Run with different options
python src/main.py --help
python src/newsletter_cli.py --help
```

### Adding New Publishers
Edit `config/publishers.yaml` to add new publisher URLs for RSS discovery.

### Customizing Categories
Modify category keywords in `src/main.py:get_articles_urls()`.

## Gmail App Password Setup
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password:
   - Go to https://myaccount.google.com/apppasswords
   - Select "Mail" and "Windows Computer"
   - Copy the generated 16-character password
3. Use this password as `SENDER_PASSWORD` in `.env`

## File Formats

### Article Structure
```python
class Article(TypedDict):
    title: str
    link: str
    Category: List[str]
    published: str
    summary: str
    content: str
    ai_content: str
```

### Newsletter Output
```json
{
  "title": "DSEC AI Newsletter - January 29, 2026",
  "generated_at": "2026-01-29T12:00:00",
  "articles": [...],
  "structured_facts": [...],
  "article_count": 42,
  "facts_count": 10
}
```

## CLI Commands Reference

### Newsletter Management
- `add EMAIL [NAME]` - Add new subscriber
- `remove EMAIL` - Remove subscriber
- `list` - List all active subscribers
- `stats` - Show newsletter statistics
- `send` - Send newsletter to all subscribers
- `test EMAIL` - Send test newsletter
- `help` - Show help message

### Example Workflow
```bash
# 1. Scrape articles
python src/main.py

# 2. Add subscribers
python src/newsletter_cli.py add user@example.com "John Doe"

# 3. Test email
python src/newsletter_cli.py test your-email@example.com

# 4. Send newsletter
python src/newsletter_cli.py send
```

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
