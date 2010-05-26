=====
Pypit
=====

Pypit (pronounce "Pipe it!") is a python library for building shell pipeline easily via configuration.

The principe is simple: create a configuration which describes a programmes list with all options and your done.

Exemple
-------

Let's say we have a `file.txt` with the following content::
    
    HellO
    Foo
    BAR
    Bla

The following configuration will sort the `file.txt` and lower all capitalize chars::

    >>> config = [
    ...    {
    ...        "path": "/usr/bin",
    ...        "name": "sort",
    ...        "input": "file.txt",
    ...        "options": "-r",
    ...    },
    ...    {
    ...        "path": "/usr/bin",
    ...        "name": "tr",
    ...        "input": "STDIN",
    ...        "options": "A-Z a-z"
    ...    }
    ...]

To process this configuration::

    >>> from pypit import Pypit
    >>> result = Pypit(config).run()
    >>> print result
    hello
    foo
    bla
    bar

Explanation
-----------

`path`, `name` are required.

you can pass all options and arguments to `options`.

If `input` is "STDIN", the input will be take from the standard input. If `input` if a file name, this file will be used as input.

If `ouput` is not defined, the output will be send to the standard output. If `output` is a file name, the output will be writed to the file.

Sometimes, we need to call direclty shell command. To do so, add `'shell' = True` to the configuration and pass all options directly to `name`::

    >>> config = [
    ...    {
    ...        "shell": True,
    ...        "path": "/bin",
    ...        "name": 'echo "12345"',
    ...    },
    ...    {
    ...        "path": "/usr/bin",
    ...        "name": "wc",
    ...        "input": "STDIN",
    ...        "options": "-c"
    ...    }
    ...]
    >>> Pypit(config).run()
    '6\n'


Shell script usage
------------------

Pypit package provides a shell commands to execute pypit configuration in yaml format. To do the following example, you have to create a `config.yaml` file::

    - 
        path: /bin
        shell: true
        name: echo "12345"

    - 
        path: /usr/bin
        name: wc
        input: STDIN
        options: -c


then call the `pypit` programme with the config file as argument::

    $ pypit config.yaml
    6



