import os
import pandas as pd
import numpy as np


RAW_DATA_PATH = "data/raw/properties.csv"
PROCESSED_DATA_PATH = "data/processed/property_knowledge_base.csv"


def load_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("/", "_")
    )
    return df


def build_property_type(row):
    subclass = row.get("ms_subclass", np.nan)
    bldg_type = str(row.get("bldg_type", "")).strip()
    house_style = str(row.get("house_style", "")).strip()

    return f"{bldg_type} {house_style} Class {subclass}"


def has_value(value) -> int:
    if pd.isna(value):
        return 0
    if str(value).strip() in ["", "NA", "None", "nan"]:
        return 0
    return 1


def yes_no(value) -> int:
    if pd.isna(value):
        return 0
    value = str(value).strip().lower()
    return 1 if value in ["y", "yes", "true", "1"] else 0


def create_knowledge_base(df: pd.DataFrame) -> pd.DataFrame:
    kb = pd.DataFrame()

    kb["property_id"] = df["pid"]
    kb["neighborhood"] = df["neighborhood"]
    kb["property_type"] = df.apply(build_property_type, axis=1)
    kb["house_style"] = df["house_style"]
    kb["year_built"] = df["year_built"]
    kb["overall_quality"] = df["overall_qual"]
    kb["overall_condition"] = df["overall_cond"]
    kb["sale_price"] = df["saleprice"]

    kb["lot_area"] = df["lot_area"]
    kb["living_area_sqft"] = df["gr_liv_area"]
    kb["bedrooms"] = df["bedroom_abvgr"]
    kb["bathrooms"] = df["full_bath"] + (0.5 * df["half_bath"])
    kb["total_rooms"] = df["totrms_abvgrd"]

    kb["garage_spaces"] = df["garage_cars"].fillna(0)
    kb["garage_area"] = df["garage_area"].fillna(0)

    kb["central_air"] = df["central_air"].apply(yes_no)
    kb["fireplaces"] = df["fireplaces"].fillna(0)
    kb["has_basement"] = df["total_bsmt_sf"].fillna(0).apply(lambda x: 1 if x > 0 else 0)
    kb["finished_basement_sqft"] = df["bsmtfin_sf_1"].fillna(0) + df["bsmtfin_sf_2"].fillna(0)
    kb["has_deck"] = df["wood_deck_sf"].fillna(0).apply(lambda x: 1 if x > 0 else 0)
    kb["has_porch"] = df["open_porch_sf"].fillna(0).apply(lambda x: 1 if x > 0 else 0)
    kb["has_pool"] = df["pool_area"].fillna(0).apply(lambda x: 1 if x > 0 else 0)
    kb["has_fence"] = df["fence"].apply(has_value)

    kb["kitchen_quality"] = df["kitchen_qual"]
    kb["exterior_quality"] = df["exter_qual"]
    kb["heating_quality"] = df["heating_qc"]
    kb["garage_quality"] = df["garage_qual"].fillna("NA")

    kb["amenity_count"] = (
        kb["central_air"]
        + (kb["fireplaces"] > 0).astype(int)
        + kb["has_basement"]
        + (kb["finished_basement_sqft"] > 0).astype(int)
        + kb["has_deck"]
        + kb["has_porch"]
        + kb["has_pool"]
        + kb["has_fence"]
        + (kb["garage_spaces"] > 0).astype(int)
    )

    kb["completeness_score"] = (
        20
        + (kb["sale_price"].notna().astype(int) * 15)
        + (kb["living_area_sqft"].notna().astype(int) * 15)
        + (kb["bedrooms"].notna().astype(int) * 10)
        + (kb["bathrooms"].notna().astype(int) * 10)
        + (kb["neighborhood"].notna().astype(int) * 10)
        + (kb["garage_spaces"].notna().astype(int) * 10)
        + (kb["amenity_count"].apply(lambda x: 1 if x >= 3 else 0) * 10)
    )

    kb["recommended_keywords"] = kb.apply(
        lambda row: ", ".join([
            str(row["neighborhood"]),
            str(row["house_style"]),
            "central air" if row["central_air"] == 1 else "",
            "garage" if row["garage_spaces"] > 0 else "",
            "basement" if row["has_basement"] == 1 else "",
            "fireplace" if row["fireplaces"] > 0 else "",
            "deck" if row["has_deck"] == 1 else "",
            "porch" if row["has_porch"] == 1 else "",
        ]).replace(", ,", ",").strip(", "),
        axis=1
    )

    kb["quality_label"] = np.where(
        kb["overall_quality"] >= 7,
        "High Quality",
        np.where(kb["overall_quality"] >= 5, "Medium Quality", "Low Quality")
    )

    return kb


def main():
    os.makedirs("data/processed", exist_ok=True)

    df = load_data(RAW_DATA_PATH)
    df = clean_column_names(df)
    kb = create_knowledge_base(df)

    kb.to_csv(PROCESSED_DATA_PATH, index=False)

    print("Knowledge base created successfully.")
    print(f"Rows: {len(kb)}")
    print(f"Columns: {len(kb.columns)}")
    print(f"Saved to: {PROCESSED_DATA_PATH}")


if __name__ == "__main__":
    main()
