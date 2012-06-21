import os
import signal

from jvpn import display_curses

class Display(object):
  def __init__(self, host, interface,
               pid, logger):
    self.host = host
    self.interface = interface
    self.pid = pid
    self.logger = logger

  def Curses(self):
    self.app = display_curses.CursesFormatter(self.host, self.interface)
    try:
      if self.app.run() is False:
        ok = raw_input('Are you sure you want to disconnect? (Y/N): ')
        if ok in ('y', 'Y'):
          os.killpg(self.pid, signal.SIGTERM)
          os.wait()
          try:
            os.kill(self.pid, 0)
          except OSError:
            self.logger.info('VPN at pid %d disconnected successfully' % (self.pid))
    except EOFError:
      self.logger.info('Curses window resize failed, type \'pkill ncui\' to disconnect')

  def Gtk(self):
    pass

