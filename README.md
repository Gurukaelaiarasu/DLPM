# DLPM

This repository contains datasets and utilities for working with thin-film plasmonic metamaterials.

## Data acquisition

`scripts/data_acquisition/scrape_articles.py` extracts tables from online articles or local PDF files and stores the results in `Datasets/raw/scraped_data.csv`.

Example:

```bash
python scripts/data_acquisition/scrape_articles.py \
    --urls https://example.com/article \
    --pdfs local_paper.pdf \
    --output Datasets/raw/scraped_data.csv
```

## Dataset augmentation

`scripts/data_acquisition/augment_dataset.py` merges the scraped data with `Datasets/thinfilms_data.csv` and performs simple augmentation until at least 10k rows are produced.

Example:

```bash
python scripts/data_acquisition/augment_dataset.py \
    --existing Datasets/thinfilms_data.csv \
    --scraped Datasets/raw/scraped_data.csv \
    --output Datasets/thinfilms_data_augmented.csv \
    --target_rows 10000
```
