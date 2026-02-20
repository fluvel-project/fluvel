# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import operator
from functools import partial, wraps
import re
from typing import Any, Type, TypeAlias
from collections.abc import Callable
from dataclasses import dataclass

Rule: TypeAlias = Callable[[Any], bool]

class To:

    @staticmethod
    def Upper(raw_value: str) -> str:
        return raw_value.upper()
    
    @staticmethod
    def Lower(raw_value: str) -> str:
        return raw_value.lower()
    
    @staticmethod
    def Strip(raw_value: Any) -> str:
        return str(raw_value).strip()

    @staticmethod
    def Title(raw_value: Any) -> str:
        return str(raw_value).title()
    
    @staticmethod
    def Alpha(raw_value: Any) -> str:
        return re.sub(r'[^a-zA-Z]', '', str(raw_value))

    @staticmethod
    def Digits(raw_value: Any) -> str:
        return re.sub(r'[^0-9]', '', str(raw_value))

    @staticmethod
    def Alnum(raw_value: Any) -> str:
        return re.sub(r'[^a-zA-Z0-9]', '', str(raw_value))

    @staticmethod
    def Positive(raw_value: Any) -> int:
        return abs(raw_value)
    
    @staticmethod
    def Count(raw_value: Any) -> int:
        return len(raw_value)
         
    @staticmethod
    def Round(raw_value: Any) -> int:
        return round(raw_value)

    @staticmethod
    def Int(raw_value: Any) -> int:
        return int(float(raw_value))

    @staticmethod
    def Float(raw_value: Any) -> float:
        return float(raw_value)

    @staticmethod
    def Bool(raw_value: Any) -> bool:
        return bool(raw_value)
    
    @staticmethod
    def Default(raw_value: Any, default: Any) -> Any:
        return raw_value if raw_value in [None, "", []] else default

    @staticmethod
    def OrElse(default: Any) -> Callable[[Any], Any]:
        return lambda raw_value: To.Default(raw_value, default)

def rgetattr(obj: Any, path: str, default: Any = None) -> Any:
    """
    Allows deep access to attributes using dot notation.
    """
    try:
        for key in path.split('.'):
            # Support for dictionaries and objects
            if isinstance(obj, dict):
                obj = obj.get(key, default)
            else:
                obj = getattr(obj, key, default)
        return obj
    except (AttributeError, TypeError):
        return default

@dataclass(slots=True, frozen=True)
class Var:
    "Extract, transform, and track data access from a model."
    attr: str | Callable[[Any], Any]
    transform: Callable[[Any], Any] = lambda x: x

    def get_value(self, model: Any) -> Any:
        if isinstance(self.attr, str):
            raw_value = rgetattr(model, self.attr, None)
        else:
            raw_value = self.attr(model)
        
        return self.transform(raw_value)


def _op_left(model: Any, left: str | Var) -> Any:
    """Resolves the left operand: it is always an attribute or a variable."""
    if isinstance(left, Var):
        return left.get_value(model)
    return rgetattr(model, left, None)

def _op_right(model: Any, right: str | Var | Any) -> Any:
    """Resolves the right operand, it can be an attribute, variable, or literal."""
    if isinstance(right, Var):
        return right.get_value(model)
    return right # It's a direct literal value (int, float, bool, str)

