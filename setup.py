# From: https://github.com/pypa/sampleproject/blob/main/setup.py

# Always prefer setuptools over distutils
import pathlib

import toml
from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')


# From: https://medium.com/expedia-group-tech/simplifying-python-builds-74e76802444f
def get_install_requirements():
    try:
        # read my pipfile
        with open('Pipfile', 'r') as fh:
            pipfile = fh.read()
        # parse the toml
        pipfile_toml = toml.loads(pipfile)
    except FileNotFoundError:
        return []
    # if the package's key isn't there then just return an empty list
    try:
        required_packages = pipfile_toml['packages'].items()
    except KeyError:
        return []
        # If a version/range is specified in the Pipfile honor it
        # otherwise just list the package
    return ["{0}{1}".format(pkg, ver) if ver != "*"
            else pkg for pkg, ver in required_packages]


setup(
    name='travel_log',  # Required
    version='0.0.1',  # Required

    # This is a one-line description or tagline of what your project does. This
    # corresponds to the "Summary" metadata field:
    # https://packaging.python.org/specifications/core-metadata/#summary
    description='Creates a static website from your trip\'s pictures and tracks',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/fernandobrito/travel_log',  # Optional
    author='Fernando Brito',  # Optional
    author_email='email@fernandobrito.com',  # Optional

    classifiers=[  # Optional
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate you support Python 3. These classifiers are *not*
        # checked by 'pip install'. See instead 'python_requires' below.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],

    # This field adds keywords for your project which will appear on the
    # project page. What does your project relate to?
    #
    # Note that this is a list of additional keywords, separated
    # by commas, to be used to assist searching for the distribution in a
    # larger catalog.
    # keywords='sample, setuptools, development',  # Optional

    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is necessary to specify the `package_dir` argument.
    package_dir={'': 'src'},  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    #
    # Alternatively, if you just want to distribute a single Python file, use
    # the `py_modules` argument instead as follows, which will expect a file
    # called `my_module.py` to exist:
    #
    #   py_modules=["my_module"],
    #
    packages=find_packages(where='src'),  # Required

    # Specify which Python versions you support. In contrast to the
    # 'Programming Language' classifiers above, 'pip install' will check this
    # and refuse to install the project if the version does not match. See
    # https://packaging.python.org/guides/distributing-packages-using-setuptools/#python-requires
    python_requires='>=3.9, <4',

    # This field lists other packages that your project depends on to run.
    # Any package you put here will be installed by pip when your project is
    # installed, so they must be valid existing projects.
    #
    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=get_install_requirements(),  # Optional

    # Allows pip install -e and mypy:
    # https://mypy.readthedocs.io/en/latest/installed_packages.html#making-pep-561-compatible-packages
    zip_safe=False,

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    # package_data={  # Optional
    #     'travel_log': ['py.typed', ''],
    # },
    include_package_data=True,

    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={  # Optional
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # `pip` to create the appropriate form of executable for the target
    # platform.
    #
    # For example, the following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={},

    # List additional URLs that are relevant to your project as a dict.
    #
    # This field corresponds to the "Project-URL" metadata fields:
    # https://packaging.python.org/specifications/core-metadata/#project-url-multiple-use
    #
    # Examples listed include a pattern for specifying where the package tracks
    # issues, where the source is hosted, where to say thanks to the package
    # maintainers, and where to support the project financially. The key is
    # what's used to render the link text on PyPI.
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/fernandobrito/travel_log/issues',
        'Source': 'https://github.com/fernandobrito/travel_log',
    },
)
