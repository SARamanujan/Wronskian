#!/usr/local/bin/python
# -*- coding: utf-8 -*
'''graph_0001
wronskian
test - subplots, fonts, saving (& anim) - convert image ... curve
'''

import sys, os
import time
from math import pi, sin, cos
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.font_manager as mpfm
from scipy import misc
from PIL import Image

sys.path.append('../../pyxpm')
from pyxpm import xpm

import urllib2, urllib

ACP = lambda fn: fn.decode('utf-8').encode('cp932')
FONTJP = '/windows/fonts/HGRSMP.ttf' # HGRSKP
IMGS = {'CIRCLE': 'Tux', 'ECB': 'Tux_ecb'}
IMGD = '/tmp'
IMGU = 'https://raw.githubusercontent.com/sanjonemu/pyxpm/master/res'

NAXIS = 4

def getFN(k):
  return ACP(os.path.join(IMGD, 'cs_%s.jpg' % IMGS[k]))

def getURI(k):
  s = ''
  b = 'cs_%s_58x64_c16.xpm' % IMGS[k]
  try:
    u = urllib2.urlopen('%s/%s' % (IMGU, b))
    s = u.read()
  except (Exception, ), e:
    sys.stderr.write('\n%s\n' % repr(e))
  return s

def getIm(s, a=True):
  nda = xpm.XPM(s)
  r, c, m = nda.shape
  img = Image.frombuffer('RGBA', (c, r), nda, 'raw', 'BGRA', 0, 1)
  return np.array(img) if a else img

def first():
  # for display japanese
  fontprop = mpfm.FontProperties(fname=FONTJP, size=9)

  fig = plt.figure()
  axis = [fig.add_subplot(221 + _ % 4) for _ in range(4)]

  # fontprop
  axis[0].set_title('wronskian')

  # axis[1].imshow(np.array(Image.open(getFN('CIRCLE'))))
  axis[1].imshow(getIm(getURI('CIRCLE')))
  axis[1].set_title(IMGS['CIRCLE'])

  # axis[2].imshow(misc.toimage(mpimg.imread(getFN('ECB')), cmin=0, cmax=255))
  axis[2].imshow(getIm(getURI('ECB'), a=True))
  axis[2].set_title(IMGS['ECB'])

  # axis[3].imshow(mpimg.imread(getFN('ECB'))) # bottom <-> top (.jpg)
  axis[3].imshow(getIm(getURI('ECB'), a=False)) # bottom <-> top (PIL.Image)
  axis[3].set_title('b<->t: %s' % IMGS['ECB'])

  plt.subplots_adjust(left=None, bottom=None, right=None, top=None,
    wspace=1, hspace=1)
  plt.show()
  # fig.savefig(IMGOUT)
  # plt.close()

def draw_curve(axis, n, t, x):
  m = n % NAXIS
  ax = axis[m]
  th = np.pi * t / 50.0
  yx = np.sin(1.0*(x - th))
  yy = np.cos(1.0*(x - th))
  if m == 0: ax.plot(x, yy)
  elif m == 1: ax.plot(yx, yy)
  elif m == 2: return
  elif m == 3: ax.plot(yx, x)
  lines = ax.plot([], [])
  ax.relim()
  # ax.autoscale_view(tight=True, scalex=True, scaley=True)
  ax.grid()

def draw_axis(seconds):
  plt.ion()
  first() # includes plt.show()
  # plt.axis([0, 1000, 0, 1])
  fig = plt.figure()
  axis = [fig.add_subplot(221 + _ % NAXIS) for _ in range(NAXIS)]
  t = 0
  for i in range(seconds * 10): # about seconds when time.sleep(.01)
    # x = np.arange(-3.5, 7.0, 0.1)
    x = np.arange(-3.11, 3.11, 0.02)
    [draw_curve(axis, _, t, x) for _ in range(NAXIS) if _ != 2]
    # plt.pause(.01)
    plt.draw() # use 'draw' pyplot does not support 'pause' on python 2.5 ?
    time.sleep(.01)
    t += 1
    [ax.clear() for ax in axis if ax]
  plt.ioff()

def main():
  draw_axis(20)

if __name__ == '__main__':
  main()
