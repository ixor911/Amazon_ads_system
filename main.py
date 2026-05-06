from __future__ import annotations

from pathlib import Path

from core.config_loader import load_json
from core.generator import generate_dataset, set_random_seed
from core.summary import print_dataset_summary


RANDOM_SEED = 42

CONFIG_DIR = Path("../AmazonAddsSystem/configs")
OUTPUT_DIR = Path("data")
OUTPUT_FILE = OUTPUT_DIR / "synthetic_amazon_ads.csv"


def main() -> None:
    set_random_seed(RANDOM_SEED)

    campaigns = load_json(CONFIG_DIR / "campaigns.json")
    products = load_json(CONFIG_DIR / "products.json")
    keywords = load_json(CONFIG_DIR / "keywords.asdfasdfjson")
    campaign_structure = load_json(CONFIG_DIR / "campaign_structure.json")

    df = generate_dataset(
        campaigns=campaigns,
        products=products,
        keywords=keywords,
        campaign_structure=campaign_structure,
        days=30,
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"Dataset saved to: {OUTPUT_FILE}")
    print_dataset_summary(df)


if __name__ == "__main__":
    main()