from types import MethodType


def MixIn(pyClass, mixInClass, makeAncestor=False, mixInSuperMethods=False):
    """Mixes in the attributes of the mixInClass into the pyClass.

    These attributes are typically methods (but don't have to be).
    Note that private attributes, denoted by a double underscore,
    are not mixed in. Collisions are resolved by the mixInClass'
    attribute overwriting the pyClass'. This gives mix-ins the power
    to override the behavior of the pyClass.

    After using MixIn(), instances of the pyClass will respond to
    the messages of the mixInClass.

    An assertion fails if you try to mix in a class with itself.

    The pyClass will be given a new attribute mixInsForCLASSNAME
    which is a list of all mixInClass' that have ever been installed,
    in the order they were installed. You may find this useful
    for inspection and debugging.

    You are advised to install your mix-ins at the start up
    of your program, prior to the creation of any objects.
    This approach will result in less headaches. But like most things
    in Python, you're free to do whatever you're willing to live with. :-)

    There is a bitchin' article in the Linux Journal, April 2001,
    "Using Mix-ins with Python" by Chuck Esterbrook,
    which gives a thorough treatment of this topic.

    An example, that resides in Webware, is MiddleKit.Core.ModelUser.py,
    which install mix-ins for SQL adapters. Search for "MixIn(".

    If makeAncestor is True, then a different technique is employed:
    the mixInClass is made the first base class of the pyClass.
    You probably don't need to use this and if you do, be aware that your
    mix-in can no longer override attributes/methods in pyClass.

    If mixInSuperMethods is True, then support will be enabled for you to
    be able to call the original or "parent" method from the mixed-in method.
    This is done like so:

        class MyMixInClass(object):
        def foo(self):
            MyMixInClass.mixInSuperFoo(self)  # call the original method
            # now do whatever you want
    """
    assert mixInClass is not pyClass, (
        'mixInClass = %r, pyClass = %r' % (mixInClass, pyClass))
    if makeAncestor:
        if mixInClass not in pyClass.__bases__:
            pyClass.__bases__ = (mixInClass,) + pyClass.__bases__
    else:
        # Recursively traverse the mix-in ancestor classes in order
        # to support inheritance
        for baseClass in reversed(mixInClass.__bases__):
            MixIn(pyClass, baseClass)

        # Track the mix-ins made for a particular class
        attrName = 'mixInsFor' + pyClass.__name__
        mixIns = getattr(pyClass, attrName, None)
        if mixIns is None:
            mixIns = []
            setattr(pyClass, attrName, mixIns)

        # Record our deed for future inspection
        mixIns.append(mixInClass)

        # Install the mix-in methods into the class
        for name in dir(mixInClass):
            # skip private members, but not __repr__ et al:
            if name.startswith('__'):
                if not name.endswith('__'):
                    continue  # private
                member = getattr(mixInClass, name)
                if not isinstance(member, MethodType):
                    continue  # built in or descriptor
            else:
                member = getattr(mixInClass, name)
            if isinstance(member, MethodType):
                if mixInSuperMethods:
                    if hasattr(pyClass, name):
                        origmember = getattr(pyClass, name)
                        setattr(mixInClass, 'mixInSuper'
                            + name[0].upper() + name[1:], origmember)
                member = member.im_func
            setattr(pyClass, name, member)
