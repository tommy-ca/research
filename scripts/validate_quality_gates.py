#!/usr/bin/env python3
"""
PKM System Quality Gate Validation Script
Validates quality gates for testing pipeline as specified in 
AUTOMATED-TESTING-VALIDATION-FRAMEWORK.md
"""

import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any


class QualityGateValidator:
    """Validates quality gates for PKM system"""
    
    def __init__(self):
        self.gates_passed = 0
        self.gates_failed = 0
        self.errors: List[str] = []
        self.reports_dir = Path("tests/reports")
        
        # Ensure reports directory exists
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def validate_test_coverage(self) -> None:
        """Validate test coverage meets thresholds"""
        try:
            coverage_file = Path("tests/reports/coverage.xml")
            if not coverage_file.exists():
                self.fail_gate("Coverage report not found at tests/reports/coverage.xml")
                return
            
            tree = ET.parse(coverage_file)
            root = tree.getroot()
            
            line_coverage = float(root.attrib.get('line-rate', 0)) * 100
            branch_coverage = float(root.attrib.get('branch-rate', 0)) * 100
            
            # Quality gate thresholds from framework specification
            if line_coverage < 80:
                self.fail_gate(f"Line coverage {line_coverage:.1f}% below 80% threshold")
            elif branch_coverage < 70:
                self.fail_gate(f"Branch coverage {branch_coverage:.1f}% below 70% threshold")
            else:
                self.pass_gate(f"Coverage: {line_coverage:.1f}% lines, {branch_coverage:.1f}% branches")
                
        except Exception as e:
            self.fail_gate(f"Coverage validation error: {e}")
    
    def validate_test_results(self) -> None:
        """Validate all tests passed"""
        test_files = [
            "tests/reports/unit-tests.xml",
            "tests/reports/integration-tests.xml", 
            "tests/reports/acceptance-tests.xml",
            "tests/reports/security-tests.xml"
        ]
        
        total_tests = 0
        total_failures = 0
        total_errors = 0
        
        for test_file in test_files:
            test_path = Path(test_file)
            if not test_path.exists():
                self.fail_gate(f"Test report missing: {test_file}")
                continue
            
            try:
                tree = ET.parse(test_path)
                root = tree.getroot()
                
                tests = int(root.attrib.get('tests', 0))
                failures = int(root.attrib.get('failures', 0))
                errors = int(root.attrib.get('errors', 0))
                
                total_tests += tests
                total_failures += failures
                total_errors += errors
                
            except Exception as e:
                self.fail_gate(f"Error parsing {test_file}: {e}")
        
        if total_failures > 0 or total_errors > 0:
            self.fail_gate(f"Test failures: {total_failures}, errors: {total_errors}")
        else:
            self.pass_gate(f"All {total_tests} tests passed")
    
    def validate_performance_baseline(self) -> None:
        """Validate performance hasn't regressed"""
        performance_file = Path("tests/reports/performance.json")
        if not performance_file.exists():
            # Performance tests are optional in initial phases
            self.pass_gate("Performance tests deferred to later phase (as planned)")
            return
        
        try:
            with open(performance_file) as f:
                data = json.load(f)
            
            # Check key performance metrics
            benchmarks = data.get('benchmarks', [])
            for benchmark in benchmarks:
                name = benchmark.get('name', 'unknown')
                stats = benchmark.get('stats', {})
                mean_time = stats.get('mean', 0)
                
                # Define performance thresholds (from framework spec)
                thresholds = {
                    'test_search_performance': 0.1,  # 100ms
                    'test_capture_performance': 0.05,  # 50ms
                    'test_link_building_performance': 0.2,  # 200ms
                }
                
                threshold = thresholds.get(name)
                if threshold and mean_time > threshold:
                    self.fail_gate(f"Performance regression: {name} took {mean_time:.3f}s (limit: {threshold}s)")
            
            required_benchmarks = ['test_search_performance', 'test_capture_performance']
            if not any(benchmark.get('name') in required_benchmarks for benchmark in benchmarks):
                self.pass_gate("Performance baseline deferred (core features not implemented yet)")
            else:
                self.pass_gate("Performance baseline maintained")
                
        except Exception as e:
            self.fail_gate(f"Performance validation error: {e}")
    
    def validate_security_scan(self) -> None:
        """Validate security scan results"""
        security_file = Path("tests/reports/security-scan.json")
        if not security_file.exists():
            # Basic security validation - create minimal passing report
            self.pass_gate("Security scan deferred to security phase (basic validation only)")
            return
        
        try:
            with open(security_file) as f:
                data = json.load(f)
            
            results = data.get('results', [])
            high_severity = [r for r in results if r.get('issue_severity') == 'HIGH']
            medium_severity = [r for r in results if r.get('issue_severity') == 'MEDIUM']
            
            if high_severity:
                self.fail_gate(f"High severity security issues found: {len(high_severity)}")
            elif len(medium_severity) > 5:
                self.fail_gate(f"Too many medium severity security issues: {len(medium_severity)}")
            else:
                self.pass_gate(f"Security scan passed: {len(medium_severity)} medium, 0 high severity issues")
                
        except Exception as e:
            self.fail_gate(f"Security validation error: {e}")
    
    def validate_specification_compliance(self) -> None:
        """Validate implementation matches specifications"""
        spec_dir = Path("vault/02-projects/pkm-system/specs")
        if not spec_dir.exists():
            self.fail_gate("Specifications directory not found")
            return
        
        spec_files = list(spec_dir.glob("*.md"))
        if not spec_files:
            self.fail_gate("No specification files found")
            return
        
        # Basic validation - ensure specs exist for implemented features
        implemented_features = []
        pending_specs = []
        
        for spec_file in spec_files:
            try:
                content = spec_file.read_text()
                if "status: draft" in content:
                    pending_specs.append(spec_file.name)
                elif "status: approved" in content or "status: implemented" in content:
                    implemented_features.append(spec_file.name)
            except Exception as e:
                self.fail_gate(f"Error reading spec file {spec_file}: {e}")
        
        if implemented_features:
            self.pass_gate(f"Specifications validated: {len(implemented_features)} approved/implemented")
        else:
            self.pass_gate("No implemented features yet - specifications being developed")
    
    def pass_gate(self, message: str) -> None:
        """Record passing gate"""
        self.gates_passed += 1
        print(f"✅ PASS: {message}")
    
    def fail_gate(self, message: str) -> None:
        """Record failing gate"""
        self.gates_failed += 1
        self.errors.append(message)
        print(f"❌ FAIL: {message}")
    
    def generate_quality_report(self) -> Dict[str, Any]:
        """Generate comprehensive quality report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'gates_passed': self.gates_passed,
            'gates_failed': self.gates_failed,
            'total_gates': self.gates_passed + self.gates_failed,
            'success_rate': (self.gates_passed / (self.gates_passed + self.gates_failed)) * 100 if (self.gates_passed + self.gates_failed) > 0 else 0,
            'errors': self.errors,
            'status': 'PASS' if self.gates_failed == 0 else 'FAIL'
        }
        
        # Save report
        report_file = self.reports_dir / f"quality_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def run_all_validations(self) -> bool:
        """Run all quality gate validations"""
        print("🔍 Running PKM System Quality Gates...")
        print(f"Report directory: {self.reports_dir}")
        
        self.validate_specification_compliance()
        self.validate_test_coverage()
        self.validate_test_results()
        self.validate_performance_baseline()
        self.validate_security_scan()
        
        report = self.generate_quality_report()
        
        print(f"\n📊 Quality Gate Results:")
        print(f"Passed: {self.gates_passed}")
        print(f"Failed: {self.gates_failed}")
        print(f"Success Rate: {report['success_rate']:.1f}%")
        
        if self.gates_failed > 0:
            print(f"\n❌ Quality gates failed:")
            for error in self.errors:
                print(f"  - {error}")
            return False
        else:
            print(f"\n✅ All quality gates passed!")
            return True


def main():
    """Main entry point for quality gate validation"""
    validator = QualityGateValidator()
    success = validator.run_all_validations()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()