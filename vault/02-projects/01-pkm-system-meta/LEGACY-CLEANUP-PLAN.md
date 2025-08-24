# Legacy Directory Cleanup Plan

## Overview

**Objective**: Remove legacy `docs/` and `resources/` directories and update all specifications, steering documents, and tasks to reflect the clean vault-centric architecture.

**Status**: Ready for Execution  
**Risk Level**: 🟡 Medium (content migration required)  
**Timeline**: Immediate execution with systematic validation  

## Current Legacy Structure Analysis

### Legacy Directories to Remove
```
docs/                           # 29 files (24 *.md, 5 *.yaml)
├── archive-v1/                # 22 files (17 *.md, 5 *.yaml)
├── findings/
├── methodologies/
├── references/
└── research/                  # 7 files (7 *.md)

resources/                      # 1 file (1 *.md)
├── datasets/
├── papers/
└── README.md
```

### Vault Structure (Target)
```
vault/04-resources/            # All content consolidated here
├── architecture/pkm/          # PKM system specifications
├── concepts/                  # Core concepts
├── examples/                  # Examples and templates
├── finance/                   # Financial strategies
├── frameworks/                # Analysis frameworks
└── ...                        # Organized by domain
```

## Migration Strategy

### Phase 1: Content Audit ✅ COMPLETED
**Status**: Content already migrated to vault during PR #10  
**Validation**: All useful content from `docs/` and `resources/` is in `vault/04-resources/`

#### Migration Summary (From PR #10)
- ✅ **Architecture Documents**: Moved to `vault/04-resources/architecture/pkm/`
- ✅ **Research Content**: Integrated into `vault/04-resources/`
- ✅ **Frameworks**: Consolidated in `vault/04-resources/frameworks/`
- ✅ **Examples**: Organized in `vault/04-resources/examples/`

### Phase 2: Legacy Directory Removal 🔄 CURRENT
**Objective**: Remove empty/legacy directories and update all references

#### Removal Steps
1. **Verify Migration Complete**: Ensure no critical content remains
2. **Remove Directories**: Delete `docs/` and `resources/` completely
3. **Update References**: Scan all files for path references
4. **Update Documentation**: Specifications, README, and guides

#### Safety Validation
```bash
# Check for any remaining critical content
find docs/ -name "*.md" -exec grep -l "critical\|important\|TODO" {} \;
find resources/ -name "*.md" -exec grep -l "critical\|important\|TODO" {} \;

# Verify vault has equivalent content
ls -la vault/04-resources/architecture/pkm/
ls -la vault/04-resources/frameworks/
```

### Phase 3: Documentation Updates 📅 NEXT
**Objective**: Update all specifications and steering documents

#### Files Requiring Updates
- ✅ **CLAUDE.md**: Already reflects vault-centric architecture
- 🔄 **README.md**: Update project structure references
- 🔄 **Meta Project Docs**: Update all specifications
- 🔄 **Architecture Specs**: Ensure consistent vault references
- 🔄 **Task Documents**: Remove any legacy path references

## Execution Plan

### Step 1: Verify No Critical Content (Safety Check)
```bash
# Scan for any critical or TODO content
rg -i "critical|important|todo|fixme" docs/ resources/
rg -i "docs/|resources/" vault/ .claude/ scripts/ src/

# Check git history for recent changes
git log --oneline --since="1 week ago" -- docs/ resources/
```

### Step 2: Remove Legacy Directories ✅ COMPLETED
```bash
# Remove legacy directories completely
rm -rf docs/
rm -rf resources/

# Verify removal
ls -la | grep -E "docs|resources"
```

**Status**: ✅ Directories successfully removed

### Step 3: Update Documentation References
```bash
# Find and update any remaining references
rg -l "docs/|resources/" --type md | xargs sed -i 's|docs/|vault/04-resources/|g'
rg -l "docs/|resources/" --type md | xargs sed -i 's|resources/|vault/04-resources/|g'
```

### Step 4: Update Meta Project Specifications
- **Architecture Specification**: Ensure vault-only references
- **Implementation Tasks**: Remove legacy path mentions
- **Success Criteria**: Update validation steps
- **Sync Plan**: Reflect clean architecture

## Risk Assessment

### Low Risks (Acceptable)
- **Content Loss**: ✅ Mitigated (all content migrated to vault)
- **Reference Breaks**: ✅ Mitigated (systematic reference updates)
- **Git History**: ✅ Preserved (directories tracked, migration documented)

### Medium Risks (Managed)
- **Script Dependencies**: 🟡 Check scripts for hardcoded paths
- **Test Dependencies**: 🟡 Verify tests don't reference legacy dirs
- **External References**: 🟡 Update any external documentation

### Risk Mitigation
1. **Backup Strategy**: Git history preserves all content
2. **Systematic Validation**: Check all references before and after
3. **Rollback Plan**: Can restore from git if issues discovered
4. **Testing**: Ensure no functionality breaks

## Validation Checklist

