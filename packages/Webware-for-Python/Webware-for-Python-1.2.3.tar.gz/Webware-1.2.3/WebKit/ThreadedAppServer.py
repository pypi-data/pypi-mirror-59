#!/usr/bin/env python2

"""Threaded Application Server

The AppServer is the main process of WebKit. It handles requests for
servlets from webservers.

ThreadedAppServer uses a threaded model for handling multiple requests.

At one time there were other experimental execution models for AppServer,
but none of these were successful and have been removed.
The ThreadedAppServer/AppServer distinction is thus largely historical.

ThreadedAppServer takes the following command line arguments:

start: start the AppServer (default argument)
stop: stop the currently running AppServer
daemon: run as a daemon
ClassName.SettingName=value: change configuration settings

When started, the app server records its pid in appserver.pid.
"""

import errno
import os
import select
import socket
import sys
import threading
import traceback
import Queue

from marshal import dumps, loads
from threading import Thread, currentThread
from time import time, localtime, sleep

from ctypes import pythonapi, c_long, py_object

try:
    import fcntl
    F_GETFD, F_SETFD = fcntl.F_SETFD, fcntl.F_SETFD
except (ImportError, AttributeError):  # not Unix
    fcntl = None
else:
    try:
        FD_CLOEXEC = fcntl.FD_CLOEXEC
    except AttributeError:  # not always defined
        FD_CLOEXEC = 1

from MiscUtils.Funcs import asclocaltime
from WebUtils.Funcs import requestURI

import AppServer as AppServerModule
from PidFile import ProcessRunning
from AutoReloadingAppServer import AutoReloadingAppServer as AppServer
from ASStreamOut import ASStreamOut, ConnectionAbortedError
from HTTPExceptions import HTTPServiceUnavailable

debug = False

defaultConfig = dict(
    Host = 'localhost',  # same as '127.0.0.1'
    EnableAdapter = True,  # enable WebKit adapter
    AdapterPort = 8086,
    EnableMonitor = False,  # disable status monitoring
    SCGIPort = 8084,
    EnableSCGI = False,  # disable SCGI adapter
    MonitorPort = 8085,
    EnableHTTP = True,  # enable built-in HTTP server
    HTTPPort = 8080,
    StartServerThreads = 10,  # initial number of server threads
    MinServerThreads = 5,  # minimum number
    MaxServerThreads = 20,  # maximum number
    UseDaemonThreads = True,  # use daemonic worker threads
    MaxRequestTime = 300,  # maximum request execution time in seconds
    RequestQueueSize = 0,  # means twice the maximum number of threads
    RequestBufferSize = 8*1024,  # 8 kBytes
    ResponseBufferSize = 8*1024,  # 8 kBytes
    AddressFiles = '%s.address',  # %s stands for the protocol name
    # @@ the following setting is not yet implemented
    # SocketType = 'inet',  # inet, inet6, unix
)

# Need to know this value for communications
# (note that this limits the size of the dictionary we receive
# from the AppServer to 2,147,483,647 bytes):
intLength = len(dumps(int(1)))

# Initialize global variables
server = None
exitStatus = 0


class NotEnoughDataError(Exception):
    """Not enough data received error"""


class ProtocolError(Exception):
    """Network protocol error"""


class ThreadAbortedError(HTTPServiceUnavailable):
    """Thread aborted error"""


class RequestAbortedError(ThreadAbortedError):
    """Request aborted error"""


class RequestTooLongError(RequestAbortedError):
    """Request lasts too long error"""


class ServerShutDownError(ThreadAbortedError):
    """Server has been shut down error"""


class WorkerThread(Thread):
    """Base class for Webware worker threads that can be aborted.

    (Idea taken from: http://sebulba.wikispaces.com/recipe+thread2)
    """

    def threadID(self):
        """Return the thread's internal id."""
        try:
            return self._threadID
        except AttributeError:
            for threadID, t in threading._active.items():
                if t is self:
                    self._threadID = threadID
                    return threadID

    def abort(self, exception=ThreadAbortedError):
        """Abort the current thread by raising an exception in its context.

        A return value of one means the thread was successfully aborted,
        a value of zero means the thread could not be found,
        any other value indicates that an error has occurred.
        """
        if debug:
            print "Aborting worker thread..."
        try:
            processing = self.isAlive() and self._processing
        except AttributeError:
            processing = False
        if not processing:
            if debug:
                print "Error: Thread is not working."
        threadID = self.threadID()
        if threadID is None:
            if debug:
                print "Error: Worker thread id not found"
            return 0
        if debug:
            print "Worker thread id is", threadID
        try:
            ret = pythonapi.PyThreadState_SetAsyncExc(
                c_long(threadID), py_object(exception))
            # If it returns a number greater than one, we're in trouble,
            # and should call it again with exc=NULL to revert the effect
            if ret > 1:
                pythonapi.PyThreadState_SetAsyncExc(
                    c_long(threadID), py_object())
        except Exception:
            ret = -1
        if debug:
            if ret == 0:
                print "Error: Could not find thread", threadID
            elif ret != 1:
                print "Error: Could not abort thread", threadID
        return ret


def setCloseOnExecFlag(fd):
    """Set flag for file descriptor not to be inherited by child processes."""
    try:
        fcntl.fcntl(fd, F_SETFD, fcntl.fcntl(fd, F_GETFD) | FD_CLOEXEC)
    except IOError:
        pass


