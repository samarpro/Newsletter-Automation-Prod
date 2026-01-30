# Newsletter Feature - Quick Start Guide

## 5-Minute Setup

### Step 1: Configure Email (Gmail Example)

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer"
3. Copy the 16-character password

4. Update `.env` file:
```bash
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
SENDER_EMAIL="your-email@gmail.com"
SENDER_PASSWORD="xxxx xxxx xxxx xxxx"  # The 16-char password you copied
SENDER_NAME="DSEC AI Newsletter"
```

### Step 2: Add Subscribers

```bash
# Activate virtual environment
source .venv/bin/activate

# Add subscribers
python newsletter_cli.py add john@example.com "John Doe"
python newsletter_cli.py add jane@example.com "Jane Smith"

# List subscribers
python newsletter_cli.py list
```

### Step 3: Test Email

Send a test newsletter to yourself:

```bash
python newsletter_cli.py test your-email@gmail.com
```

Check your inbox! You should see a formatted newsletter with the latest articles.

### Step 4: Send to All Subscribers

Once you've verified the test email:

```bash
python newsletter_cli.py send
```

## Useful Commands

```bash
# View all available commands
python newsletter_cli.py help

# Show statistics
python newsletter_cli.py stats

# Remove a subscriber
python newsletter_cli.py remove john@example.com
```

## Integrate with Main Workflow

After scraping articles:

```bash
# 1. Run the scraper (generates scraped_content.json)
python main.py

# 2. Send newsletter to all subscribers
python newsletter_cli.py send
```

Or in Python:

```python
from main import main, send_newsletter

# Scrape articles
main()

# Send newsletter
send_newsletter()
```

## Common Issues & Solutions

### "SMTP credentials not configured"
- Check `.env` file has `SENDER_EMAIL` and `SENDER_PASSWORD`
- Make sure you're using the 16-char App Password from Google, not your account password

### "Failed to connect to SMTP server"
- Verify `SMTP_SERVER` and `SMTP_PORT` are correct
- For Gmail: use `smtp.gmail.com:587`

### "No articles found"
- Run `python main.py` first to generate `scraped_content.json`
- Check that articles were scraped

### "No recipients to send newsletter to"
- Add subscribers with `python newsletter_cli.py add EMAIL NAME`

## Newsletter Template

The newsletter includes:
- ✅ Professional header with title
- ✅ Up to 10 latest articles
- ✅ Article titles (clickable links)
- ✅ Categories and publication dates
- ✅ Article summaries (200 chars)
- ✅ Read more links
- ✅ Responsive design for mobile/desktop

## For Production Use

1. **Use App Passwords**: Never use your actual account password
2. **Test First**: Always test with your own email before sending to subscribers
3. **Backup Data**: Keep backups of `subscribers.json`
4. **Monitor Results**: Check sending statistics
5. **Rate Limit**: Respect SMTP provider rate limits
6. **Archive**: Check `newsletter.json` for last sent newsletter

## Next Steps

- Read full documentation: `NEWSLETTER.md`
- Explore module APIs: `email_service.py`, `newsletter_builder.py`
- Customize newsletter template in `email_service.py` (line ~132)
- Set up automatic scheduling (see NEWSLETTER.md for future enhancements)

## Support

For issues or questions:
1. Check NEWSLETTER.md for detailed documentation
2. Review the specific module docstrings
3. Enable debug logging: `import logging; logging.basicConfig(level=logging.DEBUG)`
