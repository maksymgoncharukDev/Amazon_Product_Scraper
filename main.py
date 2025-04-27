import requests
from bs4 import BeautifulSoup
import csv
import time

# Target URL (can change the search term here)
url = "https://www.amazon.ca/s?k=laptop"

# Pretend to be a real browser
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Send the request
response = requests.get(url, headers=headers)
response.raise_for_status()

# Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# Find all products on the page
products = soup.find_all("div", {"data-component-type": "s-search-result"})

# List to save product info
product_data = []

# Go through each product
for product in products:
    title_elem = product.h2
    price_whole = product.find("span", class_="a-price-whole")
    price_fraction = product.find("span", class_="a-price-fraction")

    if title_elem and price_whole and price_fraction:
        title = title_elem.text.strip()
        price = price_whole.text.strip() + "." + price_fraction.text.strip()
        product_data.append([title, price])

# Save to CSV
with open("amazon_products.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Price"])
    writer.writerows(product_data)

print("✅ Done! Data saved to 'amazon_products.csv'")
