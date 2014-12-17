import json

from bitcoin.core.key import CECKey

from shared import request, generateKeyCollection, convertPrivateKeysToBinaryFormat, convertPrivateKeyToBinaryFormat, deriveAddress
from chain import APIVersion


class Chain:
    def __init__(self, keyID="", keySecret="", blockChain="bitcoin"):
        self.keyID = keyID.strip()
        self.keySecret = keySecret.strip()
        self.blockChain = blockChain.strip()
        
    def parseAddresses(self,addresses):
        listOfAddresses = ""
        if isinstance(addresses,list):
            if len(addresses) == 0:
                raise Exception("This function requires either a list of addresses or a single address by itself")
            for address in addresses:
                listOfAddresses += address.strip() + ","
            # Take off the trailing comma
            return listOfAddresses[:-1]
        elif isinstance(addresses,str):
            # The user just passed in a single address by itself not in a 
            # list (as opposed to a single address in a list). We might as well
            # handle this properly.
            return addresses.strip()
        else:
            raise Exception("This function requires either a list of addresses or a single address by itself. So you should give it either a string or a list of strings.")
    
    # The Chain API doesn't accept lists of TX or block hashes right now.
    """
    def parseHashes(self,hashes):
        listOfHashes = ""
        if isinstance(hashes,list):
            if len(hashes) == 0:
                raise Exception("This function requires either a list of hashes or a single hash by itself")
            for hash in hashes:
                listOfHashes += hash.strip() + ","
            # Take off the trailing comma
            return listOfHashes[:-1]
        elif isinstance(hashes,str):
            # The user just passed in a single hash by itself not in a 
            # list (as opposed to a single hash in a list). We might as well
            # handle this properly.
            return hashes.strip()
        else:
            raise Exception("This function requires either a list of hashes or a single hash by itself. So you should give it either a string or a list of strings.")
    """
      
    def addressBalance(self, addresses):
        listOfAddresses = self.parseAddresses(addresses)
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/addresses/" + listOfAddresses
        print URI
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def addressTransactions(self,addresses,limit=50):
        listOfAddresses = self.parseAddresses(addresses)
        assert isinstance(limit,int)
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/addresses/" + listOfAddresses + "/transactions?limit=" + str(limit)
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def addressUnspents(self,addresses):
        listOfAddresses = self.parseAddresses(addresses)
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/addresses/" + listOfAddresses + "/unspents"
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def addressOP_RETURNs(self,addresses):
        listOfAddresses = self.parseAddresses(addresses)
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/addresses/" + listOfAddresses + "/op-returns"
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def transaction(self,hash):
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/transactions/" + hash
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def transactionOP_RETURN(self,hash):
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/transactions/" + hash + "/op-return"
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def block(self,hash=None,height=-1):
        if hash:
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/" + hash
        elif height>=0:
            assert isinstance(height,int)
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/" + str(height)
        else:
            # The user specified neither a hash or a height. Let's give them the latest block.
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/latest"
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def blockOP_RETURNs(self,hash=None,height=-1):
        if hash:
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/" + hash + "/op-returns"
        elif height>=0:
            assert isinstance(height,int)
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/" + str(height) + "/op-returns"
        else:
            # The user specified neither a hash or a height. Let's give them the latest block.
            URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/blocks/latest/op-returns"
        returnedData = request(URI)
        return json.loads(returnedData)
    
    def build(self,template):
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/transactions/build"
        templateString = json.dumps(template)
        returnedData = request(URI, data=templateString, operation='POST')
        return json.loads(returnedData)
    
    def sign(self,template, privateKeys):
        
        # convert all of the privateKeys to a standard binary format for us to work with
        privateKeysBinary = convertPrivateKeysToBinaryFormat(privateKeys, self.blockChain)
        
        """
        keyCollection is a dictionary where the key of the dict is an address and the value is a 
        tuple with (privKey, compressed)
            where `privKey` is the private key in binary format
            and `compressed` is a bool indicating whether or not the corresponding public key is compressed.
        """
        keyCollection = generateKeyCollection(privateKeysBinary, self.blockChain) 
        
        if not 'inputs' in template:
            raise Exception("This template has no inputs. There is nothing to sign.")
        
        for inputIndex in range(len(template['inputs'])): # For each input in the template...
            for signatureIndex in range(len(template['inputs'][inputIndex]['signatures'])): # For each signature in the input...
                address = template['inputs'][inputIndex]['signatures'][signatureIndex]['address'] # Get the address out of the template to make this code easier to read
                if address in keyCollection: # if we have the private key needed for this signature..
                    privateKeyBinary, compressed = keyCollection[address]
                    privKey = CECKey() # This CECKey object type is from the python-bitcoinlib library
                    privKey.set_secretbytes(privateKeyBinary)
                    privKey.set_compressed(compressed)
                    hash_to_sign = template['inputs'][inputIndex]['signatures'][signatureIndex]['hash_to_sign']
                    signature = privKey.sign(hash_to_sign.decode('hex'))
                    
                    # We now have the signature. Let's put the signature and the pubkey into the template.
                    template['inputs'][inputIndex]['signatures'][signatureIndex]['signature'] = signature.encode('hex')
                    template['inputs'][inputIndex]['signatures'][signatureIndex]['public_key'] = privKey.get_pubkey().encode('hex')
        return template
    
    def send(self,data):
        if type(data) == str:
            data = {'signed_hex': data}
        URI = "https://" + self.keyID + ":" + self.keySecret + "@api.chain.com/" + APIVersion + "/" + self.blockChain + "/transactions/send"
        templateString = json.dumps(data)
        returnedData = request(URI, data=templateString, operation='POST')
        return json.loads(returnedData)
    
    def transact(self,template):
        privateKeys = []
        for inputIndex in range(len(template['inputs'])): # For each input in the template...
            # copy the address and private_key out of the template to make this code easier to read.
            address = template['inputs'][inputIndex]['address']
            private_key = template['inputs'][inputIndex]['private_key']
            privateKeyBinary, compressed = convertPrivateKeyToBinaryFormat(private_key, self.blockChain)
            derivedAddress = deriveAddress(privateKeyBinary, compressed, self.blockChain)
            if address != derivedAddress:
                raise Exception("The address (%s) derived from the private_key in this input doesn't match the address that you gave (%s)." % (derivedAddress, address))
            privateKeys.append(private_key)
            del template['inputs'][inputIndex]['private_key'] # remove the private key from the template
        
        # At this point we have the privateKeys stored in the privateKeys list and 
        # we know that they correspond correctly to the addresses in the template
        builtTemplate = self.build(template)
        if 'code' in builtTemplate:
            # something went wrong
            return builtTemplate
        signedTemplate = self.sign(builtTemplate, privateKeys)
        return self.send(signedTemplate)
            
    