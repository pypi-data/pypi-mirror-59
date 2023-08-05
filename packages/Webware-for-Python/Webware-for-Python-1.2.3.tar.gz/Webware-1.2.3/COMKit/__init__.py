"""COMKit

This plug-in for Webware for Python allows COM objects such as ADO to be
used in free-threading mode in a threaded app server. See Appendix D of
the fine book Python Programming on Win32 by Mark Hammond and Andy
Robinson for details.

To use COM, simply set EnableCOM to True in your AppServer.config file.
This causes the app server threads to be configured properly for
COM free-threading. Then go ahead and use win32com inside your servlets.
"""

__all__ = []


def InstallInWebKit(appServer):
    # This function gets called by the app server during initialization.
    if not appServer.setting('EnableCOM', False):
        return  # enabling COM was not requested

    # This must be done BEFORE pythoncom is imported -- see the book mentioned above.
    import sys
    sys.coinit_flags = 0

    # Get the win32 extensions
    import pythoncom

    # Set references to the COM initialize and uninitialize functions
    appServer._initCOM = pythoncom.COINIT_MULTITHREADED
    appServer.initCOM = pythoncom.CoInitializeEx
    appServer.closeCOM = pythoncom.CoUninitialize

    # Monkey-patch this instance of the appServer

    # Grab references to the original initThread and delThread bound
    # methods, which we will replace
    appServer.originalInitThread = appServer.initThread
    appServer.originalDelThread = appServer.delThread

    # Create new versions of initThread and delThread which will call the
    # old versions

    def newInitThread(self):
        # This must be called at the beginning of any thread that uses COM
        self.initCOM(self._initCOM)
        # Call the original initThread
        self.originalInitThread()

    def newDelThread(self):
        # Call the original delThread
        self.originalDelThread()
        # Uninitialize COM
        self.closeCOM()

    # Replace the initThread and delThread methods with our new versions
    import new
    appServer.initThread = new.instancemethod(newInitThread, appServer, appServer.__class__)
    appServer.delThread = new.instancemethod(newDelThread, appServer, appServer.__class__)

    print 'COM has been enabled.'
