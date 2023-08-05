from __future__ import print_function
# Python version of SNOBFIT v2.1 "snobfit.m" MATLAB version by A. Neumaier.
#
# Modified and redistributed with permission.

# Original copyright and license notice:
#
# Copyright (c) 2003-2008, Arnold Neumaier
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the University of Vienna nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY ARNOLD NEUMAIER ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL  ARNOLD NEUMAIER BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
 function y = snobpoint(x, xl, xu, f0, g, sigma, u, v, dx)

 For a box [xl, xu] containing a point x, a point y in the intersection
 of [xl, xu] and [u, v] is constructed such that it is both not close to
 x and to the boundary of [xl, xu] and its function value is estimated
 from a local quadratic model around x.
 
 Input:
  x            point contained in [xl, xu]
  xl, xu       box bounds
  u, v         the point is to be generated in [u, v]
  f0           f0[1] is the function value at x, f0[2] is its uncertainty
  g, G, sigma  the local quadratic model around x is given by
               q(y) = f0[0]+g*(y-x)'+sigma*((y-x)*diag(D)*(y-x)'+f0[1])
               for a row vector y, where D = f0[1]/dx**2
  dx           resolution vector
 
 Output:
  y            point in the intersection of [xl, xu] and [u, v]
  f            corresponding estimated function value
"""

from ._snoblocf  import snobround
import numpy


def snobpoint(x, xl, xu, f0, g, sigma, u, v, dx):
    n = len(x)
    y = numpy.zeros(n)
    for i in range(n):
        if x[i] - xl[i] > xu[i] - x[i]:
            y[i] = 0.5*(xl[i] + x[i])
        else:
            y[i] = 0.5*(x[i] + xu[i])

    y = numpy.minimum(numpy.maximum(y, u), v)
    y = snobround(y, numpy.maximum(xl,u), numpy.minimum(xu,v), dx)
    D = f0[1]/dx**2
    f = f0[0] + g.dot((y-x).T) + sigma*((y-x).dot(numpy.diag(D).dot((y-x).T))+f0[1])
    return y, float(f)
