# flespi-Python

flespi-python is a flespi Rest API Wrapper for python language.

# Installation
Use the package manager pip to install flespi-python.
Install the dependencies and devDependencies and start the server.

```sh
$ pip3 install flespi
```

### Usage
```python
from flespi.rest import FlespiClient

token = 'your_token' # Without "FlespiToken"
is_development = True
# Initialize Flespi instance
flespi = FlespiClient(token=token, is_development=is_development)

response = flespi.get('gw/devices/all')

print(response)
```
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

