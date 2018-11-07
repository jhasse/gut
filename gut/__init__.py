#!/usr/bin/env python3

import subprocess

VERSION = '0.1.1'

def run(cmd, silent=False, may_fail=False):
	if silent:
		cmd += " &>/dev/null"
	print('\x1b[1m> \x1b[34m' + cmd + '\x1b[0m')
	try:
		subprocess.check_call(cmd, shell=True)
	except subprocess.CalledProcessError as err:
		if not may_fail:
			raise err

def git_is_dirty():
	return subprocess.check_output(
		'git diff --shortstat 2> /dev/null | tail -n1', shell=True) != b''

def git_has_staged_changes():
	return subprocess.check_output('git diff --name-only --cached 2> /dev/null', shell=True) != b''
