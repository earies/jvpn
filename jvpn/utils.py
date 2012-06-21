import os
import subprocess

class Utils(object):
  def __init__(self, logger):
    self.logger = logger
    self.jvpn_basedir = os.path.join(os.getenv('HOME'), '.juniper_networks', 'network_connect')
    self.libncui = os.path.join(self.jvpn_basedir, 'libncui.so')
    self.ncui = os.path.join(self.jvpn_basedir, 'ncui')

  def CompileNcui(self):
    os.environ['LD_RUN_PATH'] = self.jvpn_basedir
    self.process = subprocess.Popen([
      '/usr/bin/gcc',
      '-m32',
      self.libncui,
      '-o', self.ncui])
    self.process.wait()
    self.logger.info('ncui compiled successfully')
