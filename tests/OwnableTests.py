import smartpy  as sp

contract = sp.io.import_script_from_url("file:contracts/Ownable.py")

user1 = sp.address("tz1Rn1TTJo3RwLfDN2XyjQgQ2nf8hcdvqrsy")	# me
user2 = sp.address('tz1LxAgLZWt4xxdya3yPA8wW4zcMbD5hTkvk')

@sp.add_test(name = "Ownable tests")
def test():
	scenario = sp.test_scenario()
	c1 = contract.SampleOwnableContract(owner = user1)

	scenario += c1
	# random user should not be able to call onlyOwner function hello
	scenario += c1.hello("hello").run(sender=user2, valid=False)

	# owner user should be able to call onlyOwner function hello
	scenario += c1.hello("hello").run(sender=user1, valid=True)