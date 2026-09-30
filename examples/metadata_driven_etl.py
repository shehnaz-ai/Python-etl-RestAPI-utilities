from etl_utils.etl_runner import ETLRunner


def main():
    runner = ETLRunner(
        config_path="config/config.yaml"
    )

    results = runner.run()

    for result in results:
        print(
            f"Pipeline: {result['pipeline_name']}, "
            f"Status: {result['status']}, "
            f"Records: {result['records_processed']}"
        )


if __name__ == "__main__":
    main()