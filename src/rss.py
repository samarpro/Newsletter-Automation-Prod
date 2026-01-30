import feedparser
import requests
import yaml
import bs4

# having a list of publishers from a YAML file
# using request lib to fetch the HTML content of each publisher's page
# looking of RSS feed link in the HTML content
# if found then we have list of fresh articles from that RSS feed
# storing the articles in a structured format

## commented out because rss_urls already hardcoded below
# publishers = yaml.safe_load(open('publishers.yaml'))['publishers']
# rss_urls = []
# for publisher in publishers:
#     response = requests.get(publisher)
#     html = response.text
#     bs4_html = bs4.BeautifulSoup(html, 'html.parser')
#     head: bs4.element.Tag | None = bs4_html.find('head')
#     if head:
#        rss_link = head.find('link', type='application/rss+xml')
#        if rss_link and rss_link.has_attr('href'):
#            rss_urls.append(rss_link['href'])
           
rss_urls = ['https://www.theguardian.com/uk/technology/rss', 'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/international/section/technology/rss.xml', 'https://www.wired.com/feed/category/business/latest/rss', 'https://techcrunch.com/feed/', 'https://techcrunch.com/feed/', 'https://techcrunch.com/feed/']

# now the using rss urls to fetch articles
for url in rss_urls[::-1]:
    feed = feedparser.parse(url)
    print("Number of entries found:", len(feed.entries))
    for entry in feed.entries:

        article = {
            'title': entry.title,
            'category': entry.category
        }
        print(article)   
        