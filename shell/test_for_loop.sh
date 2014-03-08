#!/bin/bash

numtimes="$1"

for (( i = 1; i <= $numtimes; i++))
do
  echo "Hi ${i} times."
done
