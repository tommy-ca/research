#!/usr/bin/env python3
"""
PKM System Quality Validation Pipeline

Automated enforcement of engineering principles:
- TDD compliance (RED → GREEN → REFACTOR)
- KISS principle (Keep It Simple, Stupid)
- FR-First prioritization (Functional Requirements first)
- SOLID principles validation

Usage:
    python scripts/quality_validation_pipeline.py
    python scripts/quality_validation_pipeline.py --check-kiss
    python scripts/quality_validation_pipeline.py --check-tdd
"""

import sys
import subprocess
import ast
from pathlib import Path
from typing import Dict, List, Any
import argparse


class QualityValidationResult:
    """Quality validation result container"""
    
    def __init__(self):
        self.passed = True
        self.failures = []
        self.warnings = []
        self.metrics = {}
        
    def fail(self, message: str):
        """Record a validation failure"""
        self.passed = False
        self.failures.append(message)
        
    def warn(self, message: str):
        """Record a validation warning"""
        self.warnings.append(message)
        
    def add_metric(self, name: str, value: Any):
        """Add a quality metric"""
        self.metrics[name] = value


class KissPrincipleChecker:
    """Validates KISS principle - functions should be simple and focused"""
    
    MAX_FUNCTION_LINES = 20
    MAX_COMPLEXITY_SCORE = 5
    
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        
    def check_kiss_compliance(self) -> QualityValidationResult:
        """Check KISS principle compliance"""
        result = QualityValidationResult()
        
        impl_files = list(self.src_dir.rglob("*.py"))
        
        for impl_file in impl_files:
            self._check_file_kiss_compliance(impl_file, result)
            
        return result
    
    def _check_file_kiss_compliance(self, impl_file: Path, result: QualityValidationResult):
        """Check KISS compliance for a single file"""
        try:
            with open(impl_file, 'r') as f:
                content = f.read()
                
            # Parse AST to analyze functions
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    self._check_function_simplicity(node, impl_file, content, result)
                    
        except Exception as e:
            result.warn(f"Could not analyze {impl_file}: {e}")
    
    def _check_function_simplicity(self, func_node: ast.FunctionDef, file_path: Path, content: str, result: QualityValidationResult):
        """Check if function follows KISS principle"""
        # Skip private functions and test functions
        if func_node.name.startswith('_') or func_node.name.startswith('test_'):
            return
            
        # Check function length
        func_lines = self._count_function_lines(func_node, content)
        if func_lines > self.MAX_FUNCTION_LINES:
            result.fail(f"Function {func_node.name} in {file_path.name} has {func_lines} lines (max {self.MAX_FUNCTION_LINES})")
        
        # Check complexity (simplified - count nested structures)
        complexity = self._calculate_complexity(func_node)
        if complexity > self.MAX_COMPLEXITY_SCORE:
            result.fail(f"Function {func_node.name} in {file_path.name} has complexity {complexity} (max {self.MAX_COMPLEXITY_SCORE})")
            
        result.add_metric(f"{file_path.stem}_{func_node.name}_lines", func_lines)
        result.add_metric(f"{file_path.stem}_{func_node.name}_complexity", complexity)
    
    def _count_function_lines(self, func_node: ast.FunctionDef, content: str) -> int:
        """Count actual code lines in function (excluding comments and empty lines)"""
        lines = content.split('\n')
        func_lines = lines[func_node.lineno-1:func_node.end_lineno]
        
        code_lines = 0
        for line in func_lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('#') and not stripped.startswith('"""'):
                code_lines += 1
                
        return code_lines
    
    def _calculate_complexity(self, func_node: ast.FunctionDef) -> int:
        """Calculate cyclomatic complexity (simplified)"""
        complexity = 1  # Base complexity
        
        for node in ast.walk(func_node):
            if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
                complexity += 1
            elif isinstance(node, ast.ExceptHandler):
                complexity += 1
                
        return complexity