class ThreadedAppServer(AppServer):
    """Threaded Application Server.

    `ThreadedAppServer` accepts incoming socket requests, spawns a
    new thread or reuses an existing one, then dispatches the request
    to the appropriate handler (e.g., an Adapter handler, HTTP handler,
    etc., one for each protocol).

    The transaction is connected directly to the socket, so that the
    response is sent directly (if streaming is used, like if you call
    `response.flush()`). Thus the ThreadedAppServer packages the
    socket/response, rather than value being returned up the call chain.
    """


    ## Init ##

    def __init__(self, path=None):
        """Setup the AppServer.

        Create an initial thread pool (threads created with `spawnThread`),
        and the request queue, record the PID in a file, and add any enabled
        handlers (Adapter, HTTP, Monitor).
        """
        self._threadPool = []
        self._threadCount = 0
        self._threadUseCounter = []
        self._addr = {}
        self._requestID = 0
        self._socketHandlers = {}
        self._handlerCache = {}
        self._threadHandler = {}
        self._sockets = {}

        self._defaultConfig = None
        AppServer.__init__(self, path)

        try:
            threadCount = self.setting('StartServerThreads')
            self._maxServerThreads = self.setting('MaxServerThreads')
            self._minServerThreads = self.setting('MinServerThreads')
            self._useDaemonThreads = self.setting('UseDaemonThreads')
            self._requestQueueSize = self.setting('RequestQueueSize')
            if not self._requestQueueSize:
                # if not set, make queue size twice the max number of threads
                self._requestQueueSize = 2 * self._maxServerThreads
            elif self._requestQueueSize < self._maxServerThreads:
                # otherwise do not make it smaller than the max number of threads
                self._requestQueueSize = self._maxServerThreads
            self._requestBufferSize = self.setting('RequestBufferSize')
            self._responseBufferSize = self.setting('ResponseBufferSize')

            self._requestQueue = Queue.Queue(self._requestQueueSize)

            maxRequestTime = self.setting('MaxRequestTime') or None
            self._maxRequestTime = maxRequestTime
            self._checkRequestTime = None

            out = sys.stdout
            out.write('Creating %d threads' % threadCount)
            for i in range(threadCount):
                self.spawnThread()
                if not debug:
                    out.write(".")
                out.flush()
            out.write("\n")

            if self.setting('EnableAdapter'):
                self.addSocketHandler(AdapterHandler)
            if self.setting('EnableMonitor'):
                self.addSocketHandler(MonitorHandler)
            if self.setting('EnableSCGI'):
                self.addSocketHandler(SCGIHandler)
            if self.setting('EnableHTTP'):
                from HTTPServer import HTTPAppServerHandler
                self.addSocketHandler(HTTPAppServerHandler)

            self.readyForRequests()

            if maxRequestTime:
                self._checkRequestTime = time() + maxRequestTime
        except:
            AppServer.initiateShutdown(self)
            raise

    def addSocketHandler(self, handlerClass, serverAddress=None):
        """Add socket handler.

        Adds a socket handler for `serverAddress` -- `serverAddress`
        is a tuple ``(host, port)``, where ``host`` is the interface
        to connect to (for instance, the IP address on a machine with
        multiple IP numbers), and ``port`` is the port (e.g. HTTP is on
        80 by default, and Webware adapters use 8086 by default).

        The `handlerClass` is a subclass of `Handler`, and is used to
        handle the actual request -- usually returning control back
        to ThreadedAppServer in some fashion. See `Handler` for more.
        """

        if serverAddress is None:
            serverAddress = self.address(handlerClass.settingPrefix)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(serverAddress)
            sock.listen(1024)
            if fcntl:
                setCloseOnExecFlag(sock.fileno())
        except Exception:
            print "Error: Can not listen for %s on %s" % (
                handlerClass.settingPrefix, str(serverAddress))
            sys.stdout.flush()
            raise
        serverAddress = sock.getsockname()  # resolve/normalize
        self._socketHandlers[serverAddress] = handlerClass
        self._handlerCache[serverAddress] = []
        self._sockets[serverAddress] = sock
        adrStr = ':'.join(map(str, serverAddress))
        print "Listening for %s on %s" % (handlerClass.settingPrefix, adrStr)
        # write text file with server address
        adrFile = self.addressFileName(handlerClass)
        if os.path.exists(adrFile):
            print "Warning: %s already exists" % adrFile
            try:
                os.unlink(adrFile)
            except (AttributeError, OSError):  # we cannot remove the file
                if open(adrFile).read() == adrStr:
                    return  # same content, so never mind
                else:
                    print "Error: Could not remove", adrFile
                    sys.stdout.flush()
                    raise
        try:
            with open(adrFile, 'w') as f:
                f.write(adrStr)
        except IOError:
            print "Error: Could not write", adrFile
            sys.stdout.flush()
            raise

    def isPersistent(self):
        return True

    def defaultConfig(self):
        """The default AppServer.config."""
        if self._defaultConfig is None:
            self._defaultConfig = AppServer.defaultConfig(self).copy()
            # Update with ThreadedAppServer specific settings
            # as defined in defaultConfig on the module level:
            self._defaultConfig.update(defaultConfig)
        return self._defaultConfig

    _ignoreErrnos = []  # silently ignore these errors:
    for e in 'EAGAIN', 'EWOULDBLOCK', 'EINTR', 'ECONNABORTED', 'EPROTO':
        try:
            _ignoreErrnos.append(getattr(errno, e))
        except AttributeError:
            pass

    def mainloop(self, timeout=1):
        """Main thread loop.

        This is the main thread loop that accepts and dispatches
        socket requests.

        It goes through a loop as long as ``self._running > 2``.
        Setting ``self._running = 2`` asks the the main loop to end.
        When the main loop is finished, it sets ``self._running = 1``.
        When the AppServer is completely down, it sets ``self._running = 0``.

        The loop waits for connections, then based on the connecting
        port it initiates the proper Handler (e.g.,
        AdapterHandler, HTTPHandler). Handlers are reused when possible.

        The initiated handlers are put into a queue, and
        worker threads poll that queue to look for requests that
        need to be handled (worker threads use `threadloop`).

        Every so often (every 5 loops) it updates thread usage
        information (`updateThreadUsage`), and every
        ``MaxServerThreads * 2`` loops it it will manage
        threads (killing or spawning new ones, in `manageThreadCount`).
        """

        threadCheckInterval = self._maxServerThreads * 2
        threadUpdateDivisor = 5  # grab stat interval
        threadCheck = 0

        self._running = 3  # server is in the main loop now

        try:
            while self._running > 2:

                # block for timeout seconds waiting for connections
                try:
                    input, output, exc = select.select(
                        self._sockets.values(), [], [], timeout)
                except select.error as e:
                    if e[0] not in self._ignoreErrnos:
                        raise
                    if debug:
                        print "Socket select error:", e
                    continue

                for sock in input:

                    try:
                        client, addr = sock.accept()
                    except socket.error as e:
                        if e[0] not in self._ignoreErrnos:
                            raise
                        if debug:
                            print "Socket accept error:", e
                        continue

                    serverAddress = sock.getsockname()
                    try:
                        handler = self._handlerCache[serverAddress].pop()
                    except IndexError:
                        handler = self._socketHandlers[serverAddress](self,
                            serverAddress)
                    self._requestID += 1
                    handler.activate(client, self._requestID)
                    self._requestQueue.put(handler)

                if threadCheck % threadUpdateDivisor == 0:
                    self.updateThreadUsage()

                if threadCheck > threadCheckInterval:
                    threadCheck = 0
                    self.manageThreadCount()
                else:
                    threadCheck += 1

                self.abortLongRequests()
                self.restartIfNecessary()

        finally:
            self._running = 1


    ## Thread Management ##

    # These methods handle the thread pool. The AppServer pre-allocates
    # threads, and reuses threads for requests. So as more threads
    # are needed with varying load, new threads are spawned, and if there
    # are excess threads, then threads are removed.

    def updateThreadUsage(self):
        """Update the threadUseCounter list.

        Called periodically     from `mainloop`.
        """
        count = self.activeThreadCount()
        if len(self._threadUseCounter) > self._maxServerThreads:
            self._threadUseCounter.pop(0)
        self._threadUseCounter.append(count)

    def activeThreadCount(self):
        """Get a snapshot of the number of threads currently in use.

        Called from `updateThreadUsage`.
        """
        count = 0
        for t in self._threadPool:
            if t._processing:
                count += 1
        return count

    def manageThreadCount(self):
        """Adjust the number of threads in use.

        From information gleened from `updateThreadUsage`, we see about how
        many threads are being used, to see if we have too many threads or
        too few. Based on this we create or absorb threads.
        """

        # @@: This algorithm needs work. The edges (i.e. at the
        # minserverthreads) are tricky. When working with this,
        # remember thread creation is *cheap*.

        average = max = 0

        if debug:
            print "ThreadUse Samples:", self._threadUseCounter
        for i in self._threadUseCounter:
            average += i
            if i > max:
                max = i
        average /= len(self._threadUseCounter)
        if debug:
            print "Average Thread Use: ", average
            print "Max Thread Use: ", max
            print "ThreadCount: ", self._threadCount

        if len(self._threadUseCounter) < self._maxServerThreads:
            return  # not enough samples

        margin = self._threadCount / 2  # smoothing factor
        if debug:
            print "Margin:", margin

        if (average > self._threadCount - margin
                and self._threadCount < self._maxServerThreads):
            # Running low: double thread count
            n = min(self._threadCount,
                self._maxServerThreads - self._threadCount)
            if debug:
                print "Adding %s threads" % n
            for i in range(n):
                self.spawnThread()
        elif (average < self._threadCount - margin
                and self._threadCount > self._minServerThreads):
            n = min(self._threadCount - self._minServerThreads,
                self._threadCount - max)
            self.absorbThread(n)
        else:
            # cleanup any stale threads that we killed but haven't joined
            self.absorbThread(0)

    def spawnThread(self):
        """Create a new worker thread.

        Worker threads poll with the `threadloop` method.
        """
        if debug:
            print "Spawning new thread"
        t = WorkerThread(target=self.threadloop)
        t._processing = False
        if self._useDaemonThreads:
            t.setDaemon(True)
        t.start()
        self._threadPool.append(t)
        self._threadCount += 1
        if debug:
            print "New thread spawned, threadCount =", self._threadCount

    def absorbThread(self, count=1):
        """Absorb a thread.

        We do this by putting a None on the Queue.
        When a thread gets it, that tells it to exit.

        We also keep track of the threads, so after killing
        threads we go through all the threads and find the
        thread(s) that have exited, so that we can take them
        out of the thread pool.
        """
        for i in range(count):
            self._requestQueue.put(None)
            # _threadCount is an estimate, just because we
            # put None in the queue, the threads don't immediately
            # disappear, but they will eventually.
            self._threadCount -= 1
        for t in self._threadPool:
            # There may still be a None in the queue, and some
            # of the threads we want gone may not yet be gone.
            # But we'll pick them up later -- they'll wait.
            if not t.isAlive():
                t.join()  # don't need a timeout, it isn't alive
                self._threadPool.remove(t)
                if debug:
                    print "Thread absorbed, real threadCount =", len(self._threadPool)

    def abortRequest(self, requestID, exception=RequestAbortedError):
        """Abort a request by raising an exception in its worker thread.

        A return value of one means the thread was successfully aborted,
        a value of zero means the thread could not be found,
        any other value indicates that an error has occurred.
        """
        verbose = self._verbose
        if verbose:
            print "Aborting request", requestID
        for t, h in self._threadHandler.items():
            try:
                handlerRequestID = h._requestID
            except AttributeError:
                handlerRequestID = None
            if requestID == handlerRequestID:
                t._abortHandler = h
                try:
                    if self._threadHandler[t] is not h:
                        # request already finished in the meantime
                        raise KeyError
                    ret = t.abort(exception)
                except Exception:
                    ret = 0
                t._abortHandler = None
                break
        else:
            ret = 0
        if verbose:
            if ret == 0:
                print "Error: Could not find thread for this request"
            elif ret == 1:
                print "The worker thread for this request has been aborted"
            else:
                print "Error: Could not abort thread for this request"
        return ret

    def abortLongRequests(self):
        """Check for long-running requests and cancel these.

        The longest allowed execution time for requests is controlled
        by the MaxRequestTime setting.
        """
        if self._checkRequestTime is None:
            return
        currentTime = time()
        if currentTime > self._checkRequestTime:
            if debug:
                print "Checking for long-running requests"
            verbose = self._verbose
            minRequestTime = currentTime - self._maxRequestTime
            for t, h in self._threadHandler.items():
                try:
                    requestDict = h._requestDict
                    requestID = requestDict['requestID']
                    requestTime = requestDict['time']
                except (AttributeError, KeyError):
                    continue
                if requestTime < minRequestTime:
                    t._abortHandler = h
                    try:
                        if self._threadHandler[t] is not h:
                            # request already finished in the meantime
                            raise KeyError
                        if verbose:
                            print "Aborting long-running request", requestID
                        t.abort(RequestTooLongError)
                    except Exception:
                        pass
                    t._abortHandler = None
                elif requestTime < currentTime:
                    currentTime = requestTime
            self._checkRequestTime = currentTime + self._maxRequestTime


    ## Worker Threads ##

    def threadloop(self):
        """The main loop for worker threads.

        Worker threads poll the `_requestQueue` to find a request handler
        waiting to run. If they find a None in the queue, this thread has
        been selected to die, which is the way the loop ends.

        The handler object does all the work when its `handleRequest` method
        is called.

        `initThread` and `delThread` methods are called at the beginning and
        end of the thread loop, but they aren't being used for anything
        (future use as a hook).
        """
        self.initThread()
        t = currentThread()
        t._processing = False
        t._abortHandler = None
        try:
            while 1:
                try:
                    handler = self._requestQueue.get()
                except Queue.Empty:
                    continue
                if handler is None:
                    # None means time to quit
                    break
                try:
                    t._processing = True
                    self._threadHandler[t] = handler
                    try:
                        handler.handleRequest()
                    except ThreadAbortedError:
                        print "Worker thread has been aborted"
                    except Exception:
                        print "Exception in worker thread"
                        traceback.print_exc(file=sys.stderr)
                    del self._threadHandler[t]
                    t._processing = False
                finally:
                    handler.close()
                while t._abortHandler is handler:
                    # this handler is to be aborted,
                    # so don't handle another request now
                    sleep(0.1)
        finally:
            try:
                del self._threadHandler[t]
                t._processing = False
            except KeyError:
                pass
            self.delThread()
        if debug:
            print "Quitting", t

    def initThread(self):
        """Initialize thread.

        Invoked immediately by threadloop() as a hook for subclasses.
        This implementation does nothing and subclasses need not invoke super.
        """
        pass

    def delThread(self):
        """Delete thread.

        Invoked immediately by threadloop() as a hook for subclasses.
        This implementation does nothing and subclasses need not invoke super.
        """
        pass


    ## Shutting Down ##

    def shutDown(self):
        """Called on shutdown.

        Also calls `AppServer.shutDown`, but first closes all sockets
        and tells all the threads to die.
        """
        print "ThreadedAppServer is shutting down..."
        if self._running > 2:
            self._running = 2  # ask main loop to finish
            self.awakeSelect()  # unblock select call in mainloop()
            sys.stdout.flush()
            for i in range(30):  # wait at most 3 seconds for shutdown
                if self._running < 2:
                    break
                sleep(0.1)
        if self._sockets:
            # Close all sockets now:
            for sock in self._sockets.values():
                sock.close()
        if self._socketHandlers:
            # Remove the text files with the server addresses:
            for handler in self._socketHandlers.values():
                adrFile = self.addressFileName(handler)
                if os.path.exists(adrFile):
                    try:
                        os.unlink(adrFile)
                    except (AttributeError, OSError):
                        print "Warning: Could not remove", adrFile
        # Tell all threads to end:
        for i in range(self._threadCount):
            self._requestQueue.put(None)
        # Join all threads:
        closeTime = time() + 3
        for t in self._threadPool:
            timeout = max(0.1, closeTime - time())
            try:
                t.join(timeout)
            except Exception:
                pass
        # Check whether all threads have ended:
        for t in self._threadPool:
            if t.isAlive():
                if debug:
                    print "Hanging worker thread", t.threadID()
                running = True
                break
        else:
            running = False
        if running:
            # Abort all remaining threads:
            print "Aborting hanging worker threads..."
            for t in self._threadPool:
                if t.isAlive():
                    t.abort(ServerShutDownError)
            # Join remaining threads:
            closeTime = time() + 3
            for t in self._threadPool:
                if t.isAlive():
                    timeout = max(0.1, closeTime - time())
                    try:
                        t.join(timeout)
                    except Exception:
                        pass
            # Check whether remaining threads have ended:
            for t in self._threadPool:
                if t.isAlive():
                    if debug:
                        print "Warning: Could not abort thread", t.threadID()
                    else:
                        print "Warning: Could not abort all worker threads"
                    break
            else:
                print "Hanging worker threads have been aborted."
                running = False
        # Call super's shutdown:
        AppServer.shutDown(self)

    def awakeSelect(self):
        """Awake the select() call.

        The `select()` in `mainloop()` is blocking, so when
        we shut down we have to make a connect to unblock it.
        Here's where we do that.
        """
        for host, port in self._sockets:
            if host == '0.0.0.0':
                # Can't connect to 0.0.0.0; use 127.0.0.1 instead
                host = '127.0.0.1'
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.connect((host, port))
                sock.close()
            except Exception:
                pass


    ## Misc ##

    def address(self, settingPrefix):
        """Get host address.

        The address for the Adapter (Host/interface, and port),
        as taken from ``Configs/AppServer.config``,
        settings ``Host`` and ``AdapterPort``.
        """
        try:
            return self._addr[settingPrefix]
        except KeyError:
            host = self.setting(settingPrefix + 'Host', self.setting('Host'))
            port = self.setting(settingPrefix + 'Port')
            self._addr[settingPrefix] = (host, port)
            return self._addr[settingPrefix]

    def addressFileName(self, handlerClass):
        """Get the name of the text file with the server address."""
        return self.serverSidePath(
            self.setting('AddressFiles') % handlerClass.protocolName)


