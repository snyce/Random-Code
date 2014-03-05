#!/bin/bash

if [ "$#" == "0" ]; then
  echo "$0 dir1 dir2 ... dirN"
  exit 1
fi

while (( "$#" )); do
  if [[ $(ls "${1}")  == "" ]]; then
    echo "Error val: $?"
    if [[ "$?" -eq "0" ]]; then
      echo "$1 is not a directory."
      exit 1
    else
      echo "Directory ${1} is empty."
    fi
  else
    echo "Directory ${1} is not empty."
  fi
  shift
done
