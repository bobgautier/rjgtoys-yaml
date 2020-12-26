Tutorial
========

Reading YAML
------------

The function :func:`rjgtoys.yaml.yaml_load` will read YAML.

It can read a string:

.. literalinclude:: ../../examples/tutorial1.py

Or an input stream:

.. literalinclude:: ../../examples/tutorial2.py

Reading from a file can be done directly with :func:`rjgtoys.yaml.yaml_load_path`:

.. literalinclude:: ../../examples/tutorial3.py

If :func:`~rjgtoys.yaml.yaml_load_path` is passed a path to a directory, it
will return a list in which each item is the content of a file loaded from
that directory (but in no particular order, and with no indication of where the
content came from).

Using the data
--------------

Mappings returned from the loader functions are :class:`rjgtoys.thing.Thing`
instances, which means they treat attribute and item access equivalently,
and so you can do things like this:

.. literalinclude:: ../../examples/tutorial4.py

See also: rjgtoys.thing_

.. _rjgtoys.thing: https://rjgtoys.readthedocs.io/projects/thing/en/latest/

Referencing other files
-----------------------

An `!include path` tag in YAML input will be replaced by the data
loaded from the specified path (or a list, if the path specifies a directory).

Paths in `!include` tags are interpreted relative to the directory of
the file that contains the tag, or (if reading from a string or other
stream with no associated directory) the current working directory.

Here's an example of an `!include`:

.. literalinclude:: ../../examples/tutorial5.yaml

Writing YAML
------------

The function :func:`rjgtoys.yaml.yaml_dump` converts an object into YAML
and writes it to an output stream.  The default output stream is `sys.stdout`.

.. literalinclude:: ../../examples/tutorial6.py

The output should look like this:

.. literalinclude:: ../../examples/tutorial6.yaml




