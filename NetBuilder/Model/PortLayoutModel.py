import NetBuilder.Model.BaseModel

class PortLayoutModel(NetBuilder.Model.E):
    alias: str = "Ethernet"
    speeds = ["10M","100M","1G","10G","25G","40G","50G","100G","200G","400G","800G"]
    breakout: int = False
    start: int = 1
    end: int = 48

    @property
    def range(self): 
        return (self.start, self.end)
    
    @range.setter
    def range(self, Range):
        start, end = Range
        self.start = start
        self.end = end
