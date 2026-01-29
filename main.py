from imports import sync_playwright,  html, BeautifulSoup as bs4, yaml, requests, feedparser, Article, json, Client, os, dotenv
from scraper import Scraper


# getting URL of sites to get their RSS feed link
def get_rss_urls(publishers:list[str]) -> list[str]:
    """
    Given a list of publisher URLs, extract RSS links from their HTML content."""
    rss_url = set()
    for publisher in publishers:
        try:
            response = requests.get(publisher)
            html_content = response.text
            soup = bs4(html_content, 'html.parser')
            head = soup.find('head')
            if head:
                rss_link = head.find('link', type='application/rss+xml')
                if rss_link and rss_link.has_attr('href'):
                    rss_url.add(rss_link['href'])
                    print(f"Found RSS link for {publisher}: {rss_link['href']}")
                else:
                    print(f"No RSS link found in head for {publisher}")
            else:
                print(f"No head tag found for {publisher}")
        except Exception as e:
            print(f"Error processing {publisher}: {e}")
            
    return list(rss_url)

def get_articles_urls(rss_urls:list[str]) -> list[Article]:
    """Given a list of RSS feed URLs, fetch articles from each feed."""
    articles = []
    for url in rss_urls:
        try:
            feed = feedparser.parse(url)
            print(f"Number of entries found in {url[10]}...: {len(feed.entries)}")
            category_set = ["Nvidia", "Google", "Microsoft", "OpenAI", "Meta", "Amazon", "AI", "Artificial Intelligence", "Machine Learning", "Deep Learning", "Neural Networks", "NLP", "Computer Vision", "Robotics", "Data Science", "Big Data", "Analytics", "Tech Giants", "Startups", "Innovation", "Research", "Development", "Cloud Computing", "Edge Computing", "Quantum Computing", "Automation", "Ethics in AI", "AI Policy", "AI Trends", "Elon Musk", "Sam Altman", "AI Funding", "AI Acquisitions", "AI Partnerships", "AI Products", "AI Services", "AI Platforms", "AI Tools", "AI Frameworks", "AI Libraries", "AI Chips", "AI Hardware", "AI Software", "AI Applications", "AI Use Cases", "AI in Healthcare", "AI in Finance", "AI in Education", "AI in Transportation", "AI in Manufacturing", "AI in Retail", "AI in Entertainment", "AI in Gaming", "AI", "Technology"]
            for entry in feed.entries:
                category = [tag.term for tag in entry.tags] if 'tags' in entry else []
                if not any(cat in category_set for cat in category):
                    continue
                article = {
                    'title': entry.title,
                    'link': entry.link,
                    'Category': category,
                    'published': entry.get('published', 'N/A'),
                    'summary': entry.get('summary', 'N/A')
                }
                print(article['Category'])
                articles.append(article)
        except Exception as e:
            print(f"Error fetching articles from {url}: {e}")
    return articles
def main():
    print(os.environ.get('GROQ_API_KEY'))
    groq = Client(api_key=os.environ.get('GROQ_API_KEY'))
    try:
        with open("publishers.yaml", 'r') as f:
            publishers = yaml.safe_load(f)['publishers']
    except Exception as e:
        print(f"Error loading publishers.yaml: {e}")
        publishers = []

    if not publishers:
        print("No publishers found in publishers.yaml")
        return
    
    rss_urls = get_rss_urls(publishers)
    articles = get_articles_urls(rss_urls)
    scraper = Scraper()

    content = scraper.scrape(articles)
    
    if not content:
        print("No content scraped.")
        return
    
    # load scraped_content.json
    with open("scraped_content.json", 'r', encoding='utf-8') as f:
        scraped_articles = json.load(f) 


if __name__ == "__main__":
    dotenv.load_dotenv()
    main()
    
    
    
