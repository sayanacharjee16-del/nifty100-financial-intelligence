import pandas as pd
from sqlalchemy import create_engine
import os

# 1. Replace this with your actual connection string from the Neon Dashboard
# PRO TIP: Add '?sslmode=require' at the end if it's not there
NEON_CONN_STR = "postgresql://neondb_owner:npg_8kRqPGY7JuTg@ep-floral-glade-amvlhjb0-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

CLEAN_DIR = 'Data/clean/'


def load_to_neon():
    try:
        # 2. Create the connection engine
        engine = create_engine(NEON_CONN_STR)
        print("Successfully connected to Neon DB!")

        # Dimension-first loading order
        load_order = [
            ('dim_company', 'dim_company.csv'),
            ('fact_profit_loss', 'fact_profit_loss.csv'),
            ('fact_balance_sheet', 'fact_balance_sheet.csv'),
            ('fact_cash_flow', 'fact_cash_flow.csv')
        ]

        for table_name, file_name in load_order:
            file_path = os.path.join(CLEAN_DIR, file_name)
            if os.path.exists(file_path):
                df = pd.read_csv(file_path)

                # 'replace' creates the table for you automatically!
                df.to_sql(table_name, engine, if_exists='replace', index=False)
                print(f"✔ {table_name} uploaded ({len(df)} rows)")
            else:
                print(f"✘ Missing file: {file_name}")

        print("\n🚀 All data is now live on Neon!")

    except Exception as e:
        print(f"❌ Connection failed: {e}")


if __name__ == "__main__":
    load_to_neon()