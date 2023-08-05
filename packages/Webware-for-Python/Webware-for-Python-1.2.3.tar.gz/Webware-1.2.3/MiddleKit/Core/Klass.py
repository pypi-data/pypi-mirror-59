from ModelObject import ModelObject
from MiscUtils import NoDefault
from MiddleKit.Core.ListAttr import ListAttr
from MiddleKit.Core.ObjRefAttr import ObjRefAttr
from MiddleDict import MiddleDict


class Klass(MiddleDict, ModelObject):
    """A Klass represents a class specification.

    It is consisting primarily of a name and a list of attributes.
    """


    ## Init ##

    def __init__(self, klassContainer, rawDict=None):
        """Initialize a Klass definition with a raw dictionary.

        This is typically read from a file. The 'Class' field contains the name
        and can also contain the name of the superclass (like "Name : SuperName").
        Multiple inheritance is not yet supported.
        """
        MiddleDict.__init__(self, {})
        self._klassContainer = klassContainer
        self._attrsList = []
        self._attrsByName = {}
        self._superklass = None
        self._subklasses = []
        # False means never computed; None would mean computed, but not found:
        self._pyClass = False
        self._backObjRefAttrs = None
        self._allAttrs = None
        if rawDict is not None:
            self.readDict(rawDict)


    ## Reading ##

    def readDict(self, rawDict):
        name = rawDict['Class']
        if '(' in name:
            assert ')' in name, 'Invalid class spec. Missing ).'
            self._name, rest = name.split('(', 1)
            self._supername, rest = rest.split(')', 1)
            assert rest.strip() == ''
            self._name = self._name.strip()
            self._supername = self._supername.strip()
        elif ':' in name:
            # deprecated: we used to use a C++-like syntax involving colons
            # instead of a Python-like syntax with parens
            parts = [part.strip() for part in name.split(':', 2)]
            if len(parts) != 2:
                raise RuntimeError('Invalid class spec: %s' % string)
            self._name, self._supername = parts
        else:
            self._name = name
            self._supername = rawDict.get('Super', 'MiddleObject')
        self._isAbstract = rawDict.get('isAbstract', False)

        # fill in dictionary (self) with the contents of the dict argument
        for key, value in rawDict.items():
            # @@ 2001-02-21 ce: should we always strip string fields? Probably.
            if isinstance(value, basestring) and not value.strip():
                value = None
            self[key] = value

    def awakeFromRead(self, klasses):
        """Perform further initialization.

        Invoked by Klasses after all basic Klass definitions have been read.
        """
        assert self._klasses is klasses

        self._makeAllAttrs()
        # Python classes need to know their MiddleKit classes in
        # order for MiddleKit.Run.MiddleObject methods to work.
        # Invoking pyClass() makes that happen.
        self.pyClass()
        for attr in self.attrs():
            attr.awakeFromRead()

    def _makeAllAttrs(self):
        """Make all attributes.

        Makes list attributes accessible via methods for the following:
            allAttrs - every attr of the klass including inherited and derived attributes
            allDataAttrs - every attr of the klass including inherited, but NOT derived
            allDataRefAttrs - same as allDataAttrs, but only obj refs and lists

        ...and a dictionary attribute used by lookupAttr().

        Does nothing if called extra times.
        """
        if self._allAttrs is not None:
            return

        klass = self
        klasses = []
        while klass:
            klasses.append(klass)
            klass = klass.superklass()
        klasses.reverse()

        allAttrs = []
        allDataAttrs = []
        allDataRefAttrs = []
        for klass in klasses:
            attrs = klass.attrs()
            allAttrs.extend(attrs)
            for attr in attrs:
                if not attr.get('isDerived', False):
                    allDataAttrs.append(attr)
                    if isinstance(attr, (ObjRefAttr, ListAttr)):
                        allDataRefAttrs.append(attr)

        self._allAttrs = allAttrs
        self._allDataAttrs = allDataAttrs
        self._allDataRefAttrs = allDataRefAttrs

        # set up _allAttrsByName which is used by lookupAttr()
        self._allAttrsByName = {}
        for attr in allAttrs:
            self._allAttrsByName[attr.name()] = attr


    ## Names ##

    def name(self):
        return self._name

    def supername(self):
        return self._supername


    ## Id ##

    def id(self):
        """Return the id of the class, which is an integer.

        Ids can be fundamental to storing object references in concrete object stores.
        This method will throw an exception if setId() was not previously invoked.
        """
        return self._id

    def setId(self, id):
        if isinstance(id, set):
            # create an id that is a hash of the klass name
            # see Klasses.assignClassIds()
            allIds = id
            # the limit of 2 billion keeps the id easily in the range
            # of a 32 bit signed int without going negative
            limit = 2000000000
            id = abs(hash(self.name()) % limit)
            assert 0 < id < limit
            while id in allIds:
                # adjust for collision
                id += 1
            assert 0 < id < limit
            self._id = id
        else:
            self._id = id


    ## Superklass ##

    def superklass(self):
        return self._superklass

    def setSuperklass(self, klass):
        assert self._superklass is None, "Can't set superklass twice."
        self._superklass = klass
        klass.addSubklass(self)


    ## Ancestors ##

    def lookupAncestorKlass(self, name, default=NoDefault):
        """Search for and return the ancestor klass with the given name.

        Raises an exception if no such klass exists, unless a default
        is specified (in which case it is returned).
        """
        if self._superklass:
            if self._superklass.name() == name:
                return self._superklass
            else:
                return self._superklass.lookupAncestorKlass(name, default)
        else:
            if default is NoDefault:
                raise KeyError(name)
            else:
                return default

    def isKindOfKlassNamed(self, name):
        """Check whether the klass is from the given kind.

        Returns true if the klass is the same as, or inherits from,
        the klass with the given name.
        """
        if self.name() == name:
            return True
        else:
            return self.lookupAncestorKlass(name, None) is not None


    ## Subklasses ##

    def subklasses(self):
        return self._subklasses

    def addSubklass(self, klass):
        self._subklasses.append(klass)

    def descendants(self, init=1, memo=None):
        """Return all descendant klasses of this klass."""
        if memo is None:
            memo = set()
        if self in memo:
            return
        memo.add(self)
        for k in self.subklasses():
            k.descendants(init=0, memo=memo)
        if init:
            memo.remove(self)
        return memo


    ## Accessing attributes ##

    def addAttr(self, attr):
        self._attrsList.append(attr)
        self._attrsByName[attr.name()] = attr
        attr.setKlass(self)

    def attrs(self):
        """Return a list of all the klass' attributes not including inheritance."""
        return self._attrsList

    def hasAttr(self, name):
        return name in self._attrsByName

    def attr(self, name, default=NoDefault):
        """Return the attribute with the given name.

        If no such attribute exists, an exception is raised unless a default
        was provided (which is then returned).
        """
        if default is NoDefault:
            return self._attrsByName[name]
        else:
            return self._attrsByName.get(name, default)

    def lookupAttr(self, name, default=NoDefault):
        if self._allAttrs is None:
            # happens sometimes during awakeFromRead()
            self._makeAllAttrs()
        if default is NoDefault:
            return self._allAttrsByName[name]
        else:
            return self._allAttrsByName.get(name, default)

    def allAttrs(self):
        """Returns a list of all attributes.

        This includes those attributes that are inherited and derived.
        The order is top down; that is, ancestor attributes come first.
        """
        return self._allAttrs

    def allDataAttrs(self):
        """Return a list of all data attributes.

        This includes those attributes that are inherited.
        The order is top down; that is, ancestor attributes come first.
        Derived attributes are not included in the list.
        """
        return self._allDataAttrs

    def allDataRefAttrs(self):
        """Return a list of all data referencing attributes.

        Returns a list of all data attributes that are obj refs or lists,
        including those that are inherited.
        """
        return self._allDataRefAttrs


    ## Klasses access ##

    def klasses(self):
        return self._klasses

    def setKlasses(self, klasses):
        """Set the klasses object of the klass. This is the klass' owner."""
        self._klasses = klasses

    def model(self):
        return self._klasses.model()


    ## Other access ##

    def isAbstract(self):
        return self._isAbstract

    def pyClass(self):
        """Return the Python class that corresponds to this class.

        This request will even result in the Python class' module being
        imported if necessary. It will also set the Python class
        attribute _mk_klass which is used by MiddleKit.Run.MiddleObject.
        """
        if self._pyClass == False:
            if self._klassContainer._model._havePythonClasses:
                self._pyClass = self._klassContainer._model.pyClassForName(self.name())
                assert self._pyClass.__name__ == self.name(), (
                    'self.name()=%r, self._pyClass=%r' % (self.name(), self._pyClass))
                self._pyClass._mk_klass = self
            else:
                self._pyClass = None
        return self._pyClass

    def backObjRefAttrs(self):
        """Return a list of all potentially referencing attributes.

        Returns a list of all ObjRefAttrs in the given object model that can
        potentially refer to this object. The list does NOT include attributes
        inherited from superclasses.
        """
        if self._backObjRefAttrs is None:
            backObjRefAttrs = []
            # Construct targetKlasses = a list of this object's klass and all superklasses
            targetKlasses = {}
            super = self
            while super:
                targetKlasses[super.name()] = super
                super = super.superklass()
            # Look at all klasses in the model
            for klass in self._klassContainer._model.allKlassesInOrder():
                # find all ObjRefAttrs of klass that refer to one of our targetKlasses
                for attr in klass.attrs():
                    if not attr.get('isDerived', False):
                        if (isinstance(attr, ObjRefAttr)
                                and attr.targetClassName() in targetKlasses):
                            backObjRefAttrs.append(attr)
            self._backObjRefAttrs = backObjRefAttrs
        return self._backObjRefAttrs

    def setting(self, name, default=NoDefault):
        """Return the value of a particular configuration setting taken from the model."""
        return self._klassContainer.setting(name, default)


    ## As string ##

    def asShortString(self):
        return '<Klass, %s, %x, %d attrs>' % (self._name, id(self), len(self._attrsList))

    def __str__(self):
        return self.asShortString()


    ## As a dictionary key (for "set" purposes) ##

    def __hash__(self):
        return hash(self.name())  # | hash(self.model().name())

    def __cmp__(self, other):
        if other is None:
            return 1
        if not isinstance(other, Klass):
            return 1
        if self.model() is not other.model():
            value = cmp(self.model().name(), other.model().name())
            if value == 0:
                value = cmp(self.name(), other.name())
            return value
        return cmp(self.name(), other.name())


    ## Warnings ##

    def printWarnings(self, out):
        for attr in self.attrs():
            attr.printWarnings(out)


    ## Model support ##

    def willBuildDependencies(self):
        """Preps the klass for buildDependencies()."""
        self._dependencies = set()  # who self depends on
        self._dependents = set()  # who depends on self

    def buildDependencies(self):
        """Build dependencies of the klass.

        A klass' immediate dependencies are its ancestor classes (which may
        have auxilliary tables such as enums), the target klasses of all its
        obj ref attrs and their descendant classes.
        """
        if self._dependents is not None:
            # already done
            pass
        klass = self.superklass()
        while klass is not None:
            self._dependencies.add(klass)
            klass._dependents.add(self)
            klass = klass.superklass()
        from MiddleKit.Core.ObjRefAttr import ObjRefAttr
        for attr in self.allAttrs():
            if isinstance(attr, ObjRefAttr):
                klass = attr.targetKlass()
                if klass is not self and attr.boolForKey('Ref', True):
                    self._dependencies.add(klass)
                    klass._dependents.add(self)
                    for klass in klass.descendants():
                        self._dependencies.add(klass)
                        klass._dependents.add(self)

    def recordDependencyOrder(self, order, visited, indent=0):
        # print '%srecordDependencyOrder() for %s' % (' '*indent*4, self.name())
        if self in visited:
            return
        visited.add(self)
        for klass in self._dependencies:
            klass.recordDependencyOrder(order, visited, indent+1)
        order.append(self)
