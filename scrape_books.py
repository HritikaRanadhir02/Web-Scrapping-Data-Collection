#!/usr/bin/env python3
"""
Beginner web scraping example for books.toscrape.com
Saves product title, price and rating into a CSV file.
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urljoin

BASE_URL = 'http://books.toscrape.com/'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; learning-bot/1.0)'
}

def get_soup(url):
    try:
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except requests.RequestException as e:
        print(f"[!] Request error for {url}: {e}")
        return None

def parse_book(article):
    title = article.h3.a.get('title', '').strip()
    price_text = article.find('p', class_='price_color').text.strip()
    price_num = ''.join(ch for ch in price_text if (ch.isdigit() or ch == '.'))
    price = float(price_num) if price_num else None

    rating_p = article.find('p', class_='star-rating')
    rating = None
    if rating_p:
        classes = rating_p.get('class', [])
        words = [c for c in classes if c != 'star-rating']
        rating_word = words[0] if words else ''
        rating_map = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        rating = rating_map.get(rating_word, None)

    link = article.h3.a.get('href', '')
    product_url = urljoin(BASE_URL, link)

    return {
        'title': title,
        'price': price,
        'rating': rating,
        'product_page_url': product_url
    }

def find_next_page(soup, current_url):
    next_li = soup.find('li', class_='next')
    if next_li and next_li.a:
        href = next_li.a['href']
        return urljoin(current_url, href)
    return None

def scrape(start_url, output_csv='books.csv', max_pages=None):
    current_url = start_url
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['title', 'price', 'rating', 'product_page_url'])
        writer.writeheader()
        page = 1
        while current_url:
            print(f"Scraping page {page}: {current_url}")
            soup = get_soup(current_url)
            if soup is None:
                print("Stopping because the page could not be fetched.")
                break

            articles = soup.find_all('article', class_='product_pod')
            for art in articles:
                try:
                    data = parse_book(art)
                    writer.writerow(data)
                except Exception as e:
                    print(f"Failed to parse a product: {e}")

            if max_pages and page >= max_pages:
                print(f"Reached max_pages={max_pages}, stopping.")
                break

            next_url = find_next_page(soup, current_url)
            if not next_url:
                print("No next page found — scraping complete.")
                break

            current_url = next_url
            page += 1
            time.sleep(random.uniform(1, 2))

    print(f"Saved scraped data to {output_csv}")

if __name__ == '__main__':
    scrape(BASE_URL, output_csv='books.csv', max_pages=None)
