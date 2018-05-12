from __future__ import absolute_import
from __future__ import print_function
import numpy as np
import os
import re
import pprint
import string
from six.moves import input

# port_acl
# rfcipadd = "(?:10\.|127\.|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168).\d{1,3}.\d{1,3}"


# Loop Cisco config folder, pull and store data into a list and write to a file
def cisco_gen_data():
    cisco_list = []
    for (root, subFolders, files) in os.walk(ciscodir):
        for file in files:
            filepath = os.path.join(root, file)
            ciscodatafile = open('ciscodata.csv', 'a')
            with open(filepath) as ciscoconfig:
                txt = ciscoconfig.read()
                # find and format hostname
                hostname = re.search("[\n\r].*hostname\s*([^\n\r]*)", txt)
                if hostname is None:
                    hostname = 'NONE'
                else:
                    hostname = hostname.group(1)
                # find and format snmp-server location
                snmploc = re.search("(?:snmp-server location.)(.*)", txt)
                if snmploc is None:
                    snmploc = 'NONE'
                else:
                    # Convert snmploc_str to string
                    snmploc = snmploc.group(1)
                # find and format Trunk VLAN Tags
                trunkvlan = re.search("(?:switchport.trunk.allowed.vlan.)(\d+.*)", txt)
                if trunkvlan is None:
                    trunkvlan = 'NONE'
                else:
                    trunkvlan = trunkvlan.group(1)
                cisco_list = [root, hostname, snmploc, trunkvlan]
                ciscodatafile.write("%s\n" % cisco_list)
                ciscoconfig.close()
    return

# Loop Cisco config folder, pull and store vlan(s) into a list and write to a file
def cisco_portvlan_data():
    for (root, subFolders, files) in os.walk(ciscodir):
        for file in files:
            vlan_list = []
            router = [0]
            filepath = os.path.join(root, file)
            ciscovlanfile = open('ciscovlans.csv', 'a')
            with open(filepath) as ciscoconfig:
                for line in ciscoconfig.readlines():
                    cportvlans = re.search("(?:switchport.access.vlan.)(\d+)", line)
                    if cportvlans is None:
                        vlan_list.append(router)
                        continue
                    else:
                        cportvlans = cportvlans.group(1).split()
                        vlan_list.append(cportvlans)
                vlan_list = np.vstack({tuple(row) for row in vlan_list})
                print((vlan_list).T)
                ciscovlanfile.write("%s\n" % vlan_list)
                ciscoconfig.close()
    return

# Loop Extreme config folder, pull and store data into a list and write to a file
def extreme_gen_data():
    extreme_list = []
    for (root, subFolders, files) in os.walk(extremedir):
        for file in files:
            filepath = os.path.join(root, file)
            extremedatafile = open('extremedata.csv', 'a')
            with open(filepath) as extremeconfig:
                txt = extremeconfig.read()
                # find and format hostname
                sysname = re.search("(?:configure snmp sysN\w+.\")(\w+)", txt)
                if sysname is None:
                    sysname = 'NONE'
                else:
                    sysname = sysname.group(1)
                # find and format snmp-server location
                snmploc = re.search("(?:configure snmp sysL\w+.\")(\w+.*)(?:\")", txt)
                if snmploc is None:
                    snmploc = 'NONE'
                else:
                    # Convert snmploc_str to string
                    snmploc = snmploc.group(1)
                extreme_list = [root, sysname, snmploc]
                extremedatafile.write("%s\n" % extreme_list)
                extremeconfig.close()
    return

