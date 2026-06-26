def transform_records() -> pd.DataFrame:
    
    valid_csv_path = config["paths"]["valid"]

    if not os.path.exists(valid_csv_path):
        logger.warning(
            f"{valid_csv_path} does not exist yet."
        )
        return pd.DataFrame()

    df = pd.read_csv(valid_csv_path)

    required_columns = ["id"]

    missing_columns = [
        col
        for col in required_columns
        if col not in df.columns
    ]

    if missing_columns:
        logger.error(
            f"Missing required columns: {missing_columns}"
        )
        return pd.DataFrame()

    df = (
        df
        .dropna(subset=["id"])
        .drop_duplicates(subset=["id"], keep="last")
    )

    if "email" in df.columns:
        df["email"] = (
            df["email"]
            .fillna("")
            .str.strip()
            .str.lower()
        )

    if "username" in df.columns:
        df["username"] = (
            df["username"]
            .fillna("")
            .str.strip()
            .str.lower()
        )

    if "website" in df.columns:
        df["website"] = df["website"].fillna("N/A")

    if "timestamp" in df.columns:
        df["timestamp"] = df["timestamp"].fillna(
            datetime.now().isoformat()
        )

    logger.info(
        f"Successfully transformed {len(df)} unique records"
    )

    return df



















def main():
    logger.info(
        "Starting Alpha Data Pipeline Process..."
    )

    if not API_URL:
        logger.error(
            "Environment configuration missing: API_URL variable not loaded."
        )
        return

    raw_payloads = fetch_api_data(API_URL)

    if not raw_payloads:
        logger.warning(
            "Pipeline run completed early: No raw records fetched from target stream."
        )
        return

    valid, invalid = ingest_payloads(raw_payloads)

    valid_to_csv(valid)
    invalid_to_json(invalid)

    clean_df = transform_records()

    logger.info(
        "Data Pipeline run executed successfully."
    )


if __name__ == "__main__":
    main()

