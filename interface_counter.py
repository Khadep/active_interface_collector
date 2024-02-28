import os
import csv
import sys
import netmiko
from nornir import InitNornir
import nornir.core.exceptions
from nornir.core.task import Result
from nornir_netmiko import netmiko_send_command
from nornir_netmiko import netmiko_send_config
from nornir.core.filter import F
from nornir_utils.plugins.functions import print_result
import ipdb

folder = "active_switchports"
switchportlist = []



def my_task(task):
    file1 = open(
        "C:\\Users\\lucidity\\Desktop\\"+folder+"\\"+task.host.name+"active_switchports_cisco.txt", "a")

    print("starting Interface Map on " + task.host.name)
    hresults = task.run(task=netmiko_send_command,
                        command_string='show interface status')
    
    hostname = task.host.name
    file1.write("-" * 50)
    file1.write(str(hresults[0]))
    interfaces = str(hresults[0])
    interfaces1 = interfaces.splitlines()
    file1.write('\n')
    file1.write("-" * 50)
    file1.write('\n')
    file1.write("-" * 50)
    file1.flush()
    total_gi_interfaces = 0
    used_gi_interfaces = 0
    total_te_interfaces = 0
    used_te_interfaces = 0
 
    for z in interfaces1:
        try:            
            #print(z)
            intsplit = z.split()
            file1.flush()
            #print(intsplit)
            #print(intsplit[0])
            # if "Gi" in  intsplit[0] and intsplit[-5] == "connected":
            #     total_gi_interfaces = total_gi_interfaces + 1
            #     used_gi_interfaces = used_gi_interfaces + 1
            # elif "Gi" in  intsplit[0] and intsplit[-5] == "notconnect":
            #     total_gi_interfaces = total_gi_interfaces + 1
            # elif "Gi" in  intsplit[0] and intsplit[-5] == "disabled":
            #     total_gi_interfaces = total_gi_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-5] == "connected":
            #     total_te_interfaces = total_te_interfaces + 1
            #     used_te_interfaces = used_te_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-6] == "connected":
            #     total_te_interfaces = total_te_interfaces + 1
            #     used_te_interfaces = used_te_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-5] == "notconnect":
            #     total_te_interfaces = total_te_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-6] == "notconnect":
            #     total_te_interfaces = total_te_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-5] == "disabled":
            #     total_te_interfaces = total_te_interfaces + 1
            # elif "Te" in  intsplit[0] and intsplit[-6] == "disabled":
            #     total_te_interfaces = total_te_interfaces + 1
            if "Gi" in  intsplit[0] and "connected" in intsplit[-5]:
                total_gi_interfaces = total_gi_interfaces + 1
                used_gi_interfaces = used_gi_interfaces + 1
            elif "Gi" in  intsplit[0] and "notconnect" in intsplit[-5]:
                total_gi_interfaces = total_gi_interfaces + 1
            elif "Gi" in  intsplit[0] and "disabled" in intsplit[-5]:
                total_gi_interfaces = total_gi_interfaces + 1
            elif "Te" in  intsplit[0] and "connected" in intsplit[-5]:
                total_te_interfaces = total_te_interfaces + 1
                used_te_interfaces = used_te_interfaces + 1
            elif "Te" in  intsplit[0] and "connected" in intsplit[-6]:
                total_te_interfaces = total_te_interfaces + 1
                used_te_interfaces = used_te_interfaces + 1
            elif "Te" in  intsplit[0] and "notconnect" in intsplit[-5]:
                total_te_interfaces = total_te_interfaces + 1
            elif "Te" in  intsplit[0] and "notconnect" in intsplit[-6] :
                total_te_interfaces = total_te_interfaces + 1
            elif "Te" in  intsplit[0] and "disabled" in intsplit[-5] :
                total_te_interfaces = total_te_interfaces + 1
            elif "Te" in  intsplit[0] and "disabled" in intsplit[-6] :
                total_te_interfaces = total_te_interfaces + 1
        except (IndexError):
            pass
    
    #print(total_gi_interfaces)
    #print(used_gi_interfaces)
    #print(total_te_interfaces)
    #print(used_te_interfaces)
    switchdict = {}
    #ipdb.set_trace()
    switchdict['Switch'] = hostname
    #print(hostname)
    switchdict['total_gi_interfaces'] = total_gi_interfaces
    switchdict['used_gi_interfaces'] = used_gi_interfaces
    switchdict['total_te_interfaces'] = total_te_interfaces
    switchdict['used_te_interfaces'] = used_te_interfaces
    if total_gi_interfaces > 0:
        r = round(((used_gi_interfaces/total_gi_interfaces) * 100), 2)
        switchdict['gi_percentage'] = (str(r)+ "%")
    if total_te_interfaces > 0:
        s = round(((used_te_interfaces/total_te_interfaces) * 100), 2)
        switchdict['te_percentage'] = (str(s)+ "%")
    #print("Printing Dict")
    switchportlist.append(switchdict)
    #print(switchdict)
    
    


def main():
    nr = InitNornir(config_file="nornir.yaml", core={"raise_on_error": True})
    cis = nr.filter(platform="cisco_ios")
    print("starting the script!!! Thanks Khade")
    try:
        thisresult = cis.run(task=my_task)
    except (nornir.core.exceptions.NornirExecutionError):
        pass
    try:
        csv_columns = ['Switch', 'total_gi_interfaces', 'used_gi_interfaces', 'total_te_interfaces', 'used_te_interfaces', 'gi_percentage', 'te_percentage']
        csv_file = "interface_count.csv"
        #print(switchportlist)
        with open(csv_file, 'a') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=csv_columns, lineterminator='\n')
            writer.writeheader()
            for data in switchportlist:
                writer.writerow(data)
                # ipdb.set_trace()
    except IOError:
        print("I/O error")
    print("All done...Thanks for using Interface collector you can collect the info you need from the csv files that were created in the "+folder+" folder.")


main()
# if __name__ == "__main__":
#    main()
