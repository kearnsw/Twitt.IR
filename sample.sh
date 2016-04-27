#!/bin/sh

until python ./src/createSample.py "$1" "$2" "$3" "$4"; do
	echo "Server crashed with exit code $?. Respawning.." >&2
	sleep 86400
done

