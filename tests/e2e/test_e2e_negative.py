import pytest
from playwright.sync_api import Page, expect


@pytest.mark.e2e
def test_e2e_20_invalid_url_graceful_handling(page: Page):
    """E2E-20: Negative - Open an invalid URL; verify site loads without crashing or uncaught JavaScript exceptions."""
    uncaught_exceptions = []
    page.on("pageerror", lambda err: uncaught_exceptions.append(str(err)))

    response = page.goto("/non-existent-page-404-check", wait_until="domcontentloaded")

    # In single-page Netlify apps, server serves 200 with index.html fallback
    assert response is not None
    assert response.status == 200

    # Ensure no uncaught JS crashes
    assert len(uncaught_exceptions) == 0, f"Uncaught page exceptions occurred: {uncaught_exceptions}"

    # Verify navigation header remains intact so user can return home
    home_link = page.locator("a[href='/']").first
    if home_link.count() > 0:
        expect(home_link).to_be_visible()
        home_link.click()
        expect(page).to_have_url("https://ecomcicid.netlify.app/")

