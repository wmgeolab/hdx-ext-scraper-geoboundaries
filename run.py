#!/usr/bin/python
"""
Top level script. Calls other functions that generate datasets that this script then creates in HDX.

"""
import argparse
import logging
from os import environ
from os.path import join

import sys

from hdx.facades.simple import facade
from hdx.hdx_configuration import Configuration
from hdx.utilities.downloader import Download
from hdx.utilities.path import progress_storing_tempdir

from geoboundaries import generate_dataset, get_data

print("Running")
sys.exit()

logger = logging.getLogger(__name__)

lookup = "hdx-ext-scraper-geoboundaries"


def main():
    """Generate dataset and create it in HDX"""

    configuration = Configuration.read()
    with Download() as downloader:
        admin_boundaries = get_data(downloader, configuration["url"])
        countries = [{"iso3": x} for x in sorted(admin_boundaries)]
        logger.info(f"Number of countries to upload: {len(countries)}")
        for info, country in progress_storing_tempdir(lookup, countries, "iso3"):
            countryiso3 = country["iso3"]
            country_admin_boundaries = admin_boundaries[countryiso3]
            boundarytypes, dataset, resource_names = generate_dataset(
                countryiso3, country_admin_boundaries
            )
            if dataset:
                dataset.update_from_yaml()
                dataset["notes"] = f"This dataset contains the following administrative boundaries: {', '.join(boundarytypes)}.  \n  \n{dataset['notes']}"
                dataset.create_in_hdx(
                    remove_additional_resources=True,
                    hxl_update=False,
                    updated_by_script="GeoBoundaries",
                    batch=info["batch"],
                )
                existing_order = [x["name"] for x in dataset.get_resources()]
                if existing_order != resource_names:
                    sorted_resources = sorted(
                        dataset.get_resources(),
                        key=lambda x: resource_names.index(x["name"]),
                    )
                    dataset.reorder_resources(
                        [x["id"] for x in sorted_resources], hxl_update=False
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=lookup)
    parser.add_argument("-hk", "--hdx_key", default=None, help="HDX api key")
    parser.add_argument("-hs", "--hdx_site", default=None, help="HDX site to use")
    parser.add_argument(
        "-s",
        "--start",
        default="RESET",
        help="ISO3 to start. Defaults to starting from beginning.",
    )
    args = parser.parse_args()
    hdx_site = args.hdx_site
    if hdx_site is None:
        hdx_site = "stage"
    start = args.start
    if start != "RESET":
        start = f"iso3={start}"
    environ["WHERETOSTART"] = start
    facade(
        main,
        hdx_key=args.hdx_key,
        hdx_site=hdx_site,
        user_agent=lookup,
        project_config_yaml=join("config", "project_configuration.yml"),
    )
