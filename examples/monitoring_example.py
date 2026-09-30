
import pandas as pd

from etl_utils.logger import setup_logger
from etl_utils.pipeline_monitor import PipelineMonitor
from etl_utils.transformations import DataTransformer


def main():
    logger = setup_logger(
        name="customer_etl",
        log_dir="logs"
    )

    with PipelineMonitor(
            pipeline_name="customer_etl",
            audit_file="logs/customer_etl_audit.jsonl",
            logger=logger
    ) as monitor:

        logger.info("Reading customer data")

        df = pd.read_csv("data/raw/customers.csv")
        monitor.record_read(len(df))

        logger.info("Transforming customer data")

        result = (
            DataTransformer(df)
            .standardize_column_names()
            .trim_strings()
            .standardize_strings(
                ["status"],
                case="upper"
            )
            .filter_rows(
                lambda data: data["status"].eq("ACTIVE")
            )
            .result()
        )

        monitor.record_processed(len(result))
        monitor.record_rejected(len(df) - len(result))

        logger.info("Writing processed customer data")

        output = "data/processed/customers_monitored.csv"
        result.to_csv(output, index=False)

        logger.info(
            "Successfully wrote %d records to %s",
            len(result),
            output
        )


if __name__ == "__main__":
    main()