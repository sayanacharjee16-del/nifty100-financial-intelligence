import pandas as pd
import os

# Define file paths
source_dir = 'Data'
raw_dir = 'Data/cleaned/'
os.makedirs(raw_dir, exist_ok=True)

files = {
    'companies': 'companies.xlsx',
    'balancesheet': 'balancesheet.xlsx',
    'profitandloss': 'profitandloss.xlsx',
    'cashflow': 'cashflow.xlsx',
    'analysis': 'analysis.xlsx',
    'prosandcons': 'prosandcons.xlsx',
    'documents': 'documents.xlsx'
}


def extract():
    for table_name, file_name in files.items():
        path = os.path.join(source_dir, file_name)
        # Skip the title row found in your files (header=1)
        df = pd.read_excel(path, header=1)

        # Save as clean raw CSV
        output_path = os.path.join(raw_dir, f"{table_name}.csv")
        df.to_csv(output_path, index=False)
        print(f"Extracted {len(df)} rows for {table_name}")


if __name__ == "__main__":
    extract()