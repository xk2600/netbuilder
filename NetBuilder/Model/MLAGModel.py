import NetBuilder.Model.BaseModel
import NetBuilder.Model.PrefixModel

class Prefix(NetBuilder.Model.PrefixModel):
	pass

class MLAG(NetBuilder.Model.BaseModel):
	A: int = 0
	B: int = 1
	
	prefix = NetBuilder.Model.Prefix("169.254.254.0/31", subnetlen=32)
	
	@property
	def addr(self):
		debug("<mlag>.addr: called")
		if   self.role == MLAG.A:
			debug("<mlag>.addr: A")
			return str(math.floor(self.prefix))
		elif self.role == MLAG.B:
			debug("<mlag>.addr: B")
			return str(math.ceil(self.prefix))
	
	@property
	def peer(self):
		debug("<mlag>.addr: called")
		if   self.role == MLAG.A:
			debug("<mlag>.addr: A")
			return str(math.ceil(self.prefix))
		elif self.role == MLAG.B:
			debug("<mlag>.addr: B")
			return str(math.floor(self.prefix))
	
	def virtual_router_mac(device_role, index):
		assert len(device_role) == 3
		mac = [ "%x:" % ord(ch) for ch in text ]
		mac.append("%02x" % index)
		for idx in range(len(mac), 6, 1):
			mac.insert(0, "00:")
		return ''.join(mac)
	
	enabled: bool = False
	role = None
	interfaces: str = []
