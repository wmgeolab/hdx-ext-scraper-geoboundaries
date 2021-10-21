#!/usr/bin/python
"""
Unit tests for cods.

"""
from os.path import join

import pytest
from hdx.data.vocabulary import Vocabulary
from hdx.hdx_configuration import Configuration
from hdx.hdx_locations import Locations
from hdx.location.country import Country
from hdx.utilities.loader import load_json

from geoboundaries import generate_dataset, get_data

alljson = load_json(join("tests", "fixtures", "apiinput.json"))


class TestGeoBoundaries:
    @pytest.fixture(scope="function")
    def configuration(self):
        Configuration._create(
            user_agent="test",
            hdx_key="12345",
            project_config_yaml=join("tests", "config", "project_configuration.yml"),
        )
        Locations.set_validlocations(
            [
                {"name": "afg", "title": "Afghanistan"},
                {"name": "phl", "title": "Philippines"},
            ]
        )
        Country.countriesdata(use_live=False)
        Vocabulary._tags_dict = True
        Vocabulary._approved_vocabulary = {
            "tags": [
                {"name": "administrative divisions"},
                {"name": "geodata"},
                {"name": "gazetteer"},
            ],
            "id": "4e61d464-4943-4e97-973a-84673c1aaa87",
            "name": "approved",
        }
        return Configuration.read()

    @pytest.fixture(scope="class")
    def downloader(self):
        class Download:
            @staticmethod
            def download(url):
                pass

            @staticmethod
            def get_json():
                return alljson

        return Download()

    def test_get_data(self, downloader):
        admin_boundaries = get_data(downloader, "http://lala")
        assert admin_boundaries == {"AFG": alljson}

    def test_generate_dataset(self, configuration):
        boundarytypes, dataset, resource_names = generate_dataset("AFG", alljson)
        assert boundarytypes == ['ADM0', 'ADM1', 'ADM2']
        assert dataset == {
            "name": "geoboundaries-admin-boundaries-for-afghanistan",
            "title": "Afghanistan - Subnational Administrative Boundaries",
            "groups": [{"name": "afg"}],
            "maintainer": "0ec5ff66-dc01-4087-bb82-1d01f3b1c1ce",
            "owner_org": "8be95204-f453-4b66-a4f6-dbe84cb0bdee",
            "data_update_frequency": "0",
            "subnational": "1",
            "tags": [
                {
                    "name": "administrative divisions",
                    "vocabulary_id": "4e61d464-4943-4e97-973a-84673c1aaa87",
                },
                {
                    "name": "geodata",
                    "vocabulary_id": "4e61d464-4943-4e97-973a-84673c1aaa87",
                },
                {
                    "name": "gazetteer",
                    "vocabulary_id": "4e61d464-4943-4e97-973a-84673c1aaa87",
                },
            ],
            "dataset_date": "[2014-01-01T00:00:00 TO 2014-12-31T00:00:00]",
            "dataset_source": "ArcGIS Hub, GeoBoundaries, geoBoundaries, https//esoc.princeton.edu/data/administrative-boundaries-398-districts, https//hub.arcgis.com/datasets/2b63527870ef416bacf83bcaf388685f_0?geometry=53.805%2C30.812%2C81.556%2C37.181",
        }
        assert resource_names == [
            "geoBoundaries-AFG-ADM0_simplified.geojson",
            "geoBoundaries-AFG-ADM0.geojson",
            "geoBoundaries-AFG-ADM0.topojson",
            "geoBoundaries-AFG-ADM0-all.zip",
            "geoBoundaries-AFG-ADM1_simplified.geojson",
            "geoBoundaries-AFG-ADM1.geojson",
            "geoBoundaries-AFG-ADM1.topojson",
            "geoBoundaries-AFG-ADM1-all.zip",
            "geoBoundaries-AFG-ADM2_simplified.geojson",
            "geoBoundaries-AFG-ADM2.geojson",
            "geoBoundaries-AFG-ADM2.topojson",
            "geoBoundaries-AFG-ADM2-all.zip",
        ]
        resources = dataset.get_resources()
        assert resources == [
            {
                "name": "geoBoundaries-AFG-ADM0_simplified.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/01b19c6f8a4f5719bc5acd5c2430eed48b2607ff/releaseData/gbOpen/AFG/ADM0/geoBoundaries-AFG-ADM0_simplified.geojson",
                "description": "Simplified GeoJSON ADM0 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM0.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/01b19c6f8a4f5719bc5acd5c2430eed48b2607ff/releaseData/gbOpen/AFG/ADM0/geoBoundaries-AFG-ADM0.geojson",
                "description": "GeoJSON ADM0 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM0.topojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/01b19c6f8a4f5719bc5acd5c2430eed48b2607ff/releaseData/gbOpen/AFG/ADM0/geoBoundaries-AFG-ADM0.topojson",
                "description": "TopoJSON ADM0 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM0-all.zip",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/01b19c6f8a4f5719bc5acd5c2430eed48b2607ff/releaseData/gbOpen/AFG/ADM0/geoBoundaries-AFG-ADM0-all.zip",
                "description": "Other formats including shape file ADM0 boundaries for Afghanistan",
                "format": "shp",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM1_simplified.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/27d41c455c67255802b518810760c09cb9860459/releaseData/gbOpen/AFG/ADM1/geoBoundaries-AFG-ADM1_simplified.geojson",
                "description": "Simplified GeoJSON ADM1 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM1.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/27d41c455c67255802b518810760c09cb9860459/releaseData/gbOpen/AFG/ADM1/geoBoundaries-AFG-ADM1.geojson",
                "description": "GeoJSON ADM1 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM1.topojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/27d41c455c67255802b518810760c09cb9860459/releaseData/gbOpen/AFG/ADM1/geoBoundaries-AFG-ADM1.topojson",
                "description": "TopoJSON ADM1 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM1-all.zip",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/27d41c455c67255802b518810760c09cb9860459/releaseData/gbOpen/AFG/ADM1/geoBoundaries-AFG-ADM1-all.zip",
                "description": "Other formats including shape file ADM1 boundaries for Afghanistan",
                "format": "shp",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM2_simplified.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/edcdbe557b1b86cea3767bdb3b7f15e517585a34/releaseData/gbOpen/AFG/ADM2/geoBoundaries-AFG-ADM2_simplified.geojson",
                "description": "Simplified GeoJSON ADM2 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM2.geojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/edcdbe557b1b86cea3767bdb3b7f15e517585a34/releaseData/gbOpen/AFG/ADM2/geoBoundaries-AFG-ADM2.geojson",
                "description": "GeoJSON ADM2 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM2.topojson",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/edcdbe557b1b86cea3767bdb3b7f15e517585a34/releaseData/gbOpen/AFG/ADM2/geoBoundaries-AFG-ADM2.topojson",
                "description": "TopoJSON ADM2 boundaries for Afghanistan",
                "format": "geojson",
                "resource_type": "api",
                "url_type": "api",
            },
            {
                "name": "geoBoundaries-AFG-ADM2-all.zip",
                "url": "https://github.com/wmgeolab/geoBoundaries/raw/edcdbe557b1b86cea3767bdb3b7f15e517585a34/releaseData/gbOpen/AFG/ADM2/geoBoundaries-AFG-ADM2-all.zip",
                "description": "Other formats including shape file ADM2 boundaries for Afghanistan",
                "format": "shp",
                "resource_type": "api",
                "url_type": "api",
            },
        ]