class Handler(object):
    """A very general socket handler.

    Handler is an abstract superclass -- specific protocol implementations
    will subclass this. A Handler takes a socket to interact with, and
    creates a raw request.

    Handlers will be reused. When a socket is received `activate` will be
    called -- but the handler should not do anything, as it is still running
    in the main thread. The handler is put into a queue, and a worker thread
    picks it up and runs `handleRequest`, which subclasses should override.

    Several methods are provided which are typically used by subclasses.
    """

    def __init__(self, server, serverAddress):
        """Create a new socket handler.

        Each handler is attached to a specific host and port,
        and of course to the AppServer.
        """
        self._server = server
        self._serverAddress = serverAddress
        self._verbose = server._verbose
        self._silentURIs = server._silentURIs

    def activate(self, sock, requestID):
        """Activate the handler for processing the request.

        `sock` is the incoming socket that this handler will work with,
        and `requestID` is a serial number unique for each request.

        This isn't where work gets done -- the handler is queued after this,
        and work is done when `handleRequest` is called.
        """
        self._requestID = requestID
        self._sock = sock

    def close(self):
        """Close the socket.

        Called when the handler is finished. Closes the socket and
        returns the handler to the pool of inactive handlers.
        """
        self._sock = None
        self._server._handlerCache[self._serverAddress].append(self)

    def receiveDict(self):
        """Receive a dictionary from the socket.

        Utility function to receive a marshalled dictionary from the socket.
        Returns None if the request was empty.
        """
        chunks = []
        missing = intLength
        while missing > 0:
            block = self._sock.recv(missing)
            if not block:
                self._sock.close()
                if not chunks:
                    # We probably awakened due to awakeSelect being called.
                    return None
                # We got a partial request -- something went wrong.
                raise NotEnoughDataError(
                    'received only %d of %d bytes when expecting dict length' %
                    (intLength - missing, intLength))
            chunks.append(block)
            missing -= len(block)
        chunks = ''.join(chunks)
        try:
            dictLength = loads(chunks)
        except (ValueError, EOFError) as msg:
            if chunks[:3] == 'GET':
                # Common error: client is speaking HTTP.
                while msg and len(chunks) < 8192:
                    block = self._sock.recv(1)
                    if not block:
                        break
                    chunks += block
                    if chunks.endswith(('\r\r', '\n\n', '\r\n\r\n')):
                        msg = None
            if msg:
                print "ERROR:", msg
            else:
                print "ERROR: HTTP GET from WebKit adapter port."
                self._sock.sendall('''\
HTTP/1.0 505 HTTP Version Not Supported\r
Content-Type: text/plain\r
\r
Error: Invalid AppServer protocol.\r
Sorry, I don't speak HTTP. You must connect via an adapter.\r
See the Troubleshooting section of the WebKit Install Guide.\r''')
            self._sock.close()
            print ("       You can only connect to %s via an adapter"
                " like mod_webkit or wkcgi.") % (self._serverAddress[1],)
            return None
        if not isinstance(dictLength, int):
            self._sock.close()
            raise ProtocolError("Invalid AppServer protocol")
        chunks = []
        missing = dictLength
        while missing > 0:
            block = self._sock.recv(missing)
            if not block:
                self._sock.close()
                raise NotEnoughDataError(
                    'received only %d of %d bytes when expecting dict' %
                    (dictLength - missing, dictLength))
            chunks.append(block)
            missing -= len(block)
        chunks = ''.join(chunks)
        return loads(chunks)

    def handleRequest(self):
        """Handle a raw request.

        This is where the work gets done. Subclasses should override.
        """
        pass

    def startRequest(self, requestDict=None):
        """Track start of a raw request.

        Subclasses can use and override this method.
        """
        requestDict = requestDict or {}
        requestID = self._requestID
        requestTime = requestDict.get('time') or time()
        requestDict['requestID'] = requestID
        requestDict['time'] = requestTime
        # The request object is stored for tracking/debugging purposes.
        self._requestDict = requestDict
        if self._verbose:
            env = requestDict.get('environ')
            uri = requestURI(env) if env else '-'
            if not self._silentURIs or not self._silentURIs.search(uri):
                requestDict['verbose'] = True
                requestTime = localtime(requestTime)[:6]
                print '%5d  %4d-%02d-%02d %02d:%02d:%02d  %s' % (
                    (requestID,) + requestTime + (uri,))

    def endRequest(self, error=None):
        """Track end of a raw request.

        Subclasses can use and override this method.
        """
        if self._verbose:
            requestDict = self._requestDict
            if requestDict.get('verbose'):
                requestID = requestDict['requestID']
                duration = round((time() - requestDict['time'])*1000)
                if not error:
                    env = requestDict.get('environ')
                    error = requestURI(env) if env else '-'
                print '%5d  %14.0f msec  %s\n' % (
                    requestID, duration, error)


