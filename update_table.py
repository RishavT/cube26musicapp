#!/usr/bin/python
import os

def runcommand(db,sqlcommand):
	a = db.engine.execute(sqlcommand)
	return a
	
#def addrow
#ALTER TABLE mytable ALTER COLUMN mycolumn TYPE varchar(40);