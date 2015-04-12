#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys
sys.path.insert(0, "../lib") # TODO: Do this in a less hacky way
import mechabrowser
from bs4 import BeautifulSoup

class ScaffoldDownloader:
    def download(self, scaffold_id):
        browser = mechabrowser.create_browser()
        self.login(browser)
        browser.open(self.scaffold_detail_url(scaffold_id))
        
        for link in browser.links(url_regex="metaDetail"):
            description = link.text

        for link in browser.links(url_regex="MetaScaffoldGraph"):
            sequence_url = "https://img.jgi.doe.gov/cgi-bin/m/" + \
                           link.url.replace("page=metaScaffoldGraph",
                                            "page=metaScaffoldDna")
            dna_page = BeautifulSoup(browser.open(sequence_url).read())
            sequence = dna_page.find("textarea", {'name': "fasta"}).text

        filename = self.save_to_file(scaffold_id, description, sequence)
        return filename

    def save_to_file(self, scaffold_id, description, sequence):
        filename = scaffold_id + ".fa"
        with open(filename, "w") as file:
            file.write(">" + scaffold_id + " " + description)
            file.write(sequence)
        return filename

    def login(self, browser):
        browser.open("https://img.jgi.doe.gov/m/")
        browser.select_form("imghome")
        browser["login"] = "jmberros"
        browser["password"] = "jmberros"[::-1]
        browser.submit()
        return browser

    def scaffold_detail_url(self, scaffold_id):
        return "https://img.jgi.doe.gov/cgi-bin/m/main.cgi?" + \
            "section=MetaDetail&page=metaScaffoldDetail&" + \
            "taxon_oid={}&".format(self.taxon_oid(self.metagenome_id(scaffold_id))) + \
            "scaffold_oid={}&".format(scaffold_id) + \
            "data_type=assembled"
        
    def taxon_oid(self, metagenome_id):
        return {
            'KGI_S1_ANT01_95mDRAFT': "3300000119",
            'KGI_S1_ANT02_95mDRAFT': "3300000136",
            'KGI_S1_ANT03_95mDRAFT': "3300000135",
            'KGI_S2_ANT04_2345mDRAFT': "3300000129",
            'KGI_S2_ANT05_2345mDRAFT': "3300000132",
            'KGI_S2_ANT06_2345mDRAFT': "3300000123"
        }[metagenome_id]

    def scaffold_sequence_url(self, scaffold_id, start, end):
        return "https://img.jgi.doe.gov/cgi-bin/m/main.cgi?" + \
            "section=MetaScaffoldGraph&page=metaScaffoldDna&" + \
            "scaffold_oid={}&".format(scaffold_id) + \
            "taxon_oid={}&".format(self.taxon_oid(self.metagenome_id(scaffold_id))) + \
            "start_coord={}&end_coord={}".format(start, end)

    def metagenome_id(self, scaffold_id):
        return "_".join(scaffold_id.split("_")[:-1])


if __name__ == "__main__":
    downloader = ScaffoldDownloader()
    for line in sys.stdin:
        scaffold_id = line.rstrip("\n")
        output_filename = downloader.download(scaffold_id)
        print output_filename

