#!/usr/bin/env python
#
# $Id: display_curses.py 161 2012-06-19 05:16:57Z earies $

"""JVPN curses display module.

"""

__author__ = 'e@dscp.org (Ebben Aries)'

import curses
import time

from jvpn import netstats

class CursesFormatter(object):
  def __init__(self, host, interface):
    self.host = host
    self.interface = interface
    self.offset = 20
    self.stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)

  def run(self):
    try:
      while True:
        if netstats.GetNetstats(self.interface) is not None:
          self.routes_beg = 16
          self.routes_end = self.routes_beg + 5
          self.stdscr.clear()
          self.stdscr.border(0)
          self.stdscr.addstr(
              1,
              2,
              'Juniper Network Connect VPN',
              curses.A_BOLD)
          self.stdscr.addstr(
              3,
              2,
              'Connection: ')
          self.stdscr.addstr(
              3,
              self.offset,
              self.host)
          self.stdscr.addstr(
              4,
              2,
              'Status: ')
          self.stdscr.addstr(
              4,
              self.offset,
              str('%-20s' % ('Connected')))
          self.stdscr.addstr(
              5,
              2,
              'Assigned IP: ')
          self.stdscr.addstr(
              5,
              self.offset,
              netstats.GetIp(self.interface))
          self.stdscr.addstr(
              7,
              2,
              'Interface: %s' % (self.interface),
              curses.A_UNDERLINE)
          self.stdscr.addstr(
              8,
              2,
              'TX (Bytes): ')
          self.stdscr.addstr(
              8,
              self.offset,
              netstats.GetNetstats('%s' % (self.interface))[0])
          self.stdscr.addstr(
              9,
              2,
              'TX (Packets): ')
          self.stdscr.addstr(
              9,
              self.offset,
              netstats.GetNetstats('%s' % (self.interface))[1])
          self.stdscr.addstr(
              10,
              2,
              'RX (Bytes): ')
          self.stdscr.addstr(
              10,
              self.offset,
              netstats.GetNetstats('%s' % (self.interface))[2])
          self.stdscr.addstr(
              11,
              2,
              'RX (Packets): ')
          self.stdscr.addstr(
              11,
              self.offset,
              netstats.GetNetstats('%s' % (self.interface))[3])
          self.stdscr.addstr(
              15,
              2,
              'Routes: %s' % (self.interface),
              curses.A_UNDERLINE)
          for self.route in netstats.GetRoutes(self.interface):
            if self.routes_beg < self.routes_end:
              self.stdscr.addstr(
                  self.routes_beg,
                  2,
                  self.route)
              self.routes_beg += 1
            if self.routes_beg == self.routes_end:
              self.stdscr.addscr(
                  self.routes_beg,
                  2,
                  '...')
          self.stdscr.addstr(
              25,
              2,
              'Press \'ctrl-d\' to disconnect')
          self.stdscr.refresh()
          self.stdscr.nodelay(1)
          self.keypress = self.stdscr.getch()
          if (self.keypress == 4):
            self.Restore()
            curses.beep()
            break
          time.sleep(1)
        else:
          self.stdscr.clear()
          self.stdscr.border(0)
          self.stdscr.addstr(
              1,
              2,
              'Juniper Network Connect VPN',
              curses.A_BOLD)
          self.stdscr.addstr(
              4,
              2,
              'Status: ')
          self.stdscr.addstr(
              4,
              self.offset,
              str('%-20s' % ('Not Connected')))
          self.stdscr.addstr(
              25,
              2,
              'Press \'ctrl-d\' to disconnect')
          self.stdscr.refresh()
          self.stdscr.nodelay(1)
          self.keypress = self.stdscr.getch()
          if (self.keypress == 4):
            self.Restore()
            curses.beep()
            break
          time.sleep(1)
    except curses.error:
      curses.endwin()
    finally:
      curses.endwin()
    return False

  def Restore(self):
    curses.nocbreak()
    curses.echo()
    curses.noraw()
    curses.endwin()
