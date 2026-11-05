# Northline Store – E2E, API and CI/CD Automated Test Suite

[![Northline Tests](https://github.com/krunaljani-tops/task_playwright/actions/workflows/tests.yml/badge.svg)](https://github.com/krunaljani-tops/task_playwright/actions/workflows/tests.yml)
[![Playwright](https://img.shields.io/badge/playwright-1.64.1-blue.svg)](https://playwright.dev/python/)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An enterprise-grade test automation suite for the **Northline Store** e-commerce single-page application ([https://ecomcicid.netlify.app/](https://ecomcicid.netlify.app/)) and RESTful backend APIs ([MockAPI Electronic API](https://681444af225ff1af16285b31.mockapi.io/electronicapi)), built with **Python**, **Playwright**, **pytest**, **pytest-xdist**, and **GitHub Actions**.

---

## 1. Project Overview & Scope

The **Northline Store** is a modern, client-rendered single-page application (SPA) built with React, Vite, and Zustand, hosted on Netlify Edge. It features quiet luxury furniture, home objects, and apparel with real-time cart persistence and a $75.00 free shipping rule. In addition, backend electronic product data services are tested against the dedicated REST endpoint at `https://681444af225ff1af16285b31.mockapi.io/electronicapi`.

### Test Coverage Highlights
* **End-to-End UI Journeys (20 Test Scenarios):** Home page navigation, catalog browsing, category filtering, search queries, multi-attribute sorting, product details, cart state transitions, $75 free-shipping threshold calculations, multi-step checkout with Zod validation, order confirmation, responsive mobile viewports (iPhone 390x844), and cross-browser execution.
* **Backend & API Integrity (16 Test Scenarios):**
  * **Northline Catalog API & UI Fault Injection (9 Tests):** Catalog data source schema validation (`/catalog.json`), response latency benchmarks (< 2s), HTTP header security and caching checks, invalid payload resilience, UI-to-API data consistency, and network fault injection (500 mock error handling).
  * **MockAPI Electronic Endpoint REST Tests (7 Tests):** Full CRUD verification on `https://681444af225ff1af16285b31.mockapi.io/electronicapi` (GET all products with schema validation, GET single item by ID, 404 on nonexistent ID, POST product creation, PUT product modification, DELETE cleanup, category query filtering, response latency, and CORS headers).
* **CI/CD Automation:** Multi-browser matrix (Chromium, Firefox, WebKit), two-stage execution (smoke test gate fail-fast, followed by parallelized regression), automated HTML reporting, traces, and failure screenshot artifacts.

---

## 2. Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ / 3.12 | Core test scripts and page objects |
| **Automation Engine** | Playwright (`playwright`, `pytest-playwright`) | Browser interaction, request mocking, trace recordings |
| **Runner & Framework** | `pytest` | Test execution, fixtures, and assertions |
| **Parallel Execution** | `pytest-xdist` | Multi-core distributed test runs (`-n auto`) |
| **Reporting** | `pytest-html`, Playwright Traces & Screenshots | Self-contained HTML reports and debugging artifacts |
| **API & Schema Validation** | `jsonschema`, `requests` | JSON schema enforcement and API contract testing |
| **CI/CD** | GitHub Actions | Automated pipeline on push, pull request, schedule, and manual dispatch |

---

## 3. Directory Structure

```text
Task_playwright/
├── .github/
│   └── workflows/
│       └── tests.yml               # GitHub Actions CI/CD matrix pipeline
├── data/
│   ├── electronic_product_schema.json # JSON Schema for MockAPI electronic items
│   ├── products_schema.json        # Schema validation for catalog array & categories
│   ├── single_product_schema.json  # Schema validation for individual product items
│   └── test_data.json              # Static fixtures (addresses, threshold values, mock items)
├── pages/                          # Page Object Model (POM) layer
│   ├── __init__.py
│   ├── base_page.py                # Shared locators (header, footer, nav, cart badge, localStorage helpers)
│   ├── home_page.py                # Home page interactions (hero banner, collections, newsletter)
│   ├── product_page.py             # Product listing, filtering, search, sorting & detail pages
│   ├── cart_page.py                # Cart interactions, item removal, quantity updates, order summary
│   └── checkout_page.py            # Multi-step checkout form, validation alerts & order confirmation
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── test_api_suite.py       # Northline API & fault injection tests (API-01 to API-09)
│   │   └── test_electronic_api.py  # MockAPI electronic REST CRUD tests (ELEC-01 to ELEC-09)
│   └── e2e/
│       ├── __init__.py
│       ├── test_e2e_home_navigation.py       # E2E-01, E2E-02
│       ├── test_e2e_listing_search_sort.py   # E2E-03, E2E-04, E2E-05, E2E-06
│       ├── test_e2e_product_detail.py        # E2E-07
│       ├── test_e2e_cart.py                  # E2E-08, E2E-09, E2E-10, E2E-11, E2E-17
│       ├── test_e2e_shipping.py              # E2E-12, E2E-13
│       ├── test_e2e_checkout.py              # E2E-14, E2E-15, E2E-16
│       ├── test_e2e_responsive.py            # E2E-18, E2E-19
│       └── test_e2e_negative.py              # E2E-20
├── .gitignore
├── conftest.py                     # Root fixtures (base_url, api_context, mobile emulation)
├── pytest.ini                      # Test runner configuration, markers, and report options
├── requirements.txt                # Python package dependencies
└── README.md                       # Comprehensive framework documentation
```

---

## 4. Setup & Installation

### Prerequisites
* Python 3.11 or newer installed.
* Git installed.

### 1. Clone & Set Up Virtual Environment
```bash
git clone <repository-url>
cd Task_playwright

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Playwright Browsers
```bash
python -m playwright install --with-deps chromium firefox webkit
```

---

## 5. Running the Tests

### Quick Critical Smoke Tests (All 3 Browsers)
Runs critical path journeys (E2E home, navigation, listing, detail, cart, shipping, checkout, and cross-browser):
```bash
# Chromium (default)
python -m pytest -m smoke

# Firefox
python -m pytest -m smoke --browser firefox

# WebKit (Safari engine)
python -m pytest -m smoke --browser webkit
```

### Run All API Tests
Validates catalog endpoints, schemas, response times, headers, invalid payloads, UI consistency, and network fault injection:
```bash
python -m pytest tests/api
```

### Run All E2E Tests
```bash
python -m pytest tests/e2e
```

### High-Speed Parallel Execution
Leverages `pytest-xdist` to distribute tests across multiple worker processes:
```bash
python -m pytest -n auto
```

### Headed Mode with Slow Motion (Debugging / Local Observation)
```bash
python -m pytest tests/e2e/test_e2e_cart.py --headed --slowmo 300
```

### Inspecting Traces on Failure
When a test fails, Playwright saves execution traces in `test-results/`. View them using Playwright's Trace Viewer:
```bash
python -m playwright show-trace test-results/<test-folder>/trace.zip
```

---

## 6. Test Inventory & Traceability Matrix

### E2E Test Suite (20 Scenarios)

| Test ID | Area | Scenario | Expected Result | Marker |
|---|---|---|---|---|
| **E2E-01** | Home | Page loads | Title contains "Northline", header, nav, and footer visible | `smoke`, `e2e` |
| **E2E-02** | Navigation | Click main menu links | Products, Logo, Sign in, and Cart drawer open without console errors | `smoke`, `e2e` |
| **E2E-03** | Listing | Open product listing | All catalog pieces render with title, image, and price | `smoke`, `e2e` |
| **E2E-04** | Search | Search for known term ("wool") | Only matching products appear in results | `e2e` |
| **E2E-05** | Search | Search nonsense term | Displays "No products match these filters." | `e2e` |
| **E2E-06** | Sort | Sort by price: low to high | Product prices display in ascending numerical order | `e2e` |
| **E2E-07** | Detail | Open product detail | Name, price, description, and enabled Add to Cart button visible | `smoke`, `e2e` |
| **E2E-08** | Cart | Add item to cart | Cart badge increments to (1), item visible in cart | `smoke`, `e2e` |
| **E2E-09** | Cart | Increase item quantity | Line total and order subtotal double correctly | `e2e` |
| **E2E-10** | Cart | Remove item | Item is removed, empty cart state is triggered | `e2e` |
| **E2E-11** | Cart | Empty cart initial state | "Your cart is empty." message and "Continue shopping" link render | `e2e` |
| **E2E-12** | Shipping | Subtotal below $75 | Standard shipping charge ($9.99) is applied and reflected in total | `e2e` |
| **E2E-13** | Shipping | Subtotal above $75 | Shipping displays as "Free" | `smoke`, `e2e` |
| **E2E-14** | Checkout | Submit empty form | Validation errors shown for address, city, and postal code | `e2e` |
| **E2E-15** | Checkout | Submit invalid country/postal | Field-level error displayed ("Use a 2-letter country code") | `e2e` |
| **E2E-16** | Checkout | Valid checkout submission | Review step shows shipping address; placing order confirms with order ID | `smoke`, `e2e` |
| **E2E-17** | Persistence | Reload cart page | In-memory cart items and subtotals persist via localStorage | `e2e` |
| **E2E-18** | Responsive | Mobile viewport (390x844) | Mobile filter drawer toggles, product navigation, and cart work seamlessly | `e2e` |
| **E2E-19** | Cross-Browser| Engine compatibility | Verified across Chromium, Firefox, and WebKit engines | `smoke`, `e2e` |
| **E2E-20** | Negative | Open invalid URL route | SPA gracefully renders navigation and brand header without JS crashes | `e2e` |

### API Test Suite (9 Scenarios)

| Test ID | Method | Endpoint / Scenario | Validation Criteria | Marker |
|---|---|---|---|---|
| **API-01** | `GET` | `/catalog.json` | Status 200, Content-Type `application/json`, matches JSON schema | `api` |
| **API-02** | `GET` | Single product schema | Validates product entity schema (`id`, `name`, `price`, `images`) | `api` |
| **API-03** | `GET` | Invalid/unknown endpoint | Gracefully returns 200 HTML SPA fallback or 404 | `api` |
| **API-04** | `GET` | Performance Benchmark | Response latency under 2.0 seconds | `api` |
| **API-05** | `HEAD`/`GET` | Security & Cache Headers | Checks `Cache-Control`, `Strict-Transport-Security`, `Content-Type` | `api` |
| **API-06** | `GET` | `/api/cart` endpoint | Verifies routing behavior on Netlify Edge | `api` |
| **API-07** | `POST`| `/api/orders` (malformed) | Sending invalid payload does not cause a 500 server crash | `api` |
| **API-08** | Contract| UI vs API consistency | Product names and prices displayed in UI match catalog JSON | `api`, `e2e` |
| **API-09** | Mock | Network fault injection | Intercepts `/catalog.json` with 500; verifies UI graceful error alert | `api`, `e2e` |

### MockAPI Electronic REST API Test Suite (7 Scenarios)
**Target:** `https://681444af225ff1af16285b31.mockapi.io/electronicapi`

| Test ID | Method | Endpoint / Scenario | Validation Criteria | Marker |
|---|---|---|---|---|
| **ELEC-01** | `GET` | `/electronicapi` | Status 200, returns array of items, validates draft-07 JSON schema | `api` |
| **ELEC-02** | `GET` | `/electronicapi/1` | Status 200, returns single electronic product entity with required fields | `api` |
| **ELEC-03** | `GET` | `/electronicapi/999999` | Status 404 Not Found for nonexistent product ID | `api` |
| **ELEC-04** | `POST`/`PUT`/`DEL`| Full CRUD Lifecycle | Creates product (201), updates price/name (200), deletes item (200), verifies 404 | `api` |
| **ELEC-07** | `GET` | `/electronicapi?category=Headphones` | Query filter; asserts all returned products belong to "Headphones" | `api` |
| **ELEC-08** | `GET` | Performance Benchmark | Response time under 2.0 seconds | `api` |
| **ELEC-09** | `GET` | Headers & CORS | Content-Type `application/json` and CORS headers verified | `api` |

---

## 7. CI/CD Pipeline (GitHub Actions)

The workflow file `.github/workflows/tests.yml` implements a production test gate:
1. **Triggers:**
   * Push to `main`
   * Pull Requests targeting `main`
   * Nightly scheduled cron (`0 2 * * *`)
   * Manual trigger via `workflow_dispatch`
2. **Job 1: `smoke-tests` (Fail-Fast Gate):**
   * Matrix across `chromium`, `firefox`, and `webkit`.
   * Runs `pytest -m smoke`. If smoke tests fail on any engine, subsequent jobs halt immediately.
   * Uploads smoke test HTML reports and failure traces.
3. **Job 2: `regression-tests` (Full Suite):**
   * Depends on `smoke-tests` passing.
   * Executes the entire test suite in parallel (`-n auto`).
   * Publishes test report artifacts and Playwright traces retained for 30 days.

---

## 8. Defect & Observation Log

During test exploration and discovery on `https://ecomcicid.netlify.app/`, the following behaviors were documented:

1. **SPA Client-Side Route Fallback (Defect / Observation - E2E-20):**
   * *Observed:* Navigating directly to an unregistered route (e.g. `/non-existent-page`) loads the base template with header and footer, but renders an empty `<main>` container rather than a styled 404 page or automatic redirect to `/`.
   * *Recommendation:* Implement a catch-all route (`<Route path="*" element={<NotFound />} />`) in the React router to guide lost shoppers back to the catalog.
2. **Catalog Data Architecture (Observation - API-01):**
   * *Observed:* The site uses Netlify SPA routing where `/api/*` endpoints fallback to `index.html` (HTTP 200). The true data source consumed by the application is static JSON at `/catalog.json` with a client-side Zustand store providing local fallback ordering (`ecom-cart` / `ecom-local-orders`).
   * *Resolution:* API tests target `/catalog.json` as the primary contract and verify that client error handling gracefully manages missing backend endpoints.
3. **Discount Price Presentation (Locator Robustness - E2E-07):**
   * *Observed:* When a product is on sale (such as the *Linen lounge chair*), the original price ($780.00) is rendered with `line-through` adjacent to the current price ($640.00).
   * *Resolution:* Page object locators filter explicitly for non-strikethrough text to guarantee accurate price assertions.
4. **Accessible Roles & Strict-Mode Selectors:**
   * *Observed:* Multiple testimonial `<quote>` elements use internal `<footer>` tags, causing locator collisions on generic `footer` tags.
   * *Resolution:* Standardized on `page.get_by_role("contentinfo")` to ensure strict, accessible locator binding.