class MonitorHandler(Handler):
    """Monitor server status.

    Monitor is a minimal service that accepts a simple protocol,
    and returns a value indicating the status of the server.

    The protocol passes a marshalled dict, much like the Adapter
    interface, which looks like ``{'format': 'CMD'}``, where CMD
    is a command (``STATUS`` or ``QUIT``). Responds with a simple
    string, either the number of requests we've received (for
    ``STATUS``) or ``OK`` for ``QUIT`` (which also stops the server).
    """
    # @@ 2003-03 ib: we should have a RESTART command, and
    # perhaps better status indicators (number of threads, etc).

    protocolName = 'monitor'
    settingPrefix = 'Monitor'

    def handleRequest(self):
        requestDict = self.receiveDict()
        if not requestDict:
            return

        requestDict['environ'] = {'REQUEST_URI': '*%s %s*'
            % (self.settingPrefix, requestDict['format'])}
        self.startRequest(requestDict)

        conn = self._sock
        if requestDict['format'] == "STATUS":
            conn.send(str(self._server._requestID))
        elif requestDict['format'] == 'QUIT':
            conn.send("OK")
            conn.close()
            self._server.shutDown()


class TASStreamOut(ASStreamOut):
    """Response stream for ThreadedAppServer.

    The `TASStreamOut` class streams to a given socket, so that when `flush`
    is called and the buffer is ready to be written, it sends the data from the
    buffer out on the socket. This is the response stream used for requests
    generated by ThreadedAppServer.
    """

    _ignoreErrnos = []  # silently ignore these errors:
    for e in 'EPIPE', 'ECONNABORTED', 'ECONNRESET':
        try:
            _ignoreErrnos.append(getattr(errno, e))
        except AttributeError:
            pass

    def __init__(self, sock, autoCommit=False, bufferSize=8192):
        """Create stream.

        We get an extra `sock` argument, which is the socket which we'll
        stream output to (if we're streaming).
        """
        ASStreamOut.__init__(self, autoCommit, bufferSize)
        self._socket = sock

    def flush(self):
        """Flush stream.

        Calls `ASStreamOut.ASStreamOut.flush`, and if that returns True
        (indicating the buffer is full enough) then we send data from
        the buffer out on the socket.
        """
        result = ASStreamOut.flush(self)
        if result:  # a true return value means we can send
            reslen = len(self._buffer)
            sent = 0
            bufferSize = self._bufferSize
            while sent < reslen:
                try:
                    sent += self._socket.send(
                        self._buffer[sent:sent+bufferSize])
                except socket.error as e:
                    if debug or e[0] not in self._ignoreErrnos:
                        print "StreamOut Error:", e
                    self._closed = True
                    raise ConnectionAbortedError
            self.pop(sent)


