from django.test import TestCase
import requests, os, zipfile, io
import config

# Create your tests here.

def unzip_file(file_url, local_folder):
        # getting zip file from file_url & extracting to local_folder
        # must be call before parsing xml: Converter.unzip_file(FILE_URL, LOCAL_FOLDER)
        # returns 0 if operation is succefully or another value if error occured
        zipfile_name = "zipfile.zip" # destination local filename

        def rename_xml_files (folder):
            # analyse file list of directory <folder> & rename current unzipped files to uo.xml and fop.xml
            # if filename not contains "uo" or "fop" string - file doesn`t rename.
            # os module required
            files = os.listdir (folder)
            for file in files:
                #rename files
                new_filename = ""
                if (file.upper().find('UO') >= 0): new_filename = 'uo.xml'
                if (file.upper().find('FOP') >= 0): new_filename = 'fop.xml'
                if (new_filename != ""): os.rename(folder + file, folder + new_filename)
        # -------------- end of rename_xml_files()

        print ("Request to remote url ...")
        response = requests.get(file_url, stream=True)
        print ("Response: " + str(response.status_code))
        if (response.status_code != 200):
            print ("ERROR of requests.get(" + file_url + ") in module ratu/service.py")
            return 1
        file_size = int (response.headers['Content-Length'])

        with open(zipfile_name, 'wb') as fd: # download zipfile
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

            if (os.stat(zipfile_name).st_size == file_size):
                print ("File downloaded succefully.")
            else: 
                print ("Download file error")
                return 2

        print("Unzip file ...") # unzip files
        # try:
        zip_file = zipfile.ZipFile(zipfile_name)
        zip_file.extractall(local_folder)
        # except:
        #     print ("ERROR unzip file")
        #     return 3
            
        rename_xml_files (local_folder) # rename unzipped files to short statical names
        os.remove (zipfile_name) # remove zip file
        print ("Download and unzip succefully.")
        return 0

    # -------------- end of unzip_file()

unzip_file("https://data.gov.ua/dataset/b244f35a-e50a-4a80-b704-032c42ba8142/resource/06bbccbd-e19c-40d5-9e18-447b110c0b4c/download/", "unzipped_xml/")