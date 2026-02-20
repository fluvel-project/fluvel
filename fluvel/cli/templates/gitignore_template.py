# Copyright (C) 2025-2026 J. F. Escobar
# SPDX-License-Identifier: LGPL-3.0-or-later

GITIGNORE_TEMPLATE = """# Fluvel Internal
.fluvel/

# Environments
.env
.env.*
!.env.example

# Python Environment & Cache
__pycache__/
*.py[cod]
*$py.class
.venv/
venv/

# Distribution / Build
dist/
build/
*.spec
*.egg-info/
*.egg

# Logs & OS
*.log
.DS_Store
Thumbs.db

# Databases
*.sqlite
*.sqlite3
*.db
"""
