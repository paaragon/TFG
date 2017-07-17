import os
import io
import zipfile
from urllib2 import urlopen, URLError, HTTPError
import requests
from bs4 import BeautifulSoup

class DataManager(object):
    """This class download and uncompress all files from InfoRiego than pass the criteria"""

    start_date = None
    end_date = None
    years = None
    config_file = None

    csv_destionation_folder = None

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

            i = 0
            for link in zip_links:

                zip_file = self._download_zip(uri2, link)


                self._uncompress_and_save_zip(zip_file)

                if zip_file != None and self.verbose:

                    i += 1
                    print "Successfuly download and uncompress" + str(i) + "/" + str(len(zip_links)) + " in year " + year

    def _uncompress_and_save_zip(self, zip_file):
        """This function uncompress a zip file and returns it as a file in memory"""

        file_like_object = io.BytesIO(zip_file)
        zipfile_ob = zipfile.ZipFile(file_like_object)

        zipfile_ob.extract(self.csv_destionation_folder)

        return zipfile_ob

    def _download_zip(self, uri, link):
        """This function downloads a file with the given link"""

        zip_url = uri + link.get('href')
        aux_path = os.path.join(self.csv_destination_folder, link.get_text()) # TODO check if CSV exist not ZIP

        if os.path.isfile(aux_path):
            print "File already downloaded: " + aux_path
            return None

        #downloading zip file
        try:

            # open url
            zip_file = urlopen(zip_url)

            if self.verbose:
                print 'Downloading ' + link.get_text()

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

    def _parse_config_file(self):
        """this function parse the optional config file"""
        pass

    def _check_errors(self):
        """This function checks if all attributes have correct values"""

        if self.start_date is None:
            raise Exception(9, "No start date specified")

        if self.end_date is None:
            raise Exception(9, "No end date specified")

        if self.csv_destionation_folder is None:
            raise Exception(9, "No destination folder for csv files date specified")

        if self.start_date > self.end_date:
            raise Exception(9, "Start date is greater than end date")

def main():
    pass

if __name__ == '__main__':
    main()
