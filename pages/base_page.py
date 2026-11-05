import re
from playwright.sync_api import Page, Locator, expect


class BasePage:
    """Base Page Object containing common elements and utilities across Northline Store."""

    def __init__(self, page: Page):
        self.page = page
        self.header = page.locator("header")
        self.nav = page.locator("header nav")
        self.brand_link = page.locator("header a[href='/']").first
        self.products_nav_link = page.locator("header nav a[href='/products']")
        self.cart_btn = page.locator("header button").filter(has_text=re.compile(r"^Cart(\s*\(\d+\))?$", re.I)).first
        self.theme_toggle_btn = page.locator("header button[aria-label='Toggle theme']")
        self.signin_link = page.locator("header nav a[href='/login']")
        # Use contentinfo role for main footer to avoid matching quote footers
        self.footer = page.get_by_role("contentinfo")
        self.toast = page.locator("[role='status'], [role='alert'], .shadow-card")

    def navigate_to(self, path: str = "/"):
        """Navigates to the specified path, waiting for network or DOM ready."""
        self.page.goto(path)
        self.page.wait_for_load_state("domcontentloaded")
        try:
            self.page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

    def get_cart_badge_text(self) -> str:
        """Returns the inner text of the cart button in the header."""
        return self.cart_btn.inner_text().strip()

    def open_cart_drawer(self):
        """Clicks the header cart button to toggle drawer."""
        self.cart_btn.click()

    def set_local_cart(self, items: list, promo_code: str = ""):
        """Helper to inject items directly into Zustand ecom-cart localStorage."""
        subtotal = sum(float(item["lineTotal"]) for item in items)
        cart_state = {
            "state": {
                "promoCode": promo_code,
                "cart": {
                    "id": "local",
                    "items": items,
                    "itemCount": sum(item["quantity"] for item in items),
                    "subtotal": f"{subtotal:.2f}"
                }
            },
            "version": 0
        }
        import json
        try:
            self.page.evaluate(
                "(cartJson) => window.localStorage.setItem('ecom-cart', cartJson)",
                json.dumps(cart_state)
            )
        except Exception:
            # If on about:blank, navigate first
            self.navigate_to("/")
            self.page.evaluate(
                "(cartJson) => window.localStorage.setItem('ecom-cart', cartJson)",
                json.dumps(cart_state)
            )

    def clear_local_storage(self):
        """Safely clears browser local storage."""
        try:
            self.page.evaluate("() => window.localStorage.clear()")
        except Exception:
            pass
