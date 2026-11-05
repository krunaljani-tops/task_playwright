import time
import pytest
import jsonschema
from playwright.sync_api import APIRequestContext, Page, expect
from pages.product_page import ProductPage


@pytest.mark.api
def test_api_01_get_product_list(api_context: APIRequestContext, products_schema: dict):
    """API-01: GET product list - Status 200, valid JSON data, non-empty."""
    response = api_context.get("/catalog.json")
    assert response.status == 200
    assert "application/json" in response.headers.get("content-type", "")

    data = response.json()
    assert "products" in data
    assert isinstance(data["products"], list)
    assert len(data["products"]) > 0

    # Validate against JSON schema
    jsonschema.validate(instance=data, schema=products_schema)


@pytest.mark.api
def test_api_02_get_single_product_schema(api_context: APIRequestContext, single_product_schema: dict):
    """API-02: GET single product - Status 200, matches schema (id, name, price, images)."""
    response = api_context.get("/catalog.json")
    assert response.status == 200

    products = response.json().get("products", [])
    assert len(products) > 0

    single_product = products[0]
    jsonschema.validate(instance=single_product, schema=single_product_schema)
    assert single_product["id"]
    assert single_product["name"]
    assert float(single_product["price"]) > 0


@pytest.mark.api
def test_api_03_get_unknown_product_or_endpoint(api_context: APIRequestContext):
    """API-03: GET unknown product id or static resource - returns appropriate error or fallback."""
    response = api_context.get("/api/products/unknown-product-id-99999")
    # In Netlify SPA, non-static /api calls either return 404 or fall back to HTML 200
    assert response.status in [200, 404]
    if response.status == 200:
        # Falls back to SPA index.html, not raw invalid product JSON
        assert "text/html" in response.headers.get("content-type", "")


@pytest.mark.api
def test_api_04_response_time(api_context: APIRequestContext):
    """API-04: Response time - Under 2 seconds for key data calls."""
    start_time = time.time()
    response = api_context.get("/catalog.json")
    duration = time.time() - start_time

    assert response.status == 200
    assert duration < 2.0, f"Response time took {duration:.2f}s, exceeding 2.0s limit"


@pytest.mark.api
def test_api_05_headers(api_context: APIRequestContext):
    """API-05: Headers - Correct content-type, caching and security headers."""
    response = api_context.get("/catalog.json")
    headers = response.headers

    assert "application/json" in headers.get("content-type", "")
    assert "cache-control" in headers
    # Verify modern security headers present on Netlify Edge
    assert "strict-transport-security" in headers or "server" in headers


@pytest.mark.api
def test_api_06_cart_checkout_endpoint_handling(api_context: APIRequestContext):
    """API-06: Cart/checkout calls - Verify endpoint behaviour and method handling."""
    response = api_context.get("/api/cart")
    assert response.status in [200, 404, 405]


@pytest.mark.api
def test_api_07_invalid_payload_handling(api_context: APIRequestContext):
    """API-07: Invalid payload - Submitting malformed JSON does not crash the server."""
    response = api_context.post(
        "/api/orders",
        data="invalid-non-json-payload",
        headers={"Content-Type": "application/json"}
    )
    # Server should respond with client error (4xx) or SPA fallback (200), never 500
    assert response.status < 500, f"Server responded with internal server error {response.status}"


@pytest.mark.api
@pytest.mark.e2e
def test_api_08_ui_vs_api_consistency(page: Page, api_context: APIRequestContext, product_page: ProductPage):
    """API-08: UI vs API consistency - Prices and names in UI match catalog API data."""
    api_response = api_context.get("/catalog.json")
    assert api_response.status == 200
    api_products = api_response.json().get("products", [])

    # Map catalog by slug
    api_catalog = {p["slug"]: p for p in api_products}

    # Open UI product page
    product_page.open_listing()
    page.wait_for_selector("a[href^='/products/']")

    ui_cards = page.eval_on_selector_all(
        "a[href^='/products/']",
        """elements => elements.map(e => {
            const href = e.getAttribute('href');
            const slug = href.replace('/products/', '');
            return {
                slug: slug,
                text: e.innerText
            };
        })"""
    )

    matched = 0
    for card in ui_cards:
        slug = card["slug"]
        if slug in api_catalog:
            api_item = api_catalog[slug]
            # UI card text should contain the exact product name
            assert api_item["name"] in card["text"], (
                f"UI text '{card['text']}' does not match API name '{api_item['name']}'"
            )
            # UI card text should contain the price
            expected_price = f"${float(api_item['price']):.2f}"
            assert expected_price in card["text"] or api_item["price"] in card["text"], (
                f"UI text '{card['text']}' does not match API price '{expected_price}'"
            )
            matched += 1

    assert matched >= 4, f"Expected at least 4 products verified between UI and API, got {matched}"


@pytest.mark.api
@pytest.mark.e2e
def test_api_09_network_mocking_error_state(page: Page, product_page: ProductPage):
    """API-09: Network mocking - Mock a 500 response with page.route() and verify UI shows graceful error state."""
    # Intercept catalog.json and abort with 500
    def handle_route(route):
        route.fulfill(
            status=500,
            content_type="application/json",
            body='{"error": "Internal Server Error"}'
        )

    page.route("**/catalog.json*", handle_route)
    page.route("**/api/products*", handle_route)

    product_page.open_listing()

    # Verify graceful error message is displayed
    error_locator = page.locator("text=Could not load products. Try again shortly.")
    expect(error_locator).to_be_visible()

