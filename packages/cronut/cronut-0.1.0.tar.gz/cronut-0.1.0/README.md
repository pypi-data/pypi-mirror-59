Cronut
======

**cronut** is a barebones event processing library using Kafka.

## Quickstart

```python
from collections import deque
import json

from cronut import App

d = deque(maxlen=30)

app = App('myapp', broker='kafka://localhost:9096')

@app.process('topic1')
def stateless(message):
    event = json.loads(message.value())
    print(event)

@app.process('topic2', state=d)
def stateful(message, state):
    event = json.loads(message.value())
    state.appendleft(event)

@app.timer(interval=0.1, state=d)
def retrieve(state):
    event = state.pop()
    print(event)

@app.timer(interval=0.1)
def greet():
    print('howdy')

app.start()
```
