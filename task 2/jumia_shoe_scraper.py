import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Base URL (note the "page=" part will be added in the loop)
BASE_URL = "https://www.jumia.com.eg/mens-shoes/?q=men+shoes&page={}"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/128.0.0.0 Safari/537.36"
}

product_data = []
page = 1
max_products = 100

while len(product_data) < max_products:
    url = BASE_URL.format(page)
    print(f"Scraping page {page}...")

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page {page}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("article", class_="prd _fb col c-prd")

    if not products:
        print("No more products found.")
        break

    for product in products:
        name_tag = product.find("h3", class_="name")
        price_tag = product.find("div", class_="prc")
        link_tag = product.find("a", href=True)
        image_tag = product.find("img", src=True)

        name = name_tag.text.strip() if name_tag else "N/A"
        price = price_tag.text.strip() if price_tag else "N/A"
        url_link = "https://www.jumia.com.eg" + link_tag["href"] if link_tag else "N/A"
        image_url = image_tag["data-src"] if image_tag and "data-src" in image_tag.attrs else (image_tag["src"] if image_tag else "N/A")

        product_data.append({
            "Name": name,
            "Price": price,
            "Product URL": url_link,
            "Image URL": image_url
        })

        if len(product_data) >= max_products:
            break

    page += 1
    time.sleep(1)  # Be nice to the server

# Save to CSV
df = pd.DataFrame(product_data)
df.to_csv("jumia_mens_shoes.csv", index=False)
print(f"Scraped {len(df)} products and saved to jumia_mens_shoes.csv")
