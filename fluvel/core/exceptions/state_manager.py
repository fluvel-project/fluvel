# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

class FluvelBindingError(ValueError):
    """Exception thrown when the Data Binding syntax is invalid."""

    pass


class FluvelStateError(RuntimeError):
    """Exception thrown due to errors related to the State manager."""

    pass
