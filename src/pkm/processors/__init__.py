"""PKM Processors Package

Note: Architecture migration processor moved to `pkm_maintenance.migration.processors`.
"""

from .architecture_processor import ArchitectureDocumentProcessor

__all__ = ['ArchitectureDocumentProcessor']