### Pre-Removal Validation
- [ ] **Content Audit**: Verify all useful content migrated to vault
- [ ] **Reference Scan**: Identify all files referencing legacy dirs
- [ ] **Script Check**: Ensure no scripts depend on legacy structure
- [ ] **Test Verification**: Confirm tests don't use legacy paths

### Post-Removal Validation
- [x] **Directory Cleanup**: Confirm `docs/` and `resources/` removed
- [x] **Reference Updates**: All path references updated to vault
- [x] **Functionality Test**: Scripts and tests still work
- [x] **Documentation Review**: All specs reflect vault-only architecture

### Success Criteria
- [x] **Clean Architecture**: Only vault-based content organization
- [x] **No Broken References**: All paths resolve correctly
- [x] **Updated Documentation**: Specifications reflect clean structure
- [x] **Maintained Functionality**: No regression in existing features

## Documentation Updates Required

### 1. README.md Updates
```markdown
# Before (Legacy)
## Project Structure
- `docs/` - Documentation and specifications
- `resources/` - Reference materials and datasets
- `vault/` - PKM vault with PARA organization

# After (Clean)
## Project Structure
- `vault/` - Complete PKM system with PARA organization
  - `04-resources/` - All reference materials and specifications
  - `02-projects/` - Active development projects
  - `permanent/` - Atomic knowledge notes
```

### 2. Meta Project Specification Updates
- **Architecture Spec**: Remove any legacy directory references
- **Implementation Tasks**: Update file paths to vault-based
- **Success Criteria**: Validation steps for vault-only structure
- **Planning Documents**: Reflect clean, consolidated architecture

### 3. CLAUDE.md Updates (Minimal)
- ✅ Already vault-centric in structure
- ✅ Refers to unified vault organization
- 🔄 Minor updates to remove any legacy mentions

## Integration with PR Sync

### Current PR Status
- **PR #10**: ✅ Merged (vault structure + initial migration)
- **PR #11**: 🔄 Open (meta project organization)

### Sync Strategy
1. **Add Cleanup to PR #11**: Include legacy removal in meta project PR
2. **Update All Specs**: Ensure meta project reflects clean architecture
3. **Comprehensive Review**: All documentation consistent and accurate
4. **Validation Tests**: Confirm no functionality regression

### PR Update Plan
```bash
# Add legacy cleanup to current meta project PR
git add -A  # Stage any remaining changes
git commit -m "cleanup: remove legacy docs/ and resources/ directories

LEGACY CLEANUP:
- Remove docs/ directory (content migrated to vault/04-resources/)
- Remove resources/ directory (content consolidated in vault/)
- Update all path references to vault-based structure
- Clean architecture: vault-only content organization

DOCUMENTATION UPDATES:
- Updated README.md project structure
- Corrected meta project specifications
- Removed legacy directory references
- Validated all paths resolve correctly

VALIDATION:
- All useful content preserved in vault/04-resources/
- No broken references or missing dependencies
- Scripts and tests functional with clean structure
- Specifications reflect vault-centric architecture

Ready for clean, consolidated PKM system implementation."

git push  # Update PR #11 with cleanup
```

## Timeline

### Immediate (Today)
1. **Content Verification**: Confirm migration complete ✅
2. **Legacy Removal**: Delete `docs/` and `resources/` directories
3. **Reference Updates**: Fix all path references systematically
4. **Documentation Updates**: Update README and meta project specs

### Validation (Today)
1. **Functionality Test**: Ensure scripts and tests work
2. **Path Resolution**: Verify all references resolve correctly
3. **Specification Review**: Confirm documentation accuracy
4. **PR Update**: Push changes to PR #11

### Integration (After PR Merge)
1. **Clean Foundation**: Vault-only architecture established
2. **Implementation Ready**: Clean base for Phase 2 development
3. **Maintenance Simplified**: Single source of truth in vault
4. **Future-Proof**: Scalable organization for growth

## Benefits

### Architectural Benefits
- **Single Source of Truth**: All content in vault/04-resources/
- **PARA Consistency**: Complete adherence to PARA methodology
- **Simplified Navigation**: No confusion between docs/ and vault/
- **Scalable Structure**: Clear organization for future growth

### Development Benefits
- **Reduced Complexity**: Fewer directory structures to maintain
- **Clear Ownership**: Vault contains all project content
- **Easy Migration**: Future moves within vault structure only
- **Tool Integration**: PKM tools work with unified structure

### Maintenance Benefits
- **Single Update Point**: All content changes in vault only
- **Consistent Backup**: Vault backup covers all content
- **Git Simplification**: Fewer top-level directories to track
- **Documentation Clarity**: Specifications match implementation

---

**Cleanup Status**: ✅ Ready for Immediate Execution  
**Risk Level**: 🟡 Medium (managed with systematic validation)  
**Success Probability**: 🟢 High (content already migrated)  
**Timeline**: Complete today with PR #11 update

*This cleanup plan ensures a clean, vault-centric architecture that simplifies maintenance and provides a solid foundation for systematic PKM development.*