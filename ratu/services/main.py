import codecs
import io
import requests
import sys
from xml.etree.ElementTree import iterparse, XMLParser, tostring
import xmltodict
import zipfile

class Converter:

    FILE_URL=None
    LOCAL_FOLDER=None
    LOCAL_FILE_NAME=None
    
    def __init__(self):
        return 

def unzip_file(file_url, local_folder):
        # getting zip file from file_url & extracting to local_folder
        # must be call before parsing xml: Converter.unzip_file(FILE_URL, LOCAL_FOLDER)

        def rename_xml_files (folder):
            # analyse file list of directory <folder> & rename current unzipped files to uo.xml and fop.xml
            # if filename not contains "uo" or "fop" string - file doesn`t rename.
            # os module required
            files = os.listdir (folder)
            for el in files:
                #rename files
                print (el)
                new_filename = ""
                if (el.upper().find('UO') >= 0): new_filename = 'uo.xml'
                if (el.upper().find('FOP') >= 0): new_filename = 'fop.xml'
                if (new_filename != ""): os.rename(folder + el, folder + new_filename)
        # -------------- end of rename_xml_files()

        print ("Download zip file ...")
        try:
            r = requests.get(file_url)
        except:
            print ("ERROR of requests.get(" + file_url + ") in module ratu/service.py")
            return

        print("Unzipping file ...")
        try:
            zip_file = zipfile.ZipFile(io.BytesIO(r.content))
            zip_file.extractall(local_folder)
        except:
            print ("ERROR of zipfile.ZipFile()")
            return
            
        rename_xml_files (local_folder)
    # -------------- end of unzip_file()
    
    def unzip_file(self):
        # getting zip file  from FILE_URL & extracting to LOCAL_FOLDER
        try:
            r = requests.get(self.FILE_URL)
        except TimeoutError as err:   
            print ("Error open zip file " + self.FILE_URL)
            return 
        zip_file = zipfile.ZipFile(io.BytesIO(r.content))
        zip_file.extractall(self.LOCAL_FOLDER)
            
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
        print('All the records have been rewritten.')

    print('Converter has imported.')