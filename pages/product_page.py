import re
from typing import List, Dict
from playwright.sync_api import Page, Locator, expect
from pages.base_page import BasePage


class ProductPage(BasePage):
    """Page Object for Northline Store Product Listing and Detail pages."""

    def __init__(self, page: Page):
        super().__init__(page)

        # Listing locators
        self.page_heading = page.locator("h1")
        self.pieces_count = page.locator("main p").filter(has_text=re.compile(r"\d+\s+pieces", re.I))
        self.product_cards = page.locator("a[href^='/products/']").filter(has=page.locator("h3, p"))
        self.all_product_links = page.locator("a[href^='/products/']")
        self.no_results_text = page.locator("text=No products match these filters.")
        self.clear_filters_btn = page.locator("button:has-text('Clear filters')")
        self.sort_trigger = page.locator("button").filter(has_text=re.compile(r"^(Newest|Price: low to high|Popularity)$"))

        # Category buttons
        self.category_all_btn = page.locator("aside button:has-text('All products')")
        self.category_living_btn = page.locator("aside button:has-text('Living')")
        self.category_apparel_btn = page.locator("aside button:has-text('Apparel')")
        self.category_objects_btn = page.locator("aside button:has-text('Objects')")
        self.category_wellness_btn = page.locator("aside button:has-text('Wellness')")

        # Detail locators
        self.detail_title = page.locator("h1")
        self.detail_price = page.locator("main").locator("p, span").filter(has_text=re.compile(r"^\$[0-9]+(\.[0-9]{2})?$")).first
        self.detail_description = page.locator("main p").filter(has_not_text="$").first
        self.add_to_cart_btn = page.locator("button:has-text('Add to cart')")
        self.buy_now_btn = page.locator("button:has-text('Buy now')")
        self.save_btn = page.locator("button:has-text('Save')")

    def open_listing(self, query_params: str = ""):
        url = f"/products{f'?{query_params}' if query_params else ''}"
        self.navigate_to(url)
        self.page.wait_for_selector("h1")

    def open_detail(self, slug: str):
        self.navigate_to(f"/products/{slug}")
        self.page.wait_for_selector("h1", timeout=10000)

    def get_product_titles(self) -> List[str]:
        self.page.wait_for_selector("a[href^='/products/']", timeout=10000)
        return [
            el.inner_text().strip()
            for el in self.all_product_links.all()
        ]

    def get_product_prices_numeric(self) -> List[float]:
        """Extracts displayed prices from listing cards in DOM order."""
        self.page.wait_for_selector("a[href^='/products/']", timeout=10000)
        prices_data = self.page.eval_on_selector_all(
            "a[href^='/products/']",
            """elements => elements.map(e => {
                const text = e.innerText;
                const matches = text.match(/\\$([0-9]+(?:\\.[0-9]{2})?)/g);
                if (!matches) return null;
                // If discounted, last match is the actual sale price
                const finalPrice = matches[matches.length - 1].replace('$', '');
                return parseFloat(finalPrice);
            }).filter(p => p !== null)"""
        )
        return prices_data

    def select_sort(self, sort_label: str):
        """Clicks sort dropdown and selects option e.g. 'Price: low to high'."""
        self.sort_trigger.first.click()
        self.page.wait_for_timeout(300)
        self.page.locator(f"button:has-text('{sort_label}'), [role='menuitem']:has-text('{sort_label}')").first.click()
        # Wait for products to reload and become visible
        self.page.wait_for_timeout(500)
        self.page.wait_for_selector("a[href^='/products/']", timeout=10000)

    def filter_by_category(self, category_name: str):
        self.page.locator(f"aside button:has-text('{category_name}')").first.click()
        self.page.wait_for_load_state("domcontentloaded")

    def add_current_product_to_cart(self):
        self.add_to_cart_btn.first.click()
        self.page.wait_for_timeout(800)
