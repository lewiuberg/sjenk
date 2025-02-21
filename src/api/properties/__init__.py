"""Initialize the utils module."""

from pyconfs import Configuration

from properties import file

# .env file type is not supported in pyconfs. But, it can be read using toml.
secrets = Configuration.from_file(
    file.find(filename=".env"), file_format="toml"
)
settings = Configuration.from_file(
    file.find(filename="pyproject.toml"), file_format="toml"
)
config = Configuration.from_file(
    file.find(filename="configuration.toml"), file_format="toml"
)
