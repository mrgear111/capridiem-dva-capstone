# Data Dictionary

> **Dataset:** Amazon Products Sales Dataset — 42K+ Items (2025)
> **Source:** [Kaggle — Ikram Ul Hassan](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025)
> **Licence:** CC BY-NC 4.0

---

## Raw Dataset Columns

| # | Column | Data Type | Description | Example |
|---|--------|-----------|-------------|---------|
| 1 | `product_title` | String | Complete product name/title | "boAt Rockerz 450 Bluetooth Headphone" |
| 2 | `product_rating` | Float | Average customer rating (0.0–5.0 scale) | 4.1 |
| 3 | `total_reviews` | Integer | Total number of customer reviews | 12,450 |
| 4 | `purchased_last_month` | Integer | Units purchased in the last month | 500 |
| 5 | `discounted_price` | Float | Current selling price after discount (INR) | 1,299.00 |
| 6 | `original_price` | Float | Original listed price before discount (INR) | 2,999.00 |
| 7 | `discount_percentage` | Float | Percentage discount applied (0–100) | 57 |
| 8 | `is_best_seller` | Boolean | Whether the product is tagged as a Best Seller | True |
| 9 | `is_sponsored` | Boolean | Whether the product is a Sponsored/Paid listing | False |
| 10 | `has_coupon` | Boolean | Whether a special discount coupon is available | True |
| 11 | `buy_box_availability` | Boolean | Buy Box button availability on search page (NaN = False) | True |
| 12 | `delivery_date` | DateTime | Estimated delivery date | 2025-09-15 |
| 13 | `sustainability_tags` | String | Eco-friendly and sustainability-related tags | "Climate Pledge Friendly" |
| 14 | `product_image_url` | String | Direct image link of the product | https://... |
| 15 | `product_page_url` | String | Official Amazon product page URL | https://... |
| 16 | `data_collected_at` | DateTime | Date when the data was scraped/collected | 2025-08-30 |
| 17 | `product_category` | String | Assigned product category | "Electronics" |

---

## Engineered Columns (Created During ETL)

These columns are added by `scripts/etl_pipeline.py` and available in the processed dataset.

| Column | Data Type | Formula / Logic | Purpose |
|--------|-----------|----------------|---------|
| `price_band` | Categorical | Binned from `discounted_price`: Budget (<₹500), Mid-Range (₹500–₹2,000), Premium (₹2,000–₹5,000), Luxury (>₹5,000) | Segment products by price tier for analysis |
| `discount_tier` | Categorical | Binned from `discount_percentage`: Low (0–20%), Medium (20–40%), High (40–60%), Very High (>60%) | Segment products by discount intensity |
| `revenue_proxy` | Float | `discounted_price × purchased_last_month` | Estimate revenue potential per product |
| `price_reduction` | Float | `original_price − discounted_price` | Absolute savings amount in INR |
| `quality_engagement` | Float | `product_rating × log1p(total_reviews)` | Quality-weighted engagement score |

---

## Data Quality Notes

| Issue | Details | Treatment |
|-------|---------|-----------|
| Missing `product_rating` | ~100–200 rows | Imputed with category-level median |
| Missing `total_reviews` | ~100–200 rows | Imputed with 0 (no reviews yet) |
| Missing `discount_percentage` | ~50–100 rows | Recalculated from price columns |
| Missing `sustainability_tags` | ~500+ rows | Retained as NaN — not used quantitatively |
| Missing `buy_box_availability` | Varies | NaN treated as False |
| Price formatting | ₹ symbols and commas in price fields | Stripped and cast to float64 |
| Duplicates | ~200 duplicate product_title entries | Removed (kept first occurrence) |
| Extreme discounts | discount_percentage > 90% | Flagged and capped at 99th percentile |

---

## Files

| File | Location | Description |
|------|----------|-------------|
| `amazon_products_sales_data_uncleaned.csv` | `data/raw/` | Original raw dataset — never modified |
| `amazon_products_sales_data_cleaned.csv` | `data/raw/` | Pre-cleaned version from Kaggle |
| `amazon_products_cleaned.csv` | `data/processed/` | Output of ETL pipeline with engineered features |
