#!/usr/bin/env bash

if [[ $OSTYPE =~ ^darwin.* ]]; then
  if ! $(gxargs --version &> /dev/null); then
    brew install findutils
  fi
  xargs_tool='gxargs'
else
  xargs_tool='xargs'
fi

echo "Verifying requirements ..."
# This way of requirements installation enures priority/order within the requirements.txt file
cat requirements.txt | $xargs_tool -n 1 -L 1 -d "\n" -I {} pip install {}

echo "Start running ..."
time mlpiper run -f pipeline/pipeline.json --comp-root components
