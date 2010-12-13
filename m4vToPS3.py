#!/usr/bin/python
import os, re, subprocess, shlex, MySQLdb
from datetime import datetime
db = MySQLdb.connect(host="localhost", user="root", passwd="hatter",db="m4vToPS3")
#cursor = db.cursor()
#cursor.execute('SELECT * FROM users')
#result = cursor.fetchall()
#print result;

t = datetime.now()
now =  t.strftime("%Y-%m-%d")

fileLocation = '/usr/local/zend/apache2/htdocs/m4vToPS3/'
m4vReg = re.compile("m4v")
outputStr = []
inputStr = []
if os.path.isdir(fileLocation):
    dirContents = os.listdir(fileLocation)
    if ".DS_Store" in dirContents:
       dirContents.remove(".DS_Store")

    mp4Convert = []
    for film in dirContents:
        if re.search(m4vReg, film):
            if film.replace('m4v','mp4') not in dirContents: 
                mp4Convert.append(film)

    if len(mp4Convert) > 0:
        for title in mp4Convert:
            origTitle = title
            title = title.replace('.m4v','')
            title = title.replace(' ', '\ ')
            title = fileLocation+title      
            convertCli = 'ffmpeg -i '+title+'.m4v -acodec copy  -vcodec copy '+title+'.mp4'
            comandArgs = shlex.split(convertCli)
            print 'Converting ' + origTitle + ' to .mp4'
            output = subprocess.call(comandArgs)
            #output,error = subprocess.Popen(comandArgs,stdout = subprocess.PIPE).communicate()
            if output == 0:
                print origTitle + ' has been converted.'
                sql = 'INSERT INTO tbl_converted (titleName, dateConverted) VALUES ("'+origTitle+'","'+now+'")'
                print sql
                cursor = db.cursor()
                cursor.execute(sql)
            else:
                print origTitle + ' FAILED to convert !'
    else:
        print "There are no films that need converting."
else:
    print "There is a problem the the specified source directory !"
