# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in Noodle-NG.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig
import tg

import noodle
from noodle import model
from noodle.lib import app_globals, helpers 

base_config = AppConfig()
base_config.renderers = []

base_config.package = noodle

#Set the default renderer
base_config.default_renderer = 'genshi'
base_config.renderers.append('genshi')
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')

#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = noodle.model
base_config.DBSession = noodle.model.DBSession

tg.include_widgets = ['turbogears.mochikit']