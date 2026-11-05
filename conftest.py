import json
import pytest
from pathlib import Path
from playwright.sync_api import Page, APIRequestContext, Playwright
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def test_data():
    """Loads static test data JSON."""
    data_file = DATA_DIR / "test_data.json"
    with open(data_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def products_schema():
    """Loads catalog JSON schema."""
    schema_file = DATA_DIR / "products_schema.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def single_product_schema():
    """Loads single product JSON schema."""
    schema_file = DATA_DIR / "single_product_schema.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def electronic_product_schema():
    """Loads electronic product JSON schema for mockapi."""
    schema_file = DATA_DIR / "electronic_product_schema.json"
    with open(schema_file, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture(scope="session")
def electronic_api_context(playwright: Playwright) -> APIRequestContext:
    """Provides Playwright APIRequestContext configured for MockAPI electronic endpoint."""
    request_context = playwright.request.new_context(
        base_url="https://681444af225ff1af16285b31.mockapi.io",
        extra_http_headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )
    yield request_context
    request_context.dispose()


@pytest.fixture(scope="session")
def api_context(playwright: Playwright, base_url: str) -> APIRequestContext:
    """Provides Playwright APIRequestContext configured with base URL."""
    request_context = playwright.request.new_context(
        base_url=base_url,
        extra_http_headers={"Accept": "application/json"}
    )
    yield request_context
    request_context.dispose()


@pytest.fixture
def home_page(page: Page) -> HomePage:
    return HomePage(page)


@pytest.fixture
def product_page(page: Page) -> ProductPage:
    return ProductPage(page)


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    return CartPage(page)


@pytest.fixture
def checkout_page(page: Page) -> CheckoutPage:
    return CheckoutPage(page)


@pytest.fixture
def mobile_page(playwright: Playwright, base_url: str):
    """Provides an isolated browser context emulating mobile viewport (390x844)."""
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={"width": 390, "height": 844},
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        is_mobile=True,
        has_touch=True,
        base_url=base_url
    )
    page = context.new_page()
    yield page
    context.close()
    browser.close()
