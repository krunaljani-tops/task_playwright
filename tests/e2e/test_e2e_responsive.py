import re
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage
from pages.product_page import ProductPage
from pages.cart_page import CartPage


@pytest.mark.e2e
def test_e2e_18_mobile_viewport_flow(mobile_page: Page):
    """E2E-18: Responsive - Run key flow at 390x844; layout usable, menu and cart work on mobile."""
    # Verify mobile viewport is configured
    viewport = mobile_page.viewport_size
    assert viewport["width"] == 390
    assert viewport["height"] == 844

    home_page = HomePage(mobile_page)
    home_page.open()

    # Header and brand logo should be visible
    expect(home_page.header).to_be_visible()
    expect(home_page.brand_link).to_be_visible()

    # Navigate to Products
    home_page.products_nav_link.click()
    expect(mobile_page).to_have_url(re.compile(r"/products"))

    product_page = ProductPage(mobile_page)
    expect(product_page.page_heading).to_be_visible()

    # On mobile, the "Filters" toggle button is visible (class lg:hidden)
    mobile_filter_toggle = mobile_page.locator("button:has-text('Filters')")
    expect(mobile_filter_toggle).to_be_visible()

    # Open first product detail
    product_page.all_product_links.first.click()
    expect(mobile_page).to_have_url(re.compile(r"/products/"))
    expect(product_page.detail_title).to_be_visible()

    # Add to cart on mobile
    product_page.add_current_product_to_cart()

    # Check cart
    cart_page = CartPage(mobile_page)
    cart_page.open()
    expect(cart_page.heading).to_be_visible()
    expect(cart_page.item_cards.first).to_be_visible()
    expect(cart_page.checkout_link).to_be_visible()


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_19_cross_browser_compatibility(page: Page, home_page: HomePage, product_page: ProductPage):
    """E2E-19: Cross browser - Core smoke flow passes reliably on the active browser engine."""
    home_page.open()
    expect(home_page.hero_heading).to_be_visible()

    product_page.open_listing()
    expect(product_page.page_heading).to_contain_text("All products")
    expect(product_page.all_product_links.first).to_be_visible()

