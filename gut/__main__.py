import click
import os
import subprocess
from gut import run, git_is_dirty, git_has_staged_changes, random_name, VERSION

@click.command()
@click.version_option(version=VERSION)
@click.argument('command', nargs=-1, required=True)
def main(command):
	os.environ['LANG'] = 'C.UTF-8'
	try:
		if command == ("pull",):
			has_staged_changes = git_has_staged_changes()
			if has_staged_changes:
				run('git stash --keep-index')
				stash_name = random_name()
				run('git stash save "{}"'.format(stash_name))
				run('git stash apply stash@{1}')
				run('git stash show -p | git apply -R')
				run('git stash drop stash@{1}')
			needs_stash = git_is_dirty()
			if needs_stash:
				run('git stash', silent=True)
			try:
				run('git pull ' + ' '.join(command[1:]))
			finally:
				if needs_stash:
					try:
						run('git stash pop', silent=True)
						if has_staged_changes:
							run('git reset .')
							run('git stash pop', silent=True)
					except subprocess.CalledProcessError:
						run('git stash drop')
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
		elif command[0] == 'revert':
			run('git reset -- ' + command[1])
		elif command[0] == 'switch':
			needs_stash = git_is_dirty()
			if needs_stash:
				run('git stash -k', silent=True)
			try:
				run('git checkout ' + command[1])
			finally:
				if needs_stash:
					try:
						run('git stash pop', silent=True)
					except subprocess.CalledProcessError:
						run('git stash drop', silent=True)
		else:
			click.secho('gut: Unknown command ' + click.style(' '.join(command), fg='red',
			                                                  bold=True))
	except subprocess.CalledProcessError as err:
		click.secho(str(err), fg='red', bold=True)

main()
