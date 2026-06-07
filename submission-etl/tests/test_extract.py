from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup

from utils.extract import (
    fetching_content,
    extract_product
)


@patch("requests.get")
def test_fetching_content_success(mock_get):

    mock_response = MagicMock()
    mock_response.content = b"<html></html>"
    mock_response.raise_for_status.return_value = None

    mock_get.return_value = mock_response

    result = fetching_content("https://dummy-url.com")

    assert result == b"<html></html>"


@patch("requests.get")
def test_fetching_content_failed(mock_get):

    mock_get.side_effect = Exception("Connection Error")

    result = fetching_content("https://dummy-url.com")

    assert result is None


def test_extract_product():

    html = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">Hoodie 1</h3>

            <div class="price-container">
                <span class="price">$100.00</span>
            </div>

            <p>Rating: ⭐ 4.8 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")

    card = soup.find("div", class_="collection-card")

    result = extract_product(card)

    assert result["Title"] == "Hoodie 1"
    assert result["Price"] == "$100.00"
    assert result["Colors"] == "3 Colors"
    assert result["Gender"] == "Gender: Men"


def test_extract_product_none():

    result = extract_product(None)

    assert result is None

from unittest.mock import patch

from utils.extract import scrape_products


@patch("utils.extract.fetching_content")
def test_scrape_products(mock_fetch):

    html = """
    <div class="collection-card">
        <div class="product-details">
            <h3 class="product-title">Hoodie 1</h3>
            <span class="price">$100</span>
            <p>Rating: ⭐ 4.8 / 5</p>
            <p>3 Colors</p>
            <p>Size: M</p>
            <p>Gender: Men</p>
        </div>
    </div>
    """

    mock_fetch.return_value = html

    result = scrape_products()

    assert isinstance(result, list)