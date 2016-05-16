#!/usr/bin/python

fo = open("gis", "w+")
with open("parsed", "r") as f:
	for line in f:
		line = line.rstrip() 
		tokens = line.split(",")
		tokens.pop(0)
		fo.write(tokens[0] + "," + tokens[1] + "\n")
