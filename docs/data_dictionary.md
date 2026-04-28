# Data Dictionary

> **Dataset:** Amazon Products Sales Dataset — 42K+ Items (2025)
> **Source:** [Kaggle — Ikram Ul Hassan](https://www.kaggle.com/datasets/ikramshah512/amazon-products-sales-dataset-42k-items-2025)
> **Licence:** CC BY-NC 4.0 | **Marketplace:** Amazon.com (US)

---

## Processed Dataset Columns (`data/processed.csv` — 42,675 rows × 18 columns)

| # | Column | Type | Nulls | Description |
|---|--------|------|-------|-------------|
| 1 | `product_title` | String | 0 | Product name |
| 2 | `product_rating` | Float | 1,024 | Customer rating (1.0–5.0) |
| 3 | `total_reviews` | Float | 1,024 | Number of reviews |
| 4 | `purchased_last_month` | Float | 10,511 | Units purchased last month |
| 5 | `discounted_price` | Float | 2,062 | Selling price after discount (USD) |
| 6 | `original_price` | Float | 2,062 | Listed price before discount (USD) |
| 7 | `is_best_seller` | String | 0 | Badge: No Badge / Amazon's Choice / Limited time deal / Best Seller |
| 8 | `is_sponsored` | Bool | 0 | Sponsored listing (True/False) |
| 9 | `buy_box_availability` | Bool | 0 | Buy Box available |
| 10 | `delivery_date` | String | 11,983 | Parsed delivery date |
| 11 | `sustainability_tags` | String | 39,267 | Eco tags (92% missing) |
| 12 | `product_image_url` | String | 0 | Image URL |
| 13 | `product_page_url` | String | 2,069 | Amazon product page URL |
| 14 | `data_collected_at` | String | 0 | Scrape timestamp |
| 15 | `discount_percentage` | Float | 2,062 | Computed discount % (mean 6.5%, median 0%) |
| 16 | `has_coupon` | Bool | 0 | Coupon available (True/False) |
| 17 | `coupon_value` | String | 40,727 | Coupon detail e.g. "Save 15% with coupon" |
| 18 | `product_category` | String | 0 | Product category (15 categories) |

## Raw Dataset Columns (`data/raw.csv` — 16 columns)

| # | Column | Description |
|---|--------|-------------|
| 1 | `title` | Raw product title |
| 2 | `rating` | "4.6 out of 5 stars" |
| 3 | `number_of_reviews` | "12,450" (string with commas) |
| 4 | `bought_in_last_month` | "300+ bought in past month" |
| 5 | `current/discounted_price` | "$89.68" |
| 6 | `price_on_variant` | Variant pricing info |
| 7 | `listed_price` | "$159.00" |
| 8 | `is_best_seller` | Badge text |
| 9 | `is_sponsored` | "Sponsored" / "Organic" |
| 10 | `is_couponed` | Coupon text or "No Coupon" |
| 11 | `buy_box_availability` | "Add to cart" or NaN |
| 12 | `delivery_details` | "Delivery Mon, Sep 1" |
| 13 | `sustainability_badges` | Eco tags |
| 14 | `image_url` | Image URL |
| 15 | `product_url` | Product page URL |
| 16 | `collected_at` | Scrape timestamp |

## Category Distribution

| Category | Count |
|----------|-------|
| Other Electronics | 8,755 |
| Laptops | 8,693 |
| Phones | 6,563 |
| Cameras | 3,677 |
| Power & Batteries | 2,877 |
| TV & Display | 2,630 |
| Chargers & Cables | 1,833 |
| Storage | 1,630 |
| Speakers | 1,345 |
| Networking | 1,070 |
| Headphones | 997 |
| Printers & Scanners | 877 |
| Gaming | 809 |
| Smart Home | 465 |
| Wearables | 454 |

## Key Statistics

| Metric | Value |
|--------|-------|
| Mean `product_rating` | 4.40 (median 4.50) |
| Mean `discounted_price` | $243 (median $85) |
| Mean `discount_percentage` | 6.5% (median 0%) |
| Mean `purchased_last_month` | 1,294 (median 200) |
