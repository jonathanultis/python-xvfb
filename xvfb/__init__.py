# Copyright (c) 2012 Zillow
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is furnished
# to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os
import subprocess
import time
import signal
import logging

__ALL__ = ["XvfbStartException", "launch_xvfb"]

'''Start Xvfb, block until it is ready.'''


class XvfbStartException (Exception):
    '''Xvfb failed to start.'''
    pass


def launch_xvfb (DISPLAY = None, MAX_TRIES = 3):
    """Launch Xvfb as a subprocess. Export the correct DISPLAY to the environment.
    
    Xvfb uses some os signal stuff to let the parent process know when it is
    ready to handle work. This wrapper takes care of that interaction.

    This also sets up an atexit handler to shut down the Xvfb subprocess on
    normal program termination. You can still leak if you crash out due to
    segfault or something.

    DISPLAY -- optional, randomly chosen between [10, 10000] if not provided.
    MAX_TRIES -- Retries up to three times in case of failure.

    return The subprocess handle.
    """

    def ignore_signals ():
        signal.signal(signal.SIGUSR1, signal.SIG_IGN)

    # set up signal handlers to detect Xvfb startup, or failure
    def handle_xvfb_ready (signum, frame):
        handle_xvfb_ready.called = True
    handle_xvfb_ready.called = False

    def handle_xvfb_timeout (signum, frame):
        handle_xvfb_timeout.called = True
    handle_xvfb_timeout.called = False

    import signal
    old_sigusr1 = signal.getsignal (signal.SIGUSR1)
    old_sigalrm = signal.getsignal (signal.SIGALRM)

    try:
        # hook up our specialized signal handlers for interacting with Xvfb
        signal.signal (signal.SIGUSR1, handle_xvfb_ready)
        signal.signal (signal.SIGALRM, handle_xvfb_timeout)
        
        retry_count = 0
        while not handle_xvfb_ready.called and retry_count < MAX_TRIES:
            # pick a random display port. We're unlikely to collide.
            if DISPLAY:
                display = DISPLAY
            else:
                import random
                display = random.randint(10, 10000)
                display = ':' + str(display)
           
            # start xvfb - set SIGUSR1 to ignore, which obscurely tells Xvfb
            # that it should signal the parent when it is ready to proceed.
            start = time.time ()

            xvfb_cmd = ['Xvfb', '-once', '-terminate', '-screen', '0', '1024x768x24+32', display]
            import subprocess
            proc = subprocess.Popen(xvfb_cmd, preexec_fn = ignore_signals)

            # we shouldn't wait forever - if Xvfb doesn't call in
            # in a reasonable amount of time, give up
            signal.alarm(2)
           
            # we're only getting out of this pause via signal
            try:
                while not handle_xvfb_ready.called and not handle_xvfb_timeout.called:
                    signal.pause ()
            finally:
                # cancel the alarm if it is still pending
                signal.alarm (0)

            end = time.time ()
            elapsed = end - start

            if handle_xvfb_ready.called:
                #print "started Xvfb pid %d in %02.2fs" % (proc.pid, elapsed)
                # make sure the Xvfb process gets killed at program exit
                import atexit
                def try_to_kill ():
                    try:
                        proc.kill ()
                    except:
                        pass

                    try:
                        proc.wait ()
                    except:
                        pass
                atexit.register (try_to_kill)
                os.environ['DISPLAY'] = display
                logging.info ("started Xvfb pid %d in %02.4fs", proc.pid, elapsed)
            else:
                if proc and proc.pid > 0:
                    proc.kill ()
                    proc.wait ()
                
                # reset for the next try 
                handle_xvfb_timeout.called = False
                handle_xvfb_ready.called = False

                #print "failed to start Xvfb, killed after waiting %02.4fs" % elapsed
                logging.error ("failed to start Xvfb, killed after waiting %02.4fs", elapsed)
                retry_count += 1
    
    finally:
        # restore the original signal handlers
        signal.signal (signal.SIGUSR1, old_sigusr1)
        signal.signal (signal.SIGALRM, old_sigalrm)

    if retry_count >= MAX_TRIES:
        logging.critical ("giving up on Xvfb after %d attempts", MAX_TRIES)
        raise XvfbStartException ()

    return proc



