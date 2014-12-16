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

# Transaction building, signing, and sending:

template = {'inputs':[{'address':"muZpTpBYhxmRFuCjLc7C6BBDF32C8XVJUi"}], 
            'outputs':[{'address':'mmNokPYu68QMpomzEAweFDbuVSGHZDoo7X','amount':12345},
                       {'address':'n2C2NkYDp2XS94eiuEdnmMxxMhW8LDNZHy','amount':678910}],
            #'change_address':'n41hcnYquATYFGrAx2QvSaF9D8SLhbUX6f',
            #'miner_fee_rate':55777, 
            'min_confirmations':0
            }

template = chainClient.build(template)
print "Built template:\n" + str(template)

# The template is now built. We can sign it:

#privateKeys = ['92FmWh2A6moe8RgNdqDeFjVaSrVBVxiQLQMaVKKimcZr8vRyQ14'] # corresponding address: mxurpXudoLffLYASFSNffb4CYBQbypa69d
privateKeys = ['cVDJUtDjdaM25yNVVDLLX3hcHUfth4c7tY3rSc4hy9e8ibtCuj6G'] # corresponding address: muZpTpBYhxmRFuCjLc7C6BBDF32C8XVJUi - This is a compressed pubkey address.
template = chainClient.sign(template,privateKeys)
print "Template after signing:\n" + str(template)

# Send the signed template:
print chainClient.send(template)
# All done!

# If you want to send your own raw transaction, you can do that too:
raw = "0100000001f5fe76d1ac4cea2c6aa84b09cb03a1285cbffef788d7a18893dbe4873cecc5a1000000008b483045022100ad4b975ccf6081574d8e1119dd6e4efc19c9f9af292d0b8613aa782fe4a4e53802207a67c701685d5f94e180a03141c4069d7fb371df8f2516cf6cb4e44484aa4c60014104211ff0847051e57139d60a4bdc0ff6d8dfaed4dce4c4927eec69b6f583b99a007c0987fa7ec11af9a33c7ce1e70f30a36b6235c4071e4b993223afa76786898effffffff0230517d01000000001976a914bc65f5d30afd0299f769f87737d99e5c3973938a88ac40787d01000000001976a91462032ad95797e5f7dc0fba7321dcffce787da3a488ac00000000"
print chainClient.send(raw) 

# We can do the building, signing, and sending all in one step:

template = {'inputs':[
                      {
                       'address':"muZpTpBYhxmRFuCjLc7C6BBDF32C8XVJUi",
                      'private_key':"cVDJUtDjdaM25yNVVDLLX3hcHUfth4c7tY3rSc4hy9e8ibtCuj6G"
                      },
                      {
                       'address':"mxurpXudoLffLYASFSNffb4CYBQbypa69d",
                      'private_key':"92FmWh2A6moe8RgNdqDeFjVaSrVBVxiQLQMaVKKimcZr8vRyQ14"
                      }
                     ], 
            'outputs':[
                       {'address':'mmNokPYu68QMpomzEAweFDbuVSGHZDoo7X','amount':12345},
                       {'address':'n2C2NkYDp2XS94eiuEdnmMxxMhW8LDNZHy','amount':89987}
                      ],
            #'change_address':'n41hcnYquATYFGrAx2QvSaF9D8SLhbUX6f',
            #'miner_fee_rate':55777,
            'min_confirmations':0
            }
print chainClient.transact(template)
