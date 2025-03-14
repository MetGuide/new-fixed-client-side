
# by dracaryS
# 5.2.2020
# Website: <dracarys.work>
# Discord: dracaryS#9089
# Skype: kuun_12

import os
import glob
__file__ = __file__.split('\\')
__file__ = str(__file__[len(__file__)-1])
out = open("check_bad_files_output.txt", "w+")

fileCount = 0
readCount = 0
for fileName in glob.glob('*.py'):
	fileCount+=1

# first check all don't using python files....
out.write("****************************************************\n")
out.write("************* PY FILES *****************************\n")
out.write("****************************************************\n")
print "Py Files Check is start... "
for fileName in glob.glob('*.py'):
	if fileName == "system.py"\
	or fileName == "prototype.py"\
	or fileName == __file__:
		continue
	status = True
	fileName = fileName[:-3].lower()
	for fileNameNext in glob.glob('*.py'):
		lines = open(fileNameNext).readlines()
		for line in lines:
			if line.lower().find("import "+fileName+"\n") != -1:
				status = False
				break
		if not status:
			break
	if status:
		out.write(fileName+"\n")
	readCount+=1
	print "Py Files Check is status %d\n"% (readCount*float(float(100)/float(fileCount)))

fileCount = 0
readCount = 0
for fileName in glob.glob('uiscript/*.py'):
	fileCount+=1
	
# second check all don't usign script files....
out.write("****************************************************\n")
out.write("************* SCRIPT FILES *************************\n")
out.write("****************************************************\n")
print "Script Files Check is start... "
for fileName in glob.glob('uiscript/*.py'):
	fileName = fileName.split("\\")[1].lower()
	status = True
	for fileNameNext in glob.glob('*.py'):
		lines = open(fileNameNext).readlines()
		for line in lines:
			if line.lower().find(fileName+'"') != -1:
				status = False
				break
		if not status:
			break
	if status:
		out.write("uiscript/"+fileName+"\n")
	readCount+=1
	print "Script Files Check is status %d\n"% (readCount*float(float(100)/float(fileCount)))
out.close()
print "by dracaryS <dracarys.work>"
print "Working done... Check the check_bad_files_output.txt file..."
os.system("PAUSE")
