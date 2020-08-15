import urllib.request, urllib.parse, urllib.error
import re
import pandas as pd
import string

url='https://fantasy.premierleague.com/api/bootstrap-static/'
fhand=urllib.request.urlopen(url)

info=''
for line in fhand:
    info=info+line.decode().strip()
    
#Gameweek Summaries
data=re.findall('"name":.+?},{"id"', info)
datadict={}
for i in data:
    if 'Gameweek' in i:
        if 'Gameweek 1"' in i:
            GW=i.split(',')
            GW[12]=GW[12]+','+GW[13]
            GW[14]=GW[14]+','+GW[15]
            GW[19]=GW[19]+','+GW[20]
            
            GW.pop(13)
            GW.pop(14)
            GW.pop(18)
            datadict[i[i.find('G'):i.find('","')]]=GW[1:3]+GW[5:9]+list(GW[12:13])+["",""]+GW[13:21]
        
        elif 'Gameweek 30+' in i:
            GW=i.split(',')
            GW[12]=GW[12]+','+GW[13]
            GW[14]=GW[14]+','+GW[15]
            GW[16]=GW[16]+','+GW[17]
            GW[21]=GW[21]+','+GW[22]
            
            GW.pop(13)
            GW.pop(14)
            GW.pop(15)
            GW.pop(19)
            datadict[i[i.find('G'):i.find('","')]]=GW[1:3]+GW[5:9]+GW[12:14]+[""]+GW[14:22]
             
        else:
            GW=i.split(',')
            GW[12]=GW[12]+','+GW[13]
            GW[14]=GW[14]+','+GW[15]
            GW[16]=GW[16]+','+GW[17]
            GW[18]=GW[18]+','+GW[19]
            GW[23]=GW[23]+','+GW[24]
            
            GW.pop(13)
            GW.pop(14)
            GW.pop(15)
            GW.pop(16)
            GW.pop(20)
            datadict[i[i.find('G'):i.find('","')]]=GW[1:3]+GW[5:9]+GW[12:23]

df=pd.DataFrame(datadict)
df=df.transpose()
df=df.drop([3,4], axis=1)
df.columns=['Deadline Time', 'Average Entry Score', 'Highest Scoring Entry', 'Highest Score', 'Bench Boosts Played', 'Free Hits Played', 'Wildcards Played', 'Triple Captains Played', 'Most Selected', 'Most Transferred', 'Top Player', 'Top Player Points', 'Transfers Made', 'Most Captained', 'Most Vice-Captained']

#removed unnecessary data in df cells
for column in df.columns:
    for i in range(0,len(df[column])):
        if column in ['Bench Boosts Played', 'Free Hits Played', 'Wildcards Played', 'Triple Captains Played']:
            df[column][i]=df[column][i][df[column][i].find('played":')+8:df[column][i].find('}')]
        
        elif column=='Top Player Points':
            df[column][i]=df[column][i][df[column][i].find('points":')+8:df[column][i].find('}')]
            
        else:
            df[column][i]=df[column][i][df[column][i].find(':')+1:]
        
df['Deadline Time']=df['Deadline Time'].str.replace('"','')
df['Most Vice-Captained']=df['Most Vice-Captained'].str.replace('}','')
df.to_excel("Gameweek Summaries.xlsx")

#Teams
data=re.findall('"code":.+?},', info)
data=data[:20]
data[19]=data[19][:data[19].find('"pulse_id":')+14]+','

datadict={}
for i in data:
    team=i.split(',')
    datadict[i[i.find("name")+7:i.find('","played"')]]=team
    
df=pd.DataFrame(datadict)
df=df.transpose()
df=df.drop([0,5,11,12,20,21], axis=1)

#renamed columns
columns=[]
for i in list(df.iloc[0]):
    title=i[:i.find(':')]
    title=title.replace('"','')
    title=title.replace('_',' ')
    title=string.capwords(title)
    columns.append(title)
df.columns=columns

#removed unnecessary data in df cells
for column in df.columns:
    for i in range(0,len(df[column])):
        df[column][i]=df[column][i][df[column][i].find(':')+1:]
        df[column][i]=df[column][i].replace('"','')        

df.to_excel("Teams.xlsx")

#Playerstats
data=re.findall('"chance_of_playing_next_round":.+?},', info)
data[-1]=data[-1][:data[-1].find('}]')+1]+','

datadict={}
for i in data:
    player=i.split(',')
    fullname=i[i.find("first_name")+13:i.find('","form"')]+' '+i[i.find("second_name")+14:i.find('","selected_by_percent"')]
    datadict[fullname]=player
    
df=pd.DataFrame(datadict)
df=df.transpose()

#renamed columns
columns=[]
for i in list(df.iloc[0]):
    title=i[:i.find(':')]
    title=title.replace('"','')
    title=title.replace('_',' ')
    title=string.capwords(title)
    columns.append(title)
df.columns=columns

#removed unnecessary data in df cells
for column in df.columns:
    for i in range(0,len(df[column])):
        df[column][i]=df[column][i][df[column][i].find(':')+1:]
        df[column][i]=df[column][i].replace('"','')

df['Ict Index Rank Type']=df['Ict Index Rank Type'].str.replace('}','')
df=df.drop(['Photo',''], axis=1)
df.index.rename('Full Name', inplace=True)

df.to_excel("Players Stats.xlsx")

#Player Performances
Playerstats.reset_index(inplace=True)
Playerstats['Id']=Playerstats['Id'].astype(int)
Playerstats.set_index('Id', inplace=True)
perfdb=pd.DataFrame()

for j in [11,12]:
    url='https://fantasy.premierleague.com/api/element-summary/'
    url=url+str(j)+'/'
    
    fhand=urllib.request.urlopen(url)
    info=''
    for line in fhand:
        info=info+line.decode().strip()
        
    data=re.findall('"element":.+?}', info)
    datadict={}
    for i in data:
        GW=i.split(',')
        datadict[i[i.find("fixture"):i.find(',"opponent_team"')].replace('":',' ')]=GW
        
    df=pd.DataFrame(datadict)
    df=df.transpose()
    
    #renamed columns
    columns=[]
    for i in list(df.iloc[0]):
        title=i[:i.find(':')]
        title=title.replace('"','')
        title=title.replace('_',' ')
        title=string.capwords(title)
        columns.append(title)
    df.columns=columns
    
    #removed unnecessary data in df cells
    for column in df.columns:
        for i in range(0,len(df[column])):
            df[column][i]=df[column][i][df[column][i].find(':')+1:]
            df[column][i]=df[column][i].replace('"','')
    df['Transfers Out']=df['Transfers Out'].str.replace('}','')
    
    name=Playerstats.loc[j,'Full Name']
    df['Index']=name+' '+df['Fixture']
    perfdb=pd.concat([perfdb,df])

perfdb.set_index('Index', inplace=True)    
perfdb.to_excel("Player Performances.xlsx")
