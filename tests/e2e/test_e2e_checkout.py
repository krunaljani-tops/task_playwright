import re
import pytest
from playwright.sync_api import Page, expect
from pages.checkout_page import CheckoutPage


def _seed_cart_with_item(page: Page, checkout_page: CheckoutPage):
    """Utility to ensure cart has an item before navigating to checkout."""
    page.goto("/", wait_until="domcontentloaded")
    items = [
        {
            "id": "item-chk-1",
            "product": {
                "id": "prod-chk",
                "name": "Wool throw blanket",
                "slug": "wool-throw-blanket",
                "price": "128.00",
                "images": ["https://images.unsplash.com/photo-1598300042247-d088f8ab3a91"],
                "stockQuantity": 10
            },
            "quantity": 1,
            "unitPrice": "128.00",
            "lineTotal": "128.00"
        }
    ]
    checkout_page.set_local_cart(items)
    page.goto("/checkout", wait_until="domcontentloaded")
    expect(checkout_page.continue_to_review_btn).to_be_visible()


@pytest.mark.e2e
def test_e2e_14_checkout_empty_fields_validation(page: Page, checkout_page: CheckoutPage):
    """E2E-14: Checkout - Submit with empty fields; validation errors shown for required fields."""
    _seed_cart_with_item(page, checkout_page)

    # Click Continue to review with empty fields
    checkout_page.submit_shipping_form()

    errors = checkout_page.get_validation_errors()
    assert len(errors) >= 3, f"Expected at least 3 validation errors, got {errors}"
    assert any("address" in err.lower() for err in errors), "Expected address validation error"
    assert any("city" in err.lower() for err in errors), "Expected city validation error"
    assert any("postal" in err.lower() for err in errors), "Expected postal code validation error"


@pytest.mark.e2e
def test_e2e_15_checkout_invalid_field_formats(page: Page, checkout_page: CheckoutPage):
    """E2E-15: Checkout - Invalid country or short postal code; field-level error shown."""
    _seed_cart_with_item(page, checkout_page)

    checkout_page.fill_shipping_form({
        "line1": "123 Main St",
        "city": "Metropolis",
        "postalCode": "1",    # Invalid (< 2 chars)
        "country": "USA"      # Invalid (must be 2 letters)
    })
    checkout_page.submit_shipping_form()

    errors = checkout_page.get_validation_errors()
    assert len(errors) >= 1, f"Expected validation errors for invalid input, got {errors}"
    assert any("country" in err.lower() or "postal" in err.lower() for err in errors)


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_16_checkout_valid_submission_confirmation(page: Page, checkout_page: CheckoutPage, test_data: dict):
    """E2E-16: Checkout - Valid details; order confirmation page shown."""
    _seed_cart_with_item(page, checkout_page)

    valid_address = test_data["valid_checkout_address"]
    checkout_page.fill_shipping_form(valid_address)

    # Continue to Review step
    checkout_page.submit_shipping_form()

    # Verify review step displays the destination address
    expect(page.locator("text=Shipping to")).to_be_visible()
    expect(page.locator(f"text={valid_address['line1']}")).to_be_visible()

    # Place Order
    checkout_page.place_order()

    # Verify Order Confirmation page
    expect(page).to_have_url(re.compile(r"/orders/.+/confirmed"))
    expect(checkout_page.order_confirmed_badge).to_be_visible()
    expect(checkout_page.thank_you_title).to_be_visible()
    expect(page.get_by_text(re.compile(r"ORD-LOCAL-", re.I)).first).to_be_visible()
