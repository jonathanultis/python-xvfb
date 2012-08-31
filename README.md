====
xvfb
====

Dependencies
------------

This requires the Xvfb binary. On debian packaging systems:

> sudo apt-get install xvfb

Overview
--------

The xvfb egg provides a simple wrapper script to launch the Xvfb 'fake' X server synchronously using subprocess. It sets the DISPLAY environment variable to point at the newly launched X server. It also sets up an atexit handler that tries really hard to prevent leaking Xvfb processes when the python process exits.

Usage
------

<pre>
>>> import xvfb
>>> proc = xvfb.launch_xvfb ()
</pre>

Your Xvfb is running and the DISPLAY environment variable is configured to use it.

License
-------

Copyright (c) 2012 Zillow
http://www.zillow.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is furnished
to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

