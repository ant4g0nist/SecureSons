import smartpy as sp

ownable = sp.io.import_script_from_url("file:contracts/Ownable.py")

class Pausable(ownable.Ownable):
	def __init__(self, owner: sp.TAddress) -> None:
		super().__init__(owner)
		self.update_initial_storage(paused=False)

	def is_paused(self):
		"""
		Returns true if the contract is paused, and false otherwise.
		"""
		return self.data.paused

	def _pause(self):
		"""
		The contract will be paused. Only the owner can pause
		"""
		self._onlyOwner()
		self.whenNotPaused()
		self.data.paused = True

	def _unpause(self):
		"""
		The contract will be unpaused. Only the owner can unpause
		"""
		self._onlyOwner()
		self.whenPaused()
		self.data.paused = False

	def whenPaused(self):
		"""
		This method can be used to allow functions to be callable only when the contract is paused.
		"""
		sp.verify(self.is_paused() == True,
				  "Pausable: contract is not in paused state")

	def whenNotPaused(self):
		"""
		This method can be used to allow functions to be callable only when the contract is unpaused.
		"""
		sp.verify(self.is_paused() == False,
				  "Pausable: contract is in paused state")

class SamplePausableContract(Pausable):
	def __init__(self, owner: sp.TAddress) -> None:
		super().__init__(owner)
		self.update_initial_storage(value="yo!")

	@sp.entry_point
	def hello(self, value):
		self.whenNotPaused()
		self.data.value = value

	@sp.entry_point
	def pause(self):
		self._pause()

	@sp.entry_point
	def unpause(self):
		self._unpause()


adminUser = sp.address('tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe')

sp.add_compilation_target(
	"SamplePausableContract",
	SamplePausableContract(
		adminUser)
)
