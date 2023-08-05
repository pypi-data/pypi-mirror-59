#!/usr/bin/env python2

"""The Application singleton.

`Application` and `AppServer` work together to setup up and dispatch requests.
The distinction between the two is largely historical, but AppServer
communicates directly with Adapters (or speaks protocols like HTTP), and
Application receives the (slightly) processed input from AppServer and turns
it into `Transaction`, `HTTPRequest`, `HTTPResponse`, and `Session`.

Application is a singleton, which belongs to the AppServer. You can get access
through the Transaction object (`transaction.application()`), or you can do::

    from AppServer import globalAppServer
    application = globalAppServer.application()

Settings for Application are taken from ``Configs/Application.config``,
which is used for many global settings, even if they aren't closely tied
to the Application object itself.
"""

import os
import sys

from MiscUtils import NoDefault
from MiscUtils.NamedValueAccess import valueForName
from ConfigurableForServerSidePath import ConfigurableForServerSidePath
from ExceptionHandler import ExceptionHandler
from HTTPRequest import HTTPRequest
from HTTPExceptions import HTTPException, HTTPSessionExpired
from Transaction import Transaction
from ASStreamOut import ConnectionAbortedError
import URLParser

debug = False

defaultConfig = dict(
    PrintConfigAtStartUp = True,
    LogActivity = True,
    ActivityLogFilename = 'Logs/Activity.csv',
    ActivityLogColumns = [
        'request.remoteAddress', 'request.method',
        'request.uri', 'response.size',
        'servlet.name', 'request.timeStamp',
        'transaction.duration',
        'transaction.errorOccurred'
        ],
    SessionModule = 'Session',
    SessionStore = 'Dynamic',
    SessionStoreDir = 'Sessions',
    SessionTimeout = 60,
    SessionPrefix = '',
    SessionName = '_SID_',
    AlwaysSaveSessions = True,
    RetainSessions = True,
    IgnoreInvalidSession = True,
    UseAutomaticPathSessions = False,
    UseCookieSessions = True,
    SessionCookiePath = None,
    SecureSessionCookie = True,
    ShowDebugInfoOnErrors = True,
    EnterDebuggerOnException = False,
    IncludeEditLink = True,
    IncludeFancyTraceback = False,
    FancyTracebackContext = 5,
    UserErrorMessage = 'The site is having technical difficulties'
        ' with this page. An error has been logged, and the problem'
        ' will be fixed as soon as possible. Sorry!',
    LogErrors = True,
    ErrorLogFilename = 'Logs/Errors.csv',
    SaveErrorMessages = True,
    ErrorMessagesDir = 'ErrorMsgs',
    EmailErrors = False,
    EmailErrorReportAsAttachment = False,
    ErrorEmailServer = 'localhost',
    ErrorEmailHeaders = {
        'From': 'webware@mydomain',
        'To': ['webware@mydomain'],
        'Reply-To': 'webware@mydomain',
        'Content-Type': 'text/html',
        'Subject': 'Error'
        },
    ErrorPage = None,
    MaxValueLengthInExceptionReport = 500,
    RPCExceptionReturn = 'traceback',
    ReportRPCExceptionsInWebKit = True,
    CacheDir = 'Cache',
    Contexts = {
        'default': 'Examples',
        'Admin': 'Admin',
        'Examples': 'Examples',
        'Testing': 'Testing',
        'Docs': 'Docs',
        },
    Debug = dict(
        Sessions = False,
        ),
    DirectoryFile = ['index', 'Index', 'main', 'Main'],
    UseCascadingExtensions = True,
    ExtensionCascadeOrder = ['.py', '.psp', '.kid', '.html'],
    ExtraPathInfo = True,
    ExtensionsToIgnore = set([
        '.pyc', '.pyo', '.tmpl', '.bak', '.py_bak',
        '.py~', '.psp~', '.kid~', '.html~', '.tmpl~'
        ]),
    ExtensionsToServe = [],
    FilesToHide = set([
        '.*', '*~', '*.bak', '*.py_bak', '*.tmpl',
        '*.pyc', '*.pyo', '__init__.*', '*.config'
        ]),
    FilesToServe = [],
    UnknownFileTypes = dict(
        ReuseServlets = True,
        Technique = 'serveContent',  # or redirectSansAdapter
        CacheContent = False,
        MaxCacheContentSize = 128*1024,
        ReadBufferSize = 32*1024
        ),
)


