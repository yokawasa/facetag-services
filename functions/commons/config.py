# -*- coding: utf-8 -*-
import os
import configparser

_CONFIG_DEFAULT_SECTION = 'facetag'

class Config(object):
  def __init__(self, config_file=None):
    self._config_file= config_file
    if self._config_file:
      self._config_parser = configparser.SafeConfigParser()
      self._config_parser.read(config_file)

  def get_value(self, key, default_val=None):
    if not self._config_file:
      return os.environ[key] if key in os.environ else default_val
    v =''
    try:
      v = self._config_parser.get(_CONFIG_DEFAULT_SECTION, key)
    except configparser.NoOptionError as e:
      v = default_val
      return v
