#!/usr/bin/env python2

"""DebugAppServer

`DebugAppServer` executes all requests within the main thread, allowing
servlets to be easily debugged using any Python debugger. The drawback is
that only one request can be processed at a time using this approach.

Also, exceptions are not caught and gracefully handled with an HTML error
page. Instead, the exceptions rise uncaught which allows the debugger to
trap them so you can inspect the program.

To use, simply run "python Launch.py DebugAppServer" using whatever debugging
environment you prefer.

Caveats:

This app server supports the AutoReload feature but not for Python's standard
modules or WebKit or WebKit's dependencies (MiscUtils, WebUtils and TaskKit).
Even with that limitation, auto-reload is still useful because if you modify
any module in your site, the auto-reload will happen. Note that the app server
*will* restart when the aformentioned modules are modified, but the modules
won't actually be reloaded.

Currently the session sweeper is still run within a separate thread, and
a "close thread" is started up by the AppServer base class, but neither
of these two extra threads should pose any problems debugging servlets.

Tested on:
    - WingIDE on Windows, http://wingware.com/
    - PythonWin
    - JEdit with the JPyDbg plugin, on Windows
"""

import sys

import ThreadedAppServer
import Profiler

# We are going to replace ThreadedAppServer with our own class,
# so we need to save a reference to the original class.
OriginalThreadedAppServer = ThreadedAppServer.ThreadedAppServer

# We want the Python debugger to trap the exceptions, not WebKit
ThreadedAppServer.doesRunHandleExceptions = False


class DebugAppServer(OriginalThreadedAppServer):
    """Single-threaded AppServer for debugging purposes.

    We are piggybacking on 99% of the code in ThreadedAppServer. Our
    trick is to replace the request queue with a dummy object that
    executes requests immediately instead of pushing them onto a queue
    to be handled by other threads.
    """


    ## Init ##

    _excludePrefixes = 'WebKit MiscUtils WebUtils TaskKit'.split()

    def __init__(self, path=None):
        """Initialize DebugAppServer."""
        # Initialize the base class
        OriginalThreadedAppServer.__init__(self, path)
        # Replace the request queue with a dummy object that merely
        # runs request handlers as soon as they are "pushed"
        self._requestQueue = DummyRequestQueue()
        print 'You are running the debugging app server.'

    def config(self):
        """Return default configuration."""
        # Force ThreadedAppServer to create an empty thread pool by hacking
        # the settings to zero. This is not strictly necessary to do.
        if self._config is None:
            OriginalThreadedAppServer.config(self)
            self.setSetting('StartServerThreads', 0)
            self.setSetting('MaxServerThreads', 0)
            self.setSetting('MinServerThreads', 0)
        return self._config


    ## Overridden methods ##

    def mainloop(self):
        """Main loop for Windows.

        This is needed for COM support on Windows, because special thread
        initialization is required on any thread that runs servlets, in
        this case the main thread itself.
        """
        self.initThread()
        try:
            OriginalThreadedAppServer.mainloop(self)
        finally:
            self.delThread()

    def createApplication(self):
        """Create and return an application object. Invoked by __init__."""
        return DebugApplication(server=self)

    def restart(self):
        # The normal restart technique is to exit the application
        # with a special exit code and let an extra-process script
        # start the app server up again. That works poorly for a
        # debugging environment which is attached to a particular process.
        Profiler.reset()
        self.initiateShutdown()
        self._closeThread.join()
        sys.stdout.flush()
        sys.stderr.flush()
        self._imp.delModules(includePythonModules=False,
            excludePrefixes=self._excludePrefixes)
        raise ThreadedAppServer.RestartAppServerError


from Application import Application


class DebugApplication(Application):
    """This is a modified Application class for debugging."""


    ## Overridden methods ##

    # Don't handle exceptions gracefully because we want
    # them to rise uncaught so the debugger will kick in.

    # @@ 2005-07-15 CE: This works well for exceptions within responding to
    # a request, but for problems during importing a servlet, the exception
    # gets printed to console and the debugger does not kick in.

    def handleException(self):
        """Handle exception.

        This should only be used in cases where there is no transaction object,
        for example if an exception occurs when attempting to save a session
        to disk.
        """
        raise

    def handleExceptionInTransaction(self, excInfo, transaction):
        """Handle exception with info.

        Raises exception `excInfo` (as returned by ``sys.exc_info()``)
        that was generated by `transaction`.
        """
        raise


class DummyRequestQueue(object):
    """This is a dummy replacement for the request queue.

    It merely executes handlers as soon as they are "pushed".
    """


    ## Overridden methods ##

    @staticmethod
    def put(handler):
        handler.handleRequest()
        handler.close()


## Globals ##

# Replace ThreadedAppServer class in the ThreadedAppServer module with our
# DebugAppServer.  This seems like an awful hack, but it works and
# requires less code duplication than other approaches I could think of, and
# required a very minimal amount of modification to ThreadedAppServer.py.
ThreadedAppServer.ThreadedAppServer = DebugAppServer

# Grab the main function from ThreadedAppServer -- it has been "tricked"
# into using DebugAppServer instead.
main = ThreadedAppServer.main

# Tweak ThreadedAppServer so that it never runs the main loop in a thread:
def runMainLoopInThread():
    return 0
ThreadedAppServer.runMainLoopInThread = runMainLoopInThread
