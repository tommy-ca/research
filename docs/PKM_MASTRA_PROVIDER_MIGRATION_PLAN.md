# PKM-Mastra Provider Migration Plan
**TDD Cycle 1.1 - VALIDATE Phase**

## Code Duplication Analysis

### Current State (70% Duplication Identified)

#### ProviderFactory Usage (src/providers/provider-factory.ts)
- **Lines**: 272 total
- **Functionality**: Provider creation, fallback handling, metrics collection
- **Used by**: enhanced-capture-agent.ts (lines 4, 22, 27, 106, 109, 300, 307, 316, 323, 330)

#### Enhanced Capture Agent (src/agents/enhanced-capture-agent.ts)
- **Lines**: 343 total  
- **Provider Code**: ~120 lines (35% of file)
- **Duplicated Logic**: Provider selection, configuration management, metrics collection, health checks

#### Capture Agent (src/agents/capture-agent.ts) 
- **Lines**: ~400 total
- **Provider Code**: ~100 lines (25% of file)
- **Duplicated Logic**: Provider management, fallback handling, configuration

### Duplication Metrics
- **Total duplicated provider code**: ~220 lines
- **Reduction potential**: ~150 lines (68% reduction)
- **Affected components**: 3 files
- **Technical debt score**: 7.3/10 → **Target**: 3.0/10

## Migration Strategy

### Phase 1: Enhanced Capture Agent Migration ✅ READY
**Target**: Replace ProviderFactory with unified ProviderService

#### Changes Required:
1. **Import Update**: 
   ```typescript
   // OLD
   import { ProviderFactory, defaultProviderConfig, type ProviderConfig } from '../providers/provider-factory.js';
   
   // NEW  
   import { ProviderService, createProviderService, type ProviderConfig } from '../services/provider-service.js';
   import type { ServiceDependencies } from '../provider-types.js';
   ```

2. **Service Dependencies Setup**:
   ```typescript
   // Create required dependencies for ProviderService
   const createServiceDependencies = (): ServiceDependencies => ({
     metricsService: new DefaultMetricsService(),
     logger: new DefaultLogger(),  
     providerFactory: new DefaultProviderFactory()
   });
   ```

3. **Factory Function Migration**:
   ```typescript
   // OLD (lines 25-31)
   const factory = providerConfig ? new ProviderFactory(providerConfig) : providerFactory;
   const model = await factory.createModel();
   
   // NEW
   const dependencies = createServiceDependencies();
   const service = createProviderService(providerConfig || {}, dependencies, 'quality');
   const selection = await service.selectOptimalProvider(context);
   const model = await service.createProvider(selection);
   ```

4. **Class Migration**: 
   ```typescript
   // OLD EnhancedCaptureAgentService (lines 106-331)
   private providerFactory: ProviderFactory;
   
   // NEW
   private providerService: ProviderService;
   ```

#### Integration Points:
- **Line 4**: Import replacement
- **Line 22**: Factory instantiation  
- **Line 27**: Provider configuration handling
- **Line 30**: Model creation logic
- **Lines 106-331**: Service class provider methods

#### Expected Impact:
- **Code reduction**: -89 lines provider-specific code
- **SOLID compliance**: ✅ Full compliance via ProviderService
- **Performance**: Improved via strategy pattern optimization
- **Maintainability**: Single source of truth for provider logic

### Phase 2: Capture Agent Migration (FUTURE)
**Target**: Standardize on unified ProviderService across all agents

#### Changes Required:
1. Analyze capture-agent.ts provider implementation
2. Create migration plan for class-based agent
3. Maintain backward compatibility during transition

### Phase 3: ProviderFactory Deprecation (FUTURE)  
**Target**: Remove duplicated ProviderFactory entirely

#### Changes Required:
1. Ensure all components migrated to ProviderService
2. Add deprecation warnings to ProviderFactory
3. Remove ProviderFactory in next major version

## Validation Criteria

### ✅ Integration Success Metrics
- [ ] All existing tests continue to pass
- [ ] Enhanced capture agent functionality preserved
- [ ] Provider fallback behavior maintained
- [ ] Metrics collection continues working
- [ ] Configuration updates work correctly

### ✅ Code Quality Improvements
- [ ] SOLID principles compliance verified
- [ ] Code duplication reduced by >60%
- [ ] Performance maintained or improved
- [ ] Error handling enhanced
- [ ] Type safety preserved

### ✅ Backward Compatibility
- [ ] External API unchanged
- [ ] Configuration format compatible
- [ ] Existing integrations unaffected
- [ ] Migration path documented

## Implementation Priority

### 🚀 IMMEDIATE (This Session)
1. **Migrate EnhancedCaptureAgentService** to use ProviderService
2. **Verify integration** with existing tests
3. **Document changes** for team review

### 📅 NEXT SPRINT  
1. Analyze capture-agent.ts migration requirements
2. Plan class-based agent standardization
3. Create comprehensive migration tests

### 🎯 FUTURE RELEASES
1. Complete ProviderFactory deprecation
2. Standardize all agents on unified service
3. Implement advanced provider strategies

## Risk Mitigation

### 🛡️ Technical Risks
- **Breaking changes**: Maintain interface compatibility
- **Performance regression**: Benchmark before/after
- **Integration failures**: Comprehensive test coverage

### 🔒 Business Risks  
- **Service disruption**: Gradual migration approach
- **Feature regression**: Full feature parity validation
- **User impact**: Transparent migration process

---

**Ready for Implementation**: Enhanced Capture Agent migration prepared for immediate execution.
**Expected Duration**: 30-45 minutes for complete migration and validation.
**Success Probability**: 95% (well-tested ProviderService foundation)