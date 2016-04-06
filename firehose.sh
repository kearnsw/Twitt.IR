#!/bin/sh

until python Firehose.py "$1" "$2"; do
	echo "Server crashed with exit code $?. Respawning.." >&2
	sleep 30
done

