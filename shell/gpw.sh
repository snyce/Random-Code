#!/bin/sh

# Error retcodes (ok, just being goofy)
E_NO_ARGS=65
E_TOO_SHORT=75
E_TOO_LONG=85
E_NUMBER_ONE=1

# the length of the password in chars
pwlen="${1}"
numpw="${2}"

if [[ -z "${2}" ]]
then
  numpw="1"
else
  numpw="${2}"
fi

if [[ -z "${1}" ]]
then
  pwlen="10"
else
  pwlen="${1}"
fi

if [ "${pwlen}" -gt "250" ]
then
  #Comment this whole if loop out if you want larger than 250
  echo "Password should probably be <= 250 characters"
  exit ${E_TOO_LONG}
fi

if [ "$#" -eq 0 ]
then 
  echo "Usage: ./gpw.sh length amount (amount is optional)"
  exit ${E_NO_ARGS}
else
  if ! [[ "${pwlen}" =~ ^[0-9]+$ ]]
  then
    echo "Sorry Charlie, $pwlen is not an interger, exiting!"
    sleep 2;
    echo "I said GOOD DAY!"
    exit ${E_NUMBER_ONE}
  else
    if [ ${pwlen} -lt 5 ] 
    then
      echo "Password should probably be greater than $pwlen characters long."
      exit ${E_TOO_SHORT}
    else
      if [[ ${numpw} -eq "1" ]]
      then
        echo "Generating password that is ${pwlen} characters long."
        sleep 1;
        LANG=C; tr -cd "[:upper:][:alnum:][:punct:]" < /dev/urandom | head -c ${pwlen} | xargs -0; LANG=en_US.UTF-8
      else
        echo "Generating $numpw passwords of ${pwlen} characters."
        sleep 1;
        for ((i = 1; i <= ${numpw}; i++))
         do 
           LANG=C; tr -cd "[:upper:][:alnum:][:punct:]" < /dev/urandom | head -c ${pwlen} | xargs -0; LANG=en_US.UTF-8
         done
        fi
    fi
  fi
fi
