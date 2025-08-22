"""PKM Core Package"""

from .base import BasePkmProcessor

# Import optional modules that may exist
try:
    from .atomic_notes import PkmAtomicNote
except ImportError:
    PkmAtomicNote = None

try:
    from .process_inbox import PkmProcessInbox
except ImportError:
    PkmProcessInbox = None

try:
    from .capture import PkmCapture
except ImportError:
    PkmCapture = None

__all__ = [
    'BasePkmProcessor'
]

# Add optional modules to __all__ if they exist
if PkmAtomicNote is not None:
    __all__.append('PkmAtomicNote')
if PkmProcessInbox is not None:
    __all__.append('PkmProcessInbox')
if PkmCapture is not None:
    __all__.append('PkmCapture')
