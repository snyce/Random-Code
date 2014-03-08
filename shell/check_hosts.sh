#!/bin/bash 

### Feel free to modify to suit your needs ###
### NOTE: this is not portable as it stands, OSX will not handle the echo -e###
### could substitute printf, but I'll leave that as an exercise for the reader###

# set these up for a litte bit more modular design
# Get the EUID of the user to make sure that they are running with superuser privs
getId=$(/usr/bin/id -u)

# Use dmidecode to get the processor and system info (using egrep to clean up returned results)
# Make sure the user has the EUID of "0" to be able to get the information required (mainly dmidecode)
if [ ${getId} = "0" ]
then
  procType=$(/usr/sbin/dmidecode -s processor-version | egrep -v 'dmidecode|SMBIOS')
  sysInfo=$(/usr/sbin/dmidecode -t 1 | egrep -v 'dmidecode|SMBIOS')
else
  echo -e "\nSorry can't get Processor and System information from dmidecode!"
fi

# Get the hostname and ipaddress(es)
host=$(/bin/hostname)
ipAddy=$(/sbin/ifconfig | grep -v 127.0.0.1 | grep "inet addr" | awk -F: '{ print $2 }' | sed -e 's/Bcast//')

# use below on OSX
# ipAddy=$(ifconfig | grep inet | awk '{print $2}' | grep -v [:num:])

# Get the memory and cpu count
memBase=$(/bin/cat /proc/meminfo | grep MemTotal | awk '{ print $2 }')
cpuCount=$(/bin/cat /proc/cpuinfo | grep "^processor" | wc -l)
memTotal=$(/usr/bin/expr $memBase / 1000 / 1000)

# Make sure the release, and architecture match the correct version
release=$(/bin/cat /etc/redhat-release)
relver=$(/bin/cat /etc/redhat-release | awk '{ print $3 }')
arch=$(/bin/uname -i)

# Make sure the /Data partition is large enough and then print the layout
diskLayout=$(/bin/df -lh)
disk=$(/bin/df | grep /Data | awk '{ print $1 }')

# DEBUG variables to test the script with
#disk="167772150"
#disk="167772160"
#memTotal='33000000'
#arch="i686"
#cpuCount="7"

if [ ${getId} != "0" ]
then
  echo -e "You must be, or have superuser privileges to run this script!\n"
  exit 1
else
  # Add logic to make sure the values are withing spec - this is not modular enough, need to be able to specify 
  # the default values based on the BOM 
  echo -e "\n==========================================================\n"
  echo -e "[Hostname]: \n$host\n"
  echo -e "[IP Address]: \n$ipAddy\n"
  if [ "$memBase" -lt "32" ]
  then
    echo -e "[Memory]: \nERROR! $memTotal GB ($memBase) is below minium 32 GB (32956180) required!\n"
  else
    echo -e "[Memory]: \n$memTotal GB\n"
  fi
  if [ "$cpuCount" -lt "4" ]
  then
    echo -e "[CPU Count]: \nERROR! CPU Count is $cpuCount, should be greater than or equal to 8!\n"
  else
    echo -e "[CPU Count]: \n$cpuCount\n"
  fi
  if [ "$relver" != "5.5" ]
  then
    echo -e "[Release]: \nERROR! The release: $release ($relver) is less than the required 5.5\n"
  else
    echo -e "[Release]: \n$release\n"
  fi
  if [ "$arch" != "x86_64" ]
  then
    echo -e "[Architecture]: \nERROR! Wrong Architecture! $arch\n"
  else
    echo -e "[Architecture]: \n$arch\n"
  fi
  if [[ "$disk" -lt "162" ]]
  then
    echo -e "[Data]: \n$disk is below the minimum 160GB (167772160)\n"
  else
    echo -e "[Data]: \n/Data is more than 160GB currently ($disk)\n"
  fi
  echo -e "[Processor Type]:\n$procType\n"
  echo -e "[System Information]:$sysInfo\n"
  echo -e "[Disk Layout]:\n$diskLayout\n"
  echo -e "\n==========================================================\n"
fi