class AdapterHandler(Handler):
    """Adapter handler.

    Handles the Adapter protocol (as used in mod_webkit, wkcgi,
    WebKit.cgi, HTTPAdapter, etc). This protocol passes a marshalled
    dictionary which contains the keys ``format`` and ``environ``.
    ``format`` is currently always the string ``CGI``, and ``environ``
    is a dictionary of string: string, with values like those passed
    in the environment to a CGI request (QUERY_STRING, HTTP_HOST, etc).

    The handler adds one more key, ``input``, which contains a file
    object based off the socket, which contains the body of the
    request (the POST data, for instance). It's left to Application
    to handle that data.
    """
    protocolName = 'adapter'
    settingPrefix = 'Adapter'

    def handleRequest(self):
        """Handle request.

        Creates the request dictionary, and creates a `TASStreamOut` object
        for the response, then calls `Application.dispatchRawRequest`, which
        does the rest of the work (here we just clean up after).
        """
        requestDict = self.receiveDict()
        if not requestDict:
            return

        self.startRequest(requestDict)
        requestDict['input'] = self.makeInput()

        streamOut = TASStreamOut(self._sock,
            bufferSize=self._server._responseBufferSize)
        transaction = self._server._app.dispatchRawRequest(
            requestDict, streamOut)
        try:
            streamOut.close()
            aborted = False
        except ConnectionAbortedError:
            aborted = True

        try:
            self._sock.shutdown(1)
            self._sock.close()
        except Exception:
            pass

        self.endRequest(aborted and '*connection aborted*')

        transaction._application = None
        transaction.die()
        del transaction

    def makeInput(self):
        """Create a file-like object from the socket."""
        return self._sock.makefile("rb", self._server._requestBufferSize)


