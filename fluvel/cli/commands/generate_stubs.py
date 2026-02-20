# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

import click

# Fluvel
from fluvel.cli.tools.StubGenerator import StubGen


@click.command
def generate_stubs():
    StubGen.generate_stubs()
