#!/usr/bin/env python3
import yaml
import sys
import os
from re import match, sub

def gen_character_names(settings):
	text = ""
	if "characters" in settings:
		for name in settings["characters"]:
			# eight backslashes becomes 2 in final version
			text += name + " as " + settings["characters"][name] + '\\\\\\\\\n' 
	return text

def sub_names(string, settings):
	if "characters" in settings:
		for name in settings["characters"]:
			string = sub(r"\b" + name + r"\b", settings["characters"][name], string)
	return string

def get_longest_name(settings):
	longest_name = "" # default name length
	if "characters" in settings:
		for name in settings["characters"]:
			character = settings["characters"][name]
			if len(character) > len(longest_name):
				longest_name = character
	return longest_name	
	
def get_issue(settings):
	if "issue" in settings:
		return settings["issue"]

def convert_lines(filename, out_filename, settings):
	with open(filename) as fh, open(out_filename, 'w') as out_fh:
		last = ""
		name = ""

		begin = ""
		with open("begin.tex.static") as begin_fh:
			begin = begin_fh.read()
		begin = sub(r'@@characters@@', gen_character_names(settings), begin)
		begin = sub(r'@@longestname@@', get_longest_name(settings), begin)

		if "title" in settings:
			begin = sub(r'@@title@@', settings["title"], begin)

		out_fh.write(begin)

		for line in fh:
			line_match = match(r'\[.+?] ([^\*\:]*?)(:|\*+)(.+)', line)
			new_line = line.strip()
			if line_match is not None:

				name = line_match.group(1) or line_match.group(2)
				msg = line_match.group(3).strip(" \n\t*")
			
				if match(r"^\*+$", name):
				    # try subbing all names because we don't know the length
					msg = sub_names(msg, settings)
					name = '*'

				if match(r'^\(\.\.\.\)', msg):
					continue

				if "characters" in settings and name in settings["characters"]:
					name = settings["characters"][name]

				# escape latex special characters
				msg = sub(r"\\", r"\\textbackslash{}", msg)
				msg = sub(r"([\$\%#_\{\}])", r"\\\1", msg)
				msg = sub(r"~", r"\\textasciitilde{}", msg)
				msg = sub(r"\^", r"\\textasciicircum{}", msg)

				# fix quotes
				msg = sub(r'"(.+?)"', r"``\1''", msg)
				msg = sub(r"'(.+?)'", r"`\1'", msg)
		
				# apply emphasis
				msg = sub(r">(.+?)<", r"\\emph\{\1\}", msg)
		
				new_line = "\\item["
				if name == last:
					new_line += "\\hbox{}"
				else:
					new_line += name

				if name == "*":
					new_line += "] \emph{" + msg + "}"
				else:
					new_line += "] " + msg
			
			out_fh.write(new_line + "\n")
			last = name	

		with open("end.tex.static") as end_fh:
			end = end_fh.read()
			out_fh.write(end)
	
def load_settings(filename):
	with open(filename) as fh:
		return yaml.load(fh.read())

def run(argv):
	if len(argv) != 4:
		print("usage: " + argv[0] + " <settings file> <skype log file> <output file (no extension)>")
		sys.exit(1)	
	
	convert_lines(argv[2], argv[3] + ".tex", load_settings(argv[1]))
	exit(os.system("pdflatex " + argv[3] + ".tex"))

run(sys.argv)
