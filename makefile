# Common tasks helper
# @author: Andrei Sura

help:
	echo 'Available tasks: egg, bdist, sdist, test_gsm, test_gsmi, coverage, clean'

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
	python -m compileall bin
	python -m compileall test


test_gsm:
	echo 'Executing bin/generate_subject_map.py ...'
	python bin/generate_subject_map.py -c gsm_config -k yes

test_gsmi:
	echo 'Executing bin/generate_subject_map_input.py ...'
	python bin/generate_subject_map_input.py -c gsmi_config -k yes

coverage:
	which figleaf || sudo easy_install figleaf
	figleaf test/TestSuite.py
	figleaf2html -d coverage .figleaf
	ls coverage/index.html

tests:
	PYTHONPATH=. python -munittest discover test

clean:
	rm -rf log/rsm.log
	rm -rf out/*
	rm -rf dist
	rm -rf build
	rm -rf rsm.egg-info
