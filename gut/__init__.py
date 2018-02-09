#!/usr/bin/env python3

import subprocess
import os
import click

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

VERSION = '0.1.0'

@click.command()
@click.version_option(version=VERSION)
@click.argument('command', nargs=-1, required=True)
def main(command):
	os.environ['LANG'] = 'C.UTF-8'
	try:
		if command == ("pull",):
			needs_stash = git_is_dirty()
			if needs_stash:
				run('git stash -k', silent=True)
			try:
				run('git pull ' + ' '.join(command[1:]))
			finally:
				if needs_stash:
					try:
						run('git stash pop', silent=True)
					except subprocess.CalledProcessError:
						run('git stash drop', silent=True)
		elif command == ('stash', 'pop'):
			needs_commit = git_is_dirty()
			if needs_commit:
				run('git commit -am GUT_TMP')
			run('git stash apply --quiet', may_fail=True)
			run('git stash drop')
			if needs_commit:
				run('git reset --soft HEAD~')
		elif command == ('stash',):
			has_staged_changes = git_has_staged_changes()
			if has_staged_changes:
				run('git commit -m GUT_TMP')
			run('git stash --include-untracked')
			if has_staged_changes:
				run('git reset --soft HEAD~')
		else:
			click.secho('gut: Unknown command ' + click.style(' '.join(command), fg='red',
			                                                  bold=True))
	except subprocess.CalledProcessError as err:
		click.secho(str(err), fg='red', bold=True)