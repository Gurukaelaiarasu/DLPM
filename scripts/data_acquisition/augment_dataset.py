import argparse
import os
import numpy as np
import pandas as pd


def augment(df: pd.DataFrame, target_rows: int) -> pd.DataFrame:
    """Augment dataframe until at least target_rows are reached."""
    out = [df]
    current = len(df)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    while current < target_rows:
        copy_df = df.sample(frac=1, replace=True).reset_index(drop=True)
        for col in numeric_cols:
            noise = np.random.normal(scale=0.05, size=len(copy_df))
            copy_df[col] = pd.to_numeric(copy_df[col], errors="coerce") * (1 + noise)
        out.append(copy_df)
        current += len(copy_df)
    return pd.concat(out, ignore_index=True)[:target_rows]


def main(existing: str, scraped: str, output: str, target_rows: int):
    dfs = []
    for path in [existing, scraped]:
        if os.path.exists(path):
            dfs.append(pd.read_csv(path))
        else:
            print(f"Dataset not found: {path}")
    if not dfs:
        print("No input datasets available.")
        return

    combined = pd.concat(dfs, ignore_index=True)
    augmented = augment(combined, target_rows)
    os.makedirs(os.path.dirname(output), exist_ok=True)
    augmented.to_csv(output, index=False)
    print(f"Saved augmented dataset with {len(augmented)} rows to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine and augment thin-film datasets")
    parser.add_argument("--existing", default="Datasets/thinfilms_data.csv", help="Path to existing dataset")
    parser.add_argument("--scraped", default="Datasets/raw/scraped_data.csv", help="Path to scraped dataset")
    parser.add_argument("--output", default="Datasets/thinfilms_data_augmented.csv", help="Output CSV")
    parser.add_argument("--target_rows", type=int, default=10000, help="Minimum number of rows")
    args = parser.parse_args()
    main(args.existing, args.scraped, args.output, args.target_rows)
