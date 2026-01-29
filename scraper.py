from imports import sync_playwright,  html, BeautifulSoup as bs4, Article, json
import re
import traceback

class Scraper:
    """A web scraper using Playwright to fetch and interact with web pages.
    """
    def __init__(self) -> None:
        """Initializes the Playwright browser and page."""
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.noise_tags = ["script", "style", "noscript", "header", "footer", "meta", "link", "aside", "svg", "img", "nav"]
        self.blacklist_words = ["comment", "footer", "header", "nav", "sidebar", "advert", "ads", "sponsor", "related", "popup", "subscribe", "share", "widget", "breadcrumb", "cookie", "consent", "banner", "tool", "button", "form", "input", "search", "login", "signup","cta", "menu", "social", "follow", "like", "dislike", "rating", "review", "feedback", "poll", "survey", "tag", "tags", "category", "categories","newsletter", "archive", "copyright", "terms", "privacy", "policy", "disclaimer", "sitemap", "faq", "help", "support", "contact"]
        # Set a realistic user agent to avoid being blocked
        self.page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        })
    
    def find_content_by_density(self, tree, threshold=0.6):
        """Find the main content container by analyzing text density layer by layer.
        The Thresold signifies the minimum ratio of text in a child element compared to its parent
        to continue drilling down.
        
        Args:
            tree: lxml element tree (already cleaned of noise tags)
            threshold: If no child has more than this % of parent's text, stop drilling down
        
        Returns:
            The element containing the main content
        """
        def count_words(element):
            """Count words in an element's text content."""
            text = element.text_content().strip()
            return len(text.split())
        
        current = tree
        
        while True:
            children = list(current)
            # children is all the tags
            # iterare through all the children
            # and check if class name contains blacklist words
            # if it does, count the number of words in the child
            # subtract that from the parent's word count
            # new parent word count = parent word count - child (blacklisted) word count
            
            # If no children, we've reached a leaf - return current
            if not children:
                print(f"Reached leaf element: {current.tag}")
                return current
            
            # Count words in each child
            pattern = r"(^|[\s_-])(" + "|".join(map(re.escape, self.blacklist_words)) + r")(?=$|[\s_-])"
            regex = re.compile(pattern, re.IGNORECASE)
            child_word_counts = []

            for child in children:
                if not isinstance(child, html.HtmlElement):
                    continue

                if regex.search(child.get('class', '')):
                    current.remove(child)
                    continue
                # Filter out children with very few words (likely not content)
                if (word_count:=count_words(child)) < 20:
                    continue

                child_word_counts.append((child, word_count))

    
            
            if not child_word_counts:
                print(f"No children with substantial text in {current.tag}")
                return current
            
            # Find child with most words
            max_child, max_words = max(child_word_counts, key=lambda x: x[1])
            parent_words = count_words(current)
            
            # Calculate what percentage of parent's text is in the max child
            if parent_words > 0:
                max_ratio = max_words / parent_words
            else:
                return current
            
            print(f"Layer: {current.tag}, class:{current.get('class')} children: {len(children)}, max child: {max_child.tag} ({max_words} words, {max_ratio:.2%} of parent)")
            
            # If no single child dominates (text is evenly distributed), stop
            if max_ratio <=threshold:
                print(f"Text evenly distributed, stopping at {current.tag}")
                return current
            
            # Otherwise, drill down into the child with most text
            current = max_child
        
        return current
        
    def check_rss(self, url:str) -> bool:
        # redundant now, may be useful later
        """Check if the given URL points to an RSS feed by looking for common RSS tags.
        
        Args:
            url: The URL to check."""
        try:
            self.page.goto(url, wait_until="domcontentloaded")
            page_content = self.page.content()
            soup = bs4(page_content, 'html.parser')
            rss_tags = ['rss', 'feed', 'channel', 'item']
            for tag in rss_tags:
                if soup.find(tag):
                    print(f"RSS feed detected at {url} due to presence of <{tag}> tag.")
                    return True
            return False
        except Exception as e:
            print(f"Error checking RSS for {url}: {e}")
            return False

    def scrape(self, articles:list[Article]) -> bool:
        output = []
        for _, article in enumerate(articles):
            url = article['link']
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                page_content = self.page.content()
                
                # Parse with lxml and remove noise tags from the entire tree
                tree = html.fromstring(page_content)
                for tag in self.noise_tags:
                    noise_elements = tree.xpath(f'//{tag}')
                    for el in noise_elements:
                        el.getparent().remove(el)
            
                print(f"\n=== Analyzing {url} ===")
                
                # Use density-based content detection
                content_element = self.find_content_by_density(tree, threshold=0.6)
                extracted_text = content_element.text_content().strip()
                article['content'] = extracted_text
                print(f"Chracter count from {url}: {len(extracted_text)}\n")
                print(f"Word count from {url}: {len(extracted_text.split())}\n")
                print("success...", _+1)              
                
            except Exception as e:

                print(f"Error navigating to {url}: \n {e} {traceback.format_exc()}\n")
                print(f"Failed...", _+1)
                continue
            
        with open(output_file:="scraped_content.json", 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4
                      )
        return True
        
    def close(self) -> None:
        self.browser.close()
        self.pw.stop()
        
    
        
    