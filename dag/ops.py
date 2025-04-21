from dagster import op
import pandas as pd
from process import read_in_csv, clean_data
from api import insert_bulk_users  # Assuming this writes to Supabase

from typing import List, Dict

@op
def read_csv_op(context, filepath: str) -> pd.DataFrame:
    df = read_in_csv(filepath)
    context.log.info(f"Read CSV with {len(df)} rows.")
    return df

@op
def clean_data_op(context, df: pd.DataFrame) -> List[Dict]:
    cleaned = clean_data(df)  # this returns a list of dicts now
    context.log.info(f"Cleaned {len(cleaned)} rows.")
    return cleaned

@op
def send_to_supabase_op(context, records: List[Dict]) -> None:
    insert_bulk_users(records)
    context.log.info(f"Inserted {len(records)} rows into Supabase.")
