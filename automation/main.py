"""
main.py — RetailPulse Analytics Automation Pipeline
----------------------------------------------------
Single entry point that runs the full pipeline end-to-end:

  1. Generate/load raw data
  2. Clean + validate data
  3. Save cleaned CSV
  4. (Optional) Load into MySQL
  5. Run EDA and save charts
  6. Write a summary report + log file

Usage:
    python main.py --skip-mysql
"""

import argparse
import logging
import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "python"))

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), "..", "logs", "pipeline.log"),
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("retailpulse_pipeline")


def step(name):
    def decorator(fn):
        def wrapper(*args, **kwargs):
            logger.info(f"START: {name}")
            t0 = time.time()
            try:
                result = fn(*args, **kwargs)
                logger.info(f"DONE: {name} ({time.time()-t0:.1f}s)")
                return result
            except Exception as e:
                logger.error(f"FAILED: {name} -> {e}")
                raise
        return wrapper
    return decorator


@step("Generate raw dataset")
def generate_raw():
    import generate_dataset  # noqa: F401 (runs on import)


@step("Clean data")
def clean():
    from clean_data import run_pipeline
    return run_pipeline()


@step("Load to MySQL")
def load_mysql():
    from load_to_mysql import main as load_main
    load_main()


@step("Run EDA")
def run_eda():
    import eda  # noqa: F401 (runs on import)


def main():
    parser = argparse.ArgumentParser(description="RetailPulse Analytics Pipeline")
    parser.add_argument("--skip-mysql", action="store_true", help="Skip MySQL load step")
    parser.add_argument("--skip-generate", action="store_true", help="Skip raw data generation")
    args = parser.parse_args()

    os.chdir(os.path.join(os.path.dirname(__file__), "..", "python"))

    if not args.skip_generate:
        generate_raw()
    clean()
    if not args.skip_mysql:
        try:
            load_mysql()
        except Exception as e:
            logger.warning(f"MySQL step skipped/failed (is MySQL running & configured?): {e}")
    run_eda()

    print("\nPipeline complete. See logs/pipeline.log, data/cleaned/, and reports/ for outputs.")


if __name__ == "__main__":
    main()
