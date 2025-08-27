import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path

# Target website (free test site)
URL = "http://quotes.toscrape.com/"

def scrape_quotes(url):
    all_quotes = []
    page = 1
    
    while True:
        response = requests.get(url + f"page/{page}/")
        if response.status_code != 200:
            break
        
        soup = BeautifulSoup(response.text, "html.parser")
        quotes = soup.find_all("div", class_="quote")
        
        if not quotes:
            break
        
        for q in quotes:
            text = q.find("span", class_="text").get_text(strip=True)
            author = q.find("small", class_="author").get_text(strip=True)
            tags = [t.get_text(strip=True) for t in q.find_all("a", class_="tag")]
            all_quotes.append({"text": text, "author": author, "tags": ",".join(tags)})
        
        page += 1
    
    return pd.DataFrame(all_quotes)

if __name__ == "__main__":
    print("Scraping started...")
    df = scrape_quotes(URL)
    
    Path("data").mkdir(exist_ok=True)
    df.to_csv("data/quotes.csv", index=False, encoding="utf-8")
    print(f"Scraping completed. {len(df)} quotes saved to data/quotes.csv")
