import re
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class HomePage(BasePage):
    """Page Object for Northline Store Home page."""

    def __init__(self, page: Page):
        super().__init__(page)
        self.hero_heading = page.locator("h1").first
        self.shop_collection_btn = page.locator("a[href='/products']").filter(has_text=re.compile("Shop the collection", re.I)).first
        self.new_arrivals_btn = page.locator("a[href*='/products']").filter(has_text=re.compile("View new arrivals", re.I)).first
        self.featured_products = page.locator("a[href^='/products/']")
        self.category_cards = page.locator("a[href*='category=']")
        self.newsletter_input = page.locator("input[type='email']")
        self.newsletter_btn = page.locator("button").filter(has_text="Subscribe")

    def open(self):
        self.navigate_to("/")
        self.page.wait_for_selector("header")

    def click_shop_collection(self):
        self.shop_collection_btn.click()
        self.page.wait_for_load_state("domcontentloaded")

    def click_featured_product(self, index: int = 0):
        self.featured_products.nth(index).click()
        self.page.wait_for_load_state("domcontentloaded")

