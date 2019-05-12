import os

offlineWrapper = ["offlineWrapperWOT.py", "offlineWrapperWT.py", "offlineWrapperWT2ndVersion.py"]

for i in offlineWrapper:
	command = 'python '+i
	os.system(command)