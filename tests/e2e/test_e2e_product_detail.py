import re
import pytest
from playwright.sync_api import Page, expect
from pages.product_page import ProductPage


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_07_product_detail_page(page: Page, product_page: ProductPage):
    """E2E-07: Product detail - Open a product; name, price, description, and add-to-cart are shown."""
    product_page.open_detail("linen-lounge-chair")

    # Verify Name
    expect(product_page.detail_title).to_be_visible()
    expect(product_page.detail_title).to_have_text("Linen lounge chair")

    # Verify Price
    expect(product_page.detail_price).to_be_visible()
    expect(product_page.detail_price).to_contain_text("$640.00")

    # Verify Description
    expect(product_page.detail_description).to_be_visible()
    expect(product_page.detail_description).to_contain_text("A low, sculptural lounge chair")

    # Verify Add to Cart button
    expect(product_page.add_to_cart_btn.first).to_be_visible()
    expect(product_page.add_to_cart_btn.first).to_be_enabled()

