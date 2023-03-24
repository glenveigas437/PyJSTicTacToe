import json
class Player:
    def __init__(self, name, playerType):
        self.name = name
        self.playerType = playerType
        self.foulPlay=0
        self.foulMove=False

class PlayerEncoder(json.JSONEncoder):
    def default(self, object):
        if isinstance(object, Player):
            return {'name':object.name, 'playerType':object.playerType, 'foulPlay':object.foulPlay}
        
        return super().default(object)