class SCGIHandler(AdapterHandler):
    """SCGI handler.

    Modified Adapter handler speaking the SCGI protocol.
    """
    protocolName = 'scgi'
    settingPrefix = 'SCGI'

    def receiveDict(self):
        """Receive a dictionary from the socket.

        Utility function to receive the SCGI headers from the socket.
        Returns None if the request was empty.
        """
        chunk = ''
        while 1:
            c = self._sock.recv(1)
            if not c and not chunk:
                self._sock.close()
                return None
            if c == ':':
                break
            else:
                chunk += c
            if len(chunk) > 12:
                break
        try:
            if len(chunk) > 12 or not chunk.isdigit():
                raise ValueError('Malformed SCGI netstring')
            dictLength = long(chunk)
        except ValueError as msg:
            if chunk[:3] == 'GET':
                # Common error: client is speaking HTTP.
                while msg and len(chunk) < 8192:
                    block = self._sock.recv(1)
                    if not block:
                        break
                    chunk += block
                    if chunk.endswith(('\r\r', '\n\n', '\r\n\r\n')):
                        msg = None
            if msg:
                print "ERROR:", msg
            else:
                print "ERROR: HTTP GET from SCGI adapter port."
                self._sock.sendall('''\
HTTP/1.0 505 HTTP Version Not Supported\r
Content-Type: text/plain\r
\r
Error: Invalid AppServer protocol.\r
Sorry, I don't speak HTTP. You must connect via an SCGI adapter.\r
See the Troubleshooting section of the WebKit Install Guide.\r''')
            self._sock.close()
            print ("       You can only connect to %s via an adapter"
                " like mod_scgi or pyscgi." % self._serverAddress[1])
            return None
        chunk = ''
        missing = dictLength
        while missing > 0:
            block = self._sock.recv(missing)
            if not block:
                self._sock.close()
                raise NotEnoughDataError('received only %d of %d bytes'
                    ' when receiving netstring' % (len(chunk), dictLength))
            chunk += block
            missing -= len(block)
        if self._sock.recv(1) != ',':
            self._sock.close()
            raise ProtocolError('Missing SCGI netstring terminator')
        items = chunk.split('\0')[:-1]
        environ = {}
        try:
            for i in range(0, len(items), 2):
                environ[items[i]] = items[i+1]
        except IndexError:
            raise ProtocolError('Malformed SCGI headers')
        return dict(format='CGI', time=time(), environ=environ)


