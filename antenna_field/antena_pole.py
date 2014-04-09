from sympy import *
from sympy.abc import x, y, z, k, l, m, h, w, d
init_printing(use_unicode=False, wrap_line=False, no_global=True)

# print integrate( 1/sqrt(x*y) , (x, -h/2,h/2))

e1 =  Integral( 1/sqrt( (x-k)**2+(y-l)**2+(z-m)**2 ) , (z, -h/2,h/2))
print e1
e1r = e1.doit()
print e1r
e2 = Integral(e1r, (y, -w/2, w/2))
e2r = e2.doit()
e3 = Integral(e2r, (z, -d/2, d/2))
e3r - e3.doit()
print integrate(x**2 * exp(x) * cos(x), x)
print "done"