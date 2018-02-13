# -*- coding: utf-8 -*-

from BaseOperator import BaseOperator
import yaml
import os

class BaseFPGAOperator(BaseOperator):
  def __init__(self, name, kernel_conf_file):
    super().__init__(name)
    self.kernel_interfaces = {}

    home = os.environ['MYSTR_HOME']
    conf_file_path = home + '/conf/' + kernel_conf_file
    if os.path.exists(conf_file_path):
      f = open(home + '/conf/' + kernel_conf_file, 'r')
      self.kernel_conf = yaml.load(f)
      f.close()
      
