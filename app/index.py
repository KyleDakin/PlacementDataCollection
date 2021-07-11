import CSV_Reader as cr
import test
import sys
import os
import os.path
import pyautogui

from app import app
from flask import redirect
from flask import render_template
from flask import request
from urllib.request import urlopen
from tkinter import *
from tkinter import filedialog
from os import listdir
from datetime import datetime
import time

import base64

data = None
lineCount = 0 
render = False
source = None
fileList = {}
fileCount = 0
index = 0

if __name__ == '__main__':
    app.debug = True
    app.run()
    
## Sets the global data variable
## Used setter method so it only done here and doesn't have multiple methods
## referencing the global variable
def setData(filePath):
    global data
    data = filePath

def getData():
    return data

## Sets the global lineCount variable
## Used setter method so it only done here and doesn't have multiple methods
## referencing the global variable
def setLineCount():
    global lineCount
    lineCount += 1

def resetLineCount():
    global lineCount
    lineCount = 1

def getLineCount():
    return lineCount

def setFileList():
    global fileList
    global fileCount

    fileList = listdir('CrimeData/')
    fileCount = len(fileList)

def setIndex():
    global index
    index += 1

def getIndex():
    return index

def getFileCount():
    return fileCount

def getFileList(index):
    return fileList[index]

##Defines the default map entry
def defaultMap():
    return render_template('Maps.html', latitude=53.4569491, longitude=-2.2514661, rotation=0)
   
@app.route('/')
@app.route('/process', methods=['GET','POST'])
def processData():
    if request.method == 'POST' and '.csv' in request.form['dataProcess']:
        cr.processData(request.form['dataProcess'])
        setFileList()
        cr.count_lines('CrimeData/' +  getFileList(0))
        setData('CrimeData/' +  getFileList(0))
        setLineCount()
        address = cr.load_data(getData(), getLineCount())
        
        return render_template('Maps.html',  latitude=address[2], longitude=address[3], rotation=address[7])

    elif getData() is not None:
        address = cr.load_data(getData(), getLineCount()) 
        return render_template('Maps.html',  latitude=address[2], longitude=address[3], rotation=address[7])

    else:
        return defaultMap()


##Submits the selected data file to CSV_Reader to process data
##Sets first file from processed data to the global variable, 
##Reads the first entry and returns it to the map to be displayed
@app.route('/')
@app.route('/index', methods=['GET','POST'])
def submitData():
    if request.method == 'POST' and '.csv' in request.form['dataFile']:
        cr.count_lines('CrimeData/' + request.form['dataFile'])
        setData('CrimeData/' + request.form['dataFile'])
        setLineCount()
        address = cr.load_data(getData(), getLineCount())
        
        return render_template('Maps.html',  latitude=address[2], longitude=address[3], rotation=address[7])

    elif getData() is not None:
        address = cr.load_data(getData(), getLineCount()) 
        return render_template('Maps.html',  latitude=address[2], longitude=address[3], rotation=address[7])

    else:
        return defaultMap()
 

##Changes the map to display the next address in the .csv list
##Also changes which CSV is being read once one has finished
##If data is blank, just returns the default entry
@app.route('/')
@app.route('/changeAddress', methods=['GET','POST'])
def nextAddress():
    if getData() is not None:
        if(getLineCount() != cr.getLineCount()):
            newLocation = cr.load_data(getData(), getLineCount())
            cr.save_data(getData(), getLineCount(), check_and_cap(newLocation))
            setLineCount()
            newLocation = cr.load_data(getData(), getLineCount())
            if(newLocation is not None):
                return render_template('Maps.html', latitude=newLocation[2], longitude=newLocation[3], rotation=newLocation[7])
        else:
            setIndex()
            if(getIndex() < getFileCount()):
                setData('CrimeData/' +  getFileList(getIndex()))
                cr.count_lines('CrimeData/' +  getFileList(getIndex()))
                resetLineCount()
                newLocation = cr.load_data(getData(), getLineCount())
                return render_template('Maps.html', latitude=newLocation[2], longitude=newLocation[3], rotation=newLocation[7])
            else:
                shutdown_server()
                return 'Server shutting down...'        

    else:  
        return defaultMap()

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@property
def folder_name():
    return _folder_name

@folder_name.setter
def folder_name(name):
    _folder_name = name

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_name = folder_selected

def check_and_cap(address):
    i = 1
    dir_name = "Screenshots\\"   
    time.sleep(1)
    date = str(datetime.now())
    formatted = date.replace(':','')
    fileName = address[2] + '_'+ address[3] + '_' + address[7] + formatted + '.jpg'
    pyautogui.screenshot(os.path.join(dir_name, fileName))

    return(fileName)



