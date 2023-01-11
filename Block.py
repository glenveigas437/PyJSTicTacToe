class Block:
    def __init__(self, number):
        self.number = number
        self.vacant = True
        self.currentValue = None
        self.placedBy = None
    
    def getVacantStatus(self):
        return self.vacant
    
    def getBlockMetaData(self):
        return f"Block Number:{self.number}, Is Vacant?: {'Yes' if self.getVacantStatus() else 'No'}, Current Value is: {self.currentValue}, Placed By: {self.placedBy}"