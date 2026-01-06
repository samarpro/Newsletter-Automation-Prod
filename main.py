from scraper import Scraper
import yaml

print("Starting scraper...")
def main():
    yaml_file = 'urls.yaml'
    with open(yaml_file, 'r') as f:
        urls = yaml.safe_load(f)['urls'] 
    print(urls)
    scraper = Scraper()
    scraper.scrape(urls)
    scraper.close()
if __name__ == "__main__":
    main()
