# Makefile

SHELL := /bin/bash

help:  ## show this help.
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

#
# TESTS
#
test:  ## run selected tests
	source env.sh && py.test --cov=./lily_env --cov-config .coveragerc -r w -s -vv $(tests)

test_all:  ## run all available tests
	source env.sh && py.test --cov=./lily_env --cov-config .coveragerc -r w -s -vv tests

coverage:  # render html coverage report
	coverage html -d coverage_html && google-chrome coverage_html/index.html

#
# UPGRADE_VERSION
#
# FIXME: I should develop some django free project for upgrading the version?
# lily-upgrader --> ca upgrade version and tag and push at the same time!
# should also be able to inspect the versions of the entrypoint to know if
# something incompatible changed? --> so that would be auto-upgrader option
# --> it would have to make sure that always the newest entrypoint is available
# --> so how would it call the entrypoint? --> lily could deliver such command
# --> so it will fire it up! -->
# --> also I should deliver commands for running various other stuff of lily
# upgrade_version_patch:  ## upgrade version by patch 0.0.X
# 	source env.sh && python lily/manage.py upgrade_version PATCH

# upgrade_version_minor:  ## upgrade version by minor 0.X.0
# 	source env.sh && python lily/manage.py upgrade_version MINOR

# upgrade_version_major:  ## upgrade version by major X.0.0
# 	source env.sh && python lily/manage.py upgrade_version MAJOR
