#!/usr/bin/env python3
import yaml
import sys
import os
from re import match, sub

def gen_character_names(settings):
	text = ""
	if "characters" in settings:
		for name in settings["characters"]:
			text += name + " as " + settings["characters"][name] + r'\\'
	return text
	
def get_issue(settings):
	if "issue" in settings:
		return settings["issue"]

def convert_lines(filename, out_filename, settings):
	with open(filename) as fh, open(out_filename, 'w') as out_fh:
		last = ""

		begin = ""
		with open("static/begin.tex") as begin_fh:
			begin = begin_fh.read
		begin = sub(r'@@characters@@', gen_character_names(settings), begin)

		if "issue" in settings:
			begin = sub(r'@@issue@@', settings["issue"], begin)

		out_fh.write(begin)

		for line in fh:
			line_match = match(r'\[.+?] (.+?): (.+)', line)
			new_line = line.strip()
			if line_match is not None:
				name = line_match.group(1)
				msg = line_match.group(2)
				if "characters" in settings and name in settings["characters"]:
					name = settings["characters"][name]
		
				new_line = "\\item["
				if name == last:
					new_line += "..."
				else:
					new_line += name
				new_line += msg			
			
			out_fh.write(new_line)
			last = name	

		with open("static/end.tex") as begin_fh:
			begin = begin_fh.read
	
def load_settings(filename):
	with open(filename) as fh:
		return yaml.load(fh.read())

def run(argv):
	if len(argv) != 4:
		print("usage: " + argv[0] + " <settings file> <skype log file> <output file (no extension)>")
		sys.exit(1)	
	
	convert_lines(argv[2], argv[3] + ".tex", load_settings(argv[1]))
	os.system("./static/prepare.sh " + argv[3] + ".tex")

run(sys.argv)
