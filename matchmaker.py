import Player
import config
import random
import sys
import visualizeNetwork
from pathlib import Path

playersDict = {}
trustThreshold = 3
passIteration = 0

def main():
    global playersDict
    global trustThreshold
    global passIteration
    cwd = Path.cwd()
    desiredJSON = "user_50_v1.json"
    desiredJSONPath = cwd / desiredJSON
    playersDict = Player.Player.getPlayerDictFromJSON(desiredJSONPath)
    trustThreshold = config.simSettings['trustThreshold']
    for _ in range(config.simSettings['mmIterations']):
        passIteration += 1
        onTick()
    #print(playersDict[0].MatchList)
    visualizeNetwork.visualizeNetworkGraph(playersDict)
    
#Each tick represents an iteration of matchmaking.  Players are placed into a pool and shuffled. Order in the list represents relative queue time.
def onTick():
    global trustThreshold
    global passIteration
    foundMatch = False
    dastardlyCount = 0
    stewardMatchesMissed = 0
    trustThresholdTemp = trustThreshold
    mmList = list(playersDict.values())
    random.shuffle(mmList)
    i = 0 #outer loop variables
    j = len(mmList) 
    k = 0 #inner loop variables
    n = len(mmList)

    #outer loop iterates through players looking for games. If the player fails to find a match the algorithm skips them and moves on to the next player
    while(i < j):
        foundMatch = False
        tbm = mmList[i] #start with the first player. In theory they've been in queue the longest
        #Inner loop iterates through available players
        # 1. The To-Be-Matchmade player is compared with a player in the matchmaking list
        # 2. If the trust score is high enough they can be matchmade
        # 3. Both players increment add each other to players they've matched with and remove themselves from the list
        while(k < n):
            if(i == k):
                k += 1
                continue
            trustScore = compare(tbm, mmList[k]) 
            if trustScore is None or trustScore >= trustThreshold:
                foundMatch = True
                matchmake(tbm, mmList[k])
                tbm.MatchesFound += 1
                mmList[k].MatchesFound += 1
                tbm.MatchList.add(mmList[k].id)
                mmList[k].MatchList.add(tbm.id)
                mmList.remove(mmList[i])
                mmList.remove(mmList[k-1])
                n -= 2
                j -= 2
                k = 0
                i = 0
                break
            else:
                k += 1
        if(foundMatch == False):
            i += 1
            


def compare(tbm, mc): #player to be matched and player match Candidate
    trustedCount = 0 
    trustSet = False #if trust is never adjusted this is a player outside my web. We'll want to prioritize playing them to get them in the web

    if(mc.id in tbm.Trust and tbm.id in mc.Trust): #Players that trust each other can automatically be matched
        return sys.maxsize
    
    if(mc.id in tbm.Distrust or tbm.id in mc.Distrust): #Players can't be matched with players they don't like
        return -sys.maxsize

    # If the match candidate is trusted by players in the to-be-matched player's web of trust that boosts the trust score
    for playerID in tbm.Trust:
        if(playerID in mc.TrustedBy):
            trustSet = True
            trustedCount += 1
    #If the match candidate is not trusted by players in the to-be-matched player's web of trust that lowers the trust score
        elif(playerID in mc.DistrustedBy):
            trustSet = True
            trustedCount -= 1

    if(trustSet):
        return trustedCount
    return None

#Simulate whether the players are going to trust each other based on roles after the "game is complete"
def matchmake(tbm, mc):
    if(mc.id in tbm.Trust and tbm.id in mc.Trust): #Trust already established
        return
    match mc.PlayerType:
        case "Steward":
            tbm.Trust.add(mc.id)
            mc.TrustedBy.add(tbm.id)
        case "AlmostGood":
            randomNumber = random.randint(1,10)
            if(randomNumber > 2): #Almost good players usually are good teammates, but sometimes have off days
                tbm.Trust.add(mc.id)
                mc.TrustedBy.add(tbm.id)
            else:
                tbm.Distrust.add(mc.id)
                mc.DistrustedBy.add(tbm.id)
        case "ConstantBummer":
            randomNumber = random.randint(1,10)
            if(randomNumber > 3): #Constant bummers often produce negative experiences for partner
                tbm.Distrust.add(mc.id)
                mc.DistrustedBy.add(tbm.id)
            else:
                tbm.Trust.add(mc.id)
                mc.TrustedBy.add(tbm.id)
        case "Dastardly":                   #Dastardly present the most negative experience
            tbm.Distrust.add(mc.id)
            mc.DistrustedBy.add(tbm.id)
        case "Bad":                         #Bad players have more negative experiences than positive
            randomNumber = random.randint(1,10)
            if(randomNumber > 5):  
                tbm.Trust.add(mc.id)
                mc.TrustedBy.add(tbm.id)
            else:
                tbm.Distrust.add(mc.id)
                mc.DistrustedBy.add(tbm.id)

    match tbm.PlayerType:
        case "Steward":
            mc.Trust.add(tbm.id)
            tbm.TrustedBy.add(mc.id)
        case "AlmostGood":
            randomNumber = random.randint(1,10)
            if(randomNumber > 2): #Almost good players usually are good teammates, but sometimes have off days
                mc.Trust.add(tbm.id)
                tbm.TrustedBy.add(mc.id)
            else:
                mc.Distrust.add(tbm.id)
                tbm.DistrustedBy.add(mc.id)
        case "ConstantBummer":                  #Constant bummers often produce negative experiences for partner
            randomNumber = random.randint(1,10)
            if(randomNumber > 3):               
                mc.Distrust.add(tbm.id)
                tbm.DistrustedBy.add(mc.id)
            else:
                mc.Trust.add(tbm.id)
                tbm.TrustedBy.add(mc.id)
        case "Dastardly":                       #Dastardly present the most negative experience
            mc.Distrust.add(tbm.id)
            tbm.DistrustedBy.add(mc.id)
        case "Bad":                             #Bad players are middle of the road 
            randomNumber = random.randint(1,10)
            if(randomNumber > 5): 
                mc.Trust.add(tbm.id)
                tbm.TrustedBy.add(mc.id)
            else:
                mc.Distrust.add(tbm.id)
                tbm.DistrustedBy.add(mc.id)


main()