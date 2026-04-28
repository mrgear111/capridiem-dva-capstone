"""
ETL Pipeline — Amazon Products Sales Dataset
=============================================
Standalone script that reads the raw CSV, cleans it, engineers features,
and outputs a processed CSV ready for analysis and Tableau.

Usage:
    python scripts/etl_pipeline.py

Input:  data/raw/amazon_products_sales_data_uncleaned.csv
Output: data/processed/amazon_products_cleaned.csv
"""

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path


# ── Paths ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"

RAW_FILE = RAW_DIR / "amazon_products_sales_data_uncleaned.csv"
CLEANED_FILE = PROCESSED_DIR / "amazon_products_cleaned.csv"


def load_raw_data(filepath: Path) -> pd.DataFrame:
    """Step 1 — Load the raw CSV and perform initial inspection."""
    print(f"[1/6] Loading raw data from {filepath}")
    df = pd.read_csv(filepath)
    print(f"      Loaded {len(df):,} rows × {len(df.columns)} columns")
    print(f"      Columns: {list(df.columns)}")
    print(f"      Missing values:\n{df.isnull().sum()[df.isnull().sum() > 0]}")
    return df


def clean_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Step 2 — Handle missing values."""
    print("[2/6] Handling missing values")

    # Numeric columns — impute with median or 0
    if "product_rating" in df.columns:
        median_rating = df["product_rating"].median()
        filled = df["product_rating"].isnull().sum()
        df["product_rating"] = df["product_rating"].fillna(median_rating)
        print(f"      product_rating: filled {filled} nulls with median ({median_rating:.1f})")

    if "total_reviews" in df.columns:
        filled = df["total_reviews"].isnull().sum()
        df["total_reviews"] = df["total_reviews"].fillna(0)
        print(f"      total_reviews: filled {filled} nulls with 0")

    if "purchased_last_month" in df.columns:
        filled = df["purchased_last_month"].isnull().sum()
        df["purchased_last_month"] = df["purchased_last_month"].fillna(0)
        print(f"      purchased_last_month: filled {filled} nulls with 0")

    # Boolean columns — treat NaN as False
    for col in ["is_best_seller", "is_sponsored", "has_coupon", "buy_box_availability"]:
        if col in df.columns:
            filled = df[col].isnull().sum()
            df[col] = df[col].fillna(False)
            print(f"      {col}: filled {filled} nulls with False")

    # Text columns — leave as NaN
    for col in ["sustainability_tags"]:
        if col in df.columns:
            nulls = df[col].isnull().sum()
            print(f"      {col}: {nulls} nulls retained (not used in quantitative analysis)")

    return df


def clean_price_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Step 3 — Strip currency symbols, commas, and cast to float."""
    print("[3/6] Cleaning price columns")

    def parse_price(series):
        """Remove ₹, commas, whitespace, and % symbols; cast to float."""
        return (
            series.astype(str)
            .str.replace("₹", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.replace("%", "", regex=False)
            .str.strip()
            .replace(["", "nan", "None"], np.nan)
            .astype(float)
        )

    for col in ["discounted_price", "original_price"]:
        if col in df.columns:
            df[col] = parse_price(df[col])
            print(f"      {col}: cleaned and cast to float64")

    if "discount_percentage" in df.columns:
        df["discount_percentage"] = parse_price(df["discount_percentage"])
        print("      discount_percentage: cleaned and cast to float64")

    # Recalculate discount_percentage where missing but prices exist
    mask = df["discount_percentage"].isnull() & df["original_price"].notna() & df["discounted_price"].notna()
    if mask.sum() > 0:
        df.loc[mask, "discount_percentage"] = (
            (df.loc[mask, "original_price"] - df.loc[mask, "discounted_price"])
            / df.loc[mask, "original_price"] * 100
        ).round(1)
        print(f"      discount_percentage: recalculated {mask.sum()} values from price columns")

    return df


def handle_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Step 4 — Detect and cap outliers using IQR method."""
    print("[4/6] Detecting and capping outliers")

    for col in ["discounted_price", "original_price", "discount_percentage"]:
        if col not in df.columns:
            continue
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        upper = Q3 + 1.5 * IQR

        # Cap at 99th percentile instead of removing
        cap_val = df[col].quantile(0.99)
        outliers = (df[col] > upper).sum()
        df[col] = df[col].clip(upper=cap_val)
        print(f"      {col}: {outliers} outliers detected, capped at {cap_val:.0f}")

    # Flag extreme discounts
    if "discount_percentage" in df.columns:
        extreme = (df["discount_percentage"] > 90).sum()
        if extreme > 0:
            print(f"      WARNING: {extreme} products with discount > 90% flagged for review")

    return df


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Step 5 — Create derived columns for analysis."""
    print("[5/6] Engineering features")

    # Price band
    if "discounted_price" in df.columns:
        bins = [0, 500, 2000, 5000, float("inf")]
        labels = ["Budget (<500)", "Mid-Range (500-2000)", "Premium (2000-5000)", "Luxury (>5000)"]
        df["price_band"] = pd.cut(df["discounted_price"], bins=bins, labels=labels, right=False)
        print("      Created: price_band")

    # Discount tier
    if "discount_percentage" in df.columns:
        bins_d = [0, 20, 40, 60, 100]
        labels_d = ["Low (0-20%)", "Medium (20-40%)", "High (40-60%)", "Very High (>60%)"]
        df["discount_tier"] = pd.cut(df["discount_percentage"], bins=bins_d, labels=labels_d, right=False)
        print("      Created: discount_tier")

    # Revenue proxy
    if "discounted_price" in df.columns and "purchased_last_month" in df.columns:
        df["revenue_proxy"] = df["discounted_price"] * df["purchased_last_month"]
        print("      Created: revenue_proxy = discounted_price × purchased_last_month")

    # Price reduction
    if "original_price" in df.columns and "discounted_price" in df.columns:
        df["price_reduction"] = df["original_price"] - df["discounted_price"]
        print("      Created: price_reduction = original_price - discounted_price")

    # Quality-weighted engagement
    if "product_rating" in df.columns and "total_reviews" in df.columns:
        df["quality_engagement"] = df["product_rating"] * np.log1p(df["total_reviews"])
        print("      Created: quality_engagement = product_rating × log1p(total_reviews)")

    return df


def deduplicate_and_validate(df: pd.DataFrame) -> pd.DataFrame:
    """Step 6 — Remove duplicates and run final validation."""
    print("[6/6] Deduplication and validation")

    before = len(df)
    if "product_title" in df.columns:
        df = df.drop_duplicates(subset=["product_title"], keep="first")
    else:
        df = df.drop_duplicates(keep="first")
    dupes = before - len(df)
    print(f"      Removed {dupes} duplicate rows")

    # Final null check on key columns
    key_cols = ["product_title", "discounted_price", "product_rating",
                "total_reviews", "discount_percentage", "product_category"]
    key_cols = [c for c in key_cols if c in df.columns]
    remaining_nulls = df[key_cols].isnull().sum().sum()
    if remaining_nulls > 0:
        print(f"      WARNING: {remaining_nulls} nulls remain in key columns — dropping those rows")
        df = df.dropna(subset=key_cols)
    else:
        print("      Validation passed: no nulls in key analytical columns")

    print(f"      Final dataset: {len(df):,} rows × {len(df.columns)} columns")
    return df


def run_pipeline():
    """Execute the full ETL pipeline."""
    print("=" * 60)
    print("  ETL Pipeline — Amazon Products Sales Dataset")
    print("=" * 60)

    # Check input exists
    if not RAW_FILE.exists():
        # Try alternate filename
        alt = RAW_DIR / "amazon_products_sales_data_cleaned.csv"
        if alt.exists():
            raw_file = alt
        else:
            # Look for any CSV in raw/
            csvs = list(RAW_DIR.glob("*.csv"))
            if csvs:
                raw_file = csvs[0]
                print(f"  Using found CSV: {raw_file.name}")
            else:
                print(f"  ERROR: No CSV found in {RAW_DIR}")
                print(f"  Please place the raw dataset in data/raw/")
                return
    else:
        raw_file = RAW_FILE

    # Ensure output directory exists
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    # Run steps
    df = load_raw_data(raw_file)
    df = clean_missing_values(df)
    df = clean_price_columns(df)
    df = handle_outliers(df)
    df = engineer_features(df)
    df = deduplicate_and_validate(df)

    # Save
    df.to_csv(CLEANED_FILE, index=False)
    print(f"\n  Cleaned dataset saved to: {CLEANED_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
