#!/usr/bin/python
#-*- encoding: utf-8 -*-

import sys
import mechanize
import cookielib
from bs4 import BeautifulSoup

class ScaffoldDownloader:
    def __init__(self):
        self.browser = self.create_browser()
        self.login()

    def download(self, scaffold_id):
        self.browser.open(self.scaffold_detail_url(scaffold_id))
        
        for link in self.browser.links(url_regex="metaDetail"):
            description = link.text

        for link in self.browser.links(url_regex="MetaScaffoldGraph"):
            sequence_url = "https://img.jgi.doe.gov/cgi-bin/m/" + \
                           link.url.replace("page=metaScaffoldGraph",
                                            "page=metaScaffoldDna")
            dna_page = BeautifulSoup(self.browser.open(sequence_url).read())
            sequence = dna_page.find("textarea", {'name': "fasta"}).text

        filename = self.save_to_file(scaffold_id, description, sequence)
        return filename

    def save_to_file(self, scaffold_id, description, sequence):
        filename = scaffold_id + ".fa"
        with open(filename, "w") as file:
            file.write(">" + scaffold_id + " " + description)
            file.write(sequence)
        return filename

    def login(self):
        self.browser.open("https://img.jgi.doe.gov/m/")
        self.browser.select_form("imghome")
        self.browser["login"] = "jmberros"
        self.browser["password"] = "jmberros"[::-1]
        self.browser.submit()
        return self.browser

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

    def create_browser(self):
        # Browser
        br = mechanize.Browser()

        # Cookie Jar
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)

        # Browser options
        br.set_handle_equiv(True)
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)

        # Follows refresh 0 but not hangs on refresh > 0
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

        # Want debugging messages?
        #br.set_debug_http(True)
        #br.set_debug_redirects(True)
        #br.set_debug_responses(True)

        # User-Agent (this is cheating, ok?)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

        return br


if __name__ == "__main__":
    downloader = ScaffoldDownloader()
    for line in sys.stdin:
        scaffold_id = line.rstrip("\n")
        output_filename = downloader.download(scaffold_id)
        print output_filename

