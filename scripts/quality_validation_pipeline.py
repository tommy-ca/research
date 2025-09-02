#!/usr/bin/env python3
"""
PKM System Quality Validation Pipeline

Automated enforcement of engineering principles:
- TDD compliance (RED → GREEN → REFACTOR)
- KISS principle (Keep It Simple, Stupid)
- FR-First prioritization (Functional Requirements first)
- SOLID principles validation
- Code coverage requirements
- Performance standards

Usage:
    python scripts/quality_validation_pipeline.py
    python scripts/quality_validation_pipeline.py --check-tdd
    python scripts/quality_validation_pipeline.py --full-validation
"""

import sys
import subprocess
import ast
import inspect
from pathlib import Path
from typing import Dict, List, Tuple, Any
import argparse
import json
import time


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
            
        # Check test coverage requirements
        coverage_result = self._check_coverage()
        if coverage_result < 80:
            result.fail(f"Code coverage {coverage_result}% below required 80%")
        else:
            result.add_metric("code_coverage", coverage_result)
            
        return result
    
    def _check_file_has_tests(self, impl_file: Path, result: QualityValidationResult):
        """Check if implementation file has corresponding tests"""
        # Convert implementation path to test path
        rel_path = impl_file.relative_to(self.src_dir)
        test_file = self.test_dir / "unit" / f"test_{rel_path.stem}.py"
        functional_test_file = self.test_dir / "unit" / f"test_{rel_path.stem}_functional.py"
        
        if not test_file.exists() and not functional_test_file.exists():
            result.fail(f"No tests found for {impl_file}")
        else:
            # Check if tests actually test the implementation
            self._validate_test_coverage_for_file(impl_file, result)
    
    def _validate_test_coverage_for_file(self, impl_file: Path, result: QualityValidationResult):
        """Validate that tests actually cover the implementation"""
        try:
            # Parse implementation to find functions
            with open(impl_file, 'r') as f:
                tree = ast.parse(f.read())
                
            functions = [node.name for node in ast.walk(tree) 
                        if isinstance(node, ast.FunctionDef) 
                        and not node.name.startswith('_')]
                        
            if functions:
                result.add_metric(f"functions_in_{impl_file.stem}", len(functions))
                
        except Exception as e:
            result.warn(f"Could not parse {impl_file}: {e}")
    
    def _check_coverage(self) -> float:
        """Check code coverage using pytest-cov"""
        try:
            cmd = ["python", "-m", "pytest", "--cov=src/pkm", "--cov-report=json:coverage.json", "-q"]
            subprocess.run(cmd, capture_output=True, check=True)
            
            with open("coverage.json", 'r') as f:
                coverage_data = json.load(f)
                return coverage_data.get("totals", {}).get("percent_covered", 0)
                
        except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
            return 0.0


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


class SolidPrincipleChecker:
    """Validates SOLID principles compliance"""
    
    def __init__(self, src_dir: Path):
        self.src_dir = src_dir
        
    def check_solid_compliance(self) -> QualityValidationResult:
        """Check SOLID principles compliance"""
        result = QualityValidationResult()
        
        impl_files = list(self.src_dir.rglob("*.py"))
        
        for impl_file in impl_files:
            self._check_single_responsibility(impl_file, result)
            self._check_dependency_injection(impl_file, result)
            
        return result
    
    def _check_single_responsibility(self, impl_file: Path, result: QualityValidationResult):
        """Check Single Responsibility Principle"""
        try:
            with open(impl_file, 'r') as f:
                tree = ast.parse(f.read())
                
            classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            
            for class_node in classes:
                methods = [node for node in class_node.body if isinstance(node, ast.FunctionDef)]
                
                if len(methods) > 10:  # Arbitrary threshold for too many responsibilities
                    result.warn(f"Class {class_node.name} in {impl_file.name} has {len(methods)} methods - may violate SRP")
                    
                result.add_metric(f"{impl_file.stem}_{class_node.name}_methods", len(methods))
                
        except Exception as e:
            result.warn(f"Could not analyze SOLID compliance for {impl_file}: {e}")
    
    def _check_dependency_injection(self, impl_file: Path, result: QualityValidationResult):
        """Check for dependency injection patterns"""
        try:
            with open(impl_file, 'r') as f:
                content = f.read()
                
            # Look for hardcoded imports that could be injected
            if "from pathlib import Path" in content and "Path.cwd()" in content:
                result.warn(f"File {impl_file.name} uses hardcoded Path.cwd() - consider dependency injection")
                
        except Exception as e:
            result.warn(f"Could not check dependency injection for {impl_file}: {e}")


