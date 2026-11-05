import re
from typing import Dict, List
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Page Object for Northline Store Checkout page (/checkout)."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.locator("h1:has-text('Checkout')")
        self.empty_cart_message = page.locator("text=Your cart is empty.")

        # Accessible label-based locators
        self.line1_input = page.get_by_label("Address")
        self.line2_input = page.get_by_label("Apartment, suite (optional)")
        self.city_input = page.get_by_label("City")
        self.state_input = page.get_by_label("State")
        self.postal_code_input = page.get_by_label("Postal code")
        self.country_input = page.get_by_label("Country")
        self.phone_input = page.get_by_label("Phone (optional)")

        # Actions & Buttons
        self.continue_to_review_btn = page.locator("button:has-text('Continue to review')")
        self.back_btn = page.locator("button:has-text('Back')")
        self.place_order_btn = page.locator("button:has-text('Place order')")

        # Validation errors
        self.error_messages = page.locator(".text-danger-600, p[role='alert']")

        # Confirmation screen
        self.order_confirmed_badge = page.locator("text=Order confirmed")
        self.thank_you_title = page.locator("h1:has-text('Thank you')")
        self.keep_shopping_link = page.locator("a:has-text('Keep shopping')")

    def open(self):
        self.navigate_to("/checkout")
        self.page.wait_for_load_state("domcontentloaded")

    def fill_shipping_form(self, address_data: Dict[str, str]):
        if "line1" in address_data:
            self.line1_input.fill(address_data["line1"])
        if "line2" in address_data:
            self.line2_input.fill(address_data["line2"])
        if "city" in address_data:
            self.city_input.fill(address_data["city"])
        if "state" in address_data:
            self.state_input.fill(address_data["state"])
        if "postalCode" in address_data:
            self.postal_code_input.fill(address_data["postalCode"])
        if "country" in address_data:
            self.country_input.fill(address_data["country"])
        if "phone" in address_data:
            self.phone_input.fill(address_data["phone"])

    def submit_shipping_form(self):
        self.continue_to_review_btn.click()
        self.page.wait_for_timeout(800)

    def place_order(self):
        self.place_order_btn.first.click()
        self.page.wait_for_load_state("domcontentloaded")
        self.page.wait_for_timeout(1000)

    def get_validation_errors(self) -> List[str]:
        return [
            el.inner_text().strip()
            for el in self.error_messages.all()
            if el.inner_text().strip()
        ]
