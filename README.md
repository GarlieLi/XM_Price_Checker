# XM Price Checker

A Python-based price monitoring and web scraping system for collecting **product-level and variant-level price and availability data** from multiple e-commerce websites.

The project is designed to automate Xiaomi product price checking across multiple retailers. Website-specific scraping logic is separated into individual scraper modules, while a central Jupyter Notebook manages configuration, execution, data collection, processing, and report generation.

The final output compares collected retailer prices with the **RRP after promotion** defined in the product configuration and generates a structured price-checking report.

---

## Overview

The XM Price Checker follows a modular workflow:

1. Read the Excel configuration file.
2. Identify enabled websites and products to monitor.
3. Run the corresponding website scrapers.
4. Collect product and variant-level information.
5. Consolidate the collected data into `RawData`.
6. Match the collected data with the configured products and websites.
7. Compare retailer prices with the configured **RRP after promotion**.
8. Generate the final `Results` report.

The system separates **website-specific scraping logic** from **execution, data processing, and reporting logic**, making it easier to maintain existing scrapers and add support for new retailers.

---

## Key Features

- Multi-website price scraping
- Product and variant-level data collection
- Price and availability monitoring
- Excel-based product and website configuration
- Modular website-specific scraper architecture
- Browser automation using Playwright
- Centralized raw data collection
- Automated price comparison against promotional RRP
- Standardized final reporting
- Individual scraper testing
- Support for multiple product variants, including:
  - RAM
  - Storage
  - Color
  - Product model
  - Availability

---

## Project Structure

```text
XM_Price_Checker/
│
├── Notebooks/
│   └── XM_Price_Checker.ipynb
│
├── scrapers/
│   ├── avans.py
│   ├── electro.py
│   ├── ktr.py
│   ├── xkom.py
│   ├── browser_runner.py
│   └── ...
│
├── test_new/
│   ├── test_avans.py
│   ├── test_electro.py
│   ├── test_ktr.py
│   └── ...
│
├── run_price_check.py
├── XM_Price_Checker_Python.xlsm
└── README.md
```

> The exact list of scraper modules may change as additional retailers are added or updated.

---

## Architecture

The project follows a modular architecture built around four main components:

### 1. Excel Configuration

The Excel workbook contains the configuration used by the price checker.

It defines information such as:

- Products to monitor
- Product models
- RAM
- Storage
- Websites to check
- Website links
- Promotional RRP

The configuration allows the scraping workflow to be changed without modifying the core Python logic.

---

### 2. Notebook Controller

`Notebooks/XM_Price_Checker.ipynb` acts as the main controller of the price-checking workflow.

It is responsible for:

- Reading the Excel configuration
- Determining which websites are enabled
- Determining which products should be checked
- Loading the corresponding scraper modules
- Running the enabled scrapers
- Collecting scraper results
- Consolidating the collected data
- Writing the collected information to `RawData`
- Comparing collected prices with the configured promotional RRP
- Generating the final `Results` report

The notebook therefore acts as the orchestration layer between the configuration, scrapers, and reporting process.

---

### 3. Website Scrapers

Website-specific scraping logic is stored in the `scrapers/` directory.

Each scraper handles the structure and behavior of a particular retailer.

The modular structure means that changes to one retailer's website can generally be handled within its corresponding scraper without affecting the other websites.

---

### 4. Browser Runner

`browser_runner.py` provides shared browser automation functionality for scrapers that require Playwright.

It is responsible for common browser operations such as:

- Starting a browser
- Creating pages
- Opening target URLs
- Managing browser-based scraping execution

Keeping this functionality in a shared module avoids duplicating browser setup code across individual scrapers.

---

## Data Workflow

The overall data workflow is:

```text
Excel Configuration
        ↓
Product & Website Selection
        ↓
Enabled Scrapers
        ↓
Product Discovery
        ↓
Variant Extraction
        ↓
Price & Availability Extraction
        ↓
Raw Data Consolidation
        ↓
RawData
        ↓
Product / Website Matching
        ↓
Price Comparison
        ↓
Results
```

The system focuses on **variant-level data**, allowing different configurations of the same product to be tracked separately.

For example, the following may be represented as separate records:

- Different RAM configurations
- Different storage configurations
- Different colors
- Different product variants
- Different availability states

---

