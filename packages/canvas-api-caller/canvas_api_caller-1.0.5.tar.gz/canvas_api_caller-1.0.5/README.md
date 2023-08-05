# Canvas API Caller
Canvas API Caller is a small library that utilizes the Instructure Canvas API GET requests.

# Installation Guide
1. execute `pip install canvas-api-caller` or add `canvas-api-caller` to your `requirements.txt` file.
2. Add an environment variable named `CANVAS_BASE_URL` with the url of the full canvas API, such as `https://mycompany.test.instructure.com/api/v1/`.

# Code Examples
## General Example
The below code shows the general use of this library.
`BEARER_ACCESS_TOKEN` is the access token expected by Canvas to authenticate and identify yourself to their API.
`CANVAS_ENDPOINT` is used to call the endpoint you want to use.
`PARAM_OBJECT_OF_KEY_VALUES` are used to pass parameters through to the Canvas API, as some endpoints require additional parameters such as `student_id`.
```python
import canvas_api_caller as canvas

def main():
    return canvas.call('{BEARER_ACCESS_TOKEN}', '{CANVAS_ENDPOINT}', '{PARAM_OBJECT_OF_KEY_VALUES}')
```

## HTTP wrapper with Flask
The below code decides the canvas_api_caller call parameters through HTTP values.

A custom HTTP header called `X-Canvas-Authorization` is used in the example below to pass the `BEARER_ACCESS_TOKEN` of Canvas.
A Query Parameter called `endpoint` is used to access the `CANVAS_ENDPOINT` of canvas. 
All other Query Parameters passed through will be used for the `PARAM_OBJECT_OF_KEY_VALUES`.

Required packages:
- Flask
- Werkzeug

```python
import canvas_api_caller as canvas
from flask import Flask, jsonify, request, json
from werkzeug.datastructures import MultiDict

app = Flask(__name__)

@app.route('/canvas_api', methods=['GET'])
def canvas_api():
    return canvas.http(request)
```

### CORS Origin
When required to adjust your headers for purposes such as CORS, you can additionally add your custom headers.
When working with custom headers, make sure to have `Access-Control-Allow-Headers` specifiek and atleast `X-Canvas-Authorization` allowed.

```python
import canvas_api_caller as canvas
from flask import Flask, jsonify, request, json
from werkzeug.datastructures import MultiDict

app = Flask(__name__)

@app.route('/canvas_api', methods=['GET'])
def canvas_api():
    # Allows GET requests from any origin with the Content-Type
    # header and caches preflight response for an 3600s
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': '*',
        'Access-Control-Allow-Headers': 'X-Canvas-Authorization'
    }

    return canvas.http(request, headers)
```