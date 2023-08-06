import sys
import six

from descarteslabs.common.graft import client, syntax
from .exceptions import ProxyTypeError

PY36 = sys.version_info[:2] >= (3, 6)


class Castable(object):
    "Mixin to support casting without explicitly allowing it in ``__init__``"

    @classmethod
    def _from_graft(cls, graft):
        """
        Create an instance of this class with the given graft dict, circumventing ``__init__``

        To use safely, this class must function correctly if its ``__init__`` method is not called.

        This is used to let your class present a friendly user-facing constructor,
        but still support copy-constuction or casting when necessary.
        """
        assert syntax.is_graft(
            graft
        ), "Attempted to instantiate {} from the non-graft-like object {!r}".format(
            cls.__name__, graft
        )
        # create a new, empty ``cls`` object, circumventing its __init__ method.
        new = cls.__new__(cls)
        new.graft = graft
        return new

    @classmethod
    def _from_apply(cls, function, *args, **kwargs):
        "Shorthand for ``cls._from_graft(client.apply_graft(function, *args, **kwargs))``"
        return cls._from_graft(client.apply_graft(function, *args, **kwargs))

    def _cast(self, cls):
        "Copy of ``self`` as ``cls``. ``cls.__init__`` will not be called."
        return cls._from_graft(self.graft)


class Proxytype(Castable):
    "Proxytype abstract base class"

    @classmethod
    def _promote(cls, obj):
        "Returns `obj` as type `cls`, or raises `ProxyTypeError` if promotion is not possible."
        if isinstance(obj, cls):
            return obj
        raise ProxyTypeError("Cannot promote {} to {}".format(obj, cls.__name__))

    def __bool__(self):
        # Ensure Proxytypes can't be used in conditionals;
        # Python default would always resolve to True.
        raise TypeError(
            "Truth value of Proxytype {} objects is not supported".format(
                type(self).__name__
            )
        )

    __nonzero__ = __bool__  # for python 2

    def __contains__(self, _):
        if hasattr(self, "contains"):
            raise TypeError(
                (
                    "Please use {}.contains(other). Python requires a bool to be returned "
                    "from __contains__ and this value cannot be known for proxy types."
                ).format(self.__class__.__name__)
            )
        else:
            raise TypeError(
                "object of type {} has no contains().".format(self.__class__.__name__)
            )

    def __len__(self):
        if hasattr(self, "length"):
            raise TypeError(
                (
                    "Please use {}.length(). Python requires an int to be returned "
                    "from __len__ and this value cannot be known for proxy types."
                ).format(self.__class__.__name__)
            )
        else:
            raise TypeError(
                "object of type {} has no length()".format(self.__class__.__name__)
            )

    # NOTE(gabe): if you're looking for the `compute` and `persist` helper methods,
    # they're actually monkey-patched into here in the top-level
    # ``//descarteslabs/workflows/__init__.py`` to avoid circular dependencies
    # that are deemed a greater evil than monkey-patching.


