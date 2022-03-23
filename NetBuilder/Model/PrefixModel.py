import unittest
import math

def debug(message):
	print(f"DEBUG: {message}")
	pass                           # disables debugging output

class Prefix:
	""" Enables ipPrefixes to be treated like generic numeric types while
	    preserving thier presentation and allowing subnetting and suppernetting
	    to be applied to networks. Prefix maintains linkage to parent and child
	    prefixes as well, allowing a tree of allocations to be observed should
	    one use this to build IP based topologies or as tooling for IPAM functions.
	"""
	
	__author__    = "Christopher M. Stephan"
	__copywrite__ = "Copywrite (C) 2016 Christopher Stephan"  
	__license__   = "2-cluase BSD License"
	__version__   = "0.1.2"
	    
	IPV4 = None
	_supernet = None
	
	@staticmethod
	def toBytes(netid: int = 0):
		result = []
		remainder = netid
		for bitval in range(24, -1, -8):
			octet = remainder >> bitval
			remainder = remainder % (2 ** bitval)
			result.append(octet)
		return result
		
	@staticmethod
	def toStr(netid: int = 0):
		lnet = [ str(octet) for octet in Prefix.toBytes(netid) ]
		return '.'.join(lnet)
		
	@property
	def masklen(self):
		return self._masklen
		
	@masklen.setter
	def masklen(self, masklen):
		debug(f"<prefix>.masklen.__set__: {masklen}")
		try:
			self._masklen = int(masklen)
			self._netid = self.netid & ( 4294967295 << (32 - self._masklen) )
		except:
			raise ValueError("mask must be an integer between 0 and 32")
		debug(f"<prefix>.masklen.__set__: (self.netid, self._masklen): {self.netid}, {self.masklen}")
	
	@property
	def netid(self):
		return self._netid
		
	@property
	def net(self):
		return self.toStr(self._netid)
		
	@net.setter
	def net(self, net: str):
		debug(f"<prefix>.net.__set__: net: {net}")
		if isinstance(net, str):
			# convert to integer
			net = net.split(".")
			assert len(net) == 4, "malformed dotted decimal address, should be 'x.x.x.x'"
			try:
				for octet in net.copy():
					net = ((net << 8) + int(octet)) if isinstance(net, int) else int(octet)
			except:
				raise ValueError("net must be a dotted-decimal string")
		debug(f"<prefix>.net.__set__: {net}")
		self._netid = net
	
	@property
	def supernet(self):
		return self._supernet
		
	@supernet.setter
	def supernet(self, supernet):
		self._supernet = supernet
		
	@property
	def boundary(self):
		return self._boundary
		
	@boundary.setter
	def boundary(self, boundary):
		self._boundary = boundary
		
	@property
	def subnetlen(self):
		return self._subnetlen
		
	@subnetlen.setter
	def subnetlen(self, subnetlen):
		if isinstance(self.masklen, int) and isinstance(subnetlen, int):
			if subnetlen < self.masklen:
				self.subnetlen = self.masklen
		self._subnetlen = subnetlen
		
	@property
	def netpath(self):
		result = [self]
		cursor = self
		while cursor.supernet is not Prefix.IPV4:
			debug(f"<prefix>.netpath: cursor.supernet: {cursor.supernet}")
			result.insert(0, cursor.supernet)
			cursor = cursor.supernet
		result.insert(0, cursor.supernet)
		return result
	
	def subnet(self, masklen=None, index=0, subnetlen=None):
		if masklen is None:
			masklen = self.subnetlen
		netid = self.netid + ((1 << (32 - masklen)) * index)
		boundary = self.netid + (1 << (32 - self.masklen)) - 1
		debug(f"<prefix>.subnet: (masklen, netid, boundary): {masklen}, {netid}, {boundary}")
		if netid >= self.boundary or boundary > self.boundary:
			raise IndexError("The index of the subnet requested is beyond " + 
			                 "the bounds of this subnet's supernet")
		prefix = self.__class__(netid, masklen, supernet=self, boundary=boundary)
		if subnetlen is not None:
			prefix.subnetlen = subnetlen
		self._subnets[str(prefix)] = prefix
		return prefix
		
	def addr(self, index=0):
		return self.__class__(self.netid, supernet=self, boundary=boundary)
		
	def next(self):
		netid = self._netid + (1 << (32 - self._masklen))
		if netid >= self._boundary:
			raise IndexError("The next subnet is beyond the " + 
			                 "bounds of this subnet's supernet")
		prefix = self.__class__(netid, self._masklen, supernet = self._supernet)
		return Prefix
		
	def __str__(self):
		result = self.net + "/" + str(self.masklen)
		return result
		
	def __repr__(self):
		# TODO: FIXME
		return str(self)
		
	def __getitem__(self, indexOrPrefix: int or str or Prefix):
		""" look up an assigned subnet from this Prefix using prefix notation (str)
		    or subnet index (int) based on the subnetlen associated with this Prefix.
		    
		    indexOrPrefix: (str)   prefix notation key: 
		"""
		try:
			if isinstance(indexOrPrefix, slice):      # TODO: handle slices
				pass
			if isinstance(indexOrPrefix, int):        # int index based on subnetlen
				index = indexOrPrefix % len(self)
				debug("<prefix>.__getitem__: index: {index}")
				netid = self.netid + ((1 << (32 - self.subnetlen)) * index)
				prefix = "{netid}/{self.subnetlen}"
			elif isinstance(indexOrPrefix, str):      # string repr of Prefix
				prefix = indexOrPrefix
			else:
				raise IndexError()
			if prefix in self._subnets:
				return self._subnets[prefix]
		except IndexError as e:
			debug("<prefix>.__getitem__: index {index} does not exist, creating.")
		return self.subnet(index=index)
		
	def __setitem__(self, indexOrPrefix, prefixObject):
		# TODO: WRITE ME
		return NotImplemented
		
	def __delitem__(self, indexOrPrefix):
	    # TODO: WRITE ME
		return NotImplemented
		
	def __contains__(self, needle):
		selfbegins = self.netid
		selfends = self.next().netid - 1
		needlebegins = needle.netid
		needleends = needle.next().netid - 1
		return selfbegins <= needlebegins and selfends >= needleends
	
	def __int__(self):
		return self.netid
	
	def __add__(self, operand):
		netid = int(self) + (int(operand) % self.subnetlen)
		debug(f"<Prefix>.__add__: {int(self)} + ({int(operand)} % {self.subnetlen}) = {netid}")
		return __class__(netid, masklen=self.masklen, subnetlen=self.subnetlen, supernet=self)
		
	def __iadd__(self, operand):
		total = self.__add__(operand)
		self.netid = total.netid
		return self
	
	# subnetting functions
	def __truediv__(self, operand):
		shiftlen = int(math.log2(operand))
		masklen = min(self.masklen + shiftlen, 32)
		debug(f"<Prefix>.__truediv__: (self.masklen, shiftlen, masklen) = " +
		                              f"{self.masklen}, {shiftlen}, {masklen}")
		return self.subnet(self.netid, masklen)
		
	__floordiv__ = __truediv__
	
	def __floor__(self):
		""" return the lowest address in the prefix, aka the network address. 
		"""
		bshift = (32 - self.masklen)
		netid = (self.netid >> bshift) << bshift
		return self.__class__(netid, masklen=self.masklen, 
			subnetlen=self.subnetlen, supernet=self)
	
	def __ceil__(self):
		""" return the highest address in the prefix, aka the broadcast address. 
		"""
		bshift = (32 - self.masklen)
		netid = ((self.netid >> bshift) << bshift) + (1 << bshift) - 1
		return self.__class__(netid, masklen=self.masklen, 
			subnetlen=self.subnetlen, supernet=self)
		
	def __len__(self):
		masklendelta = (self.subnetlen - self.masklen)
		debug(f"<prefix>.__len__: {self.subnetlen} - {self.masklen} = {masklendelta}")
		return 1 << masklendelta
		
	def __index__(self):
		pass
		
	def __iter__(self):
		pass
		
	def __lt__(self, prefix):
		pass
		
	def __gt__(self, prefix):
		pass
		
	def __le__(self, prefix):
		pass
		
	def __ge__(self, prefix):
		pass
		
	def __eq__(self, prefix):
		pass
		
	def __ne__(self, prefix):
		pass
		
	def __init__(self, prefix, masklen=None, supernet=None, subnetlen=None, boundary=None):
		self._netid = None
		self._masklen = None
		self._boundary = (((2 ** 31) - 1) << 1) + 1
		self._subnetlen = 0
		self._subnets = {}
		if supernet is not None:
			self.supernet = supernet
			self.boundary = self.supernet.boundary
			self.subnetlen = self.supernet.subnetlen
			debug(f"<prefix>.__init__: <prefix>.(subnetlen, boundary) ->" +
					   f" {self.subnetlen}, {self.boundary}")
		if subnetlen is not None:
			self.subnetlen = subnetlen
			debug(f"<prefix>.__init__: <prefix>.subnetlen -> {self.subnetlen}")
		if boundary is not None:
			self.boundary = boundary
			debug(f"<prefix>.__init__: <prefix>.boundary -> {self.boundary}")
		if isinstance(prefix, str):
			try:
				prefix = prefix.split("/")
				debug(f"<prefix>.__init__: prefix: {prefix}, masklen: {masklen}")
				self.net = prefix[0]
				if len(prefix) == 1:
					self.masklen = masklen
				elif len(prefix) == 2:
					self.masklen = prefix[1]
			except:
				raise ValueError("mask must be an integer value between 0 and 32")	
		elif isinstance(prefix, int):
			self._netid = prefix
			self._masklen = masklen
		debug(f"<prefix>.__init__: returning instance <prefix {self} of <supernet>{self.supernet} >:")
		debug(f"                   " + 
				f"<netid>{self.netid}, " + 
				f"<net>{self.net}, <masklen>{self.masklen}, " + 
				f"<boundary>{self.toStr(self.boundary)}")


# Root Prefix (All IPV4 Addressing)
Prefix.IPV4 = Prefix(0, masklen=0, supernet=Prefix.IPV4)
Prefix._supernet = Prefix.IPV4

