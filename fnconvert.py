#!/usr/bin/python
import os,glob,sys
files = [(f,'{}_{}.jpg'.format(sys.argv[1],i)) for i,f in enumerate(glob.glob('*.jpg'))]
for f in files:
	os.rename(f[0],f[1])

