#!/usr/bin/python
import os, re, subprocess, shlex, MySQLdb, sys
from datetime import datetime
#from pprint import pprint

class dbConnect:
    def __init__(self):
        self.db = MySQLdb.connect(host="192.168.0.5", user="root", passwd="hatter",db="m4vToPS3")


class m4vToPS3(dbConnect):
    
    def __init__(self):
        t = datetime.now()
        self.now = t.strftime("%Y-%m-%d")
        dbConnect.__init__(self)
        
    mp4Convert = []
    def getFilesToConvert(self):
        self.fileLocation = '/usr/local/zend/apache2/htdocs/m4vToPS3/'
        #self.fileLocation = '/home/steve/Desktop/Share/'
        m4vReg = re.compile("m4v")
        if os.path.isdir(self.fileLocation):
            self.dirContents = os.listdir(self.fileLocation)
            if ".DS_Store" in self.dirContents:
                self.dirContents.remove(".DS_Store")
            for self.film in self.dirContents:
                if re.search(m4vReg, self.film):
                    if self.film.replace('m4v','mp4') not in self.dirContents:
                        self.addFilm(self.film)

    def addFilm(self, film):
        self.mp4Convert.append(film)

    def doConvert(self):
        if len(self.mp4Convert) > 0:
            for self.title in self.mp4Convert:
                self.origTitle = self.title
                self.title = self.title.replace('.m4v','')
                self.title = self.title.replace(' ', '\ ')
                self.title = self.fileLocation+self.title      
                self.convertCli = 'ffmpeg -i '+self.title+'.m4v -acodec copy  -vcodec copy '+self.title+'.mp4'
                comandArgs = shlex.split(self.convertCli)
                print 'Converting ' + self.origTitle + ' to .mp4'
                output = subprocess.call(comandArgs)
                #output,error = subprocess.Popen(comandArgs,stdout = subprocess.PIPE).communicate()
                if output == 0:
                    print self.origTitle + ' has been converted.'
                    self.sql = 'INSERT INTO tbl_converted (titleName, dateConverted) VALUES ("'+self.origTitle+'","'+self.now+'")'
                    self.cursor = self.db.cursor()
                    self.cursor.execute(self.sql)
                else:
                    print self.origTitle + ' FAILED to convert !'
        else:
            print "There are no films that need converting."

    def getFilms(self):
        print self.mp4Convert

    def listConverted(self):
        sql = "SELECT * FROM tbl_converted"
        self.cursor = self.db.cursor()
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        numrows = int(self.cursor.rowcount)
        if numrows > 0:
            print "*****************************************************"
            print "* Date        *  Film Name                          *"
            print "*****************************************************"  
            for record in result:
               output =  "* " + record[2].strftime("%d/%m/%Y") + "  *  "+ record[1]
               output = output.ljust(52,' ')
               output += "*"
               print output
        
            print "*****************************************************"
        else:
            print "There are no converted films to list."


           
convert = m4vToPS3()
option = raw_input("c) To Convert \nl) To List Converted\n")

if option == 'c':
    convert.getFilesToConvert()
    convert.doConvert()
elif option == 'l':
    convert.listConverted()

