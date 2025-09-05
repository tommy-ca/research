"""
FR-INT-001: End-to-End Workflow Integration Tests - RED PHASE

These tests define the expected behavior of complete PKM workflows.
Following TDD: Write failing tests → minimal implementation → refactor

Test Coverage:
- Complete PKM workflow integration (capture→process→daily→search→link)
- Cross-feature data consistency and flow
- Real vault operations with file system
- CLI command integration testing
- Error propagation across features
"""
import pytest
import tempfile
import subprocess
from pathlib import Path
from datetime import date
import sys
import os

# Import integration testing utilities (will be created in GREEN phase)
from tests.utils.integration_helpers import IntegrationTestRunner, VaultTestSetup


class TestCompleteE2EWorkflows:
    """Test complete end-to-end PKM workflows"""
    
    def test_complete_pkm_workflow_integration(self):
        """
        FR-INT-001: Complete PKM workflow integration test
        
        Validates the full PKM lifecycle:
        1. Capture content to inbox
        2. Process inbox items to PARA structure  
        3. Create daily note
        4. Search across organized content
        5. Generate links between related content
        
        This is the primary integration test validating all features work together.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Step 1: Capture content to inbox
            capture_result = runner.run_capture("Project planning meeting notes")
            assert capture_result.success, "Capture should succeed"
            assert vault.has_inbox_files(), "Content should be in inbox"
            
            # Step 2: Process inbox (should move to projects folder based on keywords)
            process_result = runner.run_process_inbox()
            assert process_result.success, "Processing should succeed"
            assert vault.has_project_files(), "Content should be in projects folder"
            assert not vault.has_inbox_files(), "Inbox should be empty after processing"
            
            # Step 3: Create daily note
            daily_result = runner.run_daily()
            assert daily_result.success, "Daily note creation should succeed"
            assert vault.has_daily_note_for_today(), "Daily note should exist"
            
            # Step 4: Search should find organized content
            search_result = runner.run_search("project planning")
            assert search_result.success, "Search should succeed"
            assert len(search_result.matches) > 0, "Search should find organized content"
            assert any('02-projects' in str(match.file_path) for match in search_result.matches), \
                "Search should find content in projects folder"
            
            # Step 5: Link generation should work with organized content
            project_file = vault.get_first_project_file()
            link_result = runner.run_link(project_file)
            assert link_result.success, "Link generation should succeed"
            # Should find daily note as potential link target
            daily_note_suggested = any('daily' in str(suggestion.target_file) 
                                     for suggestion in link_result.suggestions)
            assert daily_note_suggested, "Should suggest linking to daily note"
    
    def test_workflow_data_consistency(self):
        """
        FR-INT-001: Data consistency across workflow steps
        
        Ensures data created by one feature is properly accessible by others.
        Validates file system consistency and data integrity.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Create content with specific identifiable data
            test_content = "Machine learning project analysis with neural networks"
            
            # Capture and process
            runner.run_capture(test_content)
            runner.run_process_inbox()
            
            # Verify search can find the processed content
            search_result = runner.run_search("machine learning")
            assert search_result.success
            found_content = any(test_content.lower() in match.content.lower() 
                              for match in search_result.matches)
            assert found_content, "Search should find exact captured content after processing"
            
            # Verify link generation can work with processed content
            processed_file = vault.get_files_containing("machine learning")[0]
            link_result = runner.run_link(processed_file)
            assert link_result.success, "Link generation should work with processed files"
    
    def test_cli_command_integration(self):
        """
        FR-INT-001: CLI command integration testing
        
        Tests the complete workflow using actual CLI commands.
        Validates that the CLI interface works correctly for integrated workflows.
        """
        with VaultTestSetup() as vault:
            # Change to vault directory for CLI operations
            original_cwd = os.getcwd()
            try:
                os.chdir(vault.path.parent)  # CLI expects 'vault' subdirectory
                
                # Test complete CLI workflow  
                commands = [
                    ['python3', '-m', 'pkm.cli', 'capture', 'CLI integration test content'],
                    ['python3', '-m', 'pkm.cli', 'process-inbox'],
                    ['python3', '-m', 'pkm.cli', 'daily'],
                    ['python3', '-m', 'pkm.cli', 'search', 'integration'],
                ]
                
                for cmd in commands:
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(vault.path.parent))
                    assert result.returncode == 0, f"CLI command {' '.join(cmd)} should succeed. Error: {result.stderr}"
                
                # Verify the workflow completed successfully
                assert vault.has_processed_files(), "CLI workflow should result in processed files"
                assert vault.has_daily_note_for_today(), "CLI should create daily note"
                
            finally:
                os.chdir(original_cwd)
    
    def test_error_propagation_resilience(self):
        """
        FR-INT-001: Error propagation and system resilience
        
        Tests that errors in one part of the workflow don't break other parts.
        Validates graceful degradation and error isolation.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Create a scenario with a problematic file
            problematic_content = "Content with\x00null characters that might cause issues"
            runner.run_capture(problematic_content)
            
            # Processing should handle the problematic file gracefully
            process_result = runner.run_process_inbox()
            # Even if processing has issues, it should not crash completely
            assert isinstance(process_result.success, bool), "Processing should return valid result object"
            
            # Other operations should still work
            daily_result = runner.run_daily()
            assert daily_result.success, "Daily note creation should work despite processing issues"
            
            search_result = runner.run_search("test")
            assert search_result.success, "Search should work despite processing issues"
    
    def test_large_workflow_scalability(self):
        """
        FR-INT-001: Workflow scalability testing
        
        Tests workflow performance with larger amounts of content.
        Validates that integrated operations scale reasonably.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Create multiple pieces of content
            test_contents = [
                f"Project content item {i} with various keywords like planning, development, analysis"
                for i in range(10)
            ]
            
            # Capture multiple items
            for i, content in enumerate(test_contents):
                capture_result = runner.run_capture(content)
                assert capture_result.success, f"Should capture content: {content[:50]}..."
            
            # Debug: Check how many files are actually in inbox
            inbox_files = list((vault.path / '00-inbox').glob('*.md'))
            print(f"Debug: Found {len(inbox_files)} files in inbox: {[f.name for f in inbox_files]}")
            
            # Process all items
            process_result = runner.run_process_inbox()
            assert process_result.success, "Should process multiple items"
            assert process_result.processed_count == len(inbox_files), \
                f"Should process {len(inbox_files)} items (found in inbox), not {process_result.processed_count}"
            
            # Search should find all items
            search_result = runner.run_search("project")
            assert search_result.success, "Search should work with multiple items"
            assert len(search_result.matches) >= len(test_contents), \
                "Search should find all processed items"
    
    def test_feature_interaction_matrix(self):
        """
        FR-INT-001: Feature interaction matrix validation
        
        Tests all pairwise interactions between features to ensure compatibility.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Test: capture + search interaction
            runner.run_capture("Searchable content for testing")
            search_result = runner.run_search("searchable")
            assert search_result.success and len(search_result.matches) > 0, \
                "Search should find captured content"
            
            # Test: process + search interaction  
            runner.run_process_inbox()
            search_after_process = runner.run_search("searchable")
            assert search_after_process.success and len(search_after_process.matches) > 0, \
                "Search should find processed content"
            
            # Test: daily + link interaction
            daily_result = runner.run_daily()
            assert daily_result.success
            
            daily_note_path = vault.get_daily_note_for_today()
            link_result = runner.run_link(daily_note_path)
            assert link_result.success, "Link generation should work with daily notes"
            
            # Test: process + link interaction
            processed_files = vault.get_processed_files()
            if processed_files:
                link_result = runner.run_link(processed_files[0])
                assert link_result.success, "Link generation should work with processed files"


class TestWorkflowErrorScenarios:
    """Test error scenarios in integrated workflows"""
    
    def test_partial_workflow_failure_recovery(self):
        """
        FR-INT-001: Partial workflow failure recovery
        
        Tests recovery when individual steps in a workflow fail.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Successful capture
            capture_result = runner.run_capture("Test content for recovery")
            assert capture_result.success
            
            # Simulate processing failure by removing vault write permissions
            vault_path = vault.path
            original_permissions = vault_path.stat().st_mode
            try:
                vault_path.chmod(0o444)  # Read-only
                
                # Processing should fail gracefully
                process_result = runner.run_process_inbox()
                assert not process_result.success, "Processing should fail with read-only vault"
                assert "permission" in process_result.message.lower(), \
                    "Error message should indicate permission issue"
                
            finally:
                # Restore permissions
                vault_path.chmod(original_permissions)
            
            # After restoring permissions, workflow should continue
            process_result = runner.run_process_inbox()
            assert process_result.success, "Processing should succeed after permission restore"
    
    def test_corrupted_vault_recovery(self):
        """
        FR-INT-001: Corrupted vault structure recovery
        
        Tests behavior when vault structure is corrupted or missing.
        """
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Remove a critical directory
            inbox_dir = vault.path / '00-inbox'
            if inbox_dir.exists():
                inbox_dir.rmdir()
            
            # Operations should handle missing directories gracefully
            capture_result = runner.run_capture("Test with missing inbox")
            # Should either succeed (by creating directory) or fail gracefully
            assert isinstance(capture_result.success, bool), \
                "Capture should return valid result with missing inbox"
            
            process_result = runner.run_process_inbox()
            assert isinstance(process_result.success, bool), \
                "Process should return valid result with corrupted structure"


class TestPerformanceIntegration:
    """Test performance characteristics of integrated workflows"""
    
    def test_workflow_performance_baseline(self):
        """
        FR-INT-001: Workflow performance baseline measurement
        
        Establishes baseline performance metrics for integrated operations.
        """
        import time
        
        with VaultTestSetup() as vault:
            runner = IntegrationTestRunner(vault.path)
            
            # Measure complete workflow time
            start_time = time.time()
            
            # Execute workflow steps
            runner.run_capture("Performance test content")
            runner.run_process_inbox()
            runner.run_daily()
            runner.run_search("performance")
            
            end_time = time.time()
            total_time = end_time - start_time
            
            # Baseline expectation: complete workflow should finish in reasonable time
            assert total_time < 5.0, f"Complete workflow took {total_time}s, should be <5s"
            
            # Log performance for baseline establishment
            print(f"Workflow baseline performance: {total_time:.3f}s")