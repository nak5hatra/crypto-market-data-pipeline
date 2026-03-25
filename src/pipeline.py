from extract import fetch_coin_data, fetch_market_data
from transform import transform_data
from load import load_dim_coin, load_fact_crypto
from utils import get_logger

logger = get_logger(__name__)


def run_pipeline():
    """
    Orchestrates the full ETL pipeline:
    Extract → Transform → Load
    """

    try:
        logger.info("Starting extraction...")

        coin_list_path = fetch_coin_data()
        market_data_path = fetch_market_data()

        logger.info("Extraction completed")

        logger.info("Starting transformation...")

        transformed_paths = transform_data(market_data_path)

        logger.info("Transformation completed")

        logger.info("Starting load process...")

        load_dim_coin(transformed_paths["dim_coin"])
        load_fact_crypto(transformed_paths["fact_crypto"])

        logger.info("Data successfully loaded into database")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    run_pipeline()