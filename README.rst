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
    ...        "cmd": "sort -r {{input}}",
    ...    },
    ...    {
    ...        "cmd": "tr A-Z a-z",
    ...        "use_stdin": True
    ...    }
    ...]

To process this configuration::

    >>> from pypit import Pypit
    >>> result = Pypit(config).run(file_name="file.txt")
    >>> print result
    hello
    foo
    bla
    bar

Explanation
-----------

Only `cmd` is required. This is the command line to use.

If `use_sdtin` is True, the input will be take from the standard input. 

`{{input}}` will describes the input file given to the `run` function. You can use a the `{{output}}` description to specify output file. Be carrefull to specify the `output_ext` then::

    >>> config = [
    ...    {
    ...        'cmd': 'sort -r {{input}} {{output}}',
    ...        'output_ext': sorted # we need to specify the output extension. Here, the file will be "file.txt.sorted"
    ...    },
    ...    {
    ...        'cmd': 'wc -c {{input}}',
    ...    }
    ...]
    >>> Pypit(config).run(file_name='file.txt')
    '6\n'

Note that if the file is in another directory, you can specify if with `cwd` argument::

    >>> Pypit(config).run(file_name='file.txt', 'cwd'='/tmp')
    '6\n'

Finally, it is possible to take a look at the generated command line via the `cmdline` attribute::

    >>> pypit = Pypit(config)
    >>> res = pypit.run(file_name='file.txt')
    >>> pypit.cmdline
    'sort -r file.txt file.txt.sorted && wc -c file.txt.sorted
            

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

If you build your config to handle dynamic file, you can pass those file in arguments::

    -
        path: /usr/bin
        name: sort
        input: STDIN
        options: -r
    -
        path: /usr/bin
        name: wc
        input: STDIN
        options: -l

    $ pypit config.yaml file.txt
    6


Version
-------

v0.2.1
~~~~~~

 * fix issue when with utf-8 options

v0.2
~~~~

 * add dynamic file input support
