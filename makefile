# Common tasks helper
# @author: Andrei Sura

# Create a source distribution
#	https://docs.python.org/2/distutils/sourcedist.html
#	https://docs.python.org/2/distutils/setupscript.html
dist:
	#python setup.py bdist --format=gztar
	python setup.py sdist --format=gztar,zip

test_gsm:
	echo 'Executing bin/generate_subject_map.py ...'
	python bin/generate_subject_map.py -c gsm_config -k yes

test_gsmi:
	echo 'Executing bin/generate_subject_map_input.py ...'
	python bin/generate_subject_map_input.py -c gsmi_config -k yes

help:
	echo 'Available tasks: dist, clean, test_gsm, test_gsmi'

clean:
	rm -rf log/rsm.log
	rm -rf out/*
	rm -rf dist
	rm -rf build
	rm -rf rsm.egg-info
