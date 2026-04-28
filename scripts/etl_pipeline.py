"""
ETL Pipeline — Amazon Products Sales Dataset
=============================================
Reads the raw CSV (with original scraped column names), cleans it,
renames columns, engineers features, and outputs a processed CSV.

Usage:
    python scripts/etl_pipeline.py

Input:  data/raw.csv
Output: data/processed.csv
"""

import os
import re
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw.csv"
OUT_FILE = BASE_DIR / "data" / "processed.csv"


def load_raw(path):
    print(f"[1/7] Loading {path.name}")
    df = pd.read_csv(path)
    print(f"      {len(df):,} rows x {len(df.columns)} cols")
    return df


def drop_duplicates(df):
    print("[2/7] Removing duplicates")
    before = len(df)
    df = df.drop_duplicates()
    print(f"      Removed {before - len(df)} duplicates")
    return df


def clean_prices(df):
    print("[3/7] Cleaning price columns")
    # Variant price: extract dollar amount
    df["price_on_variant"] = df["price_on_variant"].str.split(":").str.get(1)
    df.loc[~df["price_on_variant"].str.contains(r"\$", na=False), "price_on_variant"] = np.nan
    df["price_on_variant"] = df["price_on_variant"].str.strip().str.split(" ").str.get(0)

    # Fill missing discounted price from variant
    df["current/discounted_price"] = df["current/discounted_price"].fillna(df["price_on_variant"])

    # Strip $ and commas, cast to float
    for col in ["current/discounted_price", "listed_price"]:
        df[col] = (df[col].astype(str)
                   .str.replace("$", "", regex=False)
                   .str.replace(",", "", regex=False)
                   .str.strip()
                   .replace(["", "nan", "None"], np.nan)
                   .astype(float))

    # Fill missing listed_price from discounted
    df["listed_price"] = df["listed_price"].fillna(df["current/discounted_price"])

    # Drop variant column
    df.drop(columns=["price_on_variant"], inplace=True)

    # Compute discount percentage
    df["discount_percentage"] = (
        (df["listed_price"] - df["current/discounted_price"]) / df["listed_price"] * 100
    ).round(2).clip(lower=0)

    print("      Prices cleaned, discount_percentage computed")
    return df


def clean_rating(df):
    print("[4/7] Cleaning rating and review columns")
    df["rating"] = (df["rating"].str.replace("out of 5 stars", "", regex=False)
                    .str.strip().astype(float))

    df["number_of_reviews"] = (df["number_of_reviews"].str.replace(",", "", regex=False)
                                .str.strip().astype(float))

    def parse_bought(val):
        if pd.isna(val):
            return np.nan
        s = str(val).lower().replace(",", "").replace("+", "").strip()
        s = s.replace("bought in past month", "").strip()
        if "k" in s:
            return int(float(s.replace("k", "")) * 1000)
        try:
            return int(float(s))
        except ValueError:
            return np.nan

    df["bought_in_last_month"] = df["bought_in_last_month"].apply(parse_bought)
    print("      Rating, reviews, bought_last_month parsed")
    return df


def clean_categoricals(df):
    print("[5/7] Cleaning categorical columns")

    def clean_badge(val):
        if pd.isna(val) or val == "No Badge":
            return "No Badge"
        if "Best Seller" in str(val):
            return "Best Seller"
        if "Amazon" in str(val) and "Choice" in str(val):
            return "Amazon's Choice"
        if "Limited" in str(val):
            return "Limited time deal"
        return "No Badge"

    df["is_best_seller"] = df["is_best_seller"].apply(clean_badge)
    df["is_sponsored"] = df["is_sponsored"].map({"Sponsored": True, "Organic": False})
    df["has_coupon"] = df["is_couponed"].ne("No Coupon")
    df["coupon_value"] = df["is_couponed"].where(df["has_coupon"])
    df.drop(columns=["is_couponed"], inplace=True)
    df["buy_box_availability"] = df["buy_box_availability"].notna()

    # Parse delivery date
    collected_year = pd.to_datetime(df["collected_at"].dropna().iloc[0]).year
    df["delivery_details"] = df["delivery_details"].str.extract(
        r"(?:Mon|Tue|Wed|Thu|Fri|Sat|Sun)?,?\s*(\w+\s+\d{1,2})"
    )[0]
    df["delivery_details"] = pd.to_datetime(
        df["delivery_details"].astype(str) + f" {collected_year}", format="%B %d %Y", errors="coerce"
    )
    df["collected_at"] = pd.to_datetime(df["collected_at"])
    print("      Badges, sponsorship, coupons, dates cleaned")
    return df


