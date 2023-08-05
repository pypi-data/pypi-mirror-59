#Jarvis 

**Status**
[![Build status](https://dev.azure.com/cubbei/JarvisCore/_apis/build/status/JarvisCore-PiP%20Publish)](https://dev.azure.com/cubbei/JarvisCore/_build/latest?definitionId=1)


This is the repository for Jarvis, the twitch bot.

##Getting Started

The simplest way to get started is to create a new file, with the basic code below:

```python
from jarviscore.client import Client

jarvis = Client(nick="yourbotsname", 
    token="yourbotstoken",
    channels=['a list', 'of channels', 'to connect to'])
jarvis.start()
```