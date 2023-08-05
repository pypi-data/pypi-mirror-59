import sys
import threading
from types import InstanceType

from MiscUtils import NoDefault
from MiscUtils.NamedValueAccess import valueForName
from MiddleKit.Core.ObjRefAttr import ObjRefAttr
from MiddleKit.Core.ListAttr import ListAttr

import ObjectStore


class MiddleObject(object):
    """Superclass for the MiddleKit objects.

    MiddleObject is the abstract superclass of objects that are manipulated
    at runtime by MiddleKit. For any objects that you expect to pull out of
    a database via MiddleKit, their classes must inherit MiddleObject.

    MiddleObjects have a serial number which persists in the database
    and is unique for the object across all timelines. In other words,
    serial numbers do not get reused.

    A serial number of 0 is not valid for persistence, so if a MiddleObject
    has such a serial number, you will know that it was not created from
    the database and it has not yet been committed to the database (upon
    which time it will receive a valid serial number).

    Normally we simply prefix data attributes with '_', but here we
    prefix them with '_mk_'. Part of the reason is to provide an extra
    degree of protection for subclasses from current and future attribute
    names used for MiddleKit's own internal book keeping purposes. Although
    users of MiddleKit subclass MiddleObject, they only need to have
    a limited understanding of it. Also, in __setattr__ we skip the
    change-detection bookkeeping on '_mk_*' attributes.
    """

    _mk_isDeleted = False


    ## Init ##

    def __init__(self):
        self.__dict__['_mk_initing'] = True
        self._mk_store = None
        self._mk_changedAttrs = None
        self._mk_serialNum = 0
        self._mk_key = None
        self._mk_changed = False
        self._mk_initing = False
        self._mk_inStore = False

    # cache the various setFoo methods first by qualified class name
    _mk_setCache = {}
    # get a reentrant lock for accessing the persistent store
    _mk_cacheLock = threading.RLock()


    ## Read Store ##

    def readStoreData(self, store, row):
        """Read data from the persistent store.

        Invoked by the store in order for this object to read data from the
        persistent store. Could be invoked multiple times for the same object
        in order to "refresh the attributes" from the persistent store.
        """
        self._mk_cacheLock.acquire()
        try:
            if self._mk_store:
                assert self._mk_store is store, \
                    'Cannot refresh data from a different store.'
                if self._mk_changed and not self._mk_initing:
                    assert store.setting('AllowRefreshOfChangedObject', False), (
                        "attempted to refresh changed object %s.%d\nchanges=%r\n"
                        "Your app needs to call store.saveChanges() before doing"
                        " anything which can cause objects to be refreshed from the"
                        " database (i.e. calling store.deleteObject()), otherwise"
                        " your changes will be lost." % (self.klass().name(),
                            self.serialNum(), self._mk_changedAttrs))
            else:
                self.setStore(store)
            assert not self._mk_isDeleted, 'Cannot refresh a deleted object.'
            if store.setting('UseBigIntObjRefColumns', False):
                fullClassName = self.__class__.__module__ + '.' + self.__class__.__name__
                cache = self._mk_setCache.setdefault(fullClassName, [])
                if not cache:
                    allAttrs = self.klass().allDataAttrs()
                    # @@ 2000-10-29 ce: next line is major hack: hasSQLColumn()
                    attrs = [attr for attr in allAttrs if attr.hasSQLColumn()]
                    attrNames = [attr.name() for attr in attrs]
                    assert len(attrNames) + 1 == len(row)  # +1 because row has serialNumber
                    for name in attrNames:
                        setMethodName = 'set' + name[0].upper() + name[1:]
                        setMethod = getattr(self.__class__, setMethodName, '_'+name)
                        cache.append(setMethod)

                assert len(cache) + 1 == len(row)
                self._mk_initing = True
                if self._mk_serialNum == 0:
                    self.setSerialNum(row[0])
                else:
                    assert self._mk_serialNum == row[0]
                # Set all of our attributes with setFoo() or by assigning to _foo
                for i, setter in enumerate(cache):
                    setter(self, row[i+1])
            else:
                self._mk_initing = True
                if self._mk_serialNum == 0:
                    self.setSerialNum(row[0])
                else:
                    assert self._mk_serialNum == row[0]
                allAttrs = self.klass().allDataAttrs()
                i = 1
                for attr in allAttrs:
                    i = attr.readStoreDataRow(self, row, i)

            self._mk_initing = False
            self._mk_inStore = True
            # setting the values above will cause _mk_changed to be set
            self._mk_changed = False  # clear it now
        finally:
            self._mk_cacheLock.release()
        return self


    ## Debug Info ##

    def __repr__(self):
        return self.debugStr()

    _debugKeys = 'serialNum'.split()

    def debugStr(self):
        out = [self.__class__.__name__, '(', '0x%x' % id(self)]
        sep = ', '
        for key in self._debugKeys:
            out.append(sep)
            out.append(key)
            out.append('=')
            try:
                out.append(repr(valueForName(self, key)))
            except Exception as exc:
                from MiscUtils.Funcs import excstr
                out.append('('+excstr(exc)+')')
        out.append(')')
        out = ''.join(out)
        return out


    ## Serial numbers ##

    def serialNum(self):
        return self._mk_serialNum

    def setSerialNum(self, value):
        """Set the serial number of the object and invalidates the object's key.

        There are some restrictions: Once the serial number is a positive value,
        indicating a legitimate value from the object store, it cannot be set
        to anything else. Also, if the serial number is negative, indicating
        a temporary serial number for new objects that haven't been committed
        to the database, it can only be set to a positive value.
        """
        assert isinstance(value, (int, long)), \
            "Type is: %r, value is: %r" % (type(value), value)
        if self._mk_serialNum < 0:
            assert value > 0
        else:
            assert self._mk_serialNum == 0
        self._mk_serialNum = value
        self._mk_key = None

    # for people who capitalize the attributes in their model:
    SerialNum = serialNum


    ## Change ##

    def isChanged(self):
        return self._mk_changed

    def setChanged(self, flag):
        self._mk_changed = flag


    ## In Store ##

    def isInStore(self):
        return self._mk_inStore

    def isNew(self):
        """Check if this is a new object.

        Returns true if the object was newly created (whether added to the
        store or not). Objects fetched from the database will return false.
        """
        return self._mk_serialNum < 1

    def isDeleted(self):
        return self._mk_isDeleted


    ## Keys ##

    def key(self):
        """Return the object's key as needed and used by the ObjectStore.

        Will return None if setKey() was never invoked, or not invoked
        after a setSerialNum().
        """
        return self._mk_key

    def setKey(self, key):
        """Set the object's key.

        Restrictions: Cannot set the key twice.
        """
        assert self._mk_serialNum >= 1, \
            "Cannot make keys for objects that haven't been persisted yet."
        assert self._mk_key is None
        self._mk_key = key


    ## Misc utility ##

    def refetch(self):
        """Refetch the object's attributes from the store.

        Only works for non-changed objects from a store.
        @@ not covered by test suite yet
        """
        assert self.isInStore()
        assert not self.isChanged()
        result = self.store().fetchObject(self.__class__, self.serialNum())
        assert result is self, \
            'expecting result to be self. self=%r, result=%r' % (self, result)

    def allAttrs(self, includeUnderscoresInKeys=True):
        """Return a dictionary mapping the names of attributes to their values.

        Only attributes defined in the MiddleKit object model are included.
        An example return value might be
            {'_x': 1, '_y': 1},
        or if includeUnderscoresInKeys is false,
            {'x': 1, 'y': 1}.
        """
        allAttrs = {}
        allAttrDefs = self.klass().allAttrs()
        for attrDef in allAttrDefs:
            if includeUnderscoresInKeys:
                key = attrName = '_'+attrDef.name()
            else:
                key = attrDef.name()
                attrName = '_' + key
            allAttrs[key] = getattr(self, attrName)
        return allAttrs

    def removeObjectFromListAttrs(self, obj):
        """Remove object from any list attributes that this instance might have.

        This is used if the object is deleted, so we don't have dangling references.
        """
        for attr in self.klass().allAttrs():
            if isinstance(attr, ListAttr):
                listName = '_' + attr.name()
                list = getattr(self, listName)
                if list is not None and obj in list:
                    delattr(self, listName)
                    setattr(self, listName, None)

    def updateReferencingListAttrs(self):
        """Update all referencing list attributes.

        Checks through all object references, and asks each referenced
        object to remove us from any list attributes that they might have.
        """
        for attr in self.klass().allAttrs():
            if isinstance(attr, ObjRefAttr):
                value = getattr(self, '_' + attr.name())
                if value is not None:
                    if isinstance(value, (MiddleObject, InstanceType)):
                        value.removeObjectFromListAttrs(self)
                    elif isinstance(value, long):
                        obj = self.store().objRefInMem(value)
                        if obj:
                            obj.removeObjectFromListAttrs(self)

    def referencedAttrsAndObjects(self):
        """Get all referenced attributes and objects.

        Returns a list of tuples of (attr, object) for all objects
        that this object references.
        """
        t = []
        for attr in self.klass().allDataAttrs():
            if isinstance(attr, ObjRefAttr):
                obj = self.valueForAttr(attr)
                if obj:
                    t.append((attr, obj))
            elif isinstance(attr, ListAttr):
                for obj in self.valueForAttr(attr):
                    t.append((attr, obj))
        return t

    def referencingObjectsAndAttrs(self):
        """Get all referencing attributes and objects.

        Returns a list of tuples of (object, attr) for all objects that have
        ObjRefAttrs that reference this object.
        """
        referencingObjectsAndAttrs = []
        selfSqlObjRef = self.sqlObjRef()
        for backObjRefAttr in self.klass().backObjRefAttrs():
            objects = self.store().fetchObjectsOfClass(backObjRefAttr.klass(),
                **self.referencingObjectsAndAttrsFetchKeywordArgs(backObjRefAttr))
            for obj in objects:
                assert obj.valueForAttr(backObjRefAttr) is self
                referencingObjectsAndAttrs.append((obj, backObjRefAttr))
        return referencingObjectsAndAttrs

    def referencingObjectsAndAttrsFetchKeywordArgs(self, backObjRefAttr):
        """Get keyword arguments for referencingObjectsAndAttrs().

        Used by referencingObjectsAndAttrs() to reduce the load on the
        persistent store. Specific object stores replace this as appropriate.
        """
        return dict(refreshAttrs=True)


    ## Debugging ##

    def dumpAttrs(self, out=None, verbose=False):
        """Print the attributes of the object.

        If verbose is false (the default), then the only MiddleKit specific
        attribute that gets printed is _mk_serialNum.
        """
        if out is None:
            out = sys.stdout
        out.write('%s %x\n' % (self.__class__.__name__, id(self)))
        keys = dir(self)
        keyWidth = max([len(key) for key in keys])
        for key in sorted(keys):
            if verbose:
                dump = True
            else:
                dump = not key.startswith('_mk_') or key == '_mk_serialNum'
            if dump:
                name = key.ljust(keyWidth)
                out.write('%s = %s\n' % (name, getattr(self, key)))
        out.write('\n')


    ## Misc access ##

    def store(self):
        return self._mk_store

    def setStore(self, store):
        assert not self._mk_store, \
            'The store was previously set and cannot be set twice.'
        self._mk_store = store
        self._mk_inStore = True


    ## Sneaky MiddleKit stuff ##

    def klass(self):
        """Return the MiddleKit class definition for this object.

        These definitions are instances of MiddleKit.Core.Klass and
        come from the MiddleKit model. Be sure the MiddleKit model
        is loaded. See the docs for more details.
        """
        return self._mk_klass  # If you get AttributeError, then the MK model wasn't loaded.

    def addReferencedObjectsToStore(self, store):
        """Adds all MK objects referenced by this object to the store."""
        assert store
        values = [self.valueForAttr(attr) for attr in self.klass().allDataRefAttrs()]
        for value in values:
            if isinstance(value, MiddleObject):
                store.addObject(value)
            elif isinstance(value, list):
                for obj in value:
                    if isinstance(obj, MiddleObject):
                        store.addObject(obj)


    ## Accessing attributes by name ##

    def valueForKey(self, attrName, default=NoDefault):
        """Get value of a named attribute for a given key.

        Returns the value of the named attribute by invoking its "get"
        accessor method. You can use this when you want a value whose
        name is determined at runtime.

        It also insulates you from the naming convention used for the
        accessor methods as defined in Attr.pyGetName(). For example, the
        test suites use this instead of directly invoking the "get" methods.

        If the attribute is not found, this method will look for any
        Python attribute or method that matches.

        If a value is still not found, the default argument is returned
        if specified, otherwise LookupError is raised with the attrName.
        """
        attr = self.klass().lookupAttr(attrName, None)
        if attr:
            return self.valueForAttr(attr, default)
        else:
            value = getattr(self, attrName, NoDefault)
            if value is not NoDefault:
                if callable(value):
                    value = value()
                return value
            if default is NoDefault:
                raise LookupError(attrName)
            else:
                return default

    def setValueForKey(self, attrName, value):
        """Set value of a named attribute for a given key.

        Sets the value of the named attribute by invoking its "set"
        accessor method. You can use this when you want a value whose
        name is determined at runtime.

        It also insulates you from the naming convention used for the
        accessor methods as defined in Attr.pySetName(). For example, the
        test suites use this instead of directly invoking the "set" methods.

        If the required set method is not found, a LookupError is raised
        with the attrName.
        """
        try:
            attr = self.klass().lookupAttr(attrName)
        except KeyError:
            method = None
        else:
            pySetName = attr.pySetName()
            method = getattr(self, pySetName, None)
        if method is None:
            attrs = ','.join(sorted(
                attr.name() for attr in self.klass().allAttrs()))
            raise LookupError('%s, class=%s, all attrs=%s'
                % (attrName, self.__class__, attrs))
        return method(value)

    def valueForAttr(self, attr, default=NoDefault):
        getMethod = self.klass()._getMethods.get(attr.name())
        if getMethod is None:
            pyGetName = attr.pyGetName()
            getMethod = getattr(self.klass().pyClass(), pyGetName, None)
            if getMethod is None:
                getMethod = False  # indicates that the search was already done
            self.klass()._getMethods[attr.name()] = getMethod
        if getMethod:
            return getMethod(self)
        else:
            if default is NoDefault:
                raise LookupError(attr['Name'])
            else:
                return default

    def setValueForAttr(self, attr, value):
        return self.setValueForKey(attr['Name'], value)


    ## Problems ##

    def objRefErrorWasRaised(self, error, sourceKlassName, sourceAttrName):
        """Invoked by getter methods when ObjRefErrors are raised.

        Prints very useful information to stdout.
        Override if you wish other actions to be taken.
        The value returned is used for the obj ref (defaults to None).
        """
        klassId, objSerialNum = error.args
        try:
            rep = repr(self)
        except Exception as e:
            rep = '(exception during repr: %s: %s)' % (e.__class__.__name__, e)
        try:
            klassName = self.store().klassForId(klassId).name()
        except Exception as e:
            klassName = '%i (exception during klassName fetch: %s: %s)' % (
                klassId, e.__class__.__name__, e)
        sys.stdout.flush()
        sys.stderr.flush()
        print ('WARNING: MiddleKit: In object %(rep)s, attribute'
            ' %(sourceKlassName)s.%(sourceAttrName)s dangles with value'
            ' %(klassName)s.%(objSerialNum)s' % locals())
        sys.stdout.flush()
        return None

    def clone(self, memo=None, depthAttr=None):
        """Clone middle object(s) generically.

        You may or may not want objects referenced by ObjRefAttr or ListAttr
        attributes to be cloned in addition to the object itself. You can
        control this by adding a "Copy" column in your Classes.csv file, and
        set the value for each attribute which may reference another object.

        The possible values for "Copy" are:
        'deep': referenced objects will be cloned and references to them will be set
        'shallow' (default): the cloned object references the same object as the original
        'none': the attribute in the cloned object is set to 'None'

        Clone will call itself recursively to copy references deeply, and
        gracefully handles recursive references (where a referenced object
        may have already been cloned). In this case only one clone is created,
        not two cloned instances of the same original.

        If you want a mapping from original to cloned objects, pass in an empty
        dict for the memo argument.  It will be filled in during the clone
        operation, such that the keys are the original object instances and
        the values are the corresponding clones.

        The parameter depthAttr may be set to a column name which, if set, will
        take precedence over the value in the 'Copy' column for that attribute.
        """

        def copyAttrValue(source, dest, attr, memo, depthAttr):
            if depthAttr and depthAttr in attr:
                copymode = attr[depthAttr]
            else:
                copymode = attr.get('Copy', 'shallow')

            if copymode == 'deep' and isinstance(attr, ObjRefAttr):
                # Clone the value of an attribute from the source object,
                # and set it in the attribute of the dest object.
                value = getattr(source, attr.pyGetName())()
                if value:
                    clonedvalue = value.clone(memo, depthAttr)
                else:
                    clonedvalue = None
                retvalue = getattr(dest, attr.pySetName())(clonedvalue)
            elif copymode == 'none':
                # Shouldn't set attribute to None explicitly since attribute
                # may have isRequired=True. Besides, the object will initialize
                # all attributes to None anyways.
                pass
            else:
                # Copy the value of an attribute from the source object
                # to the dest object.
                # print 'copying value of ' + attr.name()
                value = getattr(source, attr.pyGetName())()
                retvalue = getattr(dest, attr.pySetName())(value)

        if memo is None:
            # print 'Initializing memo'
            memo = {}

        # if we've already cloned this object, return the clone
        if self in memo:
            return memo[self]

        # make an instance of ourselves
        copy = self.__class__()
        # print 'cloning %s %s as %s' % (self.klass().name(), str(self), str(copy))

        memo[self] = copy

        # iterate over our persistent attributes
        for attr in self.klass().allDataAttrs():
            if isinstance(attr, ListAttr):
                valuelist = getattr(self, attr.pyGetName())()
                setmethodname = "addTo" + attr.name()[0].upper() + attr.name()[1:]
                setmethod = getattr(copy, setmethodname)

                # if cloning to create an extension object,
                # we might want to copy fewer subobjects
                copymode = attr['Copy']
                if depthAttr and depthAttr in attr:
                    copymode = attr[depthAttr]

                if copymode == 'deep':
                    backrefname = attr.backRefAttrName()
                    setrefname = "set" + backrefname[0].upper() + backrefname[1:]
                    for value in valuelist:
                        # clone the value
                        valcopy = value.clone(memo, depthAttr)

                        # set the value's back ref to point to self
                        setrefmethod = getattr(valcopy, setrefname)
                        backrefattr = valcopy.klass().lookupAttr(backrefname)
                        setrefmethod(None)

                        # add the value to the list
                        retval = setmethod(valcopy)
                elif attr['Copy'] == 'none':
                    # leave the list empty
                    pass
                else:
                    pass
            else:
                copyAttrValue(self, copy, attr, memo, depthAttr)

        return copy
