import time
import pytest
import jsonschema
from faker import Faker
from playwright.sync_api import APIRequestContext

fake = Faker()


def _call_with_retry(fn, max_retries=3, delay=1.0):
    """Executes an API request with retry on transient network/DNS errors."""
    last_err = None
    for attempt in range(max_retries):
        try:
            return fn()
        except Exception as e:
            last_err = e
            time.sleep(delay * (attempt + 1))
    raise last_err


@pytest.mark.api
def test_electronic_api_01_get_all_products(electronic_api_context: APIRequestContext, electronic_product_schema: dict):
    """ELEC-API-01: GET /electronicapi - Status 200, non-empty JSON list, validates schema."""
    response = _call_with_retry(lambda: electronic_api_context.get("/electronicapi"))
    assert response.status == 200, f"Expected 200 OK, got {response.status}"
    assert "application/json" in response.headers.get("content-type", "")

    products = response.json()
    assert isinstance(products, list), "Response should be a JSON array"
    assert len(products) > 0, "Product list should not be empty"

    # Validate first 5 items against schema
    for item in products[:5]:
        jsonschema.validate(instance=item, schema=electronic_product_schema)


@pytest.mark.api
def test_electronic_api_02_get_single_product(electronic_api_context: APIRequestContext, electronic_product_schema: dict):
    """ELEC-API-02: GET /electronicapi/1 - Status 200, returns correct product matching schema."""
    response = _call_with_retry(lambda: electronic_api_context.get("/electronicapi/1"))
    assert response.status == 200, f"Expected 200 OK, got {response.status}"

    product = response.json()
    assert isinstance(product, dict), "Response should be a JSON object"
    assert product["id"] == "1"
    assert "name" in product
    assert "price" in product
    assert "brand" in product
    assert "category" in product

    jsonschema.validate(instance=product, schema=electronic_product_schema)


@pytest.mark.api
def test_electronic_api_03_get_nonexistent_product(electronic_api_context: APIRequestContext):
    """ELEC-API-03: GET /electronicapi/999999 - Unknown ID returns 404 Not Found."""
    response = _call_with_retry(lambda: electronic_api_context.get("/electronicapi/999999"))
    assert response.status == 404, f"Expected 404 Not Found for nonexistent ID, got {response.status}"


@pytest.mark.api
def test_electronic_api_04_crud_lifecycle(electronic_api_context: APIRequestContext, electronic_product_schema: dict):
    """ELEC-API-04 to 06: Full CRUD lifecycle - POST create, PUT update, and DELETE product."""
    # 1. POST - Create new product
    payload = {
        "name": f"Test {fake.word().capitalize()} Headphones",
        "price": str(fake.random_int(min=50, max=500)),
        "brand": "PlaywrightTech",
        "category": "Headphones",
        "description": fake.sentence(nb_words=10),
        "image": "https://picsum.photos/seed/test/400/400",
        "rating": "4.5",
        "stock": "25"
    }

    create_resp = _call_with_retry(lambda: electronic_api_context.post("/electronicapi", data=payload))
    assert create_resp.status == 201, f"Expected 201 Created, got {create_resp.status}: {create_resp.text()}"
    created_product = create_resp.json()
    new_id = created_product.get("id")
    assert new_id is not None, "Created product should return an ID"
    assert created_product["name"] == payload["name"]
    assert created_product["brand"] == payload["brand"]
    jsonschema.validate(instance=created_product, schema=electronic_product_schema)

    try:
        # 2. PUT - Update existing product
        update_payload = {
            "name": f"{created_product['name']} (Updated)",
            "price": "999"
        }
        update_resp = _call_with_retry(lambda: electronic_api_context.put(f"/electronicapi/{new_id}", data=update_payload))
        assert update_resp.status == 200, f"Expected 200 OK on PUT, got {update_resp.status}"
        updated_product = update_resp.json()
        assert updated_product["name"] == update_payload["name"]
        assert updated_product["price"] == "999"

        # Verify with GET
        verify_resp = _call_with_retry(lambda: electronic_api_context.get(f"/electronicapi/{new_id}"))
        assert verify_resp.status == 200
        assert verify_resp.json()["name"] == update_payload["name"]
    finally:
        # 3. DELETE - Clean up created product
        del_resp = _call_with_retry(lambda: electronic_api_context.delete(f"/electronicapi/{new_id}"))
        assert del_resp.status == 200, f"Expected 200 OK on DELETE, got {del_resp.status}"

        # 4. Verify DELETE - Subsequent GET should return 404
        after_del_resp = _call_with_retry(lambda: electronic_api_context.get(f"/electronicapi/{new_id}"))
        assert after_del_resp.status == 404, f"Deleted product should return 404, got {after_del_resp.status}"


@pytest.mark.api
def test_electronic_api_07_filter_by_category(electronic_api_context: APIRequestContext):
    """ELEC-API-07: Query filtering - Filter products by category."""
    category = "Headphones"
    response = _call_with_retry(lambda: electronic_api_context.get(f"/electronicapi?category={category}"))
    assert response.status == 200

    products = response.json()
    assert isinstance(products, list)
    assert len(products) > 0, f"Expected at least one product in category '{category}'"
    for item in products:
        assert item.get("category") == category, f"Item category {item.get('category')} does not match {category}"


@pytest.mark.api
def test_electronic_api_08_performance_response_time(electronic_api_context: APIRequestContext):
    """ELEC-API-08: Performance - Response time under 2 seconds for key endpoint."""
    start_time = time.time()
    response = _call_with_retry(lambda: electronic_api_context.get("/electronicapi"))
    duration = time.time() - start_time

    assert response.status == 200
    assert duration < 2.0, f"MockAPI response took {duration:.2f}s, exceeding 2.0s threshold"


@pytest.mark.api
def test_electronic_api_09_headers_and_content_type(electronic_api_context: APIRequestContext):
    """ELEC-API-09: Headers - Verify Content-Type, CORS, and response headers."""
    response = _call_with_retry(lambda: electronic_api_context.get("/electronicapi"))
    headers = response.headers

    assert "application/json" in headers.get("content-type", "")
    assert "access-control-allow-origin" in headers or "server" in headers
