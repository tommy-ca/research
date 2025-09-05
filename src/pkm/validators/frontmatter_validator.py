"""
PKM Validation System - Frontmatter Validator
FR-VAL-002: YAML Frontmatter Validation Implementation

TDD REFACTOR Phase: Optimized implementation with extracted schemas
Following SOLID principles: Single responsibility, dependency inversion
Following DRY principle: Reuse schema definitions and validation rules
"""

from pathlib import Path
from typing import List, Tuple, Dict, Any, Optional
import yaml
from functools import lru_cache
from .base import BaseValidator, ValidationResult
from .schemas.frontmatter_schema import ValidationRules


class FrontmatterValidator(BaseValidator):
    """
    Validates YAML frontmatter using centralized schema definitions.
    
    Follows SOLID principles:
    - Single Responsibility: Only validates frontmatter
    - Open/Closed: Extensible through schema configuration
    - Dependency Inversion: Depends on ValidationRules abstraction
    """
    
    def __init__(self, validation_rules: Optional[ValidationRules] = None):
        """Initialize validator with optional custom validation rules"""
        self.rules = validation_rules or ValidationRules()
        
        # Performance optimization: cache compiled patterns
        self._date_pattern = self.rules.DATE_PATTERN
        self._valid_types = self.rules.VALID_TYPES
        self._valid_statuses = self.rules.VALID_STATUSES
    
    def validate(self, file_path: Path) -> List[ValidationResult]:
        """
        Validate YAML frontmatter in markdown file.
        
        Performance optimizations:
        - Content hashing for caching repeated validations
        - Early return on parsing errors
        - Efficient error accumulation
        """
        results = []
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Create content hash for caching
            import hashlib
            content_hash = hashlib.md5(content.encode()).hexdigest()
            
            frontmatter, parse_error = self._extract_frontmatter(content_hash, content)
            
            if parse_error:
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="frontmatter-parse-error",
                    severity="error",
                    message=parse_error
                ))
                return results  # Early return: can't validate content if parsing failed
            
            # Validate using optimized methods
            results.extend(self._validate_required_fields(frontmatter, file_path))
            results.extend(self._validate_field_formats(frontmatter, file_path))
            
        except FileNotFoundError:
            results.append(ValidationResult(
                file_path=file_path,
                rule="file-not-found",
                severity="error",
                message=f"File not found: {file_path}"
            ))
        except PermissionError:
            results.append(ValidationResult(
                file_path=file_path,
                rule="permission-error",
                severity="error",
                message=f"Permission denied reading file: {file_path}"
            ))
        except UnicodeDecodeError as e:
            results.append(ValidationResult(
                file_path=file_path,
                rule="encoding-error",
                severity="error",
                message=f"File encoding error - ensure file is UTF-8 encoded: {e}"
            ))
        except Exception as e:
            results.append(ValidationResult(
                file_path=file_path,
                rule="validation-error",
                severity="error",
                message=f"Unexpected validation error: {e}"
            ))
        
        return results
    
    @lru_cache(maxsize=128)
    def _extract_frontmatter(self, content_hash: str, content: str) -> Tuple[Dict[Any, Any], str]:
        """
        Extract frontmatter from markdown content - optimized with caching.
        
        Performance optimization: Cache results for repeated validation of same content.
        Content hash used as cache key to ensure cache correctness.
        """
        content = content.strip()
        
        if not content.startswith('---'):
            return {}, self.rules.format_error_message('missing_frontmatter')
        
        try:
            # Split on frontmatter delimiters - optimized approach
            parts = content.split('---', 2)
            if len(parts) < 3:
                return {}, "Invalid frontmatter structure - missing closing delimiter"
            
            frontmatter_yaml = parts[1].strip()
            
            # Handle empty frontmatter
            if not frontmatter_yaml:
                return {}, ""  # Empty frontmatter is valid YAML, just empty
            
            # Parse YAML with safe loader
            frontmatter = yaml.safe_load(frontmatter_yaml)
            return frontmatter or {}, ""
            
        except yaml.YAMLError as e:
            return {}, self.rules.format_error_message('invalid_yaml', error=str(e))
        except Exception as e:
            return {}, f"Frontmatter parsing error: {e}"
    
    def _validate_required_fields(self, frontmatter: Dict[Any, Any], file_path: Path) -> List[ValidationResult]:
        """
        Validate required fields presence using centralized rules.
        
        Performance optimization: Use set operations for fast lookups
        """
        results = []
        present_fields = set(frontmatter.keys())
        missing_fields = self.rules.REQUIRED_FIELDS - present_fields
        
        for field in missing_fields:
            results.append(ValidationResult(
                file_path=file_path,
                rule="missing-required-field",
                severity="error",
                message=self.rules.format_error_message('missing_field', field=field)
            ))
        
        return results
    
    def _validate_field_formats(self, frontmatter: Dict[Any, Any], file_path: Path) -> List[ValidationResult]:
        """
        Validate field formats using centralized rules and enhanced error messages.
        
        Performance optimizations:
        - Early returns on invalid data
        - Efficient type checking
        - Pre-compiled regex patterns
        """
        results = []
        
        # Date format validation - optimized with pre-compiled regex
        if 'date' in frontmatter:
            date_value = str(frontmatter['date'])
            if not self._date_pattern.match(date_value):
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="invalid-date-format",
                    severity="error",
                    message=self.rules.format_error_message('invalid_date', value=date_value)
                ))
        
        # Type validation - optimized with set lookup
        if 'type' in frontmatter:
            type_value = frontmatter['type']
            if type_value not in self._valid_types:
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="invalid-note-type",
                    severity="error",
                    message=self.rules.format_error_message('invalid_type', value=type_value)
                ))
        
        # Tags validation - efficient with early returns
        if 'tags' in frontmatter:
            tags_value = frontmatter['tags']
            if not isinstance(tags_value, list):
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="invalid-tags-format",
                    severity="error",
                    message=self.rules.format_error_message('invalid_tags', actual_type=type(tags_value).__name__)
                ))
            else:
                # Efficient tag content validation with early exit
                for tag in tags_value:
                    if not isinstance(tag, str):
                        results.append(ValidationResult(
                            file_path=file_path,
                            rule="invalid-tags-format",
                            severity="error",
                            message=self.rules.format_error_message('invalid_tag_content', invalid_tag=repr(tag))
                        ))
                        break  # Early exit: only report first invalid tag for cleaner output
        
        # Status validation - optimized with set lookup
        if 'status' in frontmatter:
            status_value = frontmatter['status']
            if status_value not in self._valid_statuses:
                results.append(ValidationResult(
                    file_path=file_path,
                    rule="invalid-status",
                    severity="error", 
                    message=self.rules.format_error_message('invalid_status', value=status_value)
                ))
        
        return results