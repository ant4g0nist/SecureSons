# SecureSon
Modules for developing `Secure` Smart contract for Tezos in SmartPy

## Overview

Currently available contracts
- [x] Ownable
- [x] AccessControl
- [x] Pausable

# Usage:

All the contracts in `contracts` folder contain the implementation and a sample usage of that contract.
They are all standalone. Just copy the interesting file or clone the repo and use the contracts. 

The contracts directly inherit from `sp.contract`. To develop a contract that uses `AccessControl`, just inherit the class.

Example:
```
class Gateway(AccessControl):
    def __init__(self, administrator):
        AccessControl.__init__(self, administrator)
```

# TODO
- Add Secure FA token implementation
- Add Secure Factory implementation
- Add Secure DAO implementation