# Loop Extreme config folder, pull and store vlan and IP data into a list and write to a file
def extreme_vlan_data():
    # Find root directory, all subfolders, and files
    for (root, subFolders, files) in os.walk(extremedir):
        # Loop files one at a time in each subdirectory
        for file in files:
            # Set lists to empty
            ex_vlan_list = []
            ex_ip_list = []
            ex_vlantagports_list = []
            # Set file path to relative absolute path
            filepath = os.path.join(root, file)
            # Open output files for Append
            exipaddressesfile = open('exipaddresses.csv', 'a')
            exvlansfile = open('exvlans.csv', 'a')
            exvlantagfile = open('exvlantags.csv', 'a')
            # Open each file in Extreme Config Directory, file contents = txt
            with open(filepath) as extremeconfig:
                txt = extremeconfig.read()

                # find and format sysname, store in sysname
                sysname = re.search("(?:configure snmp sysN\w+.\")(\w+)", txt)
                if sysname is None:
                    sysname = 'NONE'
                else:
                    sysname = sysname.group(1)

                # Read config files lines, pull vlan name and tag. If tag is not set, vlan is not captured.
                extremeconfig.seek(0)
                for line in extremeconfig.readlines():
                    vlannametag = re.search("(?:configure.vlan.)(\w+.tag.\d+)", line)
                    if vlannametag is None:
                        continue
                    else:
                        vlannametag = vlannametag.group(1)
                        ex_vlan_list.append([sysname,vlannametag])

                # Read lines from top of file again
                extremeconfig.seek(0)
                # Read config files lines, pull vlan name and ip address. store in list.
                for line in extremeconfig.readlines():
                    exipname = re.search("(?:configure.vlan.)(\w+.)(?:ipaddress.)(\d+.*)", line)
                    exipaddress = re.search("(?:configure.vlan.)(\w+.)(?:ipaddress.)(\d+.*)", line)
                    if exipname is None:
                        continue
                    else:
                        exipname = exipname.group(1)
                        exipaddress = exipaddress.group(2)
                        ex_ip_list.append([sysname,exipname,exipaddress])

                # Read lines from top of file again
                extremeconfig.seek(0)
                # Read config files lines, pull ports, vlans and tags.
                for line in extremeconfig.readlines():
                    vlantagports = re.search("(?:configure.vlan.)(\w+.)(?:add.ports.)(\d.*)", line)
                    vlantagname = re.search("(?:configure.vlan.)(\w+.)(?:add.ports.)(\d.*)", line)
                    if vlantagports is None:
                        continue
                    else:
                        vlantagports = vlantagports.group(1)
                        vlantagname = vlantagname.group(2)
                        ex_vlantagports_list.append([sysname,vlantagports,vlantagname])
                for item in ex_ip_list:
                    exipaddressesfile.write("%s\n" % item)
                for item in ex_vlan_list:
                    exvlansfile.write("%s\n" % item)
                for item in ex_vlantagports_list:
                    exvlantagfile.write("%s\n" % item)
    return

# Take input from chk_ciscodir() -> Rename Config Files if filename is IP Address.
def renameconfigfiles():
    # Hostname Regex
    hostname = "[\n\r].*hostname\s*([^\n\r]*)"
    # Loop ciscodir() recursively
    for (root, subFolders, files) in os.walk(ciscodir):
        for file in files:
            # IP Address Regex
            nameipaddress = "\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            # Accept file extensiosn txt, log or cfg
            ext = "(.txt|.log|.cfg)"
            # Regex Search for files with ext file extension and convert to string
            ext = re.search(ext, file)
            ext = ext.group()
            # Skip files with no extension
            if file.endswith(ext):
                # Filepath includes subdirectory
                filepath = os.path.join(root, file)
                # Open File as ciscoconfig and search for data
                with open(filepath) as ciscoconfig:
                    # Convert config file to string
                    txt = ciscoconfig.read()
                    # Search for hostname using regex
                    host_str = re.search(hostname, txt)
                    # Search for IP Address using regex
                    ip = re.search(nameipaddress, file)
                    file, ext = os.path.splitext(file)
                # Is the Filename an IP Address?
                if ip is None:
                    continue
                else:
                    # Cnvert IP Address to string
                    add = ip.group()
                if host_str is None:
                    continue
                # Convert name to string and rename file to hostname of device
                name = host_str.group(1)
                newpath = os.path.join(root, name)
                if not os.path.exists(newpath):
                    os.rename(filepath, newpath + '.txt')
            else:
                print('{} already exists, passing'.format(newpath))

    return

# Take user input for Cisco Config File(s) Location. Send to renameconfigfiles() and scan recursively.
def chk_ciscodir():
    print('Checking to see if',  ciscodir, 'exists...')
    if os.path.exists(ciscodir):
        print("Cisco Config Path Found.")
        renameconfigfiles()
    else:
        print("Path does not exist. Check Syntax")
        return

# Take user input for Extreme Config File(s) Location. Send to renameconfigfiles() and scan recursively.
def chk_extremedir():
    print('Checking to see if', extremedir, 'exists...')
    if os.path.exists(extremedir):
        print("Extreme Config Path Found.")
    else:
        print("Path does not exist. Check Syntax")
        return


# Define Global Variables
def globals():
    global router
    global ciscodir
    global extremedir
    global cisco_list
    #global vlanname
    #sysname = "(?:configure snmp sysN\w+.\")(\w+)"
    #syslocation = "(?:configure snmp sysL\w+.\")(\w+)"
    #vlanname = "(create.vlan.)(\"\w+\")"
    ciscodir = input("Enter location of Cisco Configs: ")
    extremedir = input("Enter location of Extreme Configs: ")
    return


# Main function. Script processing starts here
def main():
    globals()
    #chk_ciscodir()
    chk_extremedir()
    #cisco_gen_data()
    #cisco_portvlan_data()
    extreme_gen_data()
    extreme_vlan_data()

# Run script
main()
