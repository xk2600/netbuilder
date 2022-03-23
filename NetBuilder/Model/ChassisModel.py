import NetBuilder.Model.BaseModel

class ChassisModel(NetBuilder.Model.BaseModel):
    model_no: str
    layout: []
    
    @property
    def interfaces(self):
        """ generates a listing of interface objects based on the layout specified.
            NOTE: should include Management1 and Console port so we can map them.
        """
        return NotImplemented
