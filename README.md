# Web Scraping & Data Collection (Beginner)

## Overview

A beginner project demonstrating how to scrape product information (title, price, rating) from a demo e‑commerce website and save it into a CSV for analysis. Built with Python, `requests`, and `BeautifulSoup`.

## Features
- HTTP requests and HTML parsing
- DOM navigation and extraction
- Pagination handling
- Saving to CSV
- Polite scraping and basic error handling

## Files
- `scrape_books.py` — main script
- `requirements.txt` — dependencies
- `books.csv` — output (generated after running the script)

## Setup
```bash
#ran in Windows
python -m venv venv
venv\Scripts\activate    
pip install -r requirements.txt
python scrape_books.py
```

## Output
A CSV file named `books.csv` containing columns: `title`, `price`, `rating`, `product_page_url`.

## License
MIT — feel free to reuse for learning.

## Notes
This repo uses `http://books.toscrape.com/`, a site built for scraping practice. Do not use this code to scrape websites without permission.
