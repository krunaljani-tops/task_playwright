import re
import pytest
from playwright.sync_api import Page, expect
from pages.home_page import HomePage


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_01_home_page_loads(page: Page, home_page: HomePage):
    """E2E-01: Home Page loads - Title contains 'Northline', header, nav, and footer are visible."""
    home_page.open()
    expect(page).to_have_title(re.compile(r"Northline", re.I))
    expect(home_page.header).to_be_visible()
    expect(home_page.nav).to_be_visible()
    expect(home_page.hero_heading).to_be_visible()
    expect(home_page.footer).to_be_visible()


@pytest.mark.smoke
@pytest.mark.e2e
def test_e2e_02_navigation_menu_items(page: Page, home_page: HomePage):
    """E2E-02: Navigation - Click main menu items; correct page loads with no unhandled console errors."""
    console_errors = []
    page.on("pageerror", lambda err: console_errors.append(str(err)))

    home_page.open()

    # 1. Click Products in navbar
    home_page.products_nav_link.click()
    expect(page).to_have_url(re.compile(r"/products"))
    expect(page.locator("h1")).to_contain_text("All products")

    # 2. Click Logo back to Home
    home_page.brand_link.click()
    expect(page).to_have_url(re.compile(r"/$"))
    expect(home_page.hero_heading).to_be_visible()

    # 3. Click Sign in
    home_page.signin_link.click()
    expect(page).to_have_url(re.compile(r"/login"))
    expect(page.get_by_role("heading", name=re.compile(r"Sign in|Welcome back", re.I))).to_be_visible()

    # 4. Return to home and toggle Cart drawer
    home_page.open()
    home_page.open_cart_drawer()
    expect(page.get_by_role("heading", name="Your cart")).to_be_visible()

    # Ensure no catastrophic console error occurred
    assert len(console_errors) == 0, f"Unexpected page errors: {console_errors}"
