#investigators should install chocolatey before use this script
#only approved package from chocolatey will be included
#This script must be run in the same path as the forensic readines database

import os
import sqlite3
import pandas as pd
#input forensic readiness file name
readiness = input("Process file path:")

#read database and load wallet name and version
conn = sqlite3.connect(readiness)
c = conn.cursor()
c.execute('SELECT * FROM application')
cols=[column[0] for column in c.description]
readiness_to_dataframe = pd.DataFrame.from_records(data=c.fetchall(),columns=cols)
conn.close()
wallet_names=list(readiness_to_dataframe.name)
wallet_versions=list(readiness_to_dataframe.version)

db_name_version=[] #db_name_version=(wallet name, version of that wallet)
for l in range(0,len(wallet_names)):
    db_name_version.append((wallet_names[l],wallet_versions[l]))
print(db_name_version) 

#execute chocolatey on the shell
stream = os.popen('choco list "wallet"')
output = stream.read()
print(type(output))

#split result of command
results=output.split('\n') #list of wallet packages uploaded on the chocolatey + other explanations
wallets=[] #list of wallet packages uploaded on the chocolatey
name_version=[] #name_version =(packagename, version of that wallet package)
j=0

for i in range(0,len(results)):
    result = results[i].split(' ')
    if '[Approved]' in result:
        wallets.append(results[i])
        j=j+1
        
for k in range(0,len(wallets)):
    name=wallets[k].split(' ')
    name_version.append((name[0],name[1])) 
    
#compare forensic readiness database and chocolatey package list
for t in range(0,len(name_version)):
    if name_version[t] not in db_name_version:
        print('Wallet list updated'+str(name_version[t]))
    continue
   
        
    
            