#### Source Code: [fluvel/reactive/pyro/rules.py](../../../fluvel/reactive/pyro/rules.py)

# Reactive Rules Engine (`Pyro.Rules`)

The module provides a declarative infrastructure for the **extraction**, **transformation**, and **validation of model-based data**. It is designed to be highly readable, allowing complex logic to be defined using an almost natural syntax.

## Main Components

**1. `Var` (Dynamic Variables)**

The `Var` class is the primary resource for data extraction. It allows access to model attributes (using dot notation for depth) and apply transformations along the way.

```python

name_var = Var("user.profile.name", To.Upper)
value = name_var.get_value(MyModel) # Returns "JOHN"

# It can support dictionary access
class MyModel:
    user = {"profile": {"name": "John"}}

# Or through object composition
class Profile:
    name: str

class User:
    profile: Profile

class MyModel:
    user: User
```

Although the `Var` class is not intended to be used independently, but rather as a usability extension for the `If` and `Is` classes.

**2. `To` (Transformations)**

A collection of static utilities to normalize and convert data.

| Method | Description |
|--------|-------------|
|`To.Upper` / `To.Lower`| Changes the text case. |
|`To.Strip`| Removes whitespace. |
|`To.Alpha`| Keeps only letters (a-z, A-Z). |
|`To.Digits`| Keeps only digits (0-9). |
|`To.Alnum`| Keeps letters and numbers. |
|`To.Count`| Returns the length of the object. |
|`To.Int` / `To.Float`| Safe type conversion.|
|`To.Default`| Evaluates and returns a replacement value if the original is null or empty (`None`, `""`, `[]`). |
|`To.OrElse`| Creates a reusable transformer for `Var` that injects a default value when the source fails. |
---

**3. Validation with `Is` and `If`**
The engine separates validations into two logical categories to maintain structural clarity.

**Class `Is`: Direct Property Validations**
Ideal for checking intrinsic properties of a single attribute.

| Method | Truth Condition (True if...) |
|--------|-------------|
| `Is.Pair` / `Is.Odd` | The value is even or odd. |
| `Is.Positive` / `Is.Negative` | The number is greater than or less than zero. |
| `Is.Zero` | The value is exactly `0`. |
| `Is.Defined` / `Is.Nil` | The value is not `None` or is `None`. | 
| `Is.Truthy` / `Is.Falsy` | The value evaluates as true or false. |
| `Is.Empty` / `Is.NotEmpty` | The length of the attribute is `0` or greater than `0`. |
| `Is.Type` / `Is.NotType` | The value matches (or does not match) the specified type. |
| `Is.Alpha` / `Is.Numeric` | The string is purely alphabetic or numeric. |
| `Is.Alnum` | The string contains only letters and digits. |
| `Is.Integer` | The value is strictly an `int` |
| `Is.String` | The value is strictly a `str` |
| `Is.Decimal` | The value is strictly a `float` |
| `Is.List` | The value is strictly a `list` |
| `Is.Map` | the value is strictly a `dict` |
---

**Class `If`: Comparative and Structural Logic**
Used for relationships between attributes, variables, or literal values.

**Comparison Predicates**: These methods evaluate the relationship between the model attribute and an external value (or a `Var`).

| Method | Sugar Alias |Truth Condition (True if...) |
|:-------|:------------|:----------------------------|
| `If.Equals` / `If.NotEqual` | - | The attribute is equal (or different) to the target. |
| `If.Greater` | - | The attribute is strictly greater than the target. |
| `If.GreaterOrEqual` | `If.AtLeast` | The attribute is greater or equal than the target. |
| `If.Less` | - | The attribute is strictly less than the target. |
| `If.LessOrEqual` | `If.AtMost` | The attribute is less or equal than the target. |
| `If.InRange` | `If.Between` | The value is **within** the `min` and `max` range (inclusive). |
| `If.NotInRange` | `If.Outside` | The value is **outside** the `min` and `max` range. |
| `If.Has` / `If.HasNot` | - | A collection contains (or does not contain) the element. |
| `If.MoreThan` | - | The attribute length exceeds the maximum limit. |
| `If.AtKey` | - | The value in a specific `key` of the map is the expected one. |
| `If.Match` | - | The value matches a regular expression (Regex) pattern. |
| `If.StartsWith` / `If.EndsWith` | - | The string starts or ends with the given prefix/suffix. |

**Logical Composition**: These methods do not compare values directly, but act as "glue" to group multiple rules and determine a final result.

| Method | Sugar Alias | Truth Condition (True if...) |
|:-------|:----------- |:-----------------------------|
| `If.All` |`If.Every` | **All** nested rules are `True`. |
| `If.Any` |`If.Either` | **At least one** of the rules is `True`. |
| `If.Not` | - | Inverts the logical result of the rule. |

## Practical Example
```python
is_valid_order = If.All(
    # Technical precision
    If.AtKey("metadata", "id", "OFFER-2024"),
    If.Match("sku", r"^[A-Z]{3}-\d+$"),

    # Semantic business rules
    If.Every(
        If.AtLeast("user.age", 18),
        If.Between("quantity", 1, 100),
        If.MoreThan("items", 0)
    )
)
```

## Implementation Note for Pyro

**Predicates** are the leaves of your decision tree, while **Logic** is the structure that allows creating conditions of infinite depth. In `Pyro`, an `@effect` always expects a boolean result derived from this combination.