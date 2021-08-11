import smartpy  as sp

contract = sp.io.import_script_from_url("file:contracts/Pausable.py")

user1 = sp.address("tz1Rn1TTJo3RwLfDN2XyjQgQ2nf8hcdvqrsy")	# admin
user2 = sp.address('tz1LxAgLZWt4xxdya3yPA8wW4zcMbD5hTkvk')

@sp.add_test(name = "Ownable tests")
def test():
	owner = user1
	scenario = sp.test_scenario()
	c1 = contract.SamplePausableContract(owner = owner)
	
	scenario += c1
	
	# user should be able to call the function when not paused
	scenario += c1.hello("hello").run()
	scenario.verify(c1.data.value == 'hello')

	# random user should not be able to pause the contract
	scenario += c1.pause().run(sender=user2, valid=False)

	# owner should be able to pause the contract
	scenario += c1.pause().run(sender=owner, valid=True)
	
	# owner should be not able to call the function when paused
	scenario += c1.hello("yolo").run(sender=owner, valid=False)
	scenario.verify(c1.data.value != 'yolo')

	# user should be not able to call the function when paused
	scenario += c1.hello("yolo").run(sender=user2, valid=False)
	scenario.verify(c1.data.value != 'yolo')

	# user should not be able to unpause the contract
	scenario += c1.unpause().run(sender=user2, valid=False)

	# owner should be able to unpause the contract
	scenario += c1.unpause().run(sender=owner, valid=True)
	
	scenario += c1.hello("yolo").run(sender=user2, valid=True)
	scenario.verify(c1.data.value == 'yolo')