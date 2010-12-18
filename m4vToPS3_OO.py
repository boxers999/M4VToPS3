#!/usr/bin/python
import os, re, subprocess, shlex, MySQLdb
from datetime import datetime

class m4vToPS3:
    mp4Convert = []
    def getFilesToConvert(self):
        fileLocation = '/usr/local/zend/apache2/htdocs/m4vToPS3/'
        m4vReg = re.compile("m4v")
        if os.path.isdir(fileLocation):
            self.dirContents = os.listdir(fileLocation)
            if ".DS_Store" in self.dirContents:
                self.dirContents.remove(".DS_Store")
                for self.film in self.dirContents:
                    if re.search(m4vReg, self.film):
                        if self.film.replace('m4v','mp4') not in self.dirContents:
                            self.addFilm(self.film)

    def addFilm(self, film):
        self.mp4Convert.append(film)

    def getFilms(self):
        print self.mp4Convert

convert = m4vToPS3()
convert.getFilesToConvert()
convert.getFilms()
