# XM Price Checker

A Python-based price monitoring and web scraping system for collecting **product-level and variant-level price and availability data** from multiple e-commerce websites.

The project is designed to make Xiaomi product price checking scalable across multiple retailers. Website-specific scraping logic is separated into individual scraper modules, while a central Jupyter Notebook manages configuration, execution, data collection, and report generation.

The final output compares collected website prices with the **RRP after promotion** defined in the product configuration and generates a structured price-checking report.

---

## Overview

The XM Price Checker follows a modular scraping and reporting workflow:

1. Read the Excel configuration file.
2. Identify enabled websites and products to monitor.
3. Run the corresponding website scrapers.
4. Collect product and variant-level information, including:
   - Product name
   - Variant / color
   - RAM
   - Storage
   - Price
   - Availability
5. Combine the collected results into `RawData`.
6. Match the collected data with the configured products and websites.
7. Compare website prices with the **RRP after promotion**.
8. Generate the final `Results` report.

The project separates **scraping logic** from **execution, data processing, and reporting logic**, making it easier to add, test, and maintain individual website scrapers.

---

## Architecture

The project uses a modular architecture:

```text
Excel Configuration
        │
        ▼
XM_Price_Checker.ipynb
        │
        ├── Product Configuration
        ├── Website Configuration
        └── Links
        │
        ▼
   Enabled Scrapers
        │
        ├── avans.py
        ├── electro.py
        ├── gg.py
        ├── ktr.py
        ├── max_electro.py
        ├── mediamarkt.py
        ├── micom.py
        └── ...
        │
        ▼
Price & Availability Data
        │
        ▼
     RawData
        │
        ▼
Price Comparison
        │
        ▼
     Results


### Notebook Controller

`XM_Price_Checker.ipynb` serves as the main controller for the price-checking workflow.

It is responsible for:

* Reading the Excel configuration
* Determining which websites should be checked
* Running the enabled scrapers
* Collecting scraper results
* Preparing the output data
* Writing the results to `RawData`
* Comparing website prices with the configured promotional RRP
* Generating the final `Results` sheet

### Scrapers

Website-specific scraping logic is stored in the `scrapers/` directory.

Each scraper is responsible for handling the structure and behavior of a particular website.

This modular approach allows individual websites to be developed, tested, or updated independently.

For example:

```text
scrapers/
├── avans.py
├── electro.py
├── ktr.py
├── ...
└── xkom.py
```

### Browser Runner

`browser_runner.py` provides shared browser-related functionality used by scrapers that require browser automation.

Keeping common browser operations in a shared module avoids duplicating the same logic across individual scrapers.

### Tests

The `test_new/` directory contains tests for individual scraper modules.

The tests are organized by website so that changes to one scraper can be checked independently.

## Data Workflow

The main data flow is:

Excel Configuration
        ↓
Website Selection
        ↓
Scraper Execution
        ↓
Product Discovery
        ↓
Variant Extraction
        ↓
Price / Availability Extraction
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

The system focuses on **variant-level data**, allowing different configurations of the same product to be tracked separately.

For example, different:

* Storage configurations
* Colors
* Product variants
* Availability states

can be represented as separate records.

## Adding a New Website

To add support for another website:

1. Create a new scraper module inside `scrapers/`.
2. Implement the website-specific scraping logic.
3. Follow the existing scraper output structure.
4. Add the website to the configuration.
5. Add corresponding tests under `test_new/`.
6. Enable the website in the configuration.
7. Run the price checker and validate the output.

This structure allows the system to scale from a small number of websites to a larger collection of retailers and markets.

## Requirements

The project is developed in Python and uses a virtual environment.

Create and activate a virtual environment:

```bash
python -m venv venv
```

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install the required Python packages:

## Running the Project

The main workflow can be executed through the Jupyter notebook:

```text
Notebooks/XM_Price_Checker.ipynb
```

Alternatively, the project includes:

```text
run_price_check.py
```

which is used to execute the price-checking workflow.

Before running the scraper, make sure that:

* The required Python environment is activated.
* The Excel configuration is available.
* The relevant websites are enabled.
* Required browser dependencies are installed if browser automation is used.

## Output

The system produces two main types of output:

`RawData` contains the information directly collected from the individual website scrapers. 

This sheet preserves the collected website-level information and serves as the source data for the final report.

`Results` contains the final price-checking report.

The report compares each website's collected price information against the product's RRP after promotion.

The output is intended to provide a concise view of whether each retailer:
Matches the promotional price
Offers a lower price
Offers a higher price
Has the product unavailable

The Results sheet is the final report used for price monitoring and submission.

## Project Purpose

The project was developed to automate the collection and monitoring of XM product prices across multiple e-commerce websites.

Instead of manually visiting each retailer and recording prices, the system provides a repeatable workflow for:

· Collecting structured product data
· Monitoring product variants
· Checking retailer prices
· Tracking availability
· Comparing prices against promotional RRP
· Generating a standardized final report

The project is designed to reduce manual price-checking work while keeping the scraping, configuration, raw data, and final reporting processes structured and maintainable.