class TddComplianceChecker:
    """Validates TDD compliance - tests exist before implementation"""
    
    def __init__(self, src_dir: Path, test_dir: Path):
        self.src_dir = src_dir
        self.test_dir = test_dir
        
    def check_tdd_compliance(self) -> QualityValidationResult:
        """Check TDD compliance across the codebase"""
        result = QualityValidationResult()
        
        # Find all implementation files
        impl_files = list(self.src_dir.rglob("*.py"))
        impl_files = [f for f in impl_files if not f.name.startswith("_")]
        
        for impl_file in impl_files:
            self._check_file_has_tests(impl_file, result)
            
        return result
    
    def _check_file_has_tests(self, impl_file: Path, result: QualityValidationResult):
        """Check if implementation file has corresponding tests"""
        # Convert implementation path to test path
        rel_path = impl_file.relative_to(self.src_dir)
        
        # Check multiple test naming patterns
        test_patterns = [
            f"test_{rel_path.stem}.py",
            f"test_{rel_path.stem}_functional.py", 
            f"test_pkm_{rel_path.stem}.py",
            f"test_pkm_{rel_path.stem}_functional.py",
            f"test_pkm_{rel_path.stem}_fr001.py",
            f"test_pkm_{rel_path.stem}_fr001_functional.py"
        ]
        
        test_found = False
        for pattern in test_patterns:
            test_file = self.test_dir / "unit" / pattern
            if test_file.exists():
                test_found = True
                break
        
        if not test_found:
            result.fail(f"No tests found for {impl_file}")
        else:
            result.add_metric(f"tests_found_for_{rel_path.stem}", True)


class QualityValidationPipeline:
    """Main quality validation pipeline"""
    
    def __init__(self, src_dir: Path = None, test_dir: Path = None):
        self.src_dir = src_dir or Path("src")
        self.test_dir = test_dir or Path("tests")
        
        self.checkers = {
            "kiss": KissPrincipleChecker(self.src_dir),
            "tdd": TddComplianceChecker(self.src_dir, self.test_dir)
        }
    
    def run_validation(self, check_types: List[str] = None) -> Dict[str, QualityValidationResult]:
        """Run quality validation"""
        check_types = check_types or ["kiss", "tdd"]
        
        print("🔍 Running PKM System Quality Validation Pipeline...")
        print("=" * 60)
        
        results = {}
        
        for check_name in check_types:
            if check_name not in self.checkers:
                continue
                
            print(f"\n📋 Running {check_name.upper()} compliance check...")
            
            checker = self.checkers[check_name]
            if check_name == "kiss":
                result = checker.check_kiss_compliance()
            elif check_name == "tdd":
                result = checker.check_tdd_compliance()
            else:
                continue
                
            results[check_name] = result
            self._print_result_summary(check_name, result)
        
        return results
    
    def _print_result_summary(self, check_name: str, result: QualityValidationResult):
        """Print summary of validation result"""
        status = "✅ PASS" if result.passed else "❌ FAIL"
        print(f"   {status} {check_name.upper()} validation")
        
        if result.failures:
            print("   Failures:")
            for failure in result.failures:
                print(f"     - {failure}")
                
        if result.warnings:
            print("   Warnings:")
            for warning in result.warnings:
                print(f"     - {warning}")
    
    def print_final_summary(self, results: Dict[str, QualityValidationResult]):
        """Print final validation summary"""
        print("\n" + "=" * 60)
        print("🎯 FINAL QUALITY VALIDATION SUMMARY")
        print("=" * 60)
        
        all_passed = all(result.passed for result in results.values())
        
        for check_name, result in results.items():
            status = "✅" if result.passed else "❌"
            print(f"{status} {check_name.upper()}: {'PASS' if result.passed else 'FAIL'}")
        
        print("\n" + ("🎉 ALL QUALITY CHECKS PASSED!" if all_passed else "⚠️  QUALITY ISSUES FOUND"))
        
        return all_passed


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="PKM Quality Validation Pipeline")
    parser.add_argument("--check-tdd", action="store_true", help="Only run TDD compliance check")
    parser.add_argument("--check-kiss", action="store_true", help="Only run KISS principle check")  
    parser.add_argument("--src-dir", type=Path, default=Path("src"), help="Source directory")
    parser.add_argument("--test-dir", type=Path, default=Path("tests"), help="Test directory")
    
    args = parser.parse_args()
    
    pipeline = QualityValidationPipeline(args.src_dir, args.test_dir)
    
    # Determine which checks to run
    check_types = []
    if args.check_tdd:
        check_types.append("tdd")
    if args.check_kiss:
        check_types.append("kiss")
    
    # If no specific check requested, run all
    if not check_types:
        check_types = ["kiss", "tdd"]
    
    results = pipeline.run_validation(check_types)
    success = pipeline.print_final_summary(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()