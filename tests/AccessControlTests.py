import smartpy  as sp

contract = sp.io.import_script_from_url("file:contracts/AccessControl.py")

admin 	    = sp.address('tz1a9GCc4UU6d5Z9spyozgKTARngb8DZKbNe')
randomUser = sp.address('tz1LxAgLZWt4xxdya3yPA8wW4zcMbD5hTkvk')

@sp.add_test(name = "First Test")
def test():
	role = 'admin'

	scenario = sp.test_scenario()
	adminRole = sp.keccak(sp.pack(role))

	c1 = contract.SampleAccessControlContract(admin)

	scenario += c1
	
	# only admin can addRole
	scenario += c1.addRole(admin=admin, role=adminRole).run(sender=admin)

	# only admin can addRole
	scenario += c1.addRole(admin=admin, role=adminRole).run(sender=randomUser, valid=False)

	# can only addRole once per role
	scenario += c1.addRole(admin=admin, role=adminRole).run(sender=admin, valid=False)

	# should fail if randomUser is able to call hello
	scenario += c1.hello("hello").run(sender=randomUser, valid=False)

	# admin should be able to call hello
	scenario += c1.hello("hello").run(sender=admin)
	scenario.verify(c1.data.value == 'hello')

	# should fail if randomUser is not able to call grantRole to himself 
	scenario += c1.grantRole(address = randomUser, role=adminRole).run(sender = randomUser, valid=False)

	# admin can grant able to call hello
	scenario += c1.grantRole(address = randomUser, role=adminRole).run(sender = admin, valid=True)

	# randomUser shoud be able to call hello now!
	scenario += c1.hello("Milkybar").run(sender=randomUser, valid=True)
	scenario.verify(c1.data.value == 'Milkybar')

	# admin can revoke role of a user
	scenario += c1.revokeRole(address = randomUser, role=adminRole).run(sender = admin, valid=True)

	# randomUser shoud now not be able to call hello
	scenario += c1.hello("Hershey").run(sender=randomUser, valid=False)
	scenario.verify(c1.data.value != 'Hershey')	

	# admin can grant able to call hello
	scenario += c1.grantRole(address = randomUser, role=adminRole).run(sender = admin, valid=True)