class GenericProxytypeMetaclass(type):
    """
    Override ``isinstance`` and ``issubclass`` to make them covariant
    for `GenericProxytype`s and their concrete subclasses, and support
    ``__init_subclass__`` in Python < 3.6.

    Formally: ``issubclass(typA, typB) is True`` iff the generic type of ``typA``
    is a subclass of the generic type of ``typB``, and all the type parameters of ``typA``
    are subclasses of the equivalent type parameters of ``typB``.

    This ensures that:

    >>> from descarteslabs.workflows import List, Int
    >>> class MyIntSubclass(Int):
    ...     pass
    >>> class MyListSubclass(List):
    ...     pass
    >>> issubclass(List[MyIntSubclass], List[Int])
    True
    >>> issubclass(MyListSubclass[Int], List[Int])
    True
    >>> issubclass(MyListSubclass[MyIntSubclass], List[Int])
    True
    >>> issubclass(MyListSubclass[MyIntSubclass], List)
    True
    >>> issubclass(List[Int], List[MyIntSubclass])
    False

    The metaclass also adds an empty `_concrete_subtypes` dict to every new `GenericProxytype`,
    which is a registry of concrete subtypes of each generic type,
    so that if we've already created a type for the given parameters,
    we return that type object instead of making a duplicate.

    This ensure that, for example, ``List[Int]`` is always the same object,
    so comparing ``typA is typB`` is a safe way to determine iff they're exactly the same type.

    Horrifyingly, it also implements ``__getitem__`` to emulate ``__class_getitem__`` in Python 2,
    so ``List[Str]`` works in both versions.

    The backport of ``__init_subclass__`` in Python < 3.6 matches
    https://docs.python.org/3/reference/datamodel.html#object.__init_subclass__,
    except that ``__init_subclass__`` must be decorated with ``@classmethod``.
    """

    def __instancecheck__(self, obj):
        "Covariantly check whether ``isinstance(obj, type(self))``"
        return self.__subclasscheck__(type(obj))

    def __subclasscheck__(mycls, othercls):
        "Covariantly check whether ``issubclass(othercls, mycls)``"
        # vanilla `issubclass`, to prevent infinite recursion into this `__subclasscheck__` method
        # (except the order of the args is reversed from `issubclass`, so call it "issuperclass" instead)
        issuperclass = type.__subclasscheck__

        # Get the generic (unparameterized) versions of both classes, e.g. List[Int] -> List
        # (`_generictype` is set on all concrete subtypes by `GenericProxytype.__class_getitem__`)
        try:
            my_generic_parent_type = mycls._generictype
        except AttributeError:
            assert issuperclass(
                GenericProxytype, mycls
            ), "{} is not a subclass of GenericProxytype. Do not use the GenericProxytypeMetaclass on it!".format(
                mycls
            )
            # If `mycls` doesn't have a `_generictype` attr, it's already a generic
            my_generic_parent_type = mycls

        try:
            other_generic_parent_type = othercls._generictype
        except AttributeError:
            # NOTE(gabe): `other_generic_parent_type` might not actually be a GenericProxytype at all here,
            # but we'll catch that later in the final conditional
            other_generic_parent_type = othercls

        assert my_generic_parent_type._type_params is None, (
            "Expected {} to be generic, "
            "but _type_params is not None: {}".format(
                my_generic_parent_type, my_generic_parent_type._type_params
            )
        )
        assert getattr(other_generic_parent_type, "_type_params", None) is None, (
            "Expected {} to be generic, "
            "but _type_params is not None: {}".format(
                other_generic_parent_type, other_generic_parent_type._type_params
            )
        )

        # Check that the generic type of the other is a subclass of our generic type,
        # and either we're a generic ourselves (in which case other passes whether generic or concrete),
        # or the type parameters of other are all subclasses of our equivalent type parameters
        return issuperclass(my_generic_parent_type, other_generic_parent_type) and (
            mycls._type_params is None
            or _type_params_issubclass(othercls._type_params, mycls._type_params)
        )

    def __init__(cls, name, bases, dct):
        # Ensure every subclass gets its own `_concrete_subtypes` dict,
        # which it will use to register parameterized (concrete) subtypes
        # (so calling `List[Int]` twice will return the same object both times)

        # QUESTION(gabe): does it matter that this happens on the concrete subtypes themselves?
        cls._concrete_subtypes = {}
        super(GenericProxytypeMetaclass, cls).__init__(name, bases, dct)

        if not PY36:
            parent_cls = super(cls, cls)
            if hasattr(parent_cls, "__init_subclass__"):
                parent_cls.__init_subclass__()
                # NOTE(gabe): you'd think the `cls` argument passed into the `__init_subclass__`
                # classmethod would be `parent_cls` here, but it's actualy just `cls`,
                # so this correctly follows the `__init_subclass__` py3.6 API.

    def __getitem__(cls, idx):
        "Emulate __class_getitem__ for Python 2"
        try:
            return cls.__class_getitem__(idx)
        except AttributeError:
            raise TypeError("{!r} object is not subscriptable".format(cls.__name__))


def _type_params_issubclass(type_params, super_type_params):
    """
    Whether each element in `type_params` is a subclass of the equivalent element in `super_type_params`.

    Recursively descends tuples and dicts in the type params to determine if
    `type_params` covariantly describes a subclass of `super_type_params`.
    """
    if isinstance(type_params, tuple) and isinstance(super_type_params, tuple):
        return len(type_params) == len(super_type_params) and all(
            _type_params_issubclass(cls, super_cls)
            for cls, super_cls in zip(type_params, super_type_params)
        )
    elif isinstance(type_params, dict) and isinstance(super_type_params, dict):
        return six.viewkeys(type_params) == six.viewkeys(super_type_params) and all(
            _type_params_issubclass(cls, super_type_params[key])
            for key, cls in six.iteritems(type_params)
        )
    else:
        if isinstance(type_params, (tuple, dict)) or isinstance(
            super_type_params, (tuple, dict)
        ):
            # above checks don't catch just 1 param being a tuple or dict
            return False
        return issubclass(type_params, super_type_params)


