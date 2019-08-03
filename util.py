import importlib
import glob
import re
from subprocess import Popen, PIPE
import sys
from flask import url_for
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter
from flask_socketio import emit, SocketIO
import time
import os
def displayArray(myFile):
    fs=open('temp.py', 'w')

    rawArray=getHtml(myFile)
    plotCount=rawArray.pop()
    strCode=duplicate(rawArray)
    fs.write(strCode)
    process = Popen(['python3','-u', '-c', strCode], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    myDir = os.path.dirname(os.path.abspath(__file__))
    allPlots=glob.glob(myDir+'/static/plot[0-9].png')
    displayText=''
    for x in rawArray:
        displayText=displayText+highlight(''.join(x), PythonLexer(), HtmlFormatter())
        if plotCount>0:
            displayText+='<img src="'+url_for('static', filename=os.path.basename(allPlots.pop()))+'">'
            plotCount-=1
    return url_for('static', filename='main.js'),HtmlFormatter().get_style_defs('.highlight'), displayText+'<pre>'+str(stdout)+'</pre>'+'<br><pre>'+str(stderr)+'</pre>'
def getHtml(fileName):
    fs=open(fileName, 'r')
    myDir = os.path.dirname(os.path.abspath(__file__))
    newFile=[]
    newBlock=[]
    plotCount=0
    for line in fs:
        if 'plt.plot' in line:
            plotCount+=1
            newBlock.append(line)
            newBlock.append("plt.savefig('"+myDir+"/static/plot"+str(len(newFile))+".png')\n")
            newFile.append(newBlock)
            newBlock=[]
        else:
            newBlock.append(line)
    newFile.append(newBlock)
    newFile.append(plotCount)
    return newFile
def  duplicate(structure):
    assembledText=''
    for x in structure:
        assembledText=assembledText+''.join(x)
    return assembledText
