import smartpy as sp

class Ownable(sp.Contract):
	def __init__(self, owner: sp.TAddress) -> None:
		self.init(owner=owner)

	def _onlyOwner(self):
		sp.verify(self.data.owner == sp.sender, "Ownable: caller is not the owner")

	def _setOwner(self, address: sp.TAddress):
		"""
				Set a new owner!
		"""
		self._onlyOwner()
		self.data.owner = address

	def _renounceOwnership(self):
		"""
				Current owner can renounce his ownership!
				WARNING - cannot undo this
		"""
		self._setOwner(sp.address("tz1Ke2h7sDdakHJQh8WX4Z372du1KChsksyU"))

# Sample Usage
class SampleOwnableContract(Ownable):
	def __init__(self, owner) -> None:
		Ownable.__init__(self, owner)
		self.update_initial_storage(value="yo!")

	@sp.entry_point
	def hello(self, params):
		sp.set_type(params, sp.TString)
		self._onlyOwner()
		self.data.value = params

	@sp.entry_point
	def renounceOnwership(self):
		self._renounceOwnership()

sp.add_compilation_target("SampleOwnableContract", SampleOwnableContract(
	owner=sp.address("tz1Rn1TTJo3RwLfDN2XyjQgQ2nf8hcdvqrsy")
))