@six.add_metaclass(GenericProxytypeMetaclass)
class GenericProxytype(Proxytype):
    """
    Abstract base class for generic Proxytypes; i.e. abstract types that can be parameterized with other types.

    You can't instantiate this class directly; instead, use a built-in container type (like List, Tuple, etc.)
    or create your own by subclassing `GenericProxytype`.

    Type Parameters
    ---------------

    Type parameters can be given as 1 or more:

        * Subclasses of `Proxytype`
        * Dicts with string keys, and values that are subclasses of `Proxytype`

    For example, ``List[Int]``, ``Tuple[Str, Float]``, ``Function[{'a': Bool, 'b': Int}, Int]``
    are all valid parameterizations. ``Tuple[[Str, Float], Bool]`` and ``List["foo"]`` are not.

    Subclassing Instructions
    ------------------------

    You need to:

        * Write an appropriate ``__init__`` method.

          This should include a check like this:
          ```
          if self._type_params is None:
              raise TypeError(
                  f"Cannot instantiate a generic {type(self).__name__}; the item type must be specified"
              )
          ```

          If your Proxytype is representing a Python type, ``__init__`` should probably resemble
          the behavior of the Python type, and/or be able to take an instance of the Python type
          and represent it as the proxy type.

          After ``__init__`` is called, the object should conform to the Delayed interface;
          i.e. ``self.graft`` should be set. (Not mandatory, but typically what makes sense.)

        * If the default ``_promote`` classmethod doesn't work for you,
          which just calls ``__init__`` with whatever it's passed, then override it
          such that ``cls._promote(x)`` will return an instance of ``cls`` representing ``x``,
          or raise `ProxyTypeError` if promotion is not possible.

        * Write all the other methods to make your class useful (``__getattr__``, ``__getitem__``,
          ``calculate_secret_algorithm``, etc.). These will likely make heavy use of a pattern like
          ``return self._type_params[0]._from_apply(funcname, obj=self, ...)``.

    When creating a generic Proxytype, remember that in all the instance methods you write,
    ``self`` will be a _concrete_ subclass of your generic type, and ``self._type_params``
    will be a tuple of the type parameters for that concrete type. For example, though you
    might write ``class List(GenericProxytype)``, in ``__getitem__(self, idx)``, ``self``
    is a ``List[Float]``, or a ``List[List[Int]]``, etc. (and ``self._type_params`` would be
    ``(Float,)`` or ``(List[Int],)`` in those examples).

    `GenericProxytype` provides an implementation of `__class_getitem__` for you: the machinery that makes
    ``List[Int]`` work, for example. This implementation:

        * Checks that you're actually parameterizing a generic, not a concrete type
          (``List[Int][Str]`` will raise a `TypeError`)
        * Validates that all parameters are Proxytypes, or dicts containing Proxytypes as values.
          Note that the number or type of type parameters is _not_ checked.
        * Dynamically constructs a new concrete subclass of your generic type, where ``_type_params`` is set to
          the tuple of whatever was passed into ``__class_getitem__`` and ``_generictype`` is a reference
          to the parent generic type
        * Caches all concrete subclasses, so ``List[Int]`` will always return the same object,
          rather than constructing a new type on the fly every time

    By implementing ``__class_getitem_hook__``, you can customize the creation of concrete subclass objects.
    ``__class_getitem_hook__`` is called with ``name, bases, dct, type_params``
    (same as the arguments to ``type()``, plus ``type_params`` for convenience), and should return
    ``name, bases, dct``. These returned values are what are ultimately passed into ``type()``
    to dynamically construct the concrete subclass. ``__class_getitem_hook__`` must not modify
    ``dct["_type_params"]``, because that could invalidate the ``_concrete_subtypes`` registry.
    ``__class_getitem_hook__`` should be a `staticmethod`.

    The typical use-case for ``__class_getitem_hook__`` is adding methods or fields to ``dct`` based
    on ``type_params``, such as `Struct` does to add property getter functions for each of its fields.

    Since `GenericProxytype` uses the `GenericProxytypeMetaclass`, by inheriting from it,
    the Python ``isinstance`` and ``issubclass`` methods will also behave covariantly for your
    custom generic type: ``issubclass(MyType[MyIntSubclass], `MyType[Int])`` will be True.
    """

    _type_params = None

    @classmethod
    def __class_getitem__(cls, type_params):
        if cls._type_params is not None:
            raise TypeError(
                "{} type is not subscriptable "
                "(it's no longer generic and already has type parameters applied)".format(
                    cls.__name__
                )
            )
        if not isinstance(type_params, tuple):
            type_params = (type_params,)
        for i, type_param in enumerate(type_params):
            if isinstance(type_param, dict):
                assert all(
                    issubclass(param_cls, Proxytype)
                    for param_cls in six.itervalues(type_param)
                ), "Values in type parameter dict must all be Proxytypes: parameter {}: {}".format(
                    i, type_param
                )
            else:
                assert issubclass(
                    type_param, Proxytype
                ), "Type parameters must be Proxytypes, but for parameter {}, got {}".format(
                    i, type_param
                )

        # Look up these parameters in the _concrete_subtypes registry. If we've already created a
        # type for these parameters, return that object instead of making a duplicate.
        # It's a helpful invariant elsewhere to know that iff `clsA is clsB` (they're the same object),
        # then `clsA` and `clsB` are the same generic class, parameterized with the same types,
        # and can be safely considered equivalent.
        # (`cls._concrete_subtypes` was added by the GenericProxytypeMetaclass, and is an empty dict.)
        hashable_type_params = tuple(
            frozenset(six.iteritems(x)) if isinstance(x, dict) else x
            for x in type_params
        )
        try:
            return cls._concrete_subtypes[hashable_type_params]
        except KeyError:
            param_names = (
                # Default dict formatting would print values like `<class 'descarteslabs.common.proxytypes.Int'>`,
                # so we do our own dict formatting using `cls.__name__` for read/copy-ability
                "{{{}}}".format(
                    ", ".join(
                        "{!r}: {}".format(k, param_cls.__name__)
                        for k, param_cls in sorted(six.iteritems(type_param))
                    )
                )
                if isinstance(type_param, dict)
                else type_param.__name__
                for type_param in type_params
            )

            parameterized_name = "{}[{}]".format(cls.__name__, ", ".join(param_names))
            bases = (cls,)
            dct = {
                "_type_params": type_params,
                "_generictype": cls,
                "__module__": cls.__module__,
                # ^ so repr shows the concrete class as coming from its own module, not here
            }

            if hasattr(cls, "__class_getitem_hook__"):
                # allow subclasses to customize their parameterization
                # NOTE: subclasses MUST NOT modify `dct["_type_params"]`,
                # because that could invalidate the `_concrete_subtypes` registry.
                parameterized_name, bases, dct = cls.__class_getitem_hook__(
                    parameterized_name, bases, dct, type_params
                )

            # Dynamically construct a subclass of the generic type,
            # with `_type_params` set (making it a concrete type),
            # and a reference to this parent generic type (used for `issubclass` checking by the metaclass).
            ConcreteType = type(parameterized_name, bases, dct)

            cls._concrete_subtypes[hashable_type_params] = ConcreteType
            return ConcreteType

    @classmethod
    def _promote(cls, obj):
        if isinstance(obj, cls):
            return obj
        return cls(obj)

    @classmethod
    def _from_graft(cls, graft):
        """
        Create an instance of this class with the given graft dict, circumventing ``__init__``

        To use safely, this class must function correctly if its ``__init__`` method is not called.

        This is used to let your class present a friendly user-facing constructor,
        but still support copy-constuction or casting when necessary.
        """
        assert not is_generic(cls), "Cannot instantiate a generic {}".format(
            cls.__name__
        )
        return super(GenericProxytype, cls)._from_graft(graft)


def is_generic(type_):
    """
    Returns true if `type_` is generic, meaning it is a subclass of
    `GenericProxytype` and has no specified type parameters, or any of its type parameters are are also generic
    """
    type_parameters = getattr(type_, "_type_params", None)

    if type_parameters is not None:
        return any(map(is_generic, type_parameters))

    if isinstance(type_, dict):
        # in this case `type_` is a 'complex type', `dict[Str:Type]`
        complex_type = type_
        return any(map(is_generic, complex_type.values()))

    return issubclass(type_, GenericProxytype)
