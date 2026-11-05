import re
import pytest
from playwright.sync_api import Page, expect
from pages.product_page import ProductPage


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_03_listing_displays_products(page: Page, product_page: ProductPage):
    """E2E-03: Listing - Open product listing; products show name, image, and price."""
    product_page.open_listing()
    expect(product_page.page_heading).to_contain_text("All products")

    cards = product_page.all_product_links
    expect(cards.first).to_be_visible()
    count = cards.count()
    assert count >= 4, f"Expected at least 4 products, found {count}"

    # Verify first product contains image, title, and price
    first_card = cards.first
    expect(first_card.locator("img")).to_be_visible()
    card_text = first_card.inner_text()
    assert "$" in card_text, "Product card should display a price"


@pytest.mark.e2e
def test_e2e_04_search_known_product(page: Page, product_page: ProductPage):
    """E2E-04: Search - Search for a known product; only matching products appear."""
    product_page.open_listing("search=wool")
    expect(product_page.all_product_links.first).to_be_visible()

    titles = product_page.get_product_titles()
    assert len(titles) > 0, "Expected matching products for 'wool'"
    for title in titles:
        assert "wool" in title.lower(), f"Unexpected product '{title}' returned for search 'wool'"


@pytest.mark.e2e
def test_e2e_05_search_nonsense_term(page: Page, product_page: ProductPage):
    """E2E-05: Search - Search for a nonsense term; 'No products match these filters.' message shown."""
    product_page.open_listing("search=xyz999nonsenseterm")
    expect(product_page.no_results_text).to_be_visible()
    expect(product_page.all_product_links).to_have_count(0)


@pytest.mark.e2e
def test_e2e_06_sort_price_low_to_high(page: Page, product_page: ProductPage):
    """E2E-06: Filter/Sort - Sort by price low to high; prices are in ascending order."""
    product_page.open_listing()
    product_page.select_sort("Price: low to high")

    prices = product_page.get_product_prices_numeric()
    assert len(prices) >= 2, f"Expected at least 2 products to verify sort, found {len(prices)}"

    # Check ascending order
    for i in range(len(prices) - 1):
        assert prices[i] <= prices[i + 1], (
            f"Prices are not ascending: index {i} is {prices[i]} but index {i+1} is {prices[i+1]}. Full list: {prices}"
        )
