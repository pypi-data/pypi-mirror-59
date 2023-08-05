
"""Event handler for parsing PSP tokens.

This module is called when the Parser encounters psp tokens.
It creates a generator to handle the PSP token. When the PSP
source file is fully parsed, this module calls all of the
generators in turn to output their source code.

(c) Copyright by Jay Love, 2000 (mailto:jsliv@jslove.org)

Permission to use, copy, modify, and distribute this software and its
documentation for any purpose and without fee or royalty is hereby granted,
provided that the above copyright notice appear in all copies and that
both that copyright notice and this permission notice appear in
supporting documentation or portions thereof, including modifications,
that you make.

This software is based in part on work done by the Jakarta group.
"""

import time

from Generators import *  # ResponseObject, plus all the *Generator functions


class ParseEventHandler(object):
    """This is a key class.

    It implements the handling of all the parsing elements.
    Note: This files JSP cousin is called ParseEventListener,
    I don't know why, but Handler seemed more appropriate to me.
    """

    aspace = ' '
    defaults = dict(
        BASE_CLASS = 'WebKit.Page',
        BASE_METHOD = 'writeHTML',
        imports = dict(filename='classes'),
        threadSafe = 'no',
        instanceSafe = 'yes',
        indent = 4,
        gobbleWhitespace = True,
        formatter = 'str'
    )

    def __init__(self, ctxt, parser):
        self._ctxt = ctxt
        self._gens = []
        self._reader = ctxt.getReader()
        self._writer = ctxt.getServletWriter()
        self._parser = parser
        self._imports = []
        self._importedSymbols = []
        self._baseMethod = self.defaults['BASE_METHOD']
        self._baseClasses = [self.defaults['BASE_CLASS']]
        self._threadSafe = self.defaults['threadSafe']
        self._instanceSafe = self.defaults['instanceSafe']
        self._indent = self.defaults['indent']
        self._gobbleWhitespace = self.defaults['gobbleWhitespace']
        self._formatter = self.defaults['formatter']

    def addGenerator(self, gen):
        self._gens.append(gen)

    def handleExpression(self, start, stop, attrs):
        """Flush any template data into a CharGen and then create a new ExpressionGen."""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        exp = ExpressionGenerator(self._reader.getChars(start, stop))
        self.addGenerator(exp)

    def handleCharData(self, start, stop, chars):
        """Flush character data into a CharGen."""
        if chars:
            gen = CharDataGenerator(chars)
            self.addGenerator(gen)

    def handleComment(self, start, stop):
        """Comments get swallowed into nothing."""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        return  # just eats the comment

    def handleInclude(self, attrs, param):
        """This is for includes of the form <psp:include ...>

        This function essentially forwards the request to the specified
        URL and includes that output.
        """
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = IncludeGenerator(attrs, param, self._ctxt)
        self.addGenerator(gen)

    def handleInsert(self, attrs, param):
        """This is for includes of the form <psp:insert ...>

        This type of include is not parsed, it is just inserted in the output stream.
        """
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = InsertGenerator(attrs, param, self._ctxt)
        self.addGenerator(gen)

    def importHandler(self, imports, start, stop):
        importlist = imports.split(',')
        for imp in importlist:
            if ':' in imp:
                module, symbol = imp.split(':', 1)
                self._importedSymbols.append(symbol.strip())
                implist = "from " + module + " import " + symbol
                self._imports.append(implist)
            else:
                self._imports.append('import ' + imp.strip())

    def extendsHandler(self, bc, start, stop):
        """Extends is a page directive.

        It sets the base class (or multiple base classes) for the class
        that this class will generate. The choice of base class affects
        the choice of a method to override with the BaseMethod page directive.
        The default base class is PSPPage. PSPPage inherits from Page.py.
        """
        self._baseClasses = [s.strip() for s in bc.split(',')]

    def mainMethodHandler(self, method, start, stop):
        """BaseMethod is a page directive.

        It sets the class method that the main body of this PSP page
        over-rides. The default is WriteHTML. This value should be set
        to either WriteHTML or writeBody. See the PSPPage.py and Page.py
        servlet classes for more information.
        """
        self._baseMethod = method

    def threadSafeHandler(self, value, start, stop):
        """Handle isThreadSage.

        isThreadSafe is a page directive.
        The value can be "yes" or "no".
        Default is no because the default base class,
        Page.py, isn't thread safe.
        """
        self._threadSafe = value

    def instanceSafeHandler(self, value, start, stop):
        """Handle isInstanceSafe.

        isInstanceSafe tells the Servlet engine whether it is safe
        to use object instances of this page multiple times.
        The default is "yes".

        Saying "no" here hurts performance.
        """
        self._instanceSafe = value

    def indentTypeHandler(self, type, start, stop):
        """Declare whether tabs are used to indent source code."""
        type = type.lower()
        if type not in ('tabs', 'spaces', 'braces'):
            raise TypeError('Invalid Indentation Type')
        self._writer.setIndentType(type)

    def indentSpacesHandler(self, amount, start, stop):
        """Set number of spaces used to indent in generated source."""
        self._indentSpaces = int(amount)  # don't really need this
        self._writer.setIndentSpaces(int(amount))

    def gobbleWhitespaceHandler(self, value, start, stop):
        """Declare whether whitespace between script tags are gobble up."""
        if value.lower() in ('no', 'false', '0'):
            self._gobbleWhitespace = False

    def formatterHandler(self, value, start, stop):
        """Set an alternate formatter function to use instead of str()."""
        self._formatter = value

    directiveHandlers = {
        'imports': importHandler,
        'import': importHandler,
        'extends': extendsHandler,
        'method': mainMethodHandler,
        'isThreadSafe': threadSafeHandler,
        'isInstanceSafe': instanceSafeHandler,
        'BaseClass': extendsHandler,
        'indentSpaces': indentSpacesHandler,
        'indentType': indentTypeHandler,
        'gobbleWhitespace': gobbleWhitespaceHandler,
        'formatter': formatterHandler}

    def handleDirective(self, directive, start, stop, attrs):
        """Flush any template data into a CharGen and then create a new DirectiveGen."""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        # big switch
        if directive == 'page':
            for h in attrs:
                if h in self.directiveHandlers:
                    self.directiveHandlers[h](self, attrs[h], start, stop)
                else:
                    raise ValueError('No page directive handler: %s' % h)
        elif directive == 'include':
            filename = attrs['file']
            encoding = attrs.get('encoding')
            try:
                self._reader.pushFile(filename, encoding)
            except IOError:
                raise IOError('PSP include file not found: %s' % filename)
        else:
            raise ValueError('Invalid directive: %s' % directive)

    def handleScript(self, start, stop, attrs):
        """Handle scripting elements"""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = ScriptGenerator(self._reader.getChars(start, stop), attrs)
        self.addGenerator(gen)

    def handleScriptFile(self, start, stop, attrs):
        """Python script that goes at the file/module level"""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = ScriptFileGenerator(self._reader.getChars(start, stop), attrs)
        self.addGenerator(gen)

    def handleScriptClass(self, start, stop, attrs):
        """Python script that goes at the class level"""
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = ScriptClassGenerator(self._reader.getChars(start, stop), attrs)
        self.addGenerator(gen)

    def handleEndBlock(self):
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = EndBlockGenerator()
        self.addGenerator(gen)

    def handleMethod(self, start, stop, attrs):
        self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = MethodGenerator(self._reader.getChars(start, stop), attrs)
        self.addGenerator(gen)

    def handleMethodEnd(self, start, stop, attrs):
        # self._parser.flushCharData(self.tmplStart, self.tmplStop)
        gen = MethodEndGenerator(self._reader.getChars(start, stop), attrs)
        self.addGenerator(gen)

    # --------------------------------------
    # The generation of the page begins here
    # --------------------------------------

    def beginProcessing(self):
        pass

    def endProcessing(self):
        encoding = self._ctxt.getPythonFileEncoding()
        if encoding:
            # add encoding as a hint for both Python (PEP263) and editors
            self._writer.println('# -*- coding: %s -*-' % encoding)
        self._writer.println('# Generated automatically by PSP compiler on %s'
            % time.asctime(time.localtime(time.time())))
        self._writer.println()
        self.generateHeader()
        self.generateAll('psp:file')
        self.generateDeclarations()  # overwrite this when we can handle extends
        self.generateInitPSP()
        self.generateAll('psp:class')
        self.generateAll('Declarations')
        self._writer.println('\n')
        self.generateMainMethod()
        self.optimizeCharData()
        if self._gobbleWhitespace:
            self.gobbleWhitespace()
        self.generateAll('Service')
        self._writer.println()
        self.generateFooter()

    def setTemplateInfo(self, start, stop):
        """Mark non code data."""
        self.tmplStart = start
        self.tmplStop = stop

    def generateHeader(self):
        for imp in self._imports:
            self._writer.println(imp)
        self._writer.println('import WebKit')
        self._writer.println('from WebKit import Page')
        for baseClass in self._baseClasses:
            if '.' not in baseClass and baseClass not in self._importedSymbols:
                self._writer.println('import ' + baseClass)
        self._writer.println("__orig_file__ = %r"
            % self._ctxt.getFullPspFileName())

    def generateDeclarations(self):
        # The PSP "extends" directive allows you to use a shortcut
        # -- if the module name is the same as the class name,
        # you can say "Classname" instead of "ClassName.ClassName".
        # But we can't tell right now which names are actually class names,
        # and which names are really module names that contain a class of
        # the same name. So we have to generate code that checks at runtime.
        self._writer.println()
        self._writer.println('import types')
        self._writer.println('_baseClasses = []')
        for baseClass in self._baseClasses:
            className = baseClass.rsplit('.', 1)[-1]
            self._writer.println(
                'if isinstance(%s, types.ModuleType):' % baseClass)
            self._writer.pushIndent()
            self._writer.println(
                '_baseClasses.append(%s.%s)' % (baseClass, className))
            self._writer.popIndent()
            self._writer.println('else:')
            self._writer.pushIndent()
            self._writer.println('_baseClasses.append(%s)' % baseClass)
            self._writer.popIndent()
        self._writer.println()
        # Now write the class line:
        self._writer.printChars('class ')
        self._writer.printChars(self._ctxt.getServletClassName())
        self._writer.printChars('(')
        for i in range(len(self._baseClasses)):
            if i > 0:
                self._writer.printChars(',')
            self._writer.printChars('_baseClasses[%d]' % i)
        self._writer.printChars('):')
        self._writer.printChars('\n')
        self._writer.pushIndent()
        self._writer.println('def canBeThreaded(self):')  # sadly, still needed
        self._writer.pushIndent()
        if self._threadSafe.lower() in ('no', 'false', '0'):
            self._writer.println('return False')
        else:
            self._writer.println('return True')
        self._writer.popIndent()
        self._writer.println()
        self._writer.println('def canBeReused(self):')  # sadly, still needed
        self._writer.pushIndent()
        if self._instanceSafe.lower() in ('no', 'false', '0'):
            self._writer.println('return False')
        else:
            self._writer.println('return True')
        self._writer.popIndent()
        self._writer.println()
        if not self._writer._awakeCreated:
            self._writer.println('def awake(self, trans):')
            self._writer.pushIndent()
            self._writer.println('for baseclass in self.__class__.__bases__:')
            self._writer.pushIndent()
            self._writer.println('if hasattr(baseclass, "awake"):')
            self._writer.pushIndent()
            self._writer.println('baseclass.awake(self, trans)')
            self._writer.println('break\n')
            self._writer.popIndent()  # end if statement
            self._writer.popIndent()  # end for statement
            self._writer.println('self.initPSP()\n')
            self._writer.println()
            self._writer.popIndent()
            self._writer.println()
        self._writer.println('def __includeFile(self, filename):')
        self._writer.pushIndent()
        self._writer.println('self.write(open(filename).read())')
        self._writer.popIndent()
        self._writer.println()
        return

    def generateInitPSP(self):
        self._writer.println('def initPSP(self):\n')
        self._writer.pushIndent()
        self._writer.println('pass\n')  # nothing for now
        self._writer.popIndent()
        self._writer.println()

    def generateMainMethod(self):
        # Write the output method requested with <%@ page method=... %>
        self._writer.printIndent()
        self._writer.printChars(
            'def %s(self, transaction=None):\n' % self._baseMethod)
        self._writer.pushIndent()
        self._writer.println('"""I take a WebKit.Transaction object."""')
        self._writer.println('trans = self._transaction')
        self._writer.println(ResponseObject + ' = trans.response()')
        self._writer.println('req = trans.request()')
        self._writer.println('self._%s(%s, req, trans)\n'
            % (self._baseMethod, ResponseObject))
        # Put the real output code in a function that doesn't need
        # a 'transaction' for unit tests.
        self._writer.popIndent()
        self._writer.println('def _%s(self, %s, req=None, trans=None):'
            % (self._baseMethod, ResponseObject))
        self._writer.pushIndent()
        self._writer.println(
            '"""I take a file-like object. I am useful for unit testing."""')
        self._writer.println('_formatter = %s' % self._formatter)

    def generateFooter(self):
        self._writer.popIndent()
        self._writer.println('##footer')

    def generateAll(self, phase):
        for gen in self._gens:
            if gen.phase == phase:
                gen.generate(self._writer)

    def optimizeCharData(self):
        """Optimize the CharData.

        Too many char data generators make the servlet slow.
        If the current Generator and the next are both CharData type,
        merge their data.
        """
        gens = self._gens
        count = 0
        gencount = len(gens)
        while count < gencount-1:
            if (isinstance(gens[count], CharDataGenerator)
                    and isinstance(gens[count+1], CharDataGenerator)):
                gens[count].mergeData(gens[count+1])
                gens.remove(gens[count+1])
                gencount -= 1
            else:
                count += 1

    def gobbleWhitespace(self):
        """Gobble up whitespace.

        This method looks for a character block between two PSP blocks
        that contains only whitespace. If it finds one, it deletes it.

        This is necessary so that a write() line can't sneek in between
        a if/else, try/except etc.
        """
        debug = False
        gens = self._gens
        sideClasses = (ScriptGenerator, EndBlockGenerator)
        count = 1
        gencount = len(gens)
        if debug:
            for gen in gens:
                print "Generator type = %s" % gen.__class__
        while count < gencount - 1:
            if (isinstance(gens[count], CharDataGenerator)
                    and gens[count+1].__class__ in sideClasses
                    and gens[count-1].__class__ in sideClasses):
                if checkForTextHavingOnlyGivenChars(gens[count].chars):
                    gens.remove(gens[count])
                    gencount -= 1
            count += 1


def checkForTextHavingOnlyGivenChars(text, ws=None):
    """Checks whether text contains only whitespace (or other chars).

    Does the given text contain anything other than the ws characters?
    Return true if text is only ws characters.
    """
    if ws is None:
        return text.isspace()
    else:
        for char in text:
            if char not in ws:
                return False
        else:
            return True
