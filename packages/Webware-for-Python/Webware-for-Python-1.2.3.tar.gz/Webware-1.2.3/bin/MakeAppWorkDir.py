#!/usr/bin/env python2

"""MakeAppWorkDir.py

INTRODUCTION

This utility builds a directory tree that can be used as the current
working directory of an instance of the WebKit application server.
By using a separate directory tree like this, your application can run
without needing write access etc. to the Webware directory tree, and
you can also run more than one application server at once using the
same Webware code. This makes it easy to reuse and keep Webware
updated without disturbing your applications.

USAGE

MakeAppWorkDir.py [Options] WorkDir

Options:
  -c, --context-name=...  The name for the pre-installed context.
                          By default, it will be "MyContext".
  -d, --context-dir=...   The directory where the context will be located,
                          so you can place it outside of the WorkDir.
  -l, --library=...       Other dirs to be included in the search path.
                          You may specify this option multiple times.
  -i, --gitignore         This will add .gitignore files to the WorkDir.
  -u, --user=...          The name or uid of the user to own the WorkDir.
                          This option is supported under Unix only.
  -g, --group=...         The name or gid of the group to own the WorkDir.
                          This option is supported under Unix only.

WorkDir:
  The target working directory to be created.
"""

# FUTURE
# * Add an option to immediately create a Git repository in the new directory
#   and add all relevant files to the repository. The .gitignore file should
#   be automatically created in this case, and maybe .gitattributes as well.
# * MakeAppWorkDir.py should set the admin password like install.py does.
#   At the same time, install.py should be able to do a "app-less" install,
#   from which the admin can create appdirs using MakeAppWorkDir.py.
#   The idea here is that the results of install.py should only be "shared"
#   resources, and "per-app" resources (like the admin password) should be
#   deferred (or, at least, deferrable) to MakeAppWorkDir.py.
# CREDITS
# * Contributed to Webware for Python by Robin Dunn
# * Improved by Christoph Zwerschke

import sys
import os
import stat
import re
import glob
import shutil


