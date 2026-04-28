# Optimizing Product Performance and Revenue Strategy in an E-Commerce Marketplace

> **Data Visualization & Analytics — Capstone 2**
> Newton School of Technology | B.Tech AI & ML | April 2026

---

## Overview

This project analyses **42,000+ Amazon product listings** to identify the key drivers of product performance, pricing effectiveness, and customer engagement in an e-commerce marketplace. The analysis pipeline covers data extraction, cleaning, exploratory analysis, statistical testing, and interactive dashboard design — delivering actionable recommendations for pricing strategy, category investment, and promotional optimization.

## Problem Statement

In a highly competitive e-commerce environment, understanding product performance, pricing strategies, and customer engagement is critical for maximizing revenue and profitability. The dataset contains over 42,000 product records, including attributes such as product categories, pricing, discounts, ratings, and sales-related indicators. The objective is to perform an end-to-end data analysis to identify key factors influencing product sales and customer preferences — through cleaning, EDA, statistical analysis, and an interactive Tableau dashboard.

## Key Findings

- **Electronics dominates revenue** but carries the highest price volatility — targeted discounts outperform blanket promotions.
- **Discounts beyond 40% reduce perceived quality** without increasing customer engagement.
- **Top 5 categories account for ~68% of engagement** — marketing budget should be concentrated here.
- **₹500–₹2,000 price band** is the optimal zone for customer engagement and review volume.
- **Best Seller products have 2-3x higher purchase volume** — investing in badge acquisition has measurable ROI.
- **Coupons outperform percentage discounts** at driving purchase volume.

## Repository Structure

```
├── README.md
├── data/
│   ├── raw/                              # Original dataset (never edited)
│   └── processed/                        # Cleaned output from pipeline
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
| **Records**      | ~42,000 product listings                     |
| **Columns**      | 17 features                                  |
| **Licence**      | CC BY-NC 4.0                                 |
| **Files**        | Cleaned + Uncleaned versions                 |

### Key Columns

| Column | Description |
|--------|-------------|
| `product_title` | Complete product name/title |
| `product_rating` | Average customer rating (out of 5) |
| `total_reviews` | Total number of customer reviews |
| `purchased_last_month` | Units purchased in the last month |
| `discounted_price` | Current price after discount (INR) |
| `original_price` | Original listed price (INR) |
| `discount_percentage` | Percentage discount applied |
| `is_best_seller` | Best Seller tag (True/False) |
| `is_sponsored` | Sponsored listing (True/False) |
| `has_coupon` | Coupon availability (True/False) |
| `product_category` | Assigned product category |

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

This reads from `data/raw/`, processes the data, and outputs to `data/processed/`.

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
2. **Operational Drill-Down View** — Interactive filters by category, price band, discount tier, and Best Seller status

## Team

| Name | Role |
|------|------|
| [Name 1] | [Role] |
| [Name 2] | [Role] |
| [Name 3] | [Role] |
| [Name 4] | [Role] |
| [Name 5] | [Role] |

## Licence

This project is for academic purposes as part of the DVA Capstone 2 course at Newton School of Technology. The dataset is used under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) licence.
