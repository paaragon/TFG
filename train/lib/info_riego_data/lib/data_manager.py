# -*- coding: utf-8 -*-

import os
import io
import zipfile
from urllib2 import urlopen, URLError, HTTPError
import argparse
import urlparse
import json
import requests
from bs4 import BeautifulSoup

class DataManager(object):
    """This class download and uncompress all files from InfoRiego than pass the criteria"""

    start_date = None
    end_date = None
    years = None
    csv_destination_folder = None
    config_file = None
    verbose = True

    uri = "http://ftp.itacyl.es/Meteorologia/Datos_observacion_Red_InfoRiego/DatosHorarios/"

    def __init__(self, start_date=None, end_date=None, csv_destination_folder=None, config_file=None, verbose=True):

        self.start_date = start_date
        self.end_date = end_date
        self.csv_destination_folder = csv_destination_folder
        self.config_file = config_file
        self.verbose = verbose

        self._parse_config_file()
        self._check_errors()
        self._create_csv_folder()

    def get_data(self):
        """This function download, uncompress and correct the data"""

        start_year = self.start_date / 10000
        end_year = self.end_date / 10000

        self.years = range(start_year, end_year + 1)

        if self.verbose:
            print "Downloading data from ", start_year, " to ", end_year, "."
            print "Total of ", len(self.years), " year/s."

        # Request to InfoRiego
        req = requests.get(self.uri)
        status_code = req.status_code

        if status_code != 200:
            print "Error on request. Status code: ", status_code
            return False

        if self.verbose:
            print "Succesfully request to InfoRiego"

        year_links = self._get_year_links(req)

        if self.verbose:
            print "Years found: " + str(len(year_links))

        for year in year_links:

            uri2 = self.uri+'/'+year+'/'
            req = requests.get(uri2)

            if req.status_code != 200:
                print "Error on request. Status code: ", status_code
                return False

            zip_links = self._get_zip_links(req)

            i = 1
            for link in zip_links:

                if self.verbose:
                    print 'Downloading ' + link.get_text() + ' (' + str(i) + '/' + str(len(zip_links)) + ')'
                    i += 1

                zip_file = self._download_zip(uri2, link)
                if zip_file:
                    file_name = self._uncompress_and_save_zip(zip_file)
                    self._correct_characters(file_name)

    def _uncompress_and_save_zip(self, zip_file):
        """This function uncompress a zip file and save it in disk"""

        file_like_object = io.BytesIO(zip_file)
        zipfile_ob = zipfile.ZipFile(file_like_object)

        for name in zipfile_ob.namelist():
            zipfile_ob.extract(name, self.csv_destination_folder)

        return name

    def _download_zip(self, uri, link):
        """This function downloads a file with the given link"""

        zip_url = uri + link.get('href')
        path = urlparse.urlparse(zip_url).path.split('/')[-1]
        file_name = os.path.splitext(path)[0]

        aux_path = os.path.join(self.csv_destination_folder, file_name + ".csv")

        if os.path.isfile(aux_path):
            print "File already exists: " + aux_path
            return None

        #downloading zip file
        try:

            # open url
            zip_file = urlopen(zip_url)

            return zip_file.read()

        #handle errors
        except HTTPError, e:

            if self.verbose:
                print 'Failed downloading zip file: ' + link.get('href'), e.code, zip_url
            return None

        except URLError, e:

            if self.verbose:
                print 'Failed downloading zip file: ' + link.get('href'), e.reason, zip_url
            return None



    def _get_zip_links(self, req):
        """This function iterates through all <a> tags of a request and get all zip links"""

        html = BeautifulSoup(req.text, "lxml")
        links = html.find_all('a')

        for link in links:
            if link.get('href').endswith('.zip'):
                # only zip files
                links = [link for link in links \
                        if link.get('href').endswith('.zip') \
                        and int(link.get('href')[0:8]) >= self.start_date \
                        and int(link.get('href')[0:8]) <= self.end_date]

        return links

    def _get_year_links(self, req):
        """This function get all links from <a> tag presents in a response"""

        html = BeautifulSoup(req.text, "lxml")
        links = html.find_all('a')

        # making the list of the years
        year_links = list()
        for link in links:

            if link.get('href')[:-1].isdigit() and \
                int(link.get('href')[:-1]) in self.years:

                year_links.append(link.get('href')[:-1])

        return year_links

    def _create_csv_folder(self):

        if not os.path.exists(self.csv_destination_folder):

            if self.verbose:
                print self.csv_destination_folder + " not found. Creating it.\n"

            os.makedirs(self.csv_destination_folder)

    def _correct_characters(self, file_name):

        if self.verbose:
            print 'Correcting characters in ' + file_name

        with open(os.path.join(self.csv_destination_folder, file_name)) as csv_file:
            file_data = csv_file.read()

        file_data = file_data.decode('unicode_escape')
        file_data = file_data.replace(u'á', 'a')
        file_data = file_data.replace(u'é', 'e')
        file_data = file_data.replace(u'í', 'i')
        file_data = file_data.replace(u'ó', 'o')
        file_data = file_data.replace(u'ú', 'u')
        file_data = file_data.replace(u'º', 'o')
        file_data = file_data.replace(u'ó', 'o')
        file_data = file_data.encode("utf-8")

        # Write the file out again
        with open(os.path.join(self.csv_destination_folder, file_name), 'w') as csv_file:
            csv_file.write(file_data)

    def _parse_config_file(self):
        """this function parse the optional config file"""

        if self.config_file is not None:

            if self.verbose:
                print "Parsing config file"

            with open(self.config_file) as data_file:
                config_data = json.load(data_file)

            if "start_date" in config_data:
                self.start_date = config_data["start_date"]

            if "end_date" in config_data:
                self.end_date = config_data["end_date"]

            if "destination_folder" in config_data:
                self.csv_destination_folder = config_data["destination_folder"]

    def _check_errors(self):
        """This function checks if all attributes have correct values"""

        if self.start_date is None:
            raise Exception(9, "No start date specified")

        if self.end_date is None:
            raise Exception(9, "No end date specified")

        if self.csv_destination_folder is None:
            raise Exception(9, "No destination folder for csv files specified")

        if self.start_date > self.end_date:
            raise Exception(9, "Start date is greater than end date")

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--config-file', nargs='?', action="store", dest="config_file", help="File with the parameters download the data. It can only contain some parameters and specify the others by cli.")
    parser.add_argument('--start-date', dest="start_date", action="store", help="The start date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--end-date', dest="end_date", action="store", help="The end date of the set. (YYYYMMDD).", type=int)
    parser.add_argument('--destination-folder', dest="dest_folder", action="store", help="Folder to save the data.")


    arguments = parser.parse_args()

    config_file = arguments.config_file
    start_date = arguments.start_date
    end_date = arguments.end_date
    dest_folder = arguments.dest_folder
    data_manager = DataManager(start_date, end_date, dest_folder, config_file)
    data_manager.get_data()

if __name__ == "__main__":
    main()
