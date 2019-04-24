import os

fileName = 'NewNames.txt'

os.system('p4 set P4USER=administrator')

os.system('p4 set P4')

os.system('p4 set P4PASSWD=versionControladm1n!')

os.system('p4 login')

os.system('p4 set P4CLIENT=usc.edu')

try:                             # Catch exceptions with try/except
    listOfNames = open(fileName)
    try:                             # Catch exceptions with try/except
	    names = listOfNames.read().splitlines()
    except IOError:
	    print('An error occured trying to read the file.')                             
    for name in names:
	    try:           #Catch exceptions with try/except
		    os.system('p4 user -f ' + name)
	    except:
		    print(name + " was not deleted")
except IOError:
	print('An error occured trying to open the file.')