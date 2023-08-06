#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""
Initialization module for tpQtLib
"""

from __future__ import print_function, division, absolute_import

import os
import sys
import inspect
import logging

main = __import__('__main__')

# =================================================================================

logger = None
resource = None

# =================================================================================


def init(do_reload=False, dev=False):
    """
    Initializes module
    :param do_reload: bool, Whether to reload modules or not
    :param dev: bool, Whether artellapipe is initialized in dev mode or not
    """

    # Load logger configuration
    logging.config.fileConfig(get_logging_config(), disable_existing_loggers=False)

    from tpPyUtils import importer
    from tpQtLib.core import resource as resource_utils
    from tpQtLib.resources import res

    class tpQtLibResource(resource_utils.Resource, object):
        RESOURCES_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resources')

    class tpQtLib(importer.Importer, object):
        def __init__(self, *args, **kwargs):
            super(tpQtLib, self).__init__(module_name='tpQtLib', *args, **kwargs)

        def get_module_path(self):
            """
            Returns path where tpQtLib module is stored
            :return: str
            """

            try:
                mod_dir = os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename)
            except Exception:
                try:
                    mod_dir = os.path.dirname(__file__)
                except Exception:
                    try:
                        import tpQtLib
                        mod_dir = tpQtLib.__path__[0]
                    except Exception:
                        return None

            return mod_dir

        def update_paths(self):
            """
            Adds path to system paths at startup
            """

            paths_to_update = [self.externals_path()]

            for p in paths_to_update:
                if os.path.exists(p) and p not in sys.path:
                    sys.path.append(p)

        def externals_path(self):
            """
            Returns the paths where tpPyUtils externals packages are stored
            :return: str
            """

            return os.path.join(self.get_module_path(), 'externals')

    def init_dcc(do_reload=False):
        """
        Checks DCC we are working on an initializes proper variables
        """

        if 'cmds' in main.__dict__:
            from tpMayaLib import loader
            loader.init_ui(do_reload=do_reload)
        elif 'MaxPlus' in main.__dict__:
            from tpMaxLib import loader
            loader.init_ui(do_reload=do_reload)
        elif 'hou' in main.__dict__:
            from tpHoudiniLib import loader
            loader.init_ui(do_reload=do_reload)
        elif 'nuke' in main.__dict__:
            raise NotImplementedError('Nuke is not a supported DCC yet!')
        else:
            global Dcc
            from tpDccLib.core import dcc
            Dcc = dcc.UnknownDCC
            logger.warning('No DCC found, using abstract one!')

        from tpDccLib.core import callbackmanager
        callbackmanager.CallbacksManager.initialize()

    tpqtlib_importer = importer.init_importer(importer_class=tpQtLib, do_reload=False)
    tpqtlib_importer.update_paths()

    global logger
    global resource
    logger = tpqtlib_importer.logger
    resource = tpQtLibResource

    tpqtlib_importer.import_modules(skip_modules=['tpQtLib.externals'])
    tpqtlib_importer.import_packages(only_packages=True, skip_modules=['tpQtLib.externals'],
                                     order=['tpQtLib.core', 'tpQtLib.widgets'])
    if do_reload:
        tpqtlib_importer.reload_all()

    init_dcc(do_reload=do_reload)


def create_logger_directory():
    """
    Creates artellapipe logger directory
    """

    tppyutils_logger_dir = os.path.normpath(os.path.join(os.path.expanduser('~'), 'tpPyUtils', 'logs'))
    if not os.path.isdir(tppyutils_logger_dir):
        os.makedirs(tppyutils_logger_dir)


def get_logging_config():
    """
    Returns logging configuration file path
    :return: str
    """

    create_logger_directory()

    return os.path.normpath(os.path.join(os.path.dirname(__file__), '__logging__.ini'))


def register_class(cls_name, cls, is_unique=False):
    """
    Registers given class when loading modules
    :param cls_name: str, name of the class we want to register
    :param cls: class, class we want to register
    :param is_unique: bool, Whether if the class should be updated if new class is registered with the same name
    """

    if is_unique:
        if cls_name in sys.modules[__name__].__dict__:
            setattr(sys.modules[__name__], cls_name, getattr(sys.modules[__name__], cls_name))
    else:
        # print('>>> Registering class {} with value {}'.format(cls_name, cls))
        sys.modules[__name__].__dict__[cls_name] = cls
