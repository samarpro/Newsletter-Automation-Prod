from .imports import sync_playwright, envs, BeautifulSoup as bs4, lxml
from lxml import html

class Scraper:
    """A web scraper using Playwright to fetch and interact with web pages.
    """
    def __init__(self) -> None:
        """Initializes the Playwright browser and page."""
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.noise_tags = ["script", "style", "noscript", "header", "footer", "meta", "link", "aside", "svg", "img", "nav"]
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
            
            # If no children, we've reached a leaf - return current
            if not children:
                print(f"Reached leaf element: {current.tag}")
                return current
            
            # Count words in each child
            child_word_counts = [(child, count_words(child)) for child in children]
            
            # Filter out children with very few words (likely not content)
            child_word_counts = [(child, wc) for child, wc in child_word_counts if wc > 10]
            
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
            
            print(f"Layer: {current.tag}, children: {len(children)}, max child: {max_child.tag} ({max_words} words, {max_ratio:.2%} of parent)")
            
            # If no single child dominates (text is evenly distributed), stop
            if max_ratio < threshold:
                print(f"Text evenly distributed, stopping at {current.tag}")
                return current
            
            # Otherwise, drill down into the child with most text
            current = max_child
        
        return current
        
    
    def scrape(self, urls:list[str]) -> str:
        with open("output.txt", 'w') as f:
            for _, url in enumerate(urls):
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
                    content_element = self.find_content_by_density(tree, threshold=0.5)
                    extracted_text = content_element.text_content().strip()
                    
                    print(f"Chracter count from {url}: {len(extracted_text)}\n")
                    print("success...", _+1)
                    f.writelines(f"URL: {url}\n")
                    f.writelines(extracted_text)
                    # f.writelines("\n".join(extracted_text))
                    f.writelines("\n" + "="*50 + "\n")                
                    
                except Exception as e:
                    f.write(f"URL: {url}\n")
                    f.write(f"Error navigating to {url}: {e}\n")
                    print(f"Failed...", _+1)
                    continue
        return ''
        
    def close(self) -> None:
        self.browser.close()
        self.pw.stop()
        
    
        
    