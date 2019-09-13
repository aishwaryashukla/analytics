"""
<add description here>

(c)  2018 BlackRock.  All rights reserved.
"""

# Import these attributes into other files as needed to
# identify the project version at runtime.
try:
    from .version import git_revision as __git_revision__
    from .version import version as __version__
except ImportError:
    __git_revision__ = 'Unknown'
    __version__ = 'Unknown'
