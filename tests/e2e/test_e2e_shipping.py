import pytest
from playwright.sync_api import Page, expect
from pages.cart_page import CartPage
from pages.product_page import ProductPage


@pytest.mark.e2e
def test_e2e_12_shipping_applied_below_threshold(page: Page, cart_page: CartPage):
    """E2E-12: Shipping - Subtotal below $75; shipping charge $9.99 is applied."""
    cart_page.clear_local_storage()

    # Pre-populate cart with an item whose price is below $75 ($50.00)
    low_price_item = [
        {
            "id": "item-low-1",
            "product": {
                "id": "prod-low",
                "name": "Ceramic Mug",
                "slug": "ceramic-mug",
                "price": "50.00",
                "images": ["https://images.unsplash.com/photo-1598300042247-d088f8ab3a91"],
                "stockQuantity": 10
            },
            "quantity": 1,
            "unitPrice": "50.00",
            "lineTotal": "50.00"
        }
    ]
    cart_page.open()
    cart_page.set_local_cart(low_price_item)
    cart_page.open()

    subtotal = cart_page.get_subtotal_amount()
    assert subtotal < 75.0, f"Expected subtotal < 75.0, got {subtotal}"

    shipping_text = cart_page.get_shipping_text()
    assert shipping_text == "$9.99", f"Expected '$9.99' shipping charge, got '{shipping_text}'"

    # Total should equal subtotal (50) + shipping (9.99) + tax (4.00) = 63.99
    total = cart_page.get_total_amount()
    assert total == 63.99, f"Expected total $63.99, got {total}"


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_13_free_shipping_above_threshold(page: Page, product_page: ProductPage, cart_page: CartPage):
    """E2E-13: Shipping - Subtotal above $75; shipping shows as Free."""
    cart_page.clear_local_storage()

    # Add Ceramic pour-over set ($86.00 > $75.00)
    product_page.open_detail("ceramic-pour-over-set")
    product_page.add_current_product_to_cart()

    cart_page.open()
    subtotal = cart_page.get_subtotal_amount()
    assert subtotal >= 75.0, f"Expected subtotal >= 75.0, got {subtotal}"

    shipping_text = cart_page.get_shipping_text()
    assert shipping_text.lower() == "free", f"Expected 'Free' shipping, got '{shipping_text}'"

