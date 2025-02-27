"""Initialize the properties module."""

from pyconfs import Configuration

from properties import file

settings = Configuration.from_file(
    file.find(filename="pyproject.toml"), file_format="toml"
)
config = Configuration.from_file(
    file.find(filename="configuration.toml"), file_format="toml"
)
