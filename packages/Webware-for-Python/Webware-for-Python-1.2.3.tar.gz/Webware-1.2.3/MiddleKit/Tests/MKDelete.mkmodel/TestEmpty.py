from Foo import Foo
from Bar import Bar
from MiddleKit.Run import ObjectStore
import A, B, C, D, E, F, G, H, I, J, K, L

def test(store):

    testOther(store, A.A, DELETE_REFERENCED_ERROR)
    testOther(store, B.B, DELETE_REFERENCED_ERROR)
    testOther(store, C.C, DELETE_FOO)
    testOther(store, D.D, DELETE_FOO_AND_OBJECT)

    print '*** passed testOther'

    testSelf(store, E.E, DELETE_OBJECT)
    testSelf(store, F.F, DELETE_OBJECT_WITH_REFERENCES_ERROR)
    testSelf(store, G.G, DELETE_OBJECT)
    testSelf(store, H.H, DELETE_FOO_AND_OBJECT)

    print '*** passed testSelf'

    testSelfList(store, I.I, DELETE_FOO)
    testSelfList(store, J.J, DELETE_OBJECT_WITH_REFERENCES_ERROR)
    testSelfList(store, K.K, DELETE_FOO)
    testSelfList(store, L.L, DELETE_FOO_AND_OBJECT)

    print '*** passed testSelfList'

    testListUpdate(store, I.I, DELETE_OBJECT)

    print '*** passed testListUpdate'

    testCascadeWithRequiredBackRef(store)

# These are possible values for expectedResult
DELETE_FOO = 1
DELETE_OBJECT = 2
DELETE_FOO_AND_OBJECT = 3
DELETE_REFERENCED_ERROR = 4
DELETE_OBJECT_WITH_REFERENCES_ERROR = 5


def testOther(store, klass, expectedResult):
    """Test "other".

    Test creating an instance of a specified class, that points to an instance
    of Foo, which itself points to an instance of Bar.
    Then try to delete the Foo, and make sure that the expected result happens.
    """
    # Run the test, deleting the specified object and verifying the expected result
    obj, foo, bar = setupTest(store, klass)
    try:
        runTest(store, klass, foo, expectedResult)
    finally:
        cleanupTest(store, klass)


def testSelf(store, klass, expectedResult):
    """Test "self".

    Test creating an instance of a specified class, that points to an instance
    of Foo, which itself points to an instance of Bar. Then try to delete the
    object of the specified class, and make sure that the expected result happens.
    """
    # Run the test, deleting the specified object and verifying the expected result
    obj, foo, bar = setupTest(store, klass)
    try:
        runTest(store, klass, obj, expectedResult)
    finally:
        cleanupTest(store, klass)


def testSelfList(store, klass, expectedResult):
    """Test list of "self".

    Test creating an instance of a specified class, pointed to by the list
    attribute in an instance of Foo, which itself points to an instance of Bar.
    Then try to delete the Foo, and make sure that the expected result happens.
    """
    # Run the test, deleting the specified object and verifying the expected result
    obj, foo, bar = setupListTest(store, klass)
    try:
        runTest(store, klass, foo, expectedResult)
    finally:
        cleanupTest(store, klass)


def testListUpdate(store, klass, expectedResult):
    """Test list update.

    Test creating an instance of a specified class, pointed to by the list
    attribute in an instance of Foo, which itself points to an instance of Bar.
    Then try to delete the specified class, and make sure that Foo's list
    attribute is updated automatically.
    """
    # Run the test, deleting the specified object and verifying the expected result
    obj, foo, bar = setupListTest(store, klass)
    assert len(foo.listOfI()) == 1
    try:
        runTest(store, klass, obj, expectedResult)
        assert len(foo.listOfI()) == 0
    finally:
        cleanupTest(store, klass)


def setupTest(store, klass):
    """Setup test.

    Setup 3 objects: one of the specified klass, pointing to a Foo,
    pointing to a Bar. Returns tuple (object of specified klass, foo, bar).
    """
    # Create a Foo and a Bar, with the Foo pointing to the Bar
    bar = Bar()
    bar.setX(42)
    foo = Foo()
    foo.setBar(bar)
    store.addObject(foo)
    store.addObject(bar)
    store.saveChanges()

    # create an instance of klass pointing to Foo
    obj = klass()
    obj.setFoo(foo)
    store.addObject(obj)
    store.saveChanges()

    return obj, foo, bar


def setupListTest(store, klass):
    # Create a Foo and a Bar, with the Foo pointing to the Bar
    bar = Bar()
    bar.setX(42)
    foo = Foo()
    foo.setBar(bar)
    store.addObject(foo)
    store.addObject(bar)
    store.saveChanges()

    # create an instance of klass and put it into the list in foo
    obj = klass()
    getattr(foo, 'addToListOf%s' % klass.__name__)(obj)
    store.saveChanges()

    return obj, foo, bar


def runTest(store, klass, objectToDelete, expectedResult):
    # Try to delete the specified object, then check that the expected result is what happened
    try:
        store.deleteObject(objectToDelete)
        store.saveChanges()
    except ObjectStore.DeleteReferencedError:
        assert expectedResult == DELETE_REFERENCED_ERROR
        objects = store.fetchObjectsOfClass(klass)
        foos = store.fetchObjectsOfClass(Foo)
        assert len(objects) == 1
        assert len(foos) == 1
    except ObjectStore.DeleteObjectWithReferencesError:
        assert expectedResult == DELETE_OBJECT_WITH_REFERENCES_ERROR
        objects = store.fetchObjectsOfClass(klass)
        foos = store.fetchObjectsOfClass(Foo)
        assert len(objects) == 1
        assert len(foos) == 1
    else:
        objects = store.fetchObjectsOfClass(klass)
        foos = store.fetchObjectsOfClass(Foo)
        if expectedResult == DELETE_FOO:
            assert len(objects) == 1
            assert objects[0].foo() is None
            assert len(foos) == 0
        elif expectedResult == DELETE_OBJECT:
            assert len(objects) == 0
            assert len(foos) == 1
        elif expectedResult == DELETE_FOO_AND_OBJECT:
            assert len(objects) == 0
            assert len(foos) == 0
        else:
            raise AssertionError('unknown expectedResult value')
    bars = store.fetchObjectsOfClass(Bar)
    assert len(bars) == 1


def cleanupTest(store, klass):
    # Clean out all leftover objects
    store.clear()
    store.executeSQLTransaction(['delete from Foo;', 'delete from Bar;',
        'delete from %s;' % klass.__name__])
    print


def testCascadeWithRequiredBackRef(store):
    """See also: Classes.csv Engine & Engine Part

    The deal is that deleting an Engine should delete all its EngineParts
    via the cascade set on the parts list attribute. Previously, there was
    a bug with this if the back ref attr (EnginePart.engine in this case)
    was required (isRequired=True).
    """
    from Engine import Engine
    from EnginePart import EnginePart
    e = Engine()
    store.addObject(e)
    store.saveChanges()
    e.addToParts(EnginePart())
    e.addToParts(EnginePart())
    e.addToParts(EnginePart())
    store.saveChanges()
    assert e.parts()

    store._verboseDelete = 1
    store.deleteObject(e)
    store.saveChanges()
