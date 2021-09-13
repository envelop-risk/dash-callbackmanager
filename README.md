# dash-callbackmanager

As your dash application grows the management of callbacks becomes a bit of an overhead. The 
callback manager allows you to bundle collections of dash callbacks together allowing you to easily keep your
`app.py` clean.

## Installation:
```shell
pip install dash-callbackmanager
```

## Usage:
The callback manager allows you to easily slip out the callbacks into separate files.

```python
# callbacks.py

from dash_callbackmanager import CallbackManager

manager = CallbackManager()

@manger.callback()
def my_callback(Output("element", "children"), Input("other-element", "value")):
    ...
```

```python 
# app.py
from dash import Dash
from .callbacks import manager

app = Dash(__name__)

manager.register(app)
```