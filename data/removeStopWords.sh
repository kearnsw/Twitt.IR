#!/bin/bash
<$1 sed 's:.*:s/\\b&\\b//:g' | sed -i -f - $2
