import os
import duckdb
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
# The full path to the Iceberg table directory in GCS.
ICEBERG_TABLE_PATH = "gs://bl-dataproc-resources/warehouse/public_research/contributor_repo_commits_v2"

def query_iceberg_in_gcs():
    """
    Connects to a GCS bucket using DuckDB's Iceberg extension,
    configures authentication using environment variables, and queries the table.
    """
    # --- Get HMAC Credentials from Environment Variables ---
    gcs_access_key = os.getenv("GCS_ACCESS_KEY_ID")
    gcs_secret_key = os.getenv("GCS_SECRET_ACCESS_KEY")

    if not gcs_access_key or not gcs_secret_key:
        print("ERROR: Environment variables GCS_ACCESS_KEY_ID and GCS_SECRET_ACCESS_KEY must be set.")
        return

    print("INFO:     Found GCS credentials in environment variables.")

    # --- Initialize DuckDB and Load Extensions ---
    # Using an in-memory database
    con = duckdb.connect(config={'allow_unsigned_extensions': 'true'})

    print("INFO:     Installing and loading required extensions (httpfs, iceberg).")
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    con.execute("INSTALL iceberg;")
    con.execute("LOAD iceberg;")

    # --- Configure S3/GCS Provider Settings ---
    # We use the S3 provider since GCS is S3-compatible.
    print("INFO:     Configuring DuckDB's S3 provider for Google Cloud Storage.")
    con.execute(f"SET s3_access_key_id = '{gcs_access_key}';")
    con.execute(f"SET s3_secret_access_key = '{gcs_secret_key}';")
    con.execute("SET s3_endpoint = 'https://storage.googleapis.com';")
    # GCS often works best with 'path' style URLs
    con.execute("SET s3_url_style = 'path';")
    # Let DuckDB determine the region automatically
    con.execute("SET s3_region = 'auto';")


    print(f"INFO:     Successfully configured connection to GCS.")

    try:
        # --- Query 1: Describe the table to view column types ---
        print(f"\n--- Describing schema for table '{ICEBERG_TABLE_PATH}' ---")
        describe_query = f"""
        DESCRIBE SELECT *
        FROM iceberg_scan('{ICEBERG_TABLE_PATH}')
        LIMIT 0; -- We don't need any data, just the schema
        """
        schema_df = con.execute(describe_query).fetch_df()
        print("Query successful. Table Schema:")
        print(schema_df)

        # --- Query 2: Get a small sample of the data ---
        print(f"\n--- Querying a sample of 10 rows from '{ICEBERG_TABLE_PATH}' ---")
        query = f"""
        SELECT *
        FROM iceberg_scan('{ICEBERG_TABLE_PATH}')
        LIMIT 10;
        """
        sample_df = con.execute(query).fetch_df()
        print("Query successful. Sample data:")
        print(sample_df)

        # --- Query 3: Get the total row count ---
        print(f"\n--- Querying total row count from '{ICEBERG_TABLE_PATH}' ---")
        count_query = f"""
        SELECT COUNT(*) AS total_rows
        FROM iceberg_scan('{ICEBERG_TABLE_PATH}');
        """
        row_count = con.execute(count_query).fetch_df()
        print("Query successful. Total rows:")
        print(row_count)

        # --- (Optional) Inspect Table Metadata ---
        # This is useful for debugging if the scan fails.
        # metadata_query = f"SELECT * FROM iceberg_metadata('{ICEBERG_TABLE_PATH}')"
        # metadata_df = con.execute(metadata_query).fetch_df()
        # print("\n--- Iceberg Table Metadata ---")
        # print(metadata_df)


    except duckdb.Error as e:
        print(f"\nAn error occurred while querying the Iceberg table: {e}")
        print("Please check the following:")
        print("1. The ICEBERG_TABLE_PATH is correct.")
        print("2. The HMAC keys have the correct permissions ('Storage Object Viewer' or higher).")
        print("3. Your network connection allows access to storage.googleapis.com.")

    finally:
        # --- Clean up the connection ---
        con.close()
        print("\nINFO:     Connection closed.")


if __name__ == "__main__":
    query_iceberg_in_gcs()