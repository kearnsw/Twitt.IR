#!/bin/bash
wget -q -i urls -O - | grep "cacheResponse(" | sed 's/].*//' > parsed 
