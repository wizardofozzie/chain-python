## chain-python

Chain's official Python SDK.

## Quick Start
```bash
pip install chain-sdk
```

```python
from chain import Chain
chainClient = Chain(keyID='5587496846848', 
                    keySecret='09sdgo8990g0gdsas9d98d8a8h',
                    blockChain='bitcoin')

print chainClient.addressBalance("17x23dNjXJLzGMev6R63uyRhMWP1VHawKc")
```

See many more examples [here](https://github.com/chain-engineering/chain-python/blob/master/bin/example.py).

## Documentation

The Chain API Documentation is available at [https://chain.com/docs/python](https://chain.com/docs/python)
