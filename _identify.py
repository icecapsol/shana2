#!/usr/bin/python
import subprocess

def identify(format, chunk):
	pid = subprocess.Popen(['identify', '-format', '"%s"' % format, '-'], executable='identify', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = pid.communicate(chunk)
	return out.decode('utf-8').replace('"', '')

def identify_verbose(chunk):
	pid = subprocess.Popen(['identify', '-verbose', '-'], executable='identify', stdin=subprocess.PIPE, stdout=subprocess.PIPE)
	out, err = pid.communicate(chunk)
	return out.replace('"', '')