class Is:
    """Validations of direct properties."""

    @staticmethod
    def Pair(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) % 2 == 0

    @staticmethod
    def Odd(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) % 2 != 0

    @staticmethod
    def Positive(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) > 0

    @staticmethod
    def Zero(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) == 0

    @staticmethod
    def Negative(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) < 0

    @staticmethod
    def Defined(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) is not None

    @staticmethod
    def Nil(attr: str | Var) -> Rule:
        return lambda model: _op_left(model, attr) is None
    
    @staticmethod
    def Truthy(attr: str | Var) -> Rule:
        return lambda model: bool(_op_left(model, attr))

    @staticmethod
    def Falsy(attr: str | Var) -> Rule:
        return lambda model: not bool(_op_left(model, attr))

    @staticmethod
    def Empty(attr: str | Var) -> Rule:
        return lambda model: len(_op_left(model, attr)) == 0

    @staticmethod
    def NotEmpty(attr: str | Var) -> Rule:
        return lambda model: len(_op_left(model, attr)) > 0
    
    @staticmethod
    def Type(attr: str | Var, t: Type) -> Rule:
        return lambda model: isinstance(_op_left(model, attr), t)
    
    @staticmethod
    def NotType(attr: str | Var, t: Type) -> Rule:
        return lambda model: not isinstance(_op_left(model, attr), t)

    @staticmethod
    def Alpha(attr: str | Var) -> Rule:
        return lambda model: (val := _op_left(model, attr)) is not None and str(val).isalpha()

    @staticmethod
    def Numeric(attr: str | Var) -> Rule:
        return lambda model: (val := _op_left(model, attr)) is not None and str(val).isnumeric()

    @staticmethod
    def Alnum(attr: str | Var) -> Rule:
        return lambda model: (val := _op_left(model, attr)) is not None and str(val).isalnum()

    # Shortcuts for standard types
    Integer = lambda attr: Is.Type(attr, int)
    String  = lambda attr: Is.Type(attr, str)
    Decimal = lambda attr: Is.Type(attr, float)
    List    = lambda attr: Is.Type(attr, list)
    Map     = lambda attr: Is.Type(attr, dict)

class If:
    """Structural logic, relationships and dynamic comparisons."""

    @staticmethod
    def _create_comp(op: Callable, left: str | Var, right: Any | Var) -> Rule:
        return lambda model: op(_op_left(model, left), _op_right(model, right))
    
    Equals         = partial(_create_comp, operator.eq)
    NotEqual       = partial(_create_comp, operator.ne)
    Greater        = partial(_create_comp, operator.gt)
    GreaterOrEqual = partial(_create_comp, operator.ge) 
    Less           = partial(_create_comp, operator.lt)
    LessOrEqual    = partial(_create_comp, operator.le)
    Has            = partial(_create_comp, operator.contains)
    HasNot         = partial(_create_comp, lambda l, r: r not in l) 

    @staticmethod
    def MoreThan(attr: str | Var, max_items: int) -> Rule:
        return lambda model: len(_op_left(model, attr)) > max_items

    @staticmethod
    def InRange(attr: str | Var, min_val: Any | Var, max_val: Any | Var) -> Rule:
        return lambda model: _op_right(model, min_val) <= _op_left(model, attr) <= _op_right(model, max_val)
    
    @staticmethod
    def NotInRange(attr: str | Var, min_val: Any | Var, max_val: Any | Var) -> Rule:
        return lambda model: _op_left(model, attr) < _op_right(model, min_val) or _op_left(model, attr) > _op_right(model, max_val)

    @staticmethod
    def AtKey(attr: str | Var, key: Any | Var, expected: Any | Var) -> Rule:
        return lambda model: _op_left(model, attr)[_op_right(model, key)] == _op_right(model, expected)

    @staticmethod
    def Match(attr: str | Var, regex: str) -> Rule:
        return lambda model: bool(re.match(_op_right(model, regex), _op_left(model, attr)))

    @staticmethod
    def StartsWith(attr: str | Var, prefix: str | Var) -> Rule:
        return lambda model: str(_op_left(model, attr)).startswith(_op_right(model, prefix))

    @staticmethod
    def EndsWith(attr: str | Var, suffix: str | Var) -> Rule:
        return lambda model: str(_op_left(model, attr)).endswith(_op_right(model, suffix))

    # --- Logic ---
    @staticmethod
    def All(*conds: Rule) -> Rule:
        return lambda model: all(c(model) for c in conds)

    @staticmethod
    def Any(*conds: Rule) -> Rule:
        return lambda model: any(c(model) for c in conds)

    @staticmethod
    def Not(cond: Rule) -> Rule:
        return lambda model: not cond(model)
    
    # Sugar Syntax (Aliases for readability)
    Every = All
    Either = Any
    AtLeast = GreaterOrEqual
    AtMost = LessOrEqual
    Between = InRange
    Outside = NotInRange