#!/bin/bash
#

set -e

if [[ $# -eq 0 ]]
then
	python3 -m adbutils -i https://github.com/appium/java-client/raw/master/src/test/java/io/appium/java_client/ApiDemos-debug.apk
fi
py.test -v "$@"
