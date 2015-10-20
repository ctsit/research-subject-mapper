# Common tasks helper
# @author: Andrei Sura

help:
	@echo "Available tasks: "
	@echo "\t egg        - create the python *EGG* package"
	@echo "\t bdist      - create the binary distribution package"
	@echo "\t sdist      - create the software distribution package"
	@echo "\t test_gsm   - run the gsm application (expects the config folder 'gsm-devconfig')"
	@echo "\t test_gsmi  - run the gsmi application (expects the config folder 'gsmi-devconfig')"
	@echo "\t coverage   - run figleaf application to generate statistics on code coverage"
	@echo "\t test       - run unit tests"
	@echo "\t clean      - remove generated files"

# Create a source distribution
#	https://docs.python.org/2/distutils/sourcedist.html
#	https://docs.python.org/2/distutils/setupscript.html
egg:
	python setup.py bdist_egg

bdist:
	python setup.py bdist

sdist:
	python setup.py sdist

compile:
	python -m compileall rsm
	python -m compileall test

devconfig:
	git clone git@ctsit-forge.ctsi.ufl.edu:gsm-devconfig.git
	git clone git@ctsit-forge.ctsi.ufl.edu:gsmi-devconfig.git

test_gsm:
	@test -d gsm-devconfig || echo "Please create the 'gsm-devconfig' folder first"
	@echo "Executing rsm/generate_subject_map.py ..."
	PYTHONPATH=. python rsm/generate_subject_map.py -c gsm-devconfig -k -v

test_gsmi:
	@test -d gsmi-devconfig || echo "Please create the 'gsmi-devconfig' folder first"
	@echo 'Executing rsm/generate_subject_map_input.py ...'
	PYTHONPATH=. python rsm/generate_subject_map_input.py -c gsmi-devconfig -k -v

coverage:
	which figleaf || sudo easy_install figleaf
	figleaf test/TestSuite.py
	figleaf2html -d coverage .figleaf
	ls coverage/index.html

test: tests
tests:
	PYTHONPATH=. python -munittest discover test
	PYTHONPATH=. python test/TestSuite.py

clean:
	find . -type f -name *.pyc -print | xargs rm -f
	rm -rf log/gsm.log
	rm -rf log/gsmi.log
	rm -rf out_*
	rm -rf dist
	rm -rf build
	rm -rf rsm.egg-info
