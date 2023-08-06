# flake8: noqa
import os
from pypi_mobans_pkg._version import __version__
from pypi_mobans_pkg._version import __author__
from lml.plugin import PluginInfo


@PluginInfo('library', tags=['setupmobans', 'pypi', 'pypi-mobans-pkg'])
class Pypkg():
    def __init__(self):
        __package_path__ = os.path.dirname(__file__)
        self.resources_path = os.path.join(
            __package_path__, "resources")