## Data Output

### RawData

`RawData` contains the information collected directly from the individual website scrapers.

It serves as the source data for the final price-checking report and preserves the retailer-level information collected during the scraping process.

Typical information includes: Product name, Product model, Variant, Color, RAM, Storage, Price, Availability, Website, URL

---

### Results

`Results` contains the final price-checking report.

The report compares each retailer's collected price with the configured **RRP after promotion**.

The final report is intended to identify whether a retailer:

- Matches the promotional price
- Offers a lower price
- Offers a higher price
- Has the product unavailable

The `Results` sheet is the final output used for price monitoring and reporting.

---

## Requirements

The project uses Python and a virtual environment.

Main dependencies include:

- Python
- Pandas
- OpenPyXL
- Playwright
- Jupyter / IPython Kernel

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/GarlieLi/XM_Price_Checker.git
cd XM_Price_Checker
```

---

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv venv
```

Activate the environment in PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

---

### 3. Install Python Dependencies

Install the main dependencies manually:

```powershell
python -m pip install pandas openpyxl playwright ipykernel
```

---

### 4. Install Playwright Browsers

After installing Playwright, install the required browser:

```powershell
python -m playwright install chromium
```

This is required for scrapers that use Playwright browser automation.

---

## Adding a New Website

To add support for another retailer:

### 1. Create a scraper

Create a new Python module inside `scrapers/`:

```text
scrapers/new_website.py
```

### 2. Implement the scraping logic

The scraper should handle the retailer-specific:

- Product discovery
- Product matching
- Variant extraction
- Price extraction
- Availability extraction

### 3. Follow the existing output structure

The scraper should return data in a structure compatible with the existing price-checking workflow.

### 4. Add the website to the configuration

Add the relevant website information and URLs to the Excel configuration.

### 5. Add tests

Create a corresponding test module under:

```text
test_new/
```

### 6. Enable the website

Enable the retailer in the project configuration.

### 7. Run and validate

Run the scraper and check the resulting `RawData` and `Results` output.

---

## Testing

The `test_new/` directory contains tests for individual scraper modules.

The tests are organized by website so that changes to one scraper can be checked independently.

Example:

```text
test_new/
├── test_avans.py
├── test_electro.py
├── test_ktr.py
├── test_max_electro.py
├── test_neonet.py
├── test_oleole.py
└── test_xkom.py
```

Individual tests can be executed with:

```powershell
python test_new/test_xkom.py
```

---

## Configuration

The main configuration is maintained in:

```text
XM_Price_Checker_Python.xlsm
```

The workbook contains the product and website information used by the scraping workflow.

Before running the project, make sure:

- The required products are configured.
- Product variants are correctly defined.
- Website URLs are available.
- The correct websites are enabled.
- Promotional RRP values are up to date.

---

## Important Notes

### Excel File

The project relies on the Excel configuration workbook:

```text
XM_Price_Checker_Python.xlsm
```

The workbook should be available in the expected project location before running the price checker.

### Website Changes

E-commerce websites may change their:

- HTML structure
- CSS selectors
- APIs
- Product page structure
- Availability indicators
- Anti-bot mechanisms

As a result, individual scrapers may require updates when a retailer changes its website.

### Browser Automation

Some retailers require browser automation and therefore depend on Playwright.

If Playwright is installed but the browser executable has not been installed, run:

```powershell
python -m playwright install chromium
```

---

## Project Purpose

The XM Price Checker was developed to automate the collection and monitoring of Xiaomi product prices across multiple e-commerce websites.

Instead of manually visiting each retailer and recording prices, the system provides a repeatable workflow for:

- Collecting structured product data
- Monitoring product variants
- Checking retailer prices
- Tracking product availability
- Comparing prices against promotional RRP
- Generating a standardized final report

The project is designed to reduce manual price-checking work while keeping the **scraping, configuration, raw data, and reporting processes structured and maintainable**.

---

## Future Improvements

Potential future improvements include:

- Adding more retailers and markets
- Improving product matching
- Adding more robust error handling
- Improving scraper retry mechanisms
- Adding automated scheduled price checks
- Adding historical price tracking
- Adding price trend analysis
- Adding automated notifications for price changes
- Improving test coverage
- Adding a dashboard for monitoring results

---

## Author

**Garlie Li**