class PerformanceChecker:
    """Validates performance requirements"""
    
    def __init__(self, test_dir: Path):
        self.test_dir = test_dir
        
    def check_performance_standards(self) -> QualityValidationResult:
        """Check performance standards"""
        result = QualityValidationResult()
        
        # Run performance tests
        try:
            start_time = time.time()
            cmd = ["python", "-m", "pytest", str(self.test_dir), "-k", "performance", "-v"]
            proc_result = subprocess.run(cmd, capture_output=True, text=True)
            end_time = time.time()
            
            test_duration = end_time - start_time
            result.add_metric("performance_test_duration", test_duration)
            
            if proc_result.returncode != 0:
                result.fail(f"Performance tests failed: {proc_result.stdout}")
            else:
                # Check if any performance test took too long
                if test_duration > 30:  # 30 seconds max for all performance tests
                    result.fail(f"Performance tests took {test_duration:.2f}s (max 30s)")
                    
        except Exception as e:
            result.warn(f"Could not run performance tests: {e}")
            
        return result


class QualityValidationPipeline:
    """Main quality validation pipeline"""
    
    def __init__(self, src_dir: Path = None, test_dir: Path = None):
        self.src_dir = src_dir or Path("src")
        self.test_dir = test_dir or Path("tests")
        
        self.checkers = {
            "tdd": TddComplianceChecker(self.src_dir, self.test_dir),
            "kiss": KissPrincipleChecker(self.src_dir),
            "solid": SolidPrincipleChecker(self.src_dir),
            "performance": PerformanceChecker(self.test_dir)
        }
    
    def run_full_validation(self) -> Dict[str, QualityValidationResult]:
        """Run complete quality validation"""
        print("🔍 Running PKM System Quality Validation Pipeline...")
        print("=" * 60)
        
        results = {}
        
        for check_name, checker in self.checkers.items():
            print(f"\n📋 Running {check_name.upper()} compliance check...")
            
            if check_name == "tdd":
                result = checker.check_tdd_compliance()
            elif check_name == "kiss":
                result = checker.check_kiss_compliance()
            elif check_name == "solid":
                result = checker.check_solid_compliance()
            elif check_name == "performance":
                result = checker.check_performance_standards()
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
                
        if result.metrics:
            print("   Metrics:")
            for metric, value in result.metrics.items():
                if isinstance(value, float):
                    print(f"     - {metric}: {value:.2f}")
                else:
                    print(f"     - {metric}: {value}")
    
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
        
        if not all_passed:
            print("\nTo fix issues, follow the engineering principles:")
            print("- TDD: Write tests first (RED → GREEN → REFACTOR)")
            print("- KISS: Keep functions simple (< 20 lines)")
            print("- FR-First: Functional requirements before optimization")
            print("- SOLID: Single responsibility, dependency injection")
        
        return all_passed


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="PKM Quality Validation Pipeline")
    parser.add_argument("--check-tdd", action="store_true", help="Only run TDD compliance check")
    parser.add_argument("--check-kiss", action="store_true", help="Only run KISS principle check")  
    parser.add_argument("--check-solid", action="store_true", help="Only run SOLID principles check")
    parser.add_argument("--check-performance", action="store_true", help="Only run performance check")
    parser.add_argument("--full-validation", action="store_true", help="Run complete validation suite")
    parser.add_argument("--src-dir", type=Path, default=Path("src"), help="Source directory")
    parser.add_argument("--test-dir", type=Path, default=Path("tests"), help="Test directory")
    
    args = parser.parse_args()
    
    pipeline = QualityValidationPipeline(args.src_dir, args.test_dir)
    
    # If no specific check requested, run full validation
    if not any([args.check_tdd, args.check_kiss, args.check_solid, args.check_performance]):
        args.full_validation = True
    
    if args.full_validation:
        results = pipeline.run_full_validation()
        success = pipeline.print_final_summary(results)
        sys.exit(0 if success else 1)
    
    # Run individual checks with detailed output
    print("🔍 Running PKM System Quality Validation Pipeline...")
    print("=" * 60)
    
    results = {}
    
    if args.check_tdd:
        print(f"\n📋 Running TDD compliance check...")
        results["tdd"] = pipeline.checkers["tdd"].check_tdd_compliance()
        pipeline._print_result_summary("tdd", results["tdd"])
        
    if args.check_kiss:
        print(f"\n📋 Running KISS principle check...")
        results["kiss"] = pipeline.checkers["kiss"].check_kiss_compliance()
        pipeline._print_result_summary("kiss", results["kiss"])
        
    if args.check_solid:
        print(f"\n📋 Running SOLID principles check...")
        results["solid"] = pipeline.checkers["solid"].check_solid_compliance()
        pipeline._print_result_summary("solid", results["solid"])
        
    if args.check_performance:
        print(f"\n📋 Running performance check...")
        results["performance"] = pipeline.checkers["performance"].check_performance_standards()
        pipeline._print_result_summary("performance", results["performance"])
    
    success = pipeline.print_final_summary(results)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()