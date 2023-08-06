# -*- coding: utf-8 -*-
# :Project:   metapensiero.sqlalchemy.dbloady -- M2M functional test
# :Created:   sab 18 gen 2020, 08:30:10
# :Author:    Lele Gaifax <lele@metapensiero.it>
# :License:   GNU General Public License version 3 or later
# :Copyright: © 2020 Lele Gaifax
#

PYTHON3 ?= python3.7

.PHONY: test
test: env testdbloadydb
	env/bin/dbloady -u sqlite:////tmp/testdbloady.sqlite data.yaml
	env/bin/python model.py test

env:
	$(PYTHON3) -m venv env
	env/bin/pip install --upgrade pip
	env/bin/pip install sqlalchemy
	env/bin/pip install -e ../.. .

.PHONY: testdbloadydb
testdbloadydb:
	rm -f /tmp/testdbloady.sqlite
	env/bin/python model.py setup

.PHONY: clean
clean:
	rm -f /tmp/testdbloady.sqlite

.PHONY: realclean
realclean: clean
	rm -rf env __pycache__ testdbloady.egg-info
