import pandas as pd
from sqlalchemy import create_engine
import numpy as np

# Replace with your actual Neon connection string
CONN_STR = "postgresql://neondb_owner:npg_8kRqPGY7JuTg@ep-floral-glade-amvlhjb0-pooler.c-5.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


def generate_health_scores():
    engine = create_engine(CONN_STR)

    # 1. Pull the metrics
    # We use a broad join to ensure we get all companies even if metrics are missing
    df_pl = pd.read_sql("SELECT company_id, net_profit_margin_pct FROM fact_profit_loss WHERE fiscal_year = 2025",
                        engine)
    df_bs = pd.read_sql("SELECT company_id, debt_to_equity FROM fact_balance_sheet WHERE fiscal_year = 2025", engine)

    df = df_pl.merge(df_bs, on='company_id', how='outer')

    # 2. Data Cleaning - Fill NaNs with 0 to prevent the "Index([nan...])" error
    df['net_profit_margin_pct'] = pd.to_numeric(df['net_profit_margin_pct'], errors='coerce').fillna(0)
    df['debt_to_equity'] = pd.to_numeric(df['debt_to_equity'], errors='coerce').fillna(0)

    # 3. Scoring with Safety Checks
    # Profitability Score
    if df['net_profit_margin_pct'].nunique() > 1:
        df['p_score'] = pd.qcut(df['net_profit_margin_pct'].rank(method='first'), 5,
                                labels=[10, 20, 30, 40, 50]).astype(int)
    else:
        df['p_score'] = 30  # Default average if no data varies[cite: 1]

    # Leverage Score
    if df['debt_to_equity'].nunique() > 1:
        df['l_score'] = pd.qcut(df['debt_to_equity'].rank(method='first', ascending=False), 5,
                                labels=[10, 20, 30, 40, 50]).astype(int)
    else:
        df['l_score'] = 30  # Default average if no data varies[cite: 1]

    df['overall_score'] = df['p_score'] + df['l_score']

    # 4. Assign Health Labels[cite: 1]
    def get_label(score):
        if score >= 80: return 'EXCELLENT'
        if score >= 60: return 'GOOD'
        if score >= 40: return 'AVERAGE'
        if score >= 20: return 'WEAK'
        return 'POOR'

    df['health_label'] = df['overall_score'].apply(get_label)

    # 5. Load back to Neon[cite: 1]
    df_scores = df[['company_id', 'overall_score', 'health_label']]
    df_scores.to_sql('fact_ml_scores', engine, if_exists='replace', index=False)
    print(f"✔ Successfully scored {len(df_scores)} companies and uploaded to Neon!")


if __name__ == "__main__":
    generate_health_scores()