def assign_categories(df):
    print("[6/7] Assigning product categories")
    KEYWORDS = {
        "Laptops": ["laptop", "notebook", "macbook", "chromebook", "ultrabook"],
        "Phones": ["phone", "iphone", "samsung galaxy", "smartphone", "pixel"],
        "Cameras": ["camera", "gopro", "dslr", "mirrorless", "webcam", "lens"],
        "Headphones": ["headphone", "earbud", "airpod", "earphone", "headset"],
        "Speakers": ["speaker", "soundbar", "subwoofer", "bluetooth speaker"],
        "TV & Display": ["tv", "television", "monitor", "display", "projector"],
        "Storage": ["hard drive", "ssd", "flash drive", "memory card", "usb drive"],
        "Networking": ["router", "modem", "wifi", "ethernet", "mesh"],
        "Gaming": ["gaming", "controller", "joystick", "gamepad", "xbox", "playstation"],
        "Smart Home": ["alexa", "echo", "smart plug", "smart light", "thermostat"],
        "Wearables": ["smartwatch", "fitness tracker", "fitbit", "apple watch"],
        "Printers & Scanners": ["printer", "scanner", "ink cartridge"],
        "Power & Batteries": ["charger", "battery", "power bank", "adapter", "surge protector"],
        "Chargers & Cables": ["cable", "usb-c", "lightning", "hdmi", "cord"],
    }

    def classify(title):
        t = str(title).lower()
        for cat, kws in KEYWORDS.items():
            if any(kw in t for kw in kws):
                return cat
        return "Other Electronics"

    df["product_category"] = df["title"].apply(classify)
    print(f"      {df['product_category'].nunique()} categories assigned")
    return df


def rename_columns(df):
    print("[7/7] Renaming columns")
    df = df.rename(columns={
        "title": "product_title",
        "rating": "product_rating",
        "number_of_reviews": "total_reviews",
        "bought_in_last_month": "purchased_last_month",
        "current/discounted_price": "discounted_price",
        "listed_price": "original_price",
        "delivery_details": "delivery_date",
        "sustainability_badges": "sustainability_tags",
        "image_url": "product_image_url",
        "product_url": "product_page_url",
        "collected_at": "data_collected_at",
    })
    return df


def run_pipeline():
    print("=" * 60)
    print("  ETL Pipeline — Amazon Products Sales Dataset")
    print("=" * 60)

    if not RAW_FILE.exists():
        csvs = list(RAW_FILE.parent.glob("*.csv"))
        if csvs:
            raw = csvs[0]
        else:
            print(f"  ERROR: No CSV found in {RAW_FILE.parent}")
            return
    else:
        raw = RAW_FILE

    df = load_raw(raw)
    df = drop_duplicates(df)
    df = clean_prices(df)
    df = clean_rating(df)
    df = clean_categoricals(df)
    df = assign_categories(df)
    df = rename_columns(df)

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT_FILE, index=False)
    print(f"\n  Saved to: {OUT_FILE}")
    print(f"  Final: {len(df):,} rows x {len(df.columns)} cols")
    print("=" * 60)


if __name__ == "__main__":
    run_pipeline()
