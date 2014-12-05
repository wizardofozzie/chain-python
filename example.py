from chain import Chain
chainClient = Chain(keyID='5587496846848', 
                    keySecret='09sdgo8990g0gdsas9d98d8a8h',
                    blockChain='bitcoin')

# Returns basic balance details for one or more Bitcoin addresses.
print chainClient.addressBalance(["17x23dNjXJLzGMev6R63uyRhMWP1VHawKc","1CPttygvogBm8gNN11rpT4AngV5sgd5j6e","  1ELs7wvcPQsbdYoLWiixX9fxvRmwYX9H8b"])

# Returns a set of transactions for one or more Bitcoin addresses.
print chainClient.addressTransactions(["17x23dNjXJLzGMev6R63uyRhMWP1VHawKc","1CPttygvogBm8gNN11rpT4AngV5sgd5j6e","  1ELs7wvcPQsbdYoLWiixX9fxvRmwYX9H8b"],limit=1)

# Returns a collection of unspent outputs for a Bitcoin address. These outputs can be used as inputs for a new transaction.
print chainClient.addressUnspents(["17x23dNjXJLzGMev6R63uyRhMWP1VHawKc","1CPttygvogBm8gNN11rpT4AngV5sgd5j6e","  1ELs7wvcPQsbdYoLWiixX9fxvRmwYX9H8b"])

# Returns any OP_RETURN values sent and received by a Bitcoin Address.
print chainClient.addressOP_RETURNs("1Bj5UVzWQ84iBCUiy5eQ1NEfWfJ4a3yKG1")

# Returns details about a Bitcoin transaction, including inputs and outputs.
print chainClient.transaction("0f40015ddbb8a05e26bbacfb70b6074daa1990b813ba9bc70b7ac5b0b6ee2c45")

# Returns the OP_RETURN value and associated addresses for any transaction containing an OP_RETURN script.
print chainClient.transactionOP_RETURN("4a7d62a4a5cc912605c46c6a6ef6c4af451255a453e6cbf2b1022766c331f803")

# Returns details about a Bitcoin block, including all transaction hashes.
print chainClient.block(hash="00000000000000009cc33fe219537756a68ee5433d593034b6dc200b34aa35fa")
print chainClient.block(height=0) # based on the block height
print chainClient.block() # The latest block

# Returns the OP_RETURN value and associated addresses for all transactions in the block which contain an OP_RETURN output script.
print chainClient.blockOP_RETURNs(hash="0000000000000000179c39d35c090b7da042ded43ad49b911843fb418a983de1")
print chainClient.blockOP_RETURNs(height=308920)