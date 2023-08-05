"""MixIns

This file contains "mix-in" classes that are mixed in with classes
found in MiddleKit.Core and .Run. The mix-ins are named directly
after their target classes, which is how they get bound in InstallMixIns().

The InstallMixIns() functions is called from this module.
So all you need do is import this module to make the mix-ins take effect.
This is done in __init__.py.

If you add another mix-in then update the list of names found
in InstallMixIns().
"""

from WebUtils.Funcs import htmlEncode


def splitWords(s):
    res = []
    for c in s:
        if c.upper() == c:
            res.append(' ')
            res.append(c.lower())
        else:
            res.append(c)
    return ''.join(res)


class ObjectStore(object):

    def htObjectsOfClassNamed(self, className):
        objs = self.fetchObjectsOfClass(className)
        return self.htObjectsInList(objs, className)

    def htObjectsInList(self, objs, adjective):
        """Get HTML for list of objects.

        Returns an HTML string for a list of MiddleKit objects
        and their attributes. The adjective describes the type
        of objects and is used in the output (for example 'Customer').
        This is a utility method for use by anyone.
        """
        if objs is None:
            objs = []
        ht = []
        suffix = ('s', '')[len(objs) == 1]
        ht.append('<span class="TablePrefix">%i %s object%s</span>'
            % (len(objs), adjective, suffix))
        ht.append('<table class="ObjectsTable">')
        if objs:
            klass = objs[0].klass()
            ht.append(klass.htHeadingsRow())
            for obj in objs:
                newKlass = obj.klass()
                if newKlass != klass:
                    # If we hit a new class, write new headings
                    klass = newKlass
                    ht.append(klass.htHeadingsRow())
                ht.append(obj.htAttrsRow())
        else:
            ht.append('<tr><td class="NoObjectsCell">'
                'No %s objects.</td></tr>' % adjective)
        ht.append('</table>\n')
        return ''.join(ht)


class Klass(object):

    def htHeadingsRow(self):
        ht = ['<tr>',
              '<th class="TableHeading">class</th>',
              '<th class="TableHeading">serial</th>']
        for attr in self.allAttrs():
            heading = splitWords(attr.name())
            ht.append('<th class="TableHeading">%s</th>' % heading)
        ht.append('</tr>\n')
        return ''.join(ht)


class MiddleObject(object):

    def htAttrsRow(self):
        ht = ['<tr>',
              '<td class="TableData">%s</td>' % self.__class__.__name__,
              '<td class="TableData">%i</td>' % self.serialNum()]
        for attr in self.klass().allAttrs():
            value = getattr(self, '_' + attr.name())
            ht.append('<td class="TableData">%s</td>'
                % attr.htValue(value, self))
        ht.append('</tr>\n')
        return ''.join(ht)

    def htObjectsInList(self, listName, coalesce=1):
        klassList = self.valueForKey(listName)
        # We coalesce the classes together and present in alphabetical order
        if klassList is not None and coalesce:
            klasses = {}
            for obj in klassList:
                klassName = obj.klass().name()
                if klassName in klasses:
                    klasses[klassName].append(obj)
                else:
                    klasses[klassName] = [obj]
            klassList = []
            for name in sorted(klasses):
                klassList.extend(klasses[name])
        return self.store().htObjectsInList(klassList, listName)


class Attr(object):

    def htValue(self, value, obj):
        return htmlEncode(str(value))


class ObjRefAttr(object):

    def htValue(self, value, obj):
        if isinstance(value, long):
            classSerialNum = (value & 0xFFFFFFFF00000000L) >> 32
            objSerialNum = value & 0xFFFFFFFFL
            klass = obj.store().klassForId(classSerialNum)
            klassName = klass.name()
            return ('<a href="BrowseObject?class=%s&serialNum=%i">%s.%i</a>'
                % (klassName, objSerialNum, klassName, objSerialNum))
        else:
            return htmlEncode(str(value))


class ListAttr(object):

    def htValue(self, value, obj):
        if value is None:
            return ('<a href="BrowseList?class=%s&serialNum=%i&attr=%s">list'
                '</a>' % (obj.klass().name(), obj.serialNum(), self.name()))


def InstallMixIns():
    from MiscUtils.MixIn import MixIn

    theGlobals = globals()
    names = 'ObjectStore Klass MiddleObject Attr ObjRefAttr ListAttr'.split()
    places = 'Core Run'.split()
    for name in names:
        mixed = False
        for place in places:
            nameSpace = {}
            try:
                exec 'from MiddleKit.%s.%s import %s' % (
                    place, name, name) in nameSpace
            except ImportError:
                pass
            else:
                pyClass = nameSpace[name]
                mixIn = theGlobals[name]
                MixIn(pyClass, mixIn)
                mixed = True
                continue
        assert mixed, 'Could not mix-in %s.' % name


InstallMixIns()
