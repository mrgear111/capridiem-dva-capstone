# Optimizing Product Performance and Revenue Strategy in an E-Commerce Marketplace

> **Data Visualization & Analytics — Capstone 2**
> Newton School of Technology | B.Tech AI & ML | April 2026

---

## Overview

This project analyses **42,675 Amazon electronics product listings** to identify the key drivers of product performance, pricing effectiveness, and customer engagement in an e-commerce marketplace. The analysis pipeline covers data extraction, cleaning, exploratory analysis, statistical testing, and interactive dashboard design — delivering actionable recommendations for pricing strategy, category investment, and promotional optimization.

## Problem Statement

In a highly competitive e-commerce environment, understanding product performance, pricing strategies, and customer engagement is critical for maximizing revenue and profitability. The dataset contains over 42,000 product records, including attributes such as product categories, pricing, discounts, ratings, and sales-related indicators. The objective is to perform an end-to-end data analysis to identify key factors influencing product sales and customer preferences — through cleaning, EDA, statistical analysis, and an interactive Tableau dashboard.

## Key Findings

- **Other Electronics and Laptops dominate** the catalogue, together accounting for over 40% of all listings.
- **Most products have zero discount** — the median discount percentage is 0%, with a mean of only 6.5%.
- **Top 5 categories account for the majority of engagement** — marketing budget should be concentrated here.
- **Products priced $50–$200** represent the sweet spot for customer engagement and review volume.
- **Best Seller badge is rare** (only 275 out of 42,675 products) but correlates with higher purchase volumes.
- **Coupons are uncommon** (only ~1,948 products) but correlate with higher purchased_last_month.

## Repository Structure

```
├── README.md
├── data/
│   ├── raw.csv                           # Original dataset (never edited)
│   └── processed.csv                     # Cleaned output from pipeline
├── notebooks/
│   ├── 01_extraction.ipynb               # Data extraction and initial loading
│   ├── 02_cleaning.ipynb                 # Data cleaning and ETL pipeline
│   ├── 03_eda.ipynb                      # Exploratory data analysis
│   ├── 04_statistical_analysis.ipynb     # Statistical tests and segmentation
│   └── 05_final_load_prep.ipynb          # Final data preparation for Tableau
├── scripts/
│   └── etl_pipeline.py                   # Standalone ETL pipeline script
├── tableau/
│   ├── screenshots/                      # Dashboard screenshots
│   └── dashboard_links.md                # Tableau Public URLs
├── reports/
│   ├── project_report.pdf                # Final project report (18 sections)
│   └── presentation.pdf                  # Project presentation slides
└── docs/
    └── data_dictionary.md                # Full column definitions and metadata
```

## Dataset

| Attribute       | Value                                        |
|-----------------|----------------------------------------------|
| **Source**       | [Amazon Products Sales Dataset — 42K+ Items (2025)](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025) |
| **Author**       | Ikram Ul Hassan (Kaggle)                     |
| **Records**      | 42,675 product listings                      |
| **Columns**      | 18 features                                  |
| **Licence**      | CC BY-NC 4.0                                 |
| **Files**        | Cleaned + Uncleaned versions                 |

### Key Columns

| Column | Description |
|--------|-------------|
| `product_title` | Complete product name/title |
| `product_rating` | Average customer rating (out of 5) |
| `total_reviews` | Total number of customer reviews |
| `purchased_last_month` | Units purchased in the last month |
| `discounted_price` | Current price after discount (USD) |
| `original_price` | Original listed price (USD) |
| `discount_percentage` | Percentage discount applied |
| `is_best_seller` | Badge status: Best Seller / Amazon's Choice / Limited time deal / No Badge |
| `is_sponsored` | Sponsored listing (True/False) |
| `has_coupon` | Coupon availability (True/False) |
| `coupon_value` | Coupon detail string (e.g., "Save 15% with coupon") |
| `product_category` | Assigned category (e.g., Laptops, Phones, Cameras) |

## Setup & Usage

### Prerequisites

- Python 3.9+
- Jupyter Notebook
- Tableau Public (for dashboard)

### Installation

```bash
git clone https://github.com/mrgear111/Capstone-2-dva.git
cd Capstone-2-dva
pip install -r requirements.txt
```

### Running the ETL Pipeline

```bash
python scripts/etl_pipeline.py
```

This reads from `data/raw.csv`, processes the data, and outputs to `data/processed.csv`.

### Running Notebooks

Open notebooks in order:

```
01_extraction.ipynb → 02_cleaning.ipynb → 03_eda.ipynb → 04_statistical_analysis.ipynb → 05_final_load_prep.ipynb
```

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python 3.x | Data cleaning, EDA, statistical analysis |
| pandas | Data manipulation and transformation |
| matplotlib / seaborn | Data visualisation |
| scipy / statsmodels | Statistical testing |
| Tableau Public | Interactive dashboard |
| GitHub | Version control and collaboration |

## Tableau Dashboard

**Dashboard URL:** [INSERT TABLEAU PUBLIC URL]

The dashboard includes two views:
1. **Executive Summary View** — KPI cards, category treemap, discount-vs-rating scatter plot
2. **Operational Drill-Down View** — Interactive filters by category, price band, discount tier, and badge status

## Team

| Name | Role |
|------|------|
| [Sameer Pawar] | [Documentation &amp; Report Writing] |
| [Daksh Saini] | [Tableau Dashboard] |
| [Padam Rathi] | [Dataset &amp; Filtering] |
| [Vidhit T S] | [Tableau &amp; Pipelines] |

## Licence

This project is for academic purposes as part of the DVA Capstone 2 course at Newton School of Technology. The dataset is used under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) licence.
