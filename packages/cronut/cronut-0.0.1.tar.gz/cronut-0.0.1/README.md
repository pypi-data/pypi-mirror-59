Cronut
======

**cronut** is a barebones event processing library using Kafka.

## Quickstart

```python
from collections import deque
import json

from cronut import App

app = App('myapp', broker='localhost:9096')

@app.stateless('topic1')
def process(message):
	event = json.loads(message.value())
	print(message)

@app.stateful('topic2', state=deque(maxlen=10))
def process(message, state):
	event = json.loads(message.value())
	state.appendleft(event)
	new_event = state.pop()
	print(new_event)

app.start()
```
