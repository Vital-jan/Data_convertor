import codecs
from collections import defaultdict
from django.apps import apps
import json
import io
import os
import requests
import sys
import time
from xml.etree.ElementTree import iterparse, XMLParser, tostring
import xmltodict
import zipfile

class Converter:
    
    UPDATE_FILE_NAME = 'update.cfg'
    LOCAL_FILE_NAME = None
    FILE_URL = None # url of remote zipfile without filename, look like as "http://hostname.ccc/lllll/mmmmm/"
    LOCAL_FOLDER = "unzipped_xml/" # local folder for unzipped xml files
    ZIPFILE_NAME = "downloaded_zip.zip" # destination local filename
    
    def __init__(self):
        return 

    def rename_xml_files (self): # abstract method for rename files for each app
        return ""

    def is_update (self, url, current_size, filename):
        # returns true, if file size at the <url> changed compared to current_size 
        
        try:
            with open(filename) as file:
                try:
                    urls_dict = json.load(file)
                except:
                    urls_dict = {}
        except: 
            urls_dict = {}

        if len (urls_dict) > 0:
            if url in urls_dict:
                if int(urls_dict[url]) == current_size:
                    return False

        urls_dict[url] = current_size
        file = open (filename, "w")
        file.write (json.dumps(urls_dict))
        file.close
        return True

    def unzip_file(self):
        # os module required
        # getting zip file from self.file_url & extracting to self.LOCAL_FOLDER
        # must be call before parsing xml
        # returns 0 if operation is succefully or another value if error occured

        # if input('Download and unzip file ' + self.LOCAL_FILE_NAME + ' (y/n) ?').upper() != 'Y': return

        print ("Request to remote url ...")
        response = requests.get(self.FILE_URL, stream=True) 
        print ("Response: " + str(response.status_code))
        if (response.status_code != 200):
            print ("ERROR of requests.get(" + self.file_url + ") in module ratu/main.py")
            return 1
        file_size = int (response.headers['Content-Length'])

        if not ( self.is_update (self.FILE_URL, file_size, self.UPDATE_FILE_NAME) ):
            print ("Source files are not updated. Nothing to download.")
            return 0

        with open(self.ZIPFILE_NAME, 'wb') as fd: # download zipfile
            print ("Download zip file " + fd.name + " (" + str(file_size) + " bytes total) ...")
            done = 0
            buffer_size = 102400
            step = 10

            for chunk in response.iter_content(chunk_size=buffer_size):
                fd.write(chunk)
                done += buffer_size
                percent = round(( done / file_size * 100 ))
                if (percent >= step):
                    if percent > 100: percent = 100
                    print ( str ( percent ) + "%")
                    step += 10

            if (os.stat(self.ZIPFILE_NAME).st_size == file_size):
                print ("File downloaded succefully.")
            else: 
                print ("Download file error")
                return 2

        print("Unzip file ...") # unzip files
        try:
            zip_file = zipfile.ZipFile(self.ZIPFILE_NAME)
            zip_file.extractall(self.LOCAL_FOLDER)
        except:
            print ("ERROR unzip file")
            return 3

        # rename unzipped files to short statical names
        # analyse file list of directory <LOCAL_FOLDER> & rename current unzipped files to uo.xml and fop.xml
        # if filename not contains "uo" or "fop" string - file doesn`t rename.
        files = os.listdir (self.LOCAL_FOLDER)

        for file in files:
            new_filename = self.rename_xml_files(file)
            if (new_filename != ""): os.rename(self.LOCAL_FOLDER + file, self.LOCAL_FOLDER + new_filename)

        # remove zip file
        try:
            os.remove (self.ZIPFILE_NAME) 
        except:
            print()

        print ("Download and unzip succefully.")
        return 0

    # -------------- end of unzip_file()
      
    def parse_file(self):
        # encoding & parsing .xml source file
        with codecs.open(self.LOCAL_FOLDER + self.LOCAL_FILE_NAME, encoding="cp1251") as file:
            return xmltodict.parse(file.read())
    
    def clear_db(self):
        # clearing data base
        for table in self.tables:
            table.objects.all().delete()
            print('Old data have deleted.')

    def process(self):
        # parsing sours file in flow
        # get an iterable

        self.unzip_file()
        
        context = iterparse(self.LOCAL_FOLDER + self.LOCAL_FILE_NAME, events=("start", "end"))
        # turn it into an iterator
        context = iter(context)
        # get the root element
        event, root = context.__next__()

        #clear old DB
        self.clear_db()

        i=0
        record=self.record
        #loop for creating one record
        for event, elem in context:
            if event == "end" and elem.tag == "RECORD":
                for text in elem.iter():
                    print('\t\t', text.tag, '\t\t', text.text)
                    if type(record[text.tag]) == list: 
                        record[text.tag].append(text.text)
                    else:
                        record[text.tag]=text.text

                #writing one record
                self.save_to_db(record)
                
                i=i+1
                print(i, ' records\n\n................................................................................................')
                for key in record:
                    if type(record[key]) == list:
                        record[key].clear()
                    else:
                        record[key]=''
                root.clear()
        self.bulk_manager.done()
        print('All the records have been rewritten.')

    print('Converter has imported.')

class BulkCreateManager(object):    # https://www.caktusgroup.com/blog/2019/01/09/django-bulk-inserts/
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=200):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))