"""
PKM Validation System - Frontmatter Schema Definitions
FR-VAL-002: YAML Frontmatter Schema and Validation Rules

TDD REFACTOR Phase: Extract schema definitions for maintainability and reuse
Following DRY principle: Single source of truth for validation rules
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any, Set
import re
from datetime import datetime


class FrontmatterSchema(BaseModel):
    """Type-safe frontmatter schema using Pydantic - comprehensive validation"""
    
    # Required fields
    date: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$', description="ISO date format (YYYY-MM-DD)")
    type: Literal["daily", "zettel", "project", "area", "resource", "capture"] = Field(description="Note type classification")
    tags: List[str] = Field(description="Array of tag strings")
    status: Literal["draft", "active", "review", "complete", "archived"] = Field(description="Note status")
    
    # Optional fields
    links: Optional[List[str]] = Field(None, description="Array of wiki-style links [[note]]")
    source: Optional[str] = Field(None, description="Source of the content")
    author: Optional[str] = Field(None, description="Author of the note")
    modified: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$', description="Last modified date")
    title: Optional[str] = Field(None, description="Note title")
    
    model_config = {
        "extra": "allow",  # Allow additional custom fields
        "str_strip_whitespace": True,  # Strip whitespace from strings
    }


class ValidationRules:
    """Centralized validation rules and constants - DRY principle"""
    
    # Required field definitions
    REQUIRED_FIELDS: Set[str] = {'date', 'type', 'tags', 'status'}
    
    # Valid enum values
    VALID_TYPES: Set[str] = {'daily', 'zettel', 'project', 'area', 'resource', 'capture'}
    VALID_STATUSES: Set[str] = {'draft', 'active', 'review', 'complete', 'archived'}
    
    # Regex patterns (compiled for performance)
    DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    FRONTMATTER_DELIMITER_PATTERN = re.compile(r'^---\s*$', re.MULTILINE)
    
    # Error message templates
    ERROR_MESSAGES = {
        'missing_frontmatter': "No frontmatter found. Expected YAML frontmatter between '---' delimiters at the beginning of the file",
        'invalid_yaml': "Invalid YAML syntax in frontmatter: {error}",
        'missing_field': "Required field '{field}' is missing. All notes must have: {required_fields}",
        'invalid_date': "Invalid date format '{value}'. Expected YYYY-MM-DD format (e.g., '{example_date}')",
        'invalid_type': "Invalid note type '{value}'. Valid types: {valid_types}",
        'invalid_status': "Invalid status '{value}'. Valid statuses: {valid_statuses}",
        'invalid_tags': "Tags must be an array of strings. Found: {actual_type}",
        'invalid_tag_content': "All tags must be strings. Found non-string tag: {invalid_tag}",
    }
    
    @classmethod
    def get_example_date(cls) -> str:
        """Get current date as example for error messages"""
        return datetime.now().strftime("%Y-%m-%d")
    
    @classmethod
    def format_error_message(cls, error_type: str, **kwargs) -> str:
        """Format error message with contextual information"""
        template = cls.ERROR_MESSAGES.get(error_type, "Unknown validation error")
        
        # Add dynamic values
        if error_type == 'missing_field':
            kwargs['required_fields'] = ', '.join(sorted(cls.REQUIRED_FIELDS))
        elif error_type == 'invalid_date':
            kwargs['example_date'] = cls.get_example_date()
        elif error_type == 'invalid_type':
            kwargs['valid_types'] = ', '.join(sorted(cls.VALID_TYPES))
        elif error_type == 'invalid_status':
            kwargs['valid_statuses'] = ', '.join(sorted(cls.VALID_STATUSES))
        
        try:
            return template.format(**kwargs)
        except KeyError:
            # Fallback if template variables are missing
            return template


class FrontmatterValidator:
    """Enhanced frontmatter validation using schema definitions"""
    
    def __init__(self):
        self.rules = ValidationRules()
        self._schema_model = FrontmatterSchema
    
    def validate_structure(self, frontmatter: Dict[Any, Any]) -> List[Dict[str, str]]:
        """Validate frontmatter structure using Pydantic schema"""
        errors = []
        
        try:
            # Validate using Pydantic model
            self._schema_model(**frontmatter)
        except Exception as e:
            # Convert Pydantic validation errors to our format
            errors.append({
                'rule': 'schema-validation-error',
                'severity': 'error',
                'message': f"Schema validation failed: {e}"
            })
        
        return errors
    
    def validate_required_fields(self, frontmatter: Dict[Any, Any]) -> List[Dict[str, str]]:
        """Validate presence of required fields"""
        errors = []
        
        for field in self.rules.REQUIRED_FIELDS:
            if field not in frontmatter:
                errors.append({
                    'rule': 'missing-required-field',
                    'severity': 'error',
                    'message': self.rules.format_error_message('missing_field', field=field)
                })
        
        return errors
    
    def validate_field_formats(self, frontmatter: Dict[Any, Any]) -> List[Dict[str, str]]:
        """Validate individual field formats"""
        errors = []
        
        # Date validation
        if 'date' in frontmatter:
            date_value = str(frontmatter['date'])
            if not self.rules.DATE_PATTERN.match(date_value):
                errors.append({
                    'rule': 'invalid-date-format',
                    'severity': 'error',
                    'message': self.rules.format_error_message('invalid_date', value=date_value)
                })
        
        # Type validation
        if 'type' in frontmatter:
            type_value = frontmatter['type']
            if type_value not in self.rules.VALID_TYPES:
                errors.append({
                    'rule': 'invalid-note-type',
                    'severity': 'error',
                    'message': self.rules.format_error_message('invalid_type', value=type_value)
                })
        
        # Tags validation
        if 'tags' in frontmatter:
            tags_value = frontmatter['tags']
            if not isinstance(tags_value, list):
                errors.append({
                    'rule': 'invalid-tags-format',
                    'severity': 'error',
                    'message': self.rules.format_error_message('invalid_tags', actual_type=type(tags_value).__name__)
                })
            else:
                # Check individual tag types
                for tag in tags_value:
                    if not isinstance(tag, str):
                        errors.append({
                            'rule': 'invalid-tags-format',
                            'severity': 'error',
                            'message': self.rules.format_error_message('invalid_tag_content', invalid_tag=repr(tag))
                        })
                        break  # Only report first invalid tag
        
        # Status validation
        if 'status' in frontmatter:
            status_value = frontmatter['status']
            if status_value not in self.rules.VALID_STATUSES:
                errors.append({
                    'rule': 'invalid-status',
                    'severity': 'error',
                    'message': self.rules.format_error_message('invalid_status', value=status_value)
                })
        
        return errors


def get_frontmatter_schema() -> type[FrontmatterSchema]:
    """Get the frontmatter Pydantic schema class for external use"""
    return FrontmatterSchema


def get_validation_rules() -> ValidationRules:
    """Get validation rules instance for external use"""
    return ValidationRules()


# Export commonly used constants for convenience
__all__ = [
    'FrontmatterSchema',
    'ValidationRules', 
    'FrontmatterValidator',
    'get_frontmatter_schema',
    'get_validation_rules'
]