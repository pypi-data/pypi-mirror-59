# PSocket
The cross-platform simple tool to work with remote server through sockets.

## Installation
For most users, the recommended method to install is via pip:
```cmd
pip install psocket
```

or from source:

```cmd
python setup.py install
```

## Import
```python
from psocket import SocketClient
```
---
## Usage
```python
from psocket import SocketClient

client = SocketClient(host='172.16.0.48', port=3261)
print(client.greeting())
```

---

## Changelog
##### 1.0.0a0 (13.01.2020)
- initial commit
