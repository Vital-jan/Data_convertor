import codecs
import io
import requests
import sys
from xml.etree.ElementTree import iterparse, XMLParser, tostring
import xmltodict
import zipfile

class Converter:

    FILE_URL = None # url of remote zipfile without filename, look like as "http://hostname.ccc/lllll/mmmmm/"

    LOCAL_FOLDER = "unzipped_xml/" # local folder for unzipped xml files

    ZIPFILE_NAME = "downloaded_zip.zip" # destination local filename
    
    def __init__(self):
        return 

    def rename_xml_files (): # abstract method for rename files for each app
        return ""

    def unzip_file():
        # os module required
        # getting zip file from self.file_url & extracting to self.local_folder
        # must be call before parsing xml
        # returns 0 if operation is succefully or another value if error occured

        print ("Request to remote url ...")
        response = requests.get(self.file_url, stream=True)
        print ("Response: " + str(response.status_code))
        if (response.status_code != 200):
            print ("ERROR of requests.get(" + self.file_url + ") in module ratu/service.py")
            return 1
        file_size = int (response.headers['Content-Length'])

        with open(self.zipfile_name, 'wb') as fd: # download zipfile
            print ("Download zip file " + fd.name + " (" + str(file_size) + " bytes total) ...")
            done = 0
            buffer_size = 102400
            step = 10

            for chunk in response.iter_content(chunk_size=buffer_size):
                fd.write(chunk)
                done += buffer_size
                percent = round(( done / file_size * 100 ))
                if (percent >= step):
                    print ( str ( percent ) + "%")
                    step += 10

            if (os.stat(self.zipfile_name).st_size == file_size):
                print ("File downloaded succefully.")
            else: 
                print ("Download file error")
                return 2

        print("Unzip file ...") # unzip files
        try:
            zip_file = zipfile.ZipFile(self.zipfile_name)
            zip_file.extractall(self.local_folder)
        except:
            print ("ERROR unzip file")
            return 3

        # rename unzipped files to short statical names
        # analyse file list of directory <folder> & rename current unzipped files to uo.xml and fop.xml
        # if filename not contains "uo" or "fop" string - file doesn`t rename.
        files = os.listdir (folder)

        for file in files:
            new_filename = self.rename_xml_files ()
            if (new_filename != ""): os.rename(self.local_folder + file, self.local_folder + new_filename)

        # remove zip file
        os.remove (self.zipfile_name) 
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