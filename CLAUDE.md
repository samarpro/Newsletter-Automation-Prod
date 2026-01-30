# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

DSEC AI Newsletter is an automated system that scrapes AI/tech articles from RSS feeds, extracts content using Playwright, and distributes newsletters via email. The project uses a density-based content extraction algorithm to find main article text.

## Commands

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv sync

# Install Playwright browsers (required for scraping)
playwright install chromium

# Run the scraper (fetches RSS feeds, scrapes article content)
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

# Lint
ruff check src/
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  1. RSS Discovery & Parsing (main.py)                       │
│     get_rss_urls() → discovers RSS from publisher HTML      │
│     get_articles_urls() → parses RSS, filters by category   │
├─────────────────────────────────────────────────────────────┤
│  2. Content Extraction (scraper.py)                         │
│     Scraper.scrape() → Playwright-based content extraction  │
│     find_content_by_density() → density algorithm to find   │
│     main content by analyzing text distribution in DOM      │
├─────────────────────────────────────────────────────────────┤
│  3. Newsletter Building (newsletter_builder.py)             │
│     Loads scraped_content.json + structured_facts.json      │
│     Builds newsletter object, saves to newsletter.json      │
├─────────────────────────────────────────────────────────────┤
│  4. Email Distribution (email_service.py)                   │
│     EmailConfig → SMTP settings from .env                   │
│     SubscriberManager → manages output/subscribers.json     │
│     NewsletterSender → generates HTML, sends via SMTP       │
└─────────────────────────────────────────────────────────────┘
```

## Key Files

- `src/main.py` - Entry point, RSS discovery, CLI commands
- `src/scraper.py` - Playwright scraper with density-based content detection
- `src/email_service.py` - SMTP sending, subscriber management
- `src/newsletter_builder.py` - Newsletter composition
- `src/newsletter_cli.py` - Full CLI tool
- `src/imports.py` - Centralized imports, defines `Article` TypedDict
- `config/publishers.yaml` - Publisher URLs for RSS discovery
- `config/rss_urls.yaml` - Direct RSS feed URLs
- `output/scraped_content.json` - Extracted articles with content
- `output/subscribers.json` - Subscriber database

## Content Extraction Algorithm

The scraper uses a density-based algorithm (`find_content_by_density`) that:
1. Removes noise tags (script, style, nav, footer, ads)
2. Filters elements with blacklisted class names
3. Traverses DOM layer-by-layer, finding child with highest word count
4. Stops when text is evenly distributed (no child has >60% of parent's text)

## Configuration

Environment variables in `.env`:
```bash
SMTP_SERVER="smtp.gmail.com"
SMTP_PORT="587"
SENDER_EMAIL="your-email@gmail.com"
SENDER_PASSWORD="xxxx xxxx xxxx xxxx"  # Gmail App Password
SENDER_NAME="DSEC AI Newsletter"
GROQ_API_KEY="..."
```

## Category Filtering

Articles are filtered by category keywords defined in `main.py:get_articles_urls()` including: AI, Machine Learning, Deep Learning, major tech companies (Nvidia, Google, Microsoft, OpenAI, Meta), and AI application domains.