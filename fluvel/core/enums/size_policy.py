# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

from typing import Literal, final

from PySide6.QtWidgets import QSizePolicy

SizePolicyTypes = Literal[
    "fixed", "minimum", "maximum", "preferred", "expanding", "min-expanding", "ignored"
]


@final
class SizePolicy:
    FIXED = QSizePolicy.Policy.Fixed
    MINIMUM = QSizePolicy.Policy.Minimum
    MAXIMUM = QSizePolicy.Policy.Maximum
    PREFERRED = QSizePolicy.Policy.Preferred
    EXPANDING = QSizePolicy.Policy.Expanding
    MIN_EXPANDING = QSizePolicy.Policy.MinimumExpanding
    IGNORED = QSizePolicy.Policy.Ignored

    __MAP__: dict[SizePolicyTypes, QSizePolicy.Policy] = {
        "fixed": FIXED,
        "minimum": MINIMUM,
        "maximum": MAXIMUM,
        "preferred": PREFERRED,
        "expanding": EXPANDING,
        "min-expanding": MIN_EXPANDING,
        "ignored": IGNORED,
    }

    @staticmethod
    def get(size_policy: SizePolicyTypes | tuple[SizePolicyTypes, SizePolicyTypes]) -> QSizePolicy:
        # local binding
        _map = SizePolicy.__MAP__
        _default = QSizePolicy.Policy.Preferred

        if isinstance(size_policy, str):
            pol = _map.get(size_policy, _default)
            return QSizePolicy(pol, pol)

        elif isinstance(size_policy, tuple) and len(size_policy) == 2:
            h_pol = _map.get(size_policy[0], _default)
            v_pol = _map.get(size_policy[1], _default)
            return QSizePolicy(h_pol, v_pol)

        return QSizePolicy(_default, _default)
