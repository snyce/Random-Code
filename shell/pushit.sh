#!/bin/bash

if [ "$#" -lt "1" ]
then
  echo "Stupid script to speed up commiting changes in Puppet Labs training."
  echo "Usage: $0 <file>"
  exit 1
fi

file="${1}"

function pushit {
  git add ${file}
  git commit
  git push origin master
}

if [ -e ${file} ]
then
  pushit ${file}
else
  echo "File ${file} not found."
  exit 1
fi
