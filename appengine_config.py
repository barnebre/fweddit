'''
Created on Dec 17, 2017

@author: Brent
'''
from google.appengine.ext import vendor
# add `lib` subdirectory to `sys.path`, so our `main` module can load
# third-party libraries.
vendor.add("lib")