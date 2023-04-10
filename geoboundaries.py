#!/usr/bin/python
"""
CODS:
-----

Generates urls from the geoBoundaries website.

"""
import logging

from hdx.data.dataset import Dataset
from hdx.data.hdxobject import HDXError
from hdx.data.resource import Resource
from hdx.location.country import Country
from hdx.utilities.dictandlist import dict_of_lists_add
from hdx.utilities.path import get_filename_from_url
from slugify import slugify

logger = logging.getLogger(__name__)


def get_data(downloader, url):
    downloader.download(url)
    admin_boundaries = dict()
    ignored_countries = set()
    for boundaryinfo in downloader.get_json():
        if boundaryinfo["worldBankIncomeGroup"] in (
            "High-income Countries",
            "No income group available",
        ):
            ignored_countries.add(boundaryinfo["boundaryName"])
            continue
        countryiso3 = boundaryinfo["boundaryISO"]
        dict_of_lists_add(admin_boundaries, countryiso3, boundaryinfo)
    logger.info(
        f'Ignoring high income/no income available countries: {", ".join(sorted(ignored_countries))}'
    )
    return admin_boundaries


def get_name_url(url):
    return get_filename_from_url(url), url


def generate_dataset(countryiso3, admin_boundaries):
    countryname = Country.get_country_name_from_iso3(countryiso3)
    title = f"{countryname} - Subnational Administrative Boundaries"
    logger.info(f"Creating dataset: {title}")
    name = f"geoBoundaries admin boundaries for {countryname}"
    slugified_name = slugify(name).lower()
    dataset = Dataset({"name": slugified_name, "title": title})
    try:
        dataset.add_country_location(countryiso3)
    except HDXError as e:
        logger.error(f"{title} has a problem! {e}")
        return None, None, None
    dataset.set_maintainer("0ec5ff66-dc01-4087-bb82-1d01f3b1c1ce")
    dataset.set_organization("8be95204-f453-4b66-a4f6-dbe84cb0bdee")
    dataset.set_expected_update_frequency("Live")
    dataset.set_subnational(True)
    dataset.add_tags(["administrative boundaries-divisions", "geodata", "gazetteer"])
    logger.info(f"Dataset added: {dataset}")
    
    sources = set()
    dataset_years = set()
    resource_names = list()

    def add_resource(key, description, filetype="geojson"):
        name, url = get_name_url(admin_boundary[key])
        resource = Resource({"name": name, "url": url, "description": description})
        resource.set_file_type(filetype)
        resource_names.append(name)
        dataset.add_update_resource(resource)

    all_hdx = True
    boundarytypes = list()
    for admin_boundary in sorted(admin_boundaries, key=lambda x: x["boundaryType"]):
        if "data.humdata.org" not in admin_boundary["boundarySourceURL"]:
            all_hdx = False
        dataset_years.add(admin_boundary["boundaryYearRepresented"].replace(".0", ""))
        i = 1
        while True:
            source = admin_boundary.get(f"boundarySource")
            if source is None:
                break
            sources.add(source)
            i += 1
        logger.info(f"printing dataset sources: {sources}")
        boundarytype = admin_boundary["boundaryType"]
        boundarytypes.append(boundarytype)
        add_resource(
            "simplifiedGeometryGeoJSON",
            f"Simplified GeoJSON {boundarytype} boundaries for {countryname}",
        )
        add_resource(
            "gjDownloadURL", f"GeoJSON {boundarytype} boundaries for {countryname}"
        )
        add_resource(
            "tjDownloadURL", f"TopoJSON {boundarytype} boundaries for {countryname}"
        )
        add_resource(
            "staticDownloadLink",
            f"Other formats including shape file {boundarytype} boundaries for {countryname}",
            "shp",
        )
    if all_hdx:
        logger.info(
            f"Ignoring {countryname} as data for all admin levels comes from HDX!"
        )
        return None, None, None
    dataset_years = sorted(dataset_years)
    dataset.set_reference_period_year_range(dataset_years[0], dataset_years[-1])
    dataset["dataset_source"] = "".join(sorted(sources))
    logger.info(
        f'checking sources: {"".join(sorted(sources))}'
    )
    return boundarytypes, dataset, resource_names