# Determines whether the main look should run in another thread.
# On Win NT/2K/XP, we run the mainloop in a different thread because
# it's not safe for Ctrl-C to be caught while manipulating the queues.
# It's not safe on Linux either, but there, it appears that Ctrl-C will
# trigger an exception in ANY thread, so this fix doesn't help.
def runMainLoopInThread():
    return os.name == 'nt'

# Set to False in DebugAppServer so Python debuggers can trap exceptions:
doesRunHandleExceptions = True


class RestartAppServerError(Exception):
    """Raised by DebugAppServer when needed."""
    pass


_chdir = os.chdir

def chdir(path, force=False):
    """Execute os.chdir() with safety provision."""
    if not force:
        raise RuntimeError(
            "You cannot reliably use os.chdir() in a threaded environment.\n"
            + 16 * " "
            + "Set force=True if you want to do it anyway (using a lock).")
    _chdir(path)


## Script usage ##

def run(workDir=None):
    """Start the server (`ThreadedAppServer`).

    `workDir` is the server-side path for the server, which may not be
    the ``Webware/WebKit`` directory (though by default it is).

    After setting up the ThreadedAppServer we call `ThreadedAppServer.mainloop`
    to start the server main loop. It also catches exceptions as a last resort.
    """
    global server
    server = None
    global exitStatus
    exitStatus = 0
    os.chdir = chdir  # inhibit use of os.chdir()
    runAgain = True
    while runAgain:  # looping in support of RestartAppServerError
        try:
            try:
                runAgain = False
                server = ThreadedAppServer(workDir)
                if runMainLoopInThread():
                    # catch the exception raised by sys.exit so
                    # that we can re-call it in the main thread.
                    def _windowsmainloop():
                        global exitStatus
                        try:
                            server.mainloop()
                        except SystemExit as e:
                            exitStatus = e[0]
                    # Run the server thread
                    server._running = 2
                    t = Thread(target=_windowsmainloop)
                    t.start()
                    try:
                        while server._running > 1:
                            try:
                                sleep(1)  # wait for interrupt
                            except Exception:
                                if server._running < 3:
                                    raise  # shutdown
                    finally:
                        t.join()
                else:
                    server.mainloop()
                sys.exit(exitStatus)
            except RestartAppServerError:
                print
                print "Restarting AppServer:"
                sys.stdout.flush()
                sys.stderr.flush()
                runAgain = True
            except SystemExit as e:
                print
                print "Exiting AppServer%s." % (
                    ' for reload' if e[0] == 3 else '')
                exitStatus = e[0]
            except KeyboardInterrupt:
                print
                print "Exiting AppServer due to keyboard interrupt."
                exitStatus = 0
            except Exception as e:
                if isinstance(e, IOError) and e[0] == errno.EINTR:
                    print
                    print "Exiting AppServer due to interrupt signal."
                    exitStatus = 0
                else:
                    if doesRunHandleExceptions:
                        if not server and isinstance(e, ProcessRunning):
                            print "Error:", str(e)
                        else:
                            print
                            traceback.print_exc()
                            print
                            print "Exiting AppServer due to above exception."
                        exitStatus = 1
                    else:
                        raise
        finally:
            sys.stdout.flush()
            sys.stderr.flush()
            if server and server._running:
                server.initiateShutdown()
                server._closeThread.join()
            AppServerModule.globalAppServer = None
    sys.stdout.flush()
    sys.stderr.flush()
    os.chdir = _chdir  # allow use of os.chdir() again
    return exitStatus


# Signal handlers

def shutDown(signum, frame):
    """Signal handler for shutting down the server."""
    print
    print "App server has been signaled to shutdown."
    if server and server._running > 2:
        print "Shutting down at", asclocaltime()
        sys.stdout.flush()
        server._running = 2
        if signum == SIGINT:
            raise KeyboardInterrupt
        elif signum == SIGHUP:
            sys.exit(3)  # force reload
        else:
            sys.exit(0)  # normal exit
    else:
        print "No running app server was found."


def threadDump(signum, frame):
    """Signal handler for dumping thread stack frames to stdout."""
    print
    print "App server has been signaled to attempt a thread dump."
    print
    print "Thread stack frame dump at", asclocaltime()
    sys.stdout.flush()
    frames = sys._current_frames()
    print
    print "-" * 79
    print
    for threadID in sorted(frames):
        frame = frames[threadID]
        print "Thread ID: %d (reference count = %d)" % (
            threadID, sys.getrefcount(frame))
        print ''.join(traceback.format_list(traceback.extract_stack(frame)))
    print "-" * 79
    sys.stdout.flush()

import signal

# Shutdown signals

try:
    SIGHUP = signal.SIGHUP
    signal.signal(SIGHUP, shutDown)
except AttributeError:
    SIGHUP = None
try:
    SIGTERM = signal.SIGTERM
    signal.signal(SIGTERM, shutDown)
except AttributeError:
    SIGTERM = None
try:
    # this is Ctrl-C on Windows
    SIGINT = signal.SIGINT
    signal.signal(SIGINT, shutDown)
except AttributeError:
    SIGINT = None

# Signals for creating a thread dump

try:
    SIGQUIT = signal.SIGQUIT
    signal.signal(SIGQUIT, threadDump)
except AttributeError:
    SIGQUIT = None
try:
    # this is Ctrl-Break on Windows (not Cygwin)
    SIGBREAK = signal.SIGBREAK
    signal.signal(SIGBREAK, threadDump)
except AttributeError:
    SIGBREAK = None


# Command line interface

import re

settingRE = re.compile(
    r'^(?:--)?([a-zA-Z][a-zA-Z0-9]*\.[a-zA-Z][a-zA-Z0-9]*)=')

from MiscUtils import Configurable

usage = re.search('\n.* arguments:\n\n(.*\n)*?\n', __doc__).group(0)


def main(args):
    """Command line interface.

    Run by `Launch`, this is the main entrance and command-line interface
    for ThreadedAppServer.
    """
    function = run
    daemon = False
    workDir = None
    for arg in args:
        if settingRE.match(arg):
            match = settingRE.match(arg)
            name = match.group(1)
            value = arg[match.end():]
            Configurable.addCommandLineSetting(name, value)
        elif arg == "stop":
            function = AppServerModule.stop
        elif arg == "daemon":
            daemon = True
        elif arg == "start":
            pass
        elif arg[:8] == "workdir=":
            workDir = arg[8:]
        else:
            print usage
            return
    if daemon:
        if os.name == "posix":
            pid = os.fork()
            if pid:
                sys.exit()
        else:
            print "Daemon mode not available on your OS."
    return function(workDir=workDir)
