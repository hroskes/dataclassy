"""
 Copyright (C) 2020 biqqles.
 This Source Code Form is subject to the terms of the Mozilla Public
 License, v. 2.0. If a copy of the MPL was not distributed with this
 file, You can obtain one at http://mozilla.org/MPL/2.0/.

 This file defines functions which operate on data classes.
"""
from typing import Any, Callable, Dict, Tuple

from .dataclass import DataClassMeta, DataClass, Internal


def is_dataclass(obj: Any) -> bool:
    """Return True if the given object is a data class as implemented in this package, otherwise False."""
    return getattr(obj, '__metaclass__', None) is DataClassMeta


def is_dataclass_instance(obj: Any) -> bool:
    """Return True if the given object is an instance of a data class, otherwise False."""
    return is_dataclass(obj) and type(obj) is not DataClassMeta


def fields(dataclass: DataClass, internals=False) -> Dict[str, Any]:
    """Return a dict of `dataclass`'s fields and their values. `internals` selects whether to include internal fields.
    A field is defined as a class-level variable with a type annotation."""
    assert is_dataclass_instance(dataclass)
    return {f: getattr(dataclass, f) for f in _filter_annotations(dataclass.__annotations__, internals)}


def as_dict(dataclass: DataClass, dict_factory=dict) -> Dict[str, Any]:
    """Recursively create a dict of a dataclass instance's fields and their values.
    This function is recursively called on data classes, named tuples and iterables."""
    assert is_dataclass_instance(dataclass)
    return _recurse_structure(dataclass, dict_factory)


def as_tuple(dataclass: DataClass) -> Tuple:
    """Recursively create a tuple of the values of a dataclass instance's fields, in definition order.
    This function is recursively called on data classes, named tuples and iterables."""
    assert is_dataclass_instance(dataclass)
    return _recurse_structure(dataclass, lambda k_v: tuple(v for k, v in k_v))


def _filter_annotations(annotations: Dict[str, Any], internals: bool) -> Dict[str, Any]:
    """Filter an annotations dict for to remove or keep internal fields."""
    return annotations if internals else {f: a for f, a in annotations.items()
                                          if not f.startswith('_') and not Internal.is_internal(a)}


def _recurse_structure(var: Any, iter_proc: Callable) -> Any:
    """Recursively convert an arbitrarily nested structure beginning at `var`, copying and processing any iterables
    encountered with `iter_proc`."""
    if is_dataclass(var):
        var = fields(var, internals=True)
    if hasattr(var, '_asdict'):  # handle named tuples
        # noinspection PyCallingNonCallable, PyProtectedMember
        var = var._asdict()
    if isinstance(var, dict):
        return iter_proc((_recurse_structure(k, iter_proc), _recurse_structure(v, iter_proc)) for k, v in var.items())
    if isinstance(var, (list, tuple)):
        return type(var)(_recurse_structure(e, iter_proc) for e in var)
    return var