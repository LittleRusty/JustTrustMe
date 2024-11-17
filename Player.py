import json

class Player:
    id = 0
    Trust = set()
    TrustedBy = set()
    Distrust = set()
    DistrustedBy = set()
    NeutralOn = set()
    NeutralBy = set()
    PlayerType = "echo"
    MatchFound = False
    MatchList = set()
    MatchesFound = 0

    @classmethod
    def getPlayerFromData(cls, data):
            player = cls()
            player.id = data.get('_id', 0)
            player.Trust = set(data.get('Trust', []))
            player.TrustedBy = set(data.get('TrustedBy', []))
            player.Distrust = set(data.get('Distrust', []))
            player.DistrustedBy = set(data.get('DistrustedBy', []))
            player.NeutralOn = set(data.get('NeutralOn', []))
            player.NeutralBy = set(data.get('NeutralBy', []))
            player.PlayerType = data.get('PlayerType', "echo")
            player.MatchFound = False
            player.MatchList = set()
            player.MatchesFound = 0
            return player


    @classmethod
    def getPlayerDictFromJSON(cls, filePath):
        with open(filePath, 'r', encoding='utf-8') as file:
                jsonData = json.load(file)
        
        playersJSON = jsonData.get("players", [])
        playersDict = {}

        for player in playersJSON:
            playersDict[player.get("_id")] = cls.getPlayerFromData(player)

        return playersDict

