#!/bin/sh


if [ "$1" = "tests" ]; then
	cd test

	# Doing this in a setUp-method with micropython is just pain:
	echo "Cleaning up STORAGE_ROOT"
	rm -rf /tmp/specter_diy_tests
	
	 ../f469-disco/micropython_unix -c "import run_tests"
elif [ "$1" = "builddeps" ]; then
	git submodule update --init --recursive
	cd f469-disco
	./build_unixport.sh
	

elif [ "$1" = "sim" ]; then
	cd src
	../f469-disco/micropython_unix -c "import main; main.main()"
fi
