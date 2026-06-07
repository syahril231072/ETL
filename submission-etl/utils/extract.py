import requests
import time
from bs4 import BeautifulSoup
from datetime import datetime

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/131.0.0.0 Safari/537.36"
    )
}


def get_page_url(page):
    """
    Menghasilkan URL halaman Fashion Studio.
    """
    if page == 1:
        return "https://fashion-studio.dicoding.dev/"

    return f"https://fashion-studio.dicoding.dev/page{page}"


def fetching_content(url):
    """
    Mengambil konten HTML dari URL.
    """
    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=10
        )

        response.raise_for_status()

        return response.content

    except Exception as e:
        print(f"Fetch error ({url}): {e}")
        return None


def extract_product(card):
    """
    Mengekstrak data satu produk.
    """
    try:
        if card is None:
            return None

        title_tag = card.find(
            "h3",
            class_="product-title"
        )

        title = (
            title_tag.text.strip()
            if title_tag
            else None
        )

        price_tag = card.find(
            "span",
            class_="price"
        )

        if price_tag:
            price = price_tag.text.strip()
        else:
            price = "Price Unavailable"

        p_tags = card.find_all("p")

        rating = None
        colors = None
        size = None
        gender = None

        for p in p_tags:
            text = p.text.strip()

            if "Rating" in text:
                rating = text

            elif "Colors" in text:
                colors = text

            elif "Size" in text:
                size = text

            elif "Gender" in text:
                gender = text

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "timestamp": datetime.now()
        }

    except Exception as e:
        print(f"Extract product error: {e}")
        return None


def scrape_products():
    """
    Scraping seluruh halaman (1–50).
    """
    data = []

    for page in range(1, 51):

        url = get_page_url(page)

        print(f"Scraping page {page}: {url}")

        content = fetching_content(url)

        if not content:
            continue

        soup = BeautifulSoup(
            content,
            "html.parser"
        )

        cards = soup.find_all(
            "div",
            class_="collection-card"
        )

        for card in cards:

            product = extract_product(card)

            if product:
                data.append(product)

        time.sleep(0.2)

    print(f"Total raw data: {len(data)}")

    return data