class MakeAppWorkDir(object):
    """Make a new application runtime directory for Webware.

    This class breaks down the steps needed to create a new runtime
    directory for Webware. That includes all the needed
    subdirectories, default configuration files, and startup scripts.
    Each step can be overridden in a derived class if needed.

    Existing files will not be overwritten, but access permissions
    will be changed accordingly in any case.
    """

    def __init__(self, webwareDir, workDir, verbose=True, osType=None,
            contextName='MyContext', contextDir='', libraryDirs=None,
            gitIgnore=False, uid=None, gid=None):
        """Initializer for MakeAppWorkDir.

        Pass in at least the Webware directory and the target working
        directory. If you pass None for contextName then the default
        context will be the the WebKit/Examples directory as usual.
        """
        self._webwareDir = webwareDir
        self._webKitDir = os.path.join(webwareDir, 'WebKit')
        self._workDir = os.path.abspath(workDir)
        self._verbose = verbose
        if osType is None:
            osType = os.name
        self._contextName = contextName
        self._contextDir = contextDir
        if libraryDirs is None:
            libraryDirs = []
        self._libraryDirs = libraryDirs
        self._osType = osType
        self._gitIgnore = gitIgnore
        self._uid = uid
        self._gid = gid

    def buildWorkDir(self):
        """These are all the steps needed to make a new runtime directory.

        You can override the steps taken here with your own methods.
        """
        if os.path.exists(self._workDir):
            self.msg("The target directory already exists.")
            self.msg("Adding everything needed for a WebKit runtime directory...")
        else:
            self.msg("Making a new WebKit runtime directory...")
        self.msg()
        self.makeDirectories()
        self.copyConfigFiles()
        self.copyOtherFiles()
        self.makeLauncherScripts()
        if self._contextName is not None:
            self.makeDefaultContext()
        if self._gitIgnore:
            self.addGitIgnore()
        self.changeOwner()
        self.printCompleted()

    def makeDirectories(self):
        """Create all the needed directories if they don't already exist."""
        self.msg("Creating the directory tree...")
        standardDirs = (
            '', 'Cache', 'Configs', 'ErrorMsgs', 'Logs', 'Sessions')
        for path in standardDirs:
            path = os.path.join(self._workDir, path)
            if os.path.exists(path):
                self.msg("\t%s already exists." % path)
            else:
                os.mkdir(path)
                self.msg("\t%s" % path)
        for path in self._libraryDirs:
            path = os.path.join(self._workDir, path)
            if os.path.exists(path):
                self.msg("\t%s already exists." % path)
            else:
                os.makedirs(path)
                open(os.path.join(path, '__init__.py'), 'w').write('#\n')
                self.msg("\t%s created." % path)

    def copyConfigFiles(self):
        """Make a copy of the config files in the Configs directory."""
        self.msg("Copying config files...")
        configs = glob.glob(os.path.join(self._webKitDir,
            'Configs', '*.config'))
        for name in configs:
            newName = os.path.join(self._workDir, "Configs",
                os.path.basename(name))
            if os.path.exists(newName):
                self.msg("\t%s already exists." % newName)
            else:
                self.msg("\t%s" % newName)
                shutil.copyfile(name, newName)
            mode = os.stat(newName)[stat.ST_MODE]
            # remove public read/write/exec perms
            os.chmod(newName, mode & 0770)
        self.msg()

    def copyOtherFiles(self):
        """Make a copy of any other necessary files in the new work dir."""
        self.msg("Copying other files...")
        otherFiles = ('AppServer', 'webkit', 'error404.html')
        for name in otherFiles:
            if name == 'AppServer':
                if self._osType == 'nt':
                    name += '.bat'
                chmod = True
            elif name == 'webkit':
                if self._osType != 'posix':
                    continue
                chmod = True
            else:
                chmod = False
            newName = os.path.join(self._workDir, os.path.basename(name))
            if os.path.exists(newName):
                self.msg("\t%s already exists." % newName)
                if chmod:
                    os.chmod(newName, 0755)
            else:
                oldName = os.path.join(self._webKitDir, name)
                if os.path.exists(oldName):
                    self.msg("\t%s" % newName)
                    shutil.copyfile(oldName, newName)
                    if chmod:
                        os.chmod(newName, 0755)
                else:
                    self.msg("\tWarning: Cannot find %r." % oldName)
        self.msg()

    def makeLauncherScripts(self):
        """Create the launcher scripts and copy the CGI adapter script."""
        self.msg("Creating the launcher scripts...")
        workDir = self._workDir
        webwareDir = self._webwareDir
        webKitDir = self._webKitDir
        libraryDirs = self._libraryDirs
        uid, gid = self._uid, self._gid
        if uid is None:
            user = None
        else:
            import pwd
            user = pwd.getpwuid(uid)[0]
        if gid is None:
            group = None
        else:
            import grp
            group = grp.getgrgid(gid)[0]
        executable = sys.executable
        for name in launcherScripts:
            if name.endswith('Service.py') and self._osType != 'nt':
                continue
            newName = os.path.join(workDir, name)
            if os.path.exists(newName):
                self.msg("\t%s already exists." % newName)
                os.chmod(newName, 0755)
            else:
                oldName = os.path.join(webKitDir, name)
                if os.path.exists(oldName):
                    self.msg("\t%s" % newName)
                    script = launcherScripts[name] % locals()
                    open(newName, "w").write(script)
                    os.chmod(newName, 0755)
                else:
                    self.msg("\tWarning: Cannot find %r." % oldName)
        name = 'WebKit.cgi'
        newName = os.path.join(workDir, os.path.basename(name))
        if os.path.exists(newName):
            self.msg("\t%s already exists." % newName)
            os.chmod(newName, 0755)
        else:
            oldName = os.path.join(webKitDir, os.path.join('Adapters', name))
            if os.path.exists(oldName):
                self.msg("\t%s" % newName)
                script = open(oldName).read()
                script = re.sub('^#!/usr/bin/env python\n',
                    '#!%s\n' % executable, script, 1)
                parameter = (('workDir', workDir), ('webwareDir', webwareDir))
                for p in parameter:
                    pattern, repl = '\n%s = .*\n' % p[0], '\n%s = %r\n' % p
                    script, n = re.subn(pattern, repl, script, 1)
                    if n != 1:
                        self.msg("\tWarning: %s cannot be set in %s."
                            % (p[0], name))
                open(newName, 'w').write(script)
                os.chmod(newName, 0755)
            else:
                self.msg("\tWarning: Cannot find %r." % oldName)
        self.msg()

    def makeDefaultContext(self):
        """Make a very simple context for the newbie user to play with."""
        self.msg("Creating default context...")
        contextDir = os.path.join(
            self._workDir,
            self._contextDir or self._contextName)
        if contextDir.startswith(self._workDir):
            configDir = contextDir[len(self._workDir):]
            while configDir[:1] in (os.sep, os.altsep):
                configDir = configDir[1:]
        else:
            configDir = contextDir
        if os.path.exists(contextDir):
            self.msg("\t%s already exists." % contextDir)
        else:
            self.msg("\t%s" % contextDir)
            os.makedirs(contextDir)
        for name in exampleContext:
            filename = os.path.join(contextDir, name)
            if os.path.exists(filename):
                self.msg("\t%s already exists." % filename)
            else:
                self.msg("\t%s" % filename)
                open(filename, "w").write(exampleContext[name])
        self.msg("Updating config for default context...")
        filename = os.path.join(self._workDir, 'Configs',
            'Application.config')
        self.msg("\t%s" % filename)
        content = open(filename).readlines()
        foundContext = 0
        with open(filename, 'w') as output:
            for line in content:
                if line.startswith("Contexts[%r] = %r\n"
                        % (self._contextName, configDir)):
                    foundContext += 1
                elif line.startswith("Contexts['default'] = "):
                    output.write("Contexts[%r] = %r\n"
                        % (self._contextName, configDir))
                    output.write("Contexts['default'] = %r\n"
                        % self._contextName)
                    foundContext += 2
                else:
                    output.write(line)
        if foundContext < 2:
            self.msg("\tWarning: Default context could not be set.")
        self.msg()

    def addGitIgnore(self):
        self.msg("Creating .gitignore files...")
        existed = False
        ignore = ('*~ *.address *.bak *.default *.log *.patch *.pid'
            '*.pstats *.pyc *.pyo *.ses *.swp')
        ignore = '\n'.join(ignore.split()) + '\n'
        filename = os.path.join(self._workDir, '.gitignore')
        if os.path.exists(filename):
            existed = True
        else:
            with open(filename, 'w') as f:
                f.write(ignore)
        ignore = '!.gitignore\n'
        for subDir in 'Cache ErrorMsgs Logs Sessions'.split():
            filename = os.path.join(self._workDir, subDir, '.gitignore')
            if os.path.exists(filename):
                existed = True
            else:
                with open(filename, 'w') as f:
                    f.write(ignore)
        if existed:
            self.msg("\tDid not change existing .gitignore file.")
        self.msg()

    def changeOwner(self):
        if self._uid is None and self._gid is None:
            return
        self.msg("Changing the ownership...")
        uid = self._uid
        if uid is None:
            uid = os.getuid()
        gid = self._gid
        if gid is None:
            gid = os.getgid()
        try:
            os.chown(self._workDir, uid, gid)
        except Exception:
            self.msg("\tWarning: The ownership could not be changed.")
        else:
            for dir, dirs, files in os.walk(self._workDir):
                for file in dirs + files:
                    path = os.path.join(dir, file)
                    os.chown(path, uid, gid)
        self.msg()

    def printCompleted(self):
        run = os.path.abspath(os.path.join(self._workDir, 'AppServer'))
        print """
Congratulations, you've just created a runtime working directory for Webware.

To start the app server you can run this command:

%s

By default the built-in HTTP server is activated. So you can immediately see
an example that has been generated for you to play with and to build upon by
pointing your browser to:

http://localhost:8080

In a productive environment, you will probably want to use Apache or another
web server instead of the built-in HTTP server. The most simple (but least
efficient) solution to do this is by using the Python WebKit.cgi CGI script.
Copy it to your web server's cgi-bin directory or anywhere else that it will
execute CGIs from. If you see import errors, you may need to modify the file
permissions on your Webware directory so that the CGI script can access it.

Have fun!
""" % run

    def msg(self, text=None):
        if self._verbose:
            if text:
                print text
            else:
                print


launcherScripts = {  # launcher scripts with adjusted parameters

'Launch.py': r"""#!%(executable)s

# You can pass several parameters on the command line
# (more info by running this with option --help)
# or you can modify the default values here
# (more info in WebKit.Launch):

workDir = None
webwareDir = %(webwareDir)r
libraryDirs = %(libraryDirs)r
runProfile = False
logFile = None
pidFile = None
user = %(user)r
group = %(group)r

import sys
sys.path.insert(0, webwareDir)

from WebKit import Launch

Launch.workDir = workDir
Launch.webwareDir = webwareDir
Launch.libraryDirs = libraryDirs
Launch.runProfile = runProfile
Launch.logFile = logFile
Launch.pidFile = pidFile
Launch.user = user
Launch.group = group

if __name__ == '__main__':
    Launch.main()
""",

'AppServerService.py': r"""#!%(executable)s

# You can adjust several parameters here
# (more info in WebKit.AppServerService):

workDir = None
webwareDir = %(webwareDir)r
libraryDirs = %(libraryDirs)r
runProfile = False
logFile = None
appServer = 'ThreadedAppServer'
serviceName = 'WebKit'
serviceDisplayName = 'WebKit Application Server'
serviceDescription = ("This is the threaded application server"
    " of the Webware for Python web framework.")
serviceDeps = []

import sys
import os
sys.path.insert(0, webwareDir)

from WebKit import AppServerService as service

class AppServerService(service.AppServerService):
    # this class must be defined here in __main__
    _svc_name_ = serviceName
    _svc_display_name_ = serviceDisplayName
    _svc_description_ = serviceDescription
    _svc_deps_ = serviceDeps
    _workDir = workDir or os.path.dirname(__file__)
    _webwareDir = webwareDir
    _libraryDirs = libraryDirs
    _runProfile = runProfile
    _logFile = logFile
    _appServer = appServer

if __name__ == '__main__':
    service.AppServerService = AppServerService
    service.main()
"""

}  # end of launcher scripts


exampleContext = {  # files copied to example context

# This is used to create a very simple sample context for the new
# work dir to give the newbie something easy to play with.

'__init__.py': r"""
def contextInitialize(appServer, path):
    # You could put initialization code here to be executed
    # when the context is loaded into WebKit.
    pass
""",

'Main.py': r"""
from WebKit.Page import Page

class Main(Page):

    def title(self):
        return 'My Sample Context'

    def writeContent(self):
        self.writeln('<h1>Welcome to Webware for Python!</h1>')
        self.writeln('''
        <p>This is a sample context generated for you and has purposely been kept
        very simple to give you something to play with to get yourself started.
        The code that implements this page is located in <b>%s</b>.</p>
        ''' % self.request().serverSidePath())
        self.writeln('''
        <p>There are more examples and documentation in the Webware distribution,
        which you can get to from here:</p>
        <ul>
        ''')
        servletPath = self.request().servletPath()
        contextName = self.request().contextName()
        for ctx in sorted(self.application().contexts()):
            if ctx in ('default', contextName) or '/' in ctx:
                continue
            self.writeln('<li><a href="%s/%s/">%s</a></li>'
                % (servletPath, ctx, ctx))
        self.writeln('</ul>')
"""

}  # end of example context files


def usage():
    """Print the docstring and exit with error."""
    print __doc__
    sys.exit(2)


def main(args=None):
    """Evaluate the command line arguments and call MakeAppWorkDir."""
    if args is None:
        args = sys.argv[1:]
    contextName = contextDir = gitIgnore = user = group = None
    libraryDirs = []
    # Get all options:
    from getopt import getopt, GetoptError
    try:
        opts, args = getopt(args, 'c:d:l:iu:g:', [
            'context-name=', 'context-dir=', 'library=',
            'gitignore', 'user=', 'group='])
    except GetoptError as error:
        print str(error)
        usage()
    for opt, arg in opts:
        if opt in ('-c', '--context-name'):
            contextName = arg
        elif opt in ('-d', '--context-dir'):
            contextDir = arg
        elif opt in ('-l', '--library'):
            libraryDirs.append(arg)
        elif opt in ('-i', '--gitignore'):
            gitIgnore = True
        elif opt in ('-u', '--user'):
            user = arg
        elif opt in ('-g', '--group'):
            group = arg
    # Get the name of the target directory:
    try:
        workDir = args.pop(0)
    except IndexError:
        usage()
    if args:  # too many parameters
        usage()
    if not contextName:
        if contextDir:
            contextName = os.path.basename(contextDir)
        else:
            contextName = 'MyContext'
    # Figure out the group id:
    gid = group
    if gid is not None:
        try:
            gid = int(gid)
        except ValueError:
            try:
                import grp
                entry = grp.getgrnam(gid)
            except KeyError:
                print 'Error: Group %r does not exist.' % gid
                sys.exit(2)
            except ImportError:
                print 'Error: Group names are supported under Unix only.'
                sys.exit(2)
            gid = entry[2]
    # Figure out the user id:
    uid = user
    if uid is not None:
        try:
            uid = int(uid)
        except ValueError:
            try:
                import pwd
                entry = pwd.getpwnam(uid)
            except KeyError:
                print 'Error: User %r does not exist.' % uid
                sys.exit(2)
            except ImportError:
                print 'Error: User names are supported under Unix only.'
                sys.exit(2)
            if not gid:
                gid = entry[3]
            uid = entry[2]
    # This assumes that this script is still located in Webware/bin:
    scriptName = sys.argv and sys.argv[0]
    if not scriptName or scriptName == '-c':
        scriptName = 'MakeAppWorkDir.py'
    binDir = os.path.dirname(os.path.abspath(scriptName))
    webwareDir = os.path.abspath(os.path.join(binDir, os.pardir))
    mawd = MakeAppWorkDir(webwareDir, workDir, True, None,
        contextName, contextDir, libraryDirs, gitIgnore, uid, gid)
    mawd.buildWorkDir()  # go!


if __name__ == '__main__':
    main()
