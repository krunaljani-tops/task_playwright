import re
from typing import Optional
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class CartPage(BasePage):
    """Page Object for Northline Store Cart page (/cart)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator("h1:has-text('Cart')")
        self.empty_cart_message = page.locator("text=Your cart is empty.")
        self.continue_shopping_link = page.locator("a:has-text('Continue shopping')")

        # Cart item rows
        self.item_cards = page.locator("main div.space-y-4 > div")
        self.remove_buttons = page.locator("button:has-text('Remove')")
        self.increase_qty_buttons = page.locator("button[aria-label='Increase quantity']")
        self.decrease_qty_buttons = page.locator("button[aria-label='Decrease quantity']")

        # Summary values
        self.subtotal_elem = page.locator("dl div").filter(has_text=re.compile(r"^Subtotal", re.I)).locator("dd")
        self.shipping_elem = page.locator("dl div").filter(has_text=re.compile(r"^Shipping", re.I)).locator("dd")
        self.tax_elem = page.locator("dl div").filter(has_text=re.compile(r"^Tax", re.I)).locator("dd")
        self.total_elem = page.locator("dl div").filter(has_text=re.compile(r"^Total", re.I)).locator("dd")
        self.free_shipping_notice = page.locator("text=Free shipping over $75.00")

        # Promo code
        self.promo_input = page.locator("input[placeholder*='Promo' i]")
        self.apply_promo_btn = page.locator("button:has-text('Apply')")

        # Checkout link/button
        self.checkout_link = page.locator("main a[href='/checkout']")

    def open(self):
        self.navigate_to("/cart")
        self.page.wait_for_load_state("domcontentloaded")

    def get_subtotal_amount(self) -> float:
        text = self.subtotal_elem.first.inner_text().strip().replace("$", "")
        return float(text)

    def get_shipping_text(self) -> str:
        return self.shipping_elem.first.inner_text().strip()

    def get_total_amount(self) -> float:
        text = self.total_elem.first.inner_text().strip().replace("$", "")
        return float(text)

    def increase_quantity(self, item_index: int = 0):
        self.increase_qty_buttons.nth(item_index).click()
        self.page.wait_for_timeout(500)

    def decrease_quantity(self, item_index: int = 0):
        self.decrease_qty_buttons.nth(item_index).click()
        self.page.wait_for_timeout(500)

    def remove_item(self, item_index: int = 0):
        self.remove_buttons.nth(item_index).click()
        self.page.wait_for_timeout(500)

    def proceed_to_checkout(self):
        self.checkout_link.first.click()
        self.page.wait_for_load_state("domcontentloaded")
