import smartpy as sp

def msgSender():
	return sp.sender

class ErrorMessages:
	missingRole = "The role you are trying does not exist!"
	noPermissionForAccount = "Account does not have required role!"
	onlyAdmins = "Only Administrator can call this method"
	duplicateRole = "Role already added!"
	onlyAdminRole = "Only admin of this Role is allowed to perform this action"

class AccessControl(sp.Contract):
	"""
			AccessControl:
	"""

	def __init__(self, administrator) -> None:

		self.init(administrator=administrator, roles=sp.big_map(
			tkey=sp.TBytes,
			tvalue=sp.TRecord(admin=sp.TAddress, members=sp.TMap(
				k=sp.TAddress, v=sp.TNat))
		))

	def _hasRole(self, role: sp.TBytes, address: sp.TAddress):
		"""
		Checks if an account has a specific role. FAILWITH with a standardized message including the required role.
		"""
		sp.verify(self.data.roles.contains(role) == True,
				  message=ErrorMessages.missingRole)
		sp.verify(self.data.roles[role].members.get(
			address, default_value=1) > 1, message=ErrorMessages.noPermissionForAccount)

		return True

	def _onlyRole(self, role: sp.TBytes):
		"""
		Checks that the sender has a specific role. FAILWITH with a standardized message including the required role.
		"""
		self._hasRole(role, msgSender())

	def _onlyAdminRole(self, role: sp.TBytes):
		"""
		Checks that only Admin users can call
		"""
		sp.verify(self.data.roles.contains(role) == True,
				  message=ErrorMessages.missingRole)
		sp.verify(self.data.roles[role].admin == msgSender(
		), message=ErrorMessages.onlyAdminRole)

	def _onlyAdministrator(self):
		"""
		Checks that only the contract Administrator can call
		"""
		sp.verify(self.data.administrator ==
				  sp.sender, ErrorMessages.onlyAdmins)

	def _addRole(self, role: sp.TBytes, admin: sp.TAddress):
		"""
		Adds a new role. FAILWITH with a standardized message if the sender is not `administrator` of the contract!
		"""
		self._onlyAdministrator()
		sp.verify(~ self.data.roles.contains(role),
				  message=ErrorMessages.duplicateRole)
		self.data.roles[role] = sp.record(
			admin=admin, members=sp.map(l={admin: 2}))

	def _grantAdminRole(self, role: sp.TBytes, address: sp.TAddress):
		"""
		Set or modify Admin user of a Role
		"""
		self._onlyAdministrator(role)
		sp.verify(self.data.roles.contains(role) == True,
				  message=ErrorMessages.missingRole)
		self.data.roles[role].admin = address

	def _grantRole(self, role: sp.TBytes, address: sp.TAddress):
		"""
		Grants a given role to an account. Only Admins of a role can call this method
		"""
		self._onlyAdminRole(role)

		sp.verify(self.data.roles.contains(role) == True,
				  message=ErrorMessages.missingRole)
		self.data.roles[role].members[address] = 2

	def _revokeRole(self, role: sp.TBytes, address: sp.TAddress):
		"""
		Revokes given role of an account. Only Admins of a role can call this method
		"""
		self._onlyAdminRole(role)
		self._hasRole(role, address)

		del self.data.roles[role].members[address]

	def _renounceRole(self, role: sp.TBytes):
		"""
		Revokes given role of the sender.
		"""
		self._onlyRole(role)
		del self.data.roles[role].members[msgSender()]

# Example Usage
class SampleAccessControlContract(AccessControl):
	role = 'admin'
	admin = sp.keccak(sp.pack(role))

	def __init__(self, administrator) -> None:
		AccessControl.__init__(self, administrator)
		self.update_initial_storage(value='ok')

	@sp.entry_point
	def hello(self, value):
		self._onlyRole(self.admin)
		self.data.value = value

	@sp.entry_point
	def addRole(self, params):
		sp.set_type(params.role, sp.TBytes)
		sp.set_type(params.admin, sp.TAddress)

		self._addRole(params.role, params.admin)

	@sp.entry_point
	def grantRole(self, params):
		sp.set_type(params.address, sp.TAddress)
		sp.set_type(params.role, sp.TBytes)
		self._grantRole(params.role, params.address)

	@sp.entry_point
	def revokeRole(self, params):
		sp.set_type(params.address, sp.TAddress)
		sp.set_type(params.role, sp.TBytes)
		self._revokeRole(params.role, params.address)

adminUser = sp.address('tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe')
adminRole = sp.keccak(sp.pack('admin'))

sp.add_compilation_target(
	"SampleAccessControlContract",
	SampleAccessControlContract(
		adminUser)
)
