import pandas as pd
import numpy as np
import os
import re

# Paths matching your PyCharm sidebar
RAW_DIR = 'Data/cleaned/'
CLEAN_DIR = 'Data/clean/'
os.makedirs(CLEAN_DIR, exist_ok=True)

import re  # Add this import at the very top


def standardize_year(year_val):
    """
    Improved logic to handle '9m', '6m', and inconsistent spacing.
    """
    if pd.isna(year_val):
        return 2024

    year_str = str(year_val).strip().upper()

    if year_str == 'TTM':
        return 2025  # Mapping TTM as the current cycle

    # Use Regex to find any 4-digit number (the year) in the string
    # This ignores '9m', 'Mar', or extra spaces automatically
    match = re.search(r'(\d{4})', year_str)
    if match:
        return int(match.group(1))

    # Handle 2-digit years like 'Mar-24'
    match_short = re.search(r'-(\d{2})$', year_str)
    if match_short:
        return 2000 + int(match_short.group(1))

    # Final fallback if no year is found
    return 2024


def transform():
    print("Initializing Data Transformation (No Sectors)...")

    # 1. Clean Companies Dimension
    # We skip sector mapping and just save the raw company master list
    df_comp = pd.read_csv(f'{RAW_DIR}companies.csv')
    df_comp.to_csv(f'{CLEAN_DIR}dim_company.csv', index=False)
    print("✔ Dimension Table: dim_company.csv created")

    # 2. Transform P&L and Calculate Ratios
    df_pl = pd.read_csv(f'{RAW_DIR}profitandloss.csv')
    df_pl['fiscal_year'] = df_pl['year'].apply(standardize_year)

    # Formulas per Section 3.2[cite: 1]
    df_pl['net_profit_margin_pct'] = (df_pl['net_profit'] / df_pl['sales']) * 100
    df_pl['interest_coverage'] = df_pl['operating_profit'] / df_pl['interest'].replace(0, np.nan)

    df_pl.to_csv(f'{CLEAN_DIR}fact_profit_loss.csv', index=False)
    print("✔ Fact Table: fact_profit_loss.csv created")

    # 3. Transform Balance Sheet
    df_bs = pd.read_csv(f'{RAW_DIR}balancesheet.csv')
    df_bs['fiscal_year'] = df_bs['year'].apply(standardize_year)

    # Formula: borrowings / (equity_capital + reserves)[cite: 1]
    df_bs['debt_to_equity'] = df_bs['borrowings'] / (df_bs['equity_capital'] + df_bs['reserves']).replace(0, np.nan)

    df_bs.to_csv(f'{CLEAN_DIR}fact_balance_sheet.csv', index=False)
    print("✔ Fact Table: fact_balance_sheet.csv created")

    # 4. Transform Cash Flow & Cross-Table Ratios
    df_cf = pd.read_csv(f'{RAW_DIR}cashflow.csv')
    df_cf['fiscal_year'] = df_cf['year'].apply(standardize_year)

    # Free Cash Flow = operating + investing[cite: 1]
    df_cf['free_cash_flow'] = df_cf['operating_activity'] + df_cf['investing_activity']

    # Merge P&L into Cash Flow for the Cash Conversion Ratio[cite: 1]
    df_cf = df_cf.merge(df_pl[['company_id', 'fiscal_year', 'net_profit']],
                        on=['company_id', 'fiscal_year'], how='left')

    # Formula: operating_activity / net_profit[cite: 1]
    df_cf['cash_conversion_ratio'] = df_cf['operating_activity'] / df_cf['net_profit'].replace(0, np.nan)

    df_cf.to_csv(f'{CLEAN_DIR}fact_cash_flow.csv', index=False)
    print("✔ Fact Table: fact_cash_flow.csv created")

    print(f"\nTransformation Complete. Files saved to: {CLEAN_DIR}")


if __name__ == "__main__":
    transform()