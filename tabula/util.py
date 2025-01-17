"""
Utility module providing some convinient functions.
"""

import os
import platform
import warnings

DEFAULT_JAVA_CONFIG = {"JAVA_PATH": 'java'}


def _java_path():
    return os.environ.get("JAVA_PATH", DEFAULT_JAVA_CONFIG["JAVA_PATH"])


def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emmitted
    when the function is used."""

    def newFunc(*args, **kwargs):
        warnings.warn(
            "Call to deprecated function {}.".format(func.__name__),
            category=DeprecationWarning,
            stacklevel=2,
        )
        return func(*args, **kwargs)

    newFunc.__name__ = func.__name__
    newFunc.__doc__ = func.__doc__
    newFunc.__dict__.update(func.__dict__)
    return newFunc


def deprecated_option(option):
    warnings.warn(
        "Call to deprecated option {}.".format(option),
        category=DeprecationWarning,
        stacklevel=2,
    )


def java_version():
    """Show Java version

    Returns:
        str: Result of ``java -version``
    """
    import subprocess

    try:
        res = subprocess.check_output([_java_path(), "-version"], stderr=subprocess.STDOUT)
        res = res.decode()

    except FileNotFoundError:
        res = (
            "`java -version` faild. `java` command is not found from this Python"
            "process. Please ensure Java is installed and PATH is set for `java`"
        )

    return res


def environment_info():
    """Show environment information for reporting.

    Returns:
        str:
            Detailed information like Python version, Java version,
            or OS environment, etc.
    """

    import sys
    import distro
    from tabula import __version__

    print(
        """Python version:
    {}
Java version:
    {}
tabula-py version: {}
platform: {}
uname:
    {}
linux_distribution: {}
mac_ver: {}
    """.format(
            sys.version,
            java_version().strip(),
            __version__,
            platform.platform(),
            str(platform.uname()),
            distro.linux_distribution(),
            platform.mac_ver(),
        )
    )
