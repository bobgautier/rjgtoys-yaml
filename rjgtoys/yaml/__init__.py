# The URL in the below is too long.
# pylint: disable=line-too-long

"""

Functions
---------

.. autofunction:: yaml_load
.. autofunction:: yaml_load_path
.. autofunction:: yaml_dump


Exceptions
----------

.. autoexception:: YamlCantLoad

The ``!include`` tag
--------------------

This is the one significant YAML 'extension' implemented in this module.

An ``!include`` tag can appear in YAML input anywhere any other kind of value
can appear.

The tag is replaced by the result of reading the file or directory specified
as the ``path``; :func:`yaml_load_path` is used to do the loading.

When an included file `F` contains its own ``!include`` tag, the path is
evaluated relative to the location of `F`.

Example:

YAML file ``/home/frodo/one-ring.yml``::

    ---
    Name: The One Ring
    Specials:
        - resize-to-wearer
    Effects:
        - !include path/to/invisibility.yml

YAML file ``/home/frodo/path/to/invisibility.yml``::

    ---
    Name: invisibility
    Message: Suddenly you disappear!

Loading::

    data = yaml_load_path('/home/frodo/one-ring.yml')

Result::

    {
      'Effects': [
          {
               'Message': 'Suddenly you disappear!',
               'Name': 'invisibility'
         }
       ],
       'Name': 'The One Ring',
       'Specials': [
           'resize-to-wearer'
       ]
    }

Internals
---------


.. autoclass:: IncludeLoader
.. autofunction:: _thing_to_yaml


"""

import io
import os
import stat
import sys

import ruamel.yaml as yaml

from rjgtoys.xc import Error, Title, raises
from rjgtoys.thing import Thing


class YamlCantLoad(Error):
    """Raised on an attempt to load YAML from something that is neither a file nor a directory."""

    path: str = Title("The path that couldn't be read")

    detail = "Can't read YAML from non-file, non-directory '{path}'"


# I don't think I can do anything about these, so turn them off:
# pylint: disable=abstract-method
# pylint: disable=too-many-ancestors

class IncludeLoader(yaml.Loader):
    """
    This :class:`ruamel.yaml.Loader` subclass handles "!include path/to/foo.yml" directives
    in YAML files.

    The implementation is based on suggestions at:

    - https://stackoverflow.com/questions/528281/how-can-i-include-a-yaml-file-inside-another
    - https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts

    """

    DEFAULT_INCLUDE_TAG = "!include"

    DEFAULT_MAPPING_TYPE = Thing

    def __init__(self, *args, root=None, mapping_type=None, **kwargs):
        """
        The `root` parameter sets the base directory from which relative file
        paths are evaluated.

        The `mapping_type` parameter specifies the type of object that is
        constructed for mappings, and should be a callable similar to `dict`.
        The default is :class:`rjgtoys.thing.Thing`.

        If the root directory is not specified explicitly, and a file object is passed
        to the :class:`IncludeLoader` constructor, the root path for includes
        defaults to the directory containing the file.  If the file
        object has no associated directory (e.g. if an :class:`io.StringIO` was passed),
        then the current working directory is used as the root directory.
        """
        # NB I included the above as the docstring here, in order to override
        # a docstring from an inherited class, that would otherwise be included
        # in the documentation, but is not helpful.

        super(IncludeLoader, self).__init__(*args, **kwargs)

        self.add_constructor(self.DEFAULT_INCLUDE_TAG, self._include)

        self.add_constructor(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            self._construct_mapping
        )

        self.root = os.path.curdir
        if root is not None:
            self.root = root
        else:
            try:
                self.root = os.path.dirname(self.stream.name)
            except AttributeError:
                pass

        self._mapping_type = mapping_type or self.DEFAULT_MAPPING_TYPE

    def _construct_mapping(self, loader, node):
        """Construct a mapping instance by making a :class:`Thing`."""

        loader.flatten_mapping(node)
        return self._mapping_type(loader.construct_pairs(node))

    def _include(self, loader, node):
        """Include a file and return its content."""

        old_root = self.root
        try:
            filename = os.path.join(self.root, loader.construct_scalar(node))
            self.root = os.path.dirname(filename)
            data = yaml_load_path(filename)
        finally:
            self.root = old_root
        return data


def yaml_load(stream):
    """Parse YAML from a stream or string, and return the object.

    If the ``stream`` parameter is a :class:`str` then it is wrapped in an
    :class:`io.StringIO` and the data is read from that.

    Otherwise, the ``stream`` is used as-is.
    """

    if isinstance(stream, str):
        stream = io.StringIO(stream)

    return yaml.load(stream, IncludeLoader)


@raises(YamlCantLoad)
def yaml_load_path(path):
    """Load YAML from a path.

    If ``path`` specifies a file, read that, or if a directory, read all the files
    in that directory, and return the list of values that was read.

    When a directory is read, the order in which the files are loaded is undefined,
    and the returned data contains no indication of where the data came from.

    """

    s = os.stat(path)

    if stat.S_ISREG(s.st_mode):
        with open(path) as f:
            return yaml_load(f)

    if not stat.S_ISDIR(s.st_mode):
        raise YamlCantLoad(path=path)

    return list(yaml_load_path(os.path.join(path, part)) for part in os.listdir(path))


def _thing_to_yaml(rep, thing):
    """Represent :class:`Thing` as a plain dict, and avoid sorting the keys.

    This is called by :func:`yaml_dump` in order to avoid emitting tags
    for :class:`Thing` instances.
    """

    # https://stackoverflow.com/questions/16782112/can-pyyaml-dump-dict-items-in-non-alphabetical-order

    value = []

    for item_key, item_value in thing.items():
        node_key = rep.represent_data(item_key)
        node_value = rep.represent_data(item_value)

        value.append((node_key, node_value))

    return yaml.nodes.MappingNode(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, value)


yaml.add_representer(Thing, _thing_to_yaml)


def yaml_dump(obj, stream=None):
    """Dump an object as YAML to an output stream.

    The default destination, if ``stream`` is omitted or ``None``, is ``sys.stdout``.
    """

    return yaml.dump(obj, stream or sys.stdout, default_flow_style=False, block_seq_indent=2)
