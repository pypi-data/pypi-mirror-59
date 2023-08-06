# GUID-core
Tool to generate GUID using sha256

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install GUID-core.

```bash
pip install guid_core
```

## Usage

```python
import guid_core

guid_core.generate_GUID(string) # returns guid



firstname=string
lastname=string
dateOfBirth=string 
gender=string

guid_core.generate_GUID2(firstname,lastname,dateOfBirth,gender) # returns guid

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