class EndResponse(Exception):
    """End response exception.

    Used to prematurely break out of the awake()/respond()/sleep()
    cycle without reporting a traceback. During servlet processing,
    if this exception is caught during awake() or respond() then sleep()
    is called and the response is sent. If caught during sleep(),
    processing ends and the response is sent.
    """


class Application(ConfigurableForServerSidePath):
    """The Application singleton.

    Purpose and usage are explained in the module docstring.
    """


    ## Init ##

    def __init__(self, server, useSessionSweeper=True):
        """Called only by `AppServer`, sets up the Application."""

        self._server = server
        self._serverSidePath = server.serverSidePath()

        self._imp = server._imp  # the import manager

        ConfigurableForServerSidePath.__init__(self)

        print 'Initializing Application...'
        print 'Current directory:', os.getcwd()

        if self.setting('PrintConfigAtStartUp'):
            self.printConfig()

        self.initVersions()
        self.initErrorPage()

        self._shutDownHandlers = []

        # Initialize task manager:
        if self._server.isPersistent():
            from TaskKit.Scheduler import Scheduler
            self._taskManager = Scheduler(
                daemon=True, exceptionHandler=self.handleException)
            self._taskManager.start()
        else:
            self._taskManager = None

        # Define this before initializing URLParser, so that contexts have a
        # chance to override this. Also be sure to define it before loading the
        # sessions, in case the loading of the sessions causes an exception.
        self._exceptionHandlerClass = ExceptionHandler

        self.makeDirs()
        self.initSessions()

        URLParser.initApp(self)
        self._rootURLParser = URLParser.ContextParser(self)

        if useSessionSweeper:
            self.startSessionSweeper()

    def initErrorPage(self):
        """Initialize the error page related attributes."""
        for path in (self._serverSidePath,
                os.path.dirname(os.path.abspath(__file__))):
            error404file = os.path.join(path, 'error404.html')
            try:
                self._error404 = open(error404file).read()
            except Exception:
                continue
            else:
                break
        else:
            self._error404 = None
        urls = self.setting('ErrorPage') or None
        if urls:
            try:
                errors = urls.keys()
            except AttributeError:
                errors = ['Exception']
                urls = {errors[0]: urls}
            for err in errors:
                if urls[err] and not urls[err].startswith('/'):
                    urls[err] = '/' + urls[err]
        self._errorPage = urls

    def initSessions(self):
        """Initialize all session related attributes."""
        self._sessionPrefix = self.setting('SessionPrefix') or ''
        if self._sessionPrefix:
            if self._sessionPrefix == 'hostname':
                from MiscUtils.Funcs import hostName
                self._sessionPrefix = hostName()
            self._sessionPrefix += '-'
        self._sessionTimeout = self.setting('SessionTimeout') * 60
        self._sessionName = (self.setting('SessionName') or
            self.defaultConfig()['SessionName'])
        self._autoPathSessions = self.setting('UseAutomaticPathSessions')
        self._alwaysSaveSessions = self.setting('AlwaysSaveSessions')
        self._retainSessions = self.setting('RetainSessions')
        moduleName = self.setting('SessionModule')
        className = moduleName.rsplit('.', 1)[-1]
        try:
            exec 'from %s import %s' % (moduleName, className)
            cls = locals()[className]
            if not isinstance(cls, type):
                raise ImportError
            self._sessionClass = cls
        except ImportError:
            print ("ERROR: Could not import Session class '%s'"
                " from module '%s'") % (className, moduleName)
            self._sessionClass = None
        moduleName = self.setting('SessionStore')
        if moduleName in (
                'Dynamic', 'File', 'Memcached', 'Memory', 'Redis', 'Shelve'):
            moduleName = 'Session%sStore' % moduleName
        className = moduleName.rsplit('.', 1)[-1]
        try:
            exec 'from %s import %s' % (moduleName, className)
            cls = locals()[className]
            if not isinstance(cls, type):
                raise ImportError
            self._sessions = cls(self)
        except ImportError as err:
            print ("ERROR: Could not import SessionStore class '%s'"
                " from module '%s':\n%s") % (className, moduleName, err)
            self._sessions = None

    def makeDirs(self):
        """Make sure some standard directories are always available."""
        self._cacheDir = self.serverSidePath(
            self.setting('CacheDir') or 'Cache')
        self._errorMessagesDir = self.serverSidePath(
            self.setting('ErrorMessagesDir') or 'ErrorMsgs')
        self._sessionDir = self.serverSidePath(
            self.setting('SessionStoreDir') or 'Sessions')
        for path in (self.serverSidePath('Logs'),
                self._cacheDir, self._errorMessagesDir, self._sessionDir):
            if path and not os.path.exists(path):
                os.makedirs(path)

    def initVersions(self):
        """Get and store versions.

        Initialize attributes that store the Webware and WebKit versions as
        both tuples and strings. These are stored in the Properties.py files.
        """
        from MiscUtils.PropertiesObject import PropertiesObject
        props = PropertiesObject(os.path.join(
            self.webwarePath(), 'Properties.py'))
        self._webwareVersion = props['version']
        self._webwareVersionString = props['versionString']
        props = PropertiesObject(os.path.join(
            self.webKitPath(), 'Properties.py'))
        self._webKitVersion = props['version']
        self._webKitVersionString = props['versionString']

    def taskManager(self):
        """Accessor: `TaskKit.Scheduler` instance."""
        return self._taskManager

    def startSessionSweeper(self):
        """Start session sweeper.

        Starts the session sweeper, `WebKit.Tasks.SessionTask`, which deletes
        session objects (and disk copies of those objects) that have expired.
        """
        if self._sessionTimeout:
            tm = self.taskManager()
            if tm:
                from time import time
                from Tasks import SessionTask
                task = SessionTask.SessionTask(self._sessions)
                sweepinterval = self._sessionTimeout / 10
                tm.addPeriodicAction(time() + sweepinterval, sweepinterval,
                    task, "SessionSweeper")
                print "Session sweeper has started."

    def shutDown(self):
        """Shut down the application.

        Called by AppServer when it is shutting down.  The `__del__` function
        of Application won't be called due to circular references.
        """
        print "Application is shutting down..."
        self._sessions.storeAllSessions()
        if self._server.isPersistent():
            self.taskManager().stop()
        del self._sessions
        del self._server

        # Call all registered shutdown handlers
        for shutDownHandler in self._shutDownHandlers:
            shutDownHandler()
        del self._shutDownHandlers

        print "Application has been successfully shutdown."

    def addShutDownHandler(self, func):
        """Add a shutdown handler.

        Functions added through `addShutDownHandler` will be called when
        the AppServer is shutting down. You can use this hook to close
        database connections, clean up resources, save data to disk, etc.
        """
        self._shutDownHandlers.append(func)


    ## Config ##

    def defaultConfig(self):
        """The default Application.config."""
        return defaultConfig  # defined on the module level

    def configFilename(self):
        return self.serverSidePath('Configs/Application.config')

    def configReplacementValues(self):
        return self._server.configReplacementValues()


    ## Versions ##

    def webwareVersion(self):
        """Return the Webware version as a tuple."""
        return self._webwareVersion

    def webwareVersionString(self):
        """Return the Webware version as a printable string."""
        return self._webwareVersionString

    def webKitVersion(self):
        """Return the WebKit version as a tuple."""
        return self._webKitVersion

    def webKitVersionString(self):
        """Return the WebKit version as a printable string."""
        return self._webKitVersionString


    ## Sessions ##

    def session(self, sessionId, default=NoDefault):
        """The session object for `sessionId`.

        Raises `KeyError` if session not found and no default is given.
        """
        if default is NoDefault:
            return self._sessions[sessionId]
        else:
            return self._sessions.get(sessionId, default)

    def hasSession(self, sessionId):
        """Check whether session `sessionId` exists."""
        return sessionId in self._sessions

    def sessions(self):
        """A dictionary of all the session objects."""
        return self._sessions

    def createSessionForTransaction(self, trans):
        """Get the session object for the transaction.

        If the session already exists, returns that, otherwise creates
        a new session.

        Finding the session ID is done in `Transaction.sessionId`.
        """
        debug = self.setting('Debug').get('Sessions')
        if debug:
            prefix = '>> [session] createSessionForTransaction:'
        sessId = trans.request().sessionId()
        if debug:
            print prefix, 'sessId =', sessId
        if sessId:
            try:
                session = self.session(sessId)
                if debug:
                    print prefix, 'retrieved session =', session
            except KeyError:
                trans.request().setSessionExpired(1)
                if not self.setting('IgnoreInvalidSession'):
                    raise HTTPSessionExpired
                sessId = None
        if not sessId:
            session = self._sessionClass(trans)
            self._sessions[session.identifier()] = session
            if debug:
                print prefix, 'created session =', session
        trans.setSession(session)
        return session

    def createSessionWithID(self, trans, sessionID):
        """Create a session object with our session ID."""
        session = self._sessionClass(trans, sessionID)
        # Replace the session if it didn't already exist,
        # otherwise we just throw it away.  setdefault is an atomic
        # operation so this guarantees that 2 different
        # copies of the session with the same ID never get placed into
        # the session store, even if multiple threads are calling
        # this method simultaneously.
        trans.application()._sessions.setdefault(sessionID, session)

    def sessionTimeout(self, trans):
        """Get the timeout (in seconds) for a user session.

        Overwrite to make this transaction dependent.
        """
        return self._sessionTimeout

    def sessionPrefix(self, trans):
        """Get the prefix string for the session ID.

        Overwrite to make this transaction dependent.
        """
        return self._sessionPrefix

    def sessionName(self, trans):
        """Get the name of the field holding the session ID.

        Overwrite to make this transaction dependent.
        """
        return self._sessionName

    def sessionCookiePath(self, trans):
        """Get the cookie path for this transaction.

        If not path is specified in the configuration setting,
        the servlet path is used for security reasons, see:
        http://www.net-security.org/dl/articles/cookie_path.pdf
        """
        return self.setting('SessionCookiePath') or (
            trans.request().servletPath() + '/')


    ## Misc Access ##

    def server(self):
        """Acessor: the AppServer"""
        return self._server

    def serverSidePath(self, path=None):
        """Get the server-side path.

        Returns the absolute server-side path of the WebKit application.
        If the optional path is passed in, then it is joined with the
        server side directory to form a path relative to the app server.
        """
        if path:
            return os.path.normpath(
                os.path.join(self._serverSidePath, path))
        else:
            return self._serverSidePath

    def webwarePath(self):
        """The path of the ``Webware/`` directory."""
        return self._server.webwarePath()

    def webKitPath(self):
        """The Path of the ``Webware/WebKit/`` directory."""
        return self._server.webKitPath()

    @staticmethod
    def name():
        """The name by which this was started. Usually `AppServer`."""
        return sys.argv[0]


    ## Activity Log ##

    def writeActivityLog(self, trans):
        """Write an entry to the activity log.

        Writes an entry to the script log file. Uses settings
        ``ActivityLogFilename`` and ``ActivityLogColumns``.
        """
        filename = self.serverSidePath(
            self.setting('ActivityLogFilename'))
        if os.path.exists(filename):
            f = open(filename, 'a')
        else:
            f = open(filename, 'w')
            f.write(','.join(self.setting('ActivityLogColumns')) + '\n')
        values = []
        objects = dict(application=self, transaction=trans,
            request=trans.request(), response=trans.response(),
             # don't cause creation of session here:
            servlet=trans.servlet(), session=trans._session)
        for column in self.setting('ActivityLogColumns'):
            try:
                value = valueForName(objects, column)
            except Exception:
                value = '(unknown)'
            if isinstance(value, float):
                # probably need more flexibility in the future
                value = '%0.2f' % value
            else:
                value = str(value)
            values.append(value)
        f.write(','.join(values) + '\n')
        f.close()


    ## Request Dispatching ##

    # These are the entry points from `AppServer`, which take a raw request,
    # turn it into a transaction, run the transaction, and clean up.

    def dispatchRawRequest(self, requestDict, strmOut):
        """Dispatch a raw request.

        Dispatch a request as passed from the Adapter through the AppServer.
        This method creates the request, response, and transaction object,
        then runs (via `runTransaction`) the transaction. It also catches any
        exceptions, which are then passed on to `handleExceptionInTransaction`.
        """
        request = self.createRequestForDict(requestDict)
        if request:
            trans = Transaction(application=self, request=request)
            if trans:
                request.setTransaction(trans)
                response = request.responseClass()(trans, strmOut)
                if response:
                    trans.setResponse(response)
                    self.runTransaction(trans)
                    try:
                        trans.response().deliver()
                    except ConnectionAbortedError as err:
                        trans.setError(err)
                    response.clearTransaction()
                    # release possible servlets on the stack
                    while 1:
                        servlet = request.pop()
                        if not servlet:
                            break
                        self.returnServlet(servlet)
                    # get current servlet (this may have changed)
                    servlet = trans.servlet()
                    if servlet:
                        # return the current servlet to its pool
                        self.returnServlet(servlet)
                if self.setting('LogActivity'):
                    self.writeActivityLog(trans)
            request.clearTransaction()
        return trans

    @staticmethod
    def createRequestForDict(requestDict):
        """Create request object for a given dictionary.

        Create a request object (subclass of `Request`) given the raw
        dictionary as passed by the adapter.

        The class of the request may be based on the contents of the
        dictionary (though only `HTTPRequest` is currently created),
        and the request will later determine the class of the response.

        Called by `dispatchRawRequest`.
        """
        format = requestDict['format']
        # Maybe an EmailAdapter would make a request with a format of Email,
        # and an EmailRequest would be generated. For now just CGI/HTTPRequest.
        assert format == 'CGI'
        request = HTTPRequest(requestDict)
        # The request object is stored for tracking/debugging purposes.
        requestDict['requestObject'] = request
        return request

    def runTransaction(self, trans):
        """Run transaction.

        Executes the transaction, handling HTTPException errors.
        Finds the servlet (using the root parser, probably
        `URLParser.ContextParser`, to find the servlet for the
        transaction, then calling `runTransactionViaServlet`.

        Called by `dispatchRawRequest`.
        """
        findServlet = self.rootURLParser().findServletForTransaction
        try:
            # remove the session identifier from the path
            self.removePathSession(trans)
            # determine the context and the servlet for the transaction
            servlet = findServlet(trans)
            # handle session field only now, because the name of the
            # session id field can depend on the context
            self.handlePathSession(trans)
            # now everything is set, run the transaction
            self.runTransactionViaServlet(servlet, trans)
        except EndResponse:
            pass
        except ConnectionAbortedError as err:
            trans.setError(err)
        except (KeyboardInterrupt, SystemExit):
            raise  # do not catch these here
        except:
            # For once, we use a bare except here in order to catch
            # exceptions from legacy code which are old-style classes.
            errClass, err = sys.exc_info()[:2]
            urls = {}
            while 1:
                trans.setError(err)
                isHTTPException = isinstance(err, HTTPException)
                if isHTTPException:
                    err.setTransaction(trans)
                if trans.response().isCommitted():
                    # response already committed, cannot display error
                    isHTTPException = False
                    break
                if not self._errorPage:
                    # no custom error page configured
                    break
                # get custom error page for this exception
                url = errClass and self.errorPage(errClass)
                if isHTTPException and not url:
                    # get custom error page for status code
                    code = err.code()
                    if code in self._errorPage:
                        url = self._errorPage[code]
                if not url or url in urls:
                    # If there is no custom error page configured,
                    # or we get into a circular chain of error pages,
                    # then we fall back to standard error handling.
                    break
                urls[url] = None
                # forward to custom error page
                try:
                    self.forward(trans, url)
                except EndResponse:
                    pass
                except ConnectionAbortedError as err:
                    trans.setError(err)
                except (KeyboardInterrupt, SystemExit):
                    raise  # do not catch these here
                except:
                    # Once more, catch all other kinds of exceptions here.
                    # If the custom error page itself throws an exception,
                    # display the new exception instead of the original one,
                    # so we notice that something is broken here.
                    errClass, err = sys.exc_info()[:2]
                    url = None
                if url:
                    return  # error has already been handled
            if isHTTPException:
                # display standard http error page
                trans.response().displayError(err)
            else:
                # standard error handling
                if (self.setting('EnterDebuggerOnException')
                        and sys.stdin.isatty()):
                    import pdb
                    pdb.post_mortem(sys.exc_info()[2])
                self.handleExceptionInTransaction(
                    sys.exc_info(), trans)

    @staticmethod
    def runTransactionViaServlet(servlet, trans):
        """Execute the transaction using the servlet.

        This is the `awake`/`respond`/`sleep` sequence of calls, or if
        the servlet supports it, a single `runTransaction` call (which is
        presumed to make the awake/respond/sleep calls on its own). Using
        `runTransaction` allows the servlet to override the basic call
        sequence, or catch errors from that sequence.

        Called by `runTransaction`.
        """
        trans.setServlet(servlet)
        if hasattr(servlet, 'runTransaction'):
            servlet.runTransaction(trans)
        else:
            # For backward compatibility (Servlet.runTransaction implements
            # this same sequence of calls, but by keeping it in the servlet
            # it's easier for the servlet to catch exceptions).
            try:
                trans.awake()
                trans.respond()
            finally:
                trans.sleep()

    def forward(self, trans, url):
        """Forward the request to a different (internal) URL.

        The transaction's URL is changed to point to the new servlet,
        and the transaction is simply run again.

        Output is _not_ accumulated, so if the original servlet had any output,
        the new output will _replace_ the old output.

        You can change the request in place to control the servlet you are
        forwarding to -- using methods like `HTTPRequest.setField`.
        """
        # Reset the response to a "blank slate"
        trans.response().reset()
        # Include the other servlet
        self.includeURL(trans, url)
        # Raise an exception to end processing of this request
        raise EndResponse

    def callMethodOfServlet(self, trans, url, method, *args, **kw):
        """Call method of another servlet.

        Call a method of the servlet referred to by the URL. Calls sleep()
        and awake() before and after the method call. Or, if the servlet
        defines it, then `runMethodForTransaction` is used (analogous to the
        use of `runTransaction` in `forward`).

        The entire process is similar to `forward`, except that instead of
        `respond`, `method` is called (`method` should be a string, `*args`
        and `**kw` are passed as arguments to that method).
        """
        # store current request and set the new URL
        request = trans.request()
        request.push(trans.servlet(),
            self.resolveInternalRelativePath(trans, url))
        # get new servlet
        servlet = self.rootURLParser().findServletForTransaction(trans)
        trans.setServlet(servlet)
        # call method of included servlet
        if hasattr(servlet, 'runMethodForTransaction'):
            result = servlet.runMethodForTransaction(
                trans, method, *args, **kw)
        else:
            servlet.awake(trans)
            result = getattr(servlet, method)(*args, **kw)
            servlet.sleep(trans)
        # return new servlet to its pool
        self.returnServlet(servlet)
        # restore current request
        trans.setServlet(request.pop())
        return result

    def includeURL(self, trans, url):
        """Include another servlet.

        Include the servlet given by the URL. Like `forward`,
        except control is ultimately returned to the servlet.
        """
        # store current request and set the new URL
        request = trans.request()
        request.push(trans.servlet(),
            self.resolveInternalRelativePath(trans, url))
        # get new servlet
        servlet = self.rootURLParser().findServletForTransaction(trans)
        trans.setServlet(servlet)
        # run the included servlet
        try:
            servlet.runTransaction(trans)
        except EndResponse:
            # we interpret an EndResponse in an included page to mean
            # that the current page may continue processing
            pass
        # return new servlet to its pool
        self.returnServlet(servlet)
        # restore current request
        trans.setServlet(request.pop())

    @staticmethod
    def resolveInternalRelativePath(trans, url):
        """Return the absolute internal path.

        Given a URL, return the absolute internal URL.
        URLs are assumed relative to the current URL.
        Absolute paths are returned unchanged.
        """
        if not url.startswith('/'):
            origDir = trans.request().urlPath()
            if not origDir.endswith('/'):
                origDir = os.path.dirname(origDir)
                if not origDir.endswith('/'):
                    origDir += '/'
            url = origDir + url
        # deal with . and .. in the path
        parts = []
        for part in url.split('/'):
            if parts and part == '..':
                parts.pop()
            elif part != '.':
                parts.append(part)
        return '/'.join(parts)

    @staticmethod
    def returnServlet(servlet):
        """Return the servlet to its pool."""
        servlet.close()

    def errorPage(self, errorClass):
        """Get the error page url corresponding to an error class."""
        if errorClass.__name__ in self._errorPage:
            return self._errorPage[errorClass.__name__]
        if errorClass is not Exception:
            for errorClass in errorClass.__bases__:
                url = self.errorPage(errorClass)
                if url:
                    return url

    def handleException(self):
        """Handle exceptions.

        This should only be used in cases where there is no transaction object,
        for example if an exception occurs when attempting to save a session
        to disk.
        """
        self._exceptionHandlerClass(self, None, sys.exc_info())

    def handleExceptionInTransaction(self, excInfo, trans):
        """Handle exception with info.

        Handles exception `excInfo` (as returned by `sys.exc_info()`)
        that was generated by `transaction`. It may display the exception
        report, email the report, etc., handled by
        `ExceptionHandler.ExceptionHandler`.
        """
        request = trans.request()
        editlink = (request.adapterName() + '/Admin/EditFile'
            if self.setting('IncludeEditLink') else None)
        self._exceptionHandlerClass(self, trans, excInfo,
            dict(editlink=editlink))

    def rootURLParser(self):
        """Accessor: the Root URL parser.

        URL parsing (as defined by subclasses of `URLParser.URLParser`)
        starts here. Other parsers are called in turn by this parser.
        """
        return self._rootURLParser

    def hasContext(self, name):
        """Checks whether context `name` exist."""
        return name in self._rootURLParser._contexts

    def addContext(self, name, path):
        """Add a context by named `name`, rooted at `path`.

        This gets imported as a package, and the last directory
        of `path` does not have to match the context name.
        (The package will be named `name`, regardless of `path`).

        Delegated to `URLParser.ContextParser`.
        """
        self._rootURLParser.addContext(name, path)

    @staticmethod
    def addServletFactory(factory):
        """Add a ServletFactory.

        Delegated to the `URLParser.ServletFactoryManager` singleton.
        """
        URLParser.ServletFactoryManager.addServletFactory(factory)

    def contexts(self):
        """Return a dictionary of context-name: context-path."""
        return self._rootURLParser._contexts

    _exceptionReportAttrNames = ['webwareVersion', 'webwarePath',
        'serverSidePath', 'contexts']

    def writeExceptionReport(self, handler):
        """Write extra information to the exception report.

        See `WebKit.ExceptionHandler` for more information.
        """
        handler.writeTitle(self.__class__.__name__)
        handler.writeAttrs(self, self._exceptionReportAttrNames)

    @staticmethod
    def removePathSession(trans):
        """Remove a possible session identifier from the path."""
        request = trans.request()
        # Try to get automatic path session:
        # If UseAutomaticPathSessions is enabled in Application.config,
        # Application redirects the browser to a URL with SID in path:
        # http://gandalf/a/_SID_=2001080221301877755/Examples/
        # The _SID_ part is extracted and removed from path here.
        # Note that We do not check for the exact name of the field
        # here because it may be context dependent.
        p = request._pathInfo
        if p:
            p = p.split('/', 2)
            if len(p) > 1 and not p[0] and '=' in p[1]:
                s = p[1]
                request._pathSID = s.split('=', 1)
                s += '/'
                del p[1]
                env = request.environ()
                request._pathInfo = env['PATH_INFO'] = '/'.join(p)
                for v in ('REQUEST_URI', 'PATH_TRANSLATED'):
                    if v in env:
                        env[v] = env[v].replace(s, '', 1)
            else:
                request._pathSID = None
        else:
            request._pathSID = None

    def handlePathSession(self, trans):
        """Handle the session identifier that has been found in the path."""
        request = trans.request()
        if request._pathSID:
            sessionName = self.sessionName(trans)
            if request._pathSID[0] == sessionName:
                if request.hasCookie(sessionName):
                    self.handleUnnecessaryPathSession(trans)
                request.cookies()[sessionName] = request._pathSID[1]
            else:
                if self._autoPathSessions:
                    if not request.hasCookie(sessionName):
                        self.handleMissingPathSession(trans)
        else:
            if self._autoPathSessions:
                if not request.hasCookie(self.sessionName(trans)):
                    self.handleMissingPathSession(trans)

    def handleMissingPathSession(self, trans):
        """Redirect requests without session info in the path.

        If UseAutomaticPathSessions is enabled in Application.config
        we redirect the browser to an absolute url with SID in path
        http://gandalf/a/_SID_=2001080221301877755/Examples/
        _SID_ is extracted and removed from path in HTTPRequest.py

        This is for convenient building of webapps that must not
        depend on cookie support.

        Note that we create an absolute URL with scheme and hostname
        because otherwise IIS will only cause an internal redirect.
        """
        request = trans.request()
        url = '%s://%s%s/%s=%s%s%s%s' % (request.scheme(),
            request.hostAndPort(), request.servletPath(),
            self.sessionName(trans), trans.session().identifier(),
            request.pathInfo(), request.extraURLPath() or '',
            '?' + request.queryString() if request.queryString() else '')
        if self.setting('Debug')['Sessions']:
            print ('>> [sessions] handling UseAutomaticPathSessions, '
                'redirecting to', url)
        trans.response().sendRedirect(url)
        raise EndResponse

    def handleUnnecessaryPathSession(self, trans):
        """Redirect request with unnecessary session info in the path.

        This is called if it has been determined that the request has a path
        session, but also cookies. In that case we redirect to eliminate the
        unnecessary path session.
        """
        request = trans.request()
        url = '%s://%s%s%s%s%s' % (request.scheme(),
            request.hostAndPort(), request.servletPath(),
            request.pathInfo(), request.extraURLPath() or '',
            '?' + request.queryString() if request.queryString() else '')
        if self.setting('Debug')['Sessions']:
            print ('>> [sessions] handling unnecessary path session, '
                'redirecting to', url)
        trans.response().sendRedirect(url)
        raise EndResponse
