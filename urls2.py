# Import necessary libraries
import os
import re
from urllib import response
import requests
import urllib.request
from datetime import datetime
from sys import stdout
from urllib.request import urlopen
import pikepdf
import sys
 
# Creates a variable called urlFile that will hold the list of URLs to be read from the file "urls.txt".
urlFile = open('urls.txt', 'r')

# Creates a variable that holds all of the URLs found in the text file
urlRead = urlFile.readlines()

# Creates an integer variable called count to keep track of how many lines have been printed on screen so far
count = 1

# Iterates through each line in the file, printing out the number of lines printed, before moving onto the next line.

for line in urlRead:

    print(count)

    # Prints out each URL on a seperate line
    url = str(line.strip())
    print(url)

    # Increase the count by 1
    count += 1

    try:

        # Identifies the name of the PDF from the URL, stores it in variable 'filename'
        filename = url.split('/')[-1]

        # Identifies the name of the publisher from the URL, stores it in variable 'publisher'
        publisher = url.split('.')[1] #Publisher is whatever comes after .com or .org in the URL

        # Create the variable destFolder to hold the downloaded PDF documents 
        destFolder = 'tempFolder'

        if not os.path.exists(destFolder): # If a folder called tempFolder does not already exist, os.makedirs() creates one

            os.makedirs(destFolder) 

        filePath = os.path.join(destFolder, filename)

        print(filename)

        print(publisher)

        r = requests.get(url, stream=True)

        print('get url')

        if r.ok:

            with open(filePath, 'wb') as f:

                f.write(r.content)

        #Creates a pdf object and saves it in tempFolder
        pdf = pikepdf.Pdf.open(filePath)

        #Using docinfo, all keys and values are printed
        docinfo = pdf.docinfo
        for key, value in docinfo.items():

            print(key, ":", value)

        print('***********************************************************')

        # Attempts to find creation date of the document, 
        try:

            tempDate = str(docinfo.CreationDate)

            tempDate = tempDate.split(':')[-1]

            tempDate = tempDate.split('+')[0]

            tempDate = tempDate.split('-')[0]

            #Prints date in a string format
            print(tempDate)

            # Converts date from string format to time format
            tempcreationDate = datetime.strptime(tempDate, "%Y%m%d%H%M%S")

            #Prints date in year month date and HH:MM:SS format
            print(tempcreationDate)

            #Removes HH:MM:SS 
            creationDate = tempcreationDate.strftime("%Y-%m-%d")


        #If creation date can not be identified then the following statement is printed
        except Exception:

            print('Creation Date is EMPTY')

        #Creation date printed as identified
        else:

            print('Creation Date is', creationDate)

        try:

            domain = docinfo.CrossMarkDomains

        except Exception:

            print('Domain/Publisher is EMPTY')

        else:

            print('Domain/Publisher is', domain)

            publisher = domain

        try:
            
            #Identifies the document title from docinfo
            title = str(docinfo.Title)

            #Titles the document correctly, removing spaces and appending with .pdf
            title = re.sub('\W+',' ', title)+".pdf"

        #If there is no title in docinfo then the filename is assigned as title
        except Exception:

            print('Title is EMPTY')

            title = filename

        else:

            print('Title is', title)


        print('---***********************************************************')

        # Assigns a destination folder titled after publisher and doc creation date
        destFolder = str(publisher) + "/" + str(creationDate)

        print(destFolder)

        if not os.path.exists(destFolder):

            os.makedirs(destFolder)  # create folder if it does not exist

        filePath = os.path.join(destFolder, str(title))

        print(title)

        print(publisher)

        # Downloads file again to save in specific folder
        r = requests.get(url, stream=True)

        if r.ok:

            with open(filePath, 'wb') as f:

                f.write(r.content)  

    except Exception:

        print('Unable to download file from: ', url)