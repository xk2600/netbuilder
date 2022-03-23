
class BaseModel:
	@classmethod
	def keys(cls):
		return [ x for x in cls.__dict__.keys() if x[0] != '_' and x not in dir(dict)]
	
	@classmethod
	def items(cls):
		return { k: v for (k,v) in cls.__dict__.items()
			if k[0] != '_' 
			or k not in dir(dict) 
			or k not in cls.__methods__ }
	
	def __init__(self, **kwargs):
		for arg, val in kwargs.items():
			if arg in [arg for arg in self.__class__.__dict__.keys() if arg[0] != "_" ]:
				setattr(self, arg, val)
