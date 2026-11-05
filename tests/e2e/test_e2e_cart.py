import re
import pytest
from playwright.sync_api import Page, expect
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_08_add_item_to_cart(page: Page, product_page: ProductPage, cart_page: CartPage):
    """E2E-08: Cart - Add item to cart; cart count increases, item appears in cart."""
    product_page.clear_local_storage()
    product_page.open_detail("linen-lounge-chair")

    # Add item
    product_page.add_current_product_to_cart()

    # Check cart header badge indicates 1 item
    badge_text = product_page.get_cart_badge_text()
    assert "1" in badge_text, f"Expected 1 in cart badge, got '{badge_text}'"

    # Navigate to Cart page and verify item is present
    cart_page.open()
    expect(cart_page.heading).to_be_visible()
    expect(page.locator("main").locator("text=Linen lounge chair").first).to_be_visible()
    assert cart_page.item_cards.count() >= 1


@pytest.mark.e2e
def test_e2e_09_change_quantity(page: Page, product_page: ProductPage, cart_page: CartPage):
    """E2E-09: Cart - Change quantity; line total and subtotal update correctly."""
    product_page.clear_local_storage()
    product_page.open_detail("wool-throw-blanket")
    product_page.add_current_product_to_cart()

    cart_page.open()
    initial_subtotal = cart_page.get_subtotal_amount()
    assert initial_subtotal == 128.00

    # Increase quantity to 2
    cart_page.increase_quantity(0)
    page.wait_for_timeout(500)

    updated_subtotal = cart_page.get_subtotal_amount()
    assert updated_subtotal == 256.00, f"Expected subtotal 256.00, got {updated_subtotal}"


@pytest.mark.e2e
def test_e2e_10_remove_item(page: Page, product_page: ProductPage, cart_page: CartPage):
    """E2E-10: Cart - Remove item; item removed, totals recalculated."""
    product_page.clear_local_storage()
    product_page.open_detail("ceramic-pour-over-set")
    product_page.add_current_product_to_cart()

    cart_page.open()
    expect(cart_page.item_cards.first).to_be_visible()

    # Remove item
    cart_page.remove_item(0)
    expect(cart_page.empty_cart_message).to_be_visible()


@pytest.mark.e2e
def test_e2e_11_empty_cart_state(page: Page, cart_page: CartPage):
    """E2E-11: Cart - Empty cart; empty-state message shown."""
    cart_page.clear_local_storage()
    cart_page.open()

    expect(cart_page.empty_cart_message).to_be_visible()
    expect(cart_page.continue_shopping_link).to_be_visible()


@pytest.mark.e2e
def test_e2e_17_cart_persistence_on_reload(page: Page, product_page: ProductPage, cart_page: CartPage):
    """E2E-17: Persistence - Reload page with items in cart; cart contents preserved."""
    product_page.clear_local_storage()
    product_page.open_detail("organic-cotton-overshirt")
    product_page.add_current_product_to_cart()

    cart_page.open()
    expect(page.locator("main").locator("text=Organic cotton overshirt").first).to_be_visible()
    subtotal_before = cart_page.get_subtotal_amount()

    # Reload page
    page.reload()
    cart_page.page.wait_for_load_state("domcontentloaded")

    # Verify cart item and subtotal are preserved
    expect(page.locator("main").locator("text=Organic cotton overshirt").first).to_be_visible()
    subtotal_after = cart_page.get_subtotal_amount()
    assert subtotal_before == subtotal_after, f"Expected {subtotal_before}, got {subtotal_after}"
