import NetBuilder.Model.ChassisModel
import NetBuilder.PortLayout



""" PortLayout Definitions--
        Representation of configuration options of a range of ports on a given device.
"""

class CU_1G(NetBuilder.Model.PortLayoutModel):
    speeds: ["10M", "100M", "1G"]

class SFP_PLUS(NetBuilder.Model.PortLayoutModel):
    speeds: ["10G"]

class SFP28(NetBuilder.Model.PortLayoutModel):
    speeds: ["25G"]

class QSFP(NetBuilder.Model.PortLayoutModel):
    speeds: ["10G","40G"]
    breakout: 4

class QSFP28(NetBuilder.Model.PortLayoutModel):
    speeds: ["10G","25G","40G","50G","100G"]
    breakout: 4

class OSFP(NetBuilder.Model.PortLayoutModel):
    speeds: ["25G","50G","100G","200G","400G"]
    breakout: 8




""" Vendor ChassisModel Definitions--
        Combines multiple `PortLayout`s into a representation of the front panel 
        ports available on a given device.
"""

class ARISTA(NetBuilder.Model.ChassisModel):
    """ ARISTA hardware specification--
            Front Panel Port Layout.
    """
    pass

ARISTA.DCS_7010T_48_F          = ARISTA(model_no="DCS-7010T-48-F",          layout=[  CU_1G(range=(1,48)),    SFP28(range=(49,51)) ])
ARISTA.DCS_7050CX3_32_F        = ARISTA(model_no="DCS-7050CX3-32S-F",       layout=[ QSFP28(range=(1,30)),    SFP28(range=(31,32)) ])
ARISTA.DCS_7050SX3_48YC12_F    = ARISTA(model_no="DCS-7050SX3-48YC12-F",    layout=[  SFP28(range=(1,48)),   QSFP28(range=(49,60)) ])
ARISTA.DCS_7260CX3_64_F        = ARISTA(model_no="DCS-7260CX3-64-F",        layout=[ QSFP28(range=(1,64))                          ])
ARISTA.DCS_7280CR2A_30F        = ARISTA(model_no="DCS-7280CR2A-30F",        layout=[ QSFP28(range=(1,30))                          ])
ARISTA.DCS_7280SR2A_48YC6_F    = ARISTA(model_no="DCS-7280SR2A-48YC6-F",    layout=[  SFP28(range=(1,48)),   QSFP28(range=(49,54)) ])


class PALOALTONETWORKS(NetBuilder.Model.ChassisModel):
    """ Palo Alto Networks hardware specification --
            Front Panel Port Layout.
    """
    pass

PALOALTONETWORKS.PA_7050_SMC_B = PALOALTONETWORKS(model_no="PA-7050-SMC-B", layout=[  SFP28(rabge=(1,8)),    QSFP28(range=(25,28)) ])
