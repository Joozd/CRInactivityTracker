### will sort players by time since last battle and indicate how much time that is.
### will write data to shelve
### will get data from clash royale api

import clashroyale, shelve, datetime, pprint

clan_id = 'VVPY8C'

## (year, month, day)
today = datetime.date.today()

apiKeyFile=open('ClashRoyaleAPIKey.txt')
apiKey=apiKeyFile.read()
apiKeyFile.close()


def getClanMembers(crClient, clanID):  # will return a dictionary with { 'tag':  'name' }
    clanObj=crClient.get_clan(clanID)
    full_clan_info=clanObj.raw_data
    clanMembers={}
    for memberRecord in full_clan_info['memberList']:
        name=memberRecord['name']
        tag=memberRecord['tag'][1:]
        clanMembers[tag]=name
    return clanMembers

def getMemberInfo(crClient, playerID): # returns a dict with {'name': 'joozd', 'battleCount': 3517, 'totalDonations': 719, 'trophies': 3178}
    memberInfoList={}
    playerData=crClient.get_player(playerID)
    playerDict=playerData.raw_data
    memberInfoList['name']=playerDict['name']
    memberInfoList['battleCount']=playerDict['battleCount']
    memberInfoList['totalDonations']=playerDict['totalDonations']
    memberInfoList['trophies']=playerDict['trophies']
    return memberInfoList

def updateShelve(memberInfoDict): # memberInfoDict = {'98VVU2GQ':['Joozd', 9487]
    shelfFile = shelve.open('CRMemberData')
    for member in memberInfoDict:
        memberInfoDict[member]['lastSeen']=today
        if member not in list(shelfFile.keys()):
            shelfFile[member]=memberInfoDict[member]
            print('new member ' + member + 'added, new info:')
            print (shelfFile[member])
            # shelfFile['98VVU2GQ']={'name':'Joozd', 'battleCount': 9487, 'lastSeen':datetime.date.today()]
            continue
        if shelfFile[member]['battleCount'] == memberInfoDict[member]['battleCount'] and shelfFile[member]['totalDonations'] == memberInfoDict[member]['totalDonations'] and shelfFile[member]['trophies'] == memberInfoDict[member]['trophies']:
            print (member + ' (' + shelfFile[member]['name'] + ') not active, last seen on ' + str(shelfFile[member]['lastSeen']))
            continue
        shelfFile[member]=memberInfoDict[member]
        shelfFile[member]['lastSeen']=today
    returnDict={}
    for key in list(shelfFile.keys()):
        returnDict[key]=shelfFile[key]
    shelfFile.close()
    return returnDict
            
    


client = clashroyale.official_api.Client(apiKey)

memberList=getClanMembers(client,clan_id)

memberInfo={}
for memberTag in memberList:
    memberInfo[memberTag]=getMemberInfo(client, memberTag)

fullList = updateShelve(memberInfo)
finalList={}
for member in fullList:
    finalList[member]=fullList[member]['lastSeen']

width= len(fullList[max(fullList, key=lambda v: fullList[v]['name'])]['name']) + 7

print('\n\n\nname'.ljust(width) + '  Last seen on')
d_view = [ (v,k) for k,v in finalList.items() ]
d_view.sort(reverse=True) # natively sort tuples by first element
for v,k in d_view:
    print ((fullList[k]['name'] + '('+ str(fullList[k]['trophies']) + ')').ljust(width)+ ': ' + str(v) + '\t' + str((today-v).days) + ' days ago.')
