#!/usr/bin/python

def runcommand(db,sqlcommand):
	a = db.engine.execute(sqlcommand)
	return a
	
def addrow