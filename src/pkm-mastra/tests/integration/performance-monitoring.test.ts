import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { SimilarityCalculatorInterface } from '@/types/quality-assessment';

/**
 * Performance Monitoring Test Framework
 * TDD Cycle 1.4 - Real-time performance tracking and metrics collection
 */

interface PerformanceMetric {
  name: string;
  value: number;
  unit: 'ms' | 'bytes' | 'count' | 'percent' | 'ops/sec';
  timestamp: string;
  category: 'latency' | 'throughput' | 'memory' | 'cpu' | 'error';
  labels?: Record<string, string>;
}

interface PerformanceAlert {
  id: string;
  severity: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  metric: string;
  threshold: number;
  actualValue: number;
  timestamp: string;
  resolved: boolean;
}

interface PerformanceProfile {
  operationName: string;
  startTime: number;
  endTime?: number;
  duration?: number;
  memoryStart: number;
  memoryPeak: number;
  memoryEnd?: number;
  subOperations: Map<string, PerformanceProfile>;
  metadata?: Record<string, any>;
}

interface PerformanceThresholds {
  qualityAssessment: { maxLatency: number; errorRate: number };
  duplicateDetection: { maxLatency: number; errorRate: number };
  workflowOrchestration: { maxLatency: number; errorRate: number };
  metadataGeneration: { maxLatency: number; errorRate: number };
  endToEnd: { maxLatency: number; errorRate: number };
}

class PerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private alerts: PerformanceAlert[] = [];
  private activeProfiles: Map<string, PerformanceProfile> = new Map();
  private thresholds: PerformanceThresholds;
  private isMonitoring: boolean = false;

  constructor(thresholds?: Partial<PerformanceThresholds>) {
    this.thresholds = {
      qualityAssessment: { maxLatency: 50, errorRate: 0.01 },
      duplicateDetection: { maxLatency: 50, errorRate: 0.01 },
      workflowOrchestration: { maxLatency: 20, errorRate: 0.005 },
      metadataGeneration: { maxLatency: 30, errorRate: 0.005 },
      endToEnd: { maxLatency: 100, errorRate: 0.02 },
      ...thresholds
    };
  }

  startMonitoring(): void {
    this.isMonitoring = true;
    this.metrics = [];
    this.alerts = [];
    this.activeProfiles.clear();
  }

  stopMonitoring(): void {
    this.isMonitoring = false;
  }

  startOperation(operationName: string, metadata?: Record<string, any>): string {
    const profileId = `${operationName}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
    const profile: PerformanceProfile = {
      operationName,
      startTime: performance.now(),
      memoryStart: this.getCurrentMemoryUsage(),
      memoryPeak: this.getCurrentMemoryUsage(),
      subOperations: new Map(),
      metadata
    };
    
    this.activeProfiles.set(profileId, profile);
    return profileId;
  }

  endOperation(profileId: string): PerformanceProfile | null {
    const profile = this.activeProfiles.get(profileId);
    if (!profile) return null;

    profile.endTime = performance.now();
    profile.duration = profile.endTime - profile.startTime;
    profile.memoryEnd = this.getCurrentMemoryUsage();
    
    this.activeProfiles.delete(profileId);

    // Record metrics
    this.recordMetric({
      name: `${profile.operationName}.latency`,
      value: profile.duration,
      unit: 'ms',
      timestamp: new Date().toISOString(),
      category: 'latency',
      labels: { operation: profile.operationName }
    });

    this.recordMetric({
      name: `${profile.operationName}.memory_peak`,
      value: profile.memoryPeak - profile.memoryStart,
      unit: 'bytes',
      timestamp: new Date().toISOString(),
      category: 'memory',
      labels: { operation: profile.operationName }
    });

    // Check thresholds and generate alerts
    this.checkThresholds(profile);

    return profile;
  }

  recordMetric(metric: PerformanceMetric): void {
    if (!this.isMonitoring) return;
    this.metrics.push(metric);
  }

  recordError(operationName: string, error: Error): void {
    this.recordMetric({
      name: `${operationName}.errors`,
      value: 1,
      unit: 'count',
      timestamp: new Date().toISOString(),
      category: 'error',
      labels: { 
        operation: operationName,
        errorType: error.name,
        errorMessage: error.message
      }
    });
  }

  getMetrics(): PerformanceMetric[] {
    return [...this.metrics];
  }

  getAlerts(): PerformanceAlert[] {
    return [...this.alerts];
  }

  getActiveAlerts(): PerformanceAlert[] {
    return this.alerts.filter(alert => !alert.resolved);
  }

  resolveAlert(alertId: string): boolean {
    const alert = this.alerts.find(a => a.id === alertId);
    if (alert) {
      alert.resolved = true;
      return true;
    }
    return false;
  }

  getPerformanceReport(): {
    summary: {
      totalOperations: number;
      averageLatency: number;
      errorRate: number;
      memoryUsage: number;
      activeAlerts: number;
    };
    operationBreakdown: Record<string, {
      count: number;
      avgLatency: number;
      minLatency: number;
      maxLatency: number;
      errorCount: number;
    }>;
    alerts: PerformanceAlert[];
  } {
    const latencyMetrics = this.metrics.filter(m => m.category === 'latency');
    const errorMetrics = this.metrics.filter(m => m.category === 'error');
    
    const operationBreakdown: Record<string, any> = {};
    
    // Group by operation
    latencyMetrics.forEach(metric => {
      const operation = metric.labels?.operation || 'unknown';
      if (!operationBreakdown[operation]) {
        operationBreakdown[operation] = {
          latencies: [],
          errorCount: 0
        };
      }
      operationBreakdown[operation].latencies.push(metric.value);
    });

    errorMetrics.forEach(metric => {
      const operation = metric.labels?.operation || 'unknown';
      if (!operationBreakdown[operation]) {
        operationBreakdown[operation] = {
          latencies: [],
          errorCount: 0
        };
      }
      operationBreakdown[operation].errorCount += metric.value;
    });

    // Calculate statistics
    Object.keys(operationBreakdown).forEach(operation => {
      const data = operationBreakdown[operation];
      const latencies = data.latencies;
      
      operationBreakdown[operation] = {
        count: latencies.length,
        avgLatency: latencies.length > 0 ? latencies.reduce((a, b) => a + b, 0) / latencies.length : 0,
        minLatency: latencies.length > 0 ? Math.min(...latencies) : 0,
        maxLatency: latencies.length > 0 ? Math.max(...latencies) : 0,
        errorCount: data.errorCount
      };
    });

    const totalOperations = latencyMetrics.length;
    const totalErrors = errorMetrics.reduce((sum, m) => sum + m.value, 0);

    return {
      summary: {
        totalOperations,
        averageLatency: totalOperations > 0 ? latencyMetrics.reduce((sum, m) => sum + m.value, 0) / totalOperations : 0,
        errorRate: totalOperations > 0 ? totalErrors / totalOperations : 0,
        memoryUsage: this.getCurrentMemoryUsage(),
        activeAlerts: this.getActiveAlerts().length
      },
      operationBreakdown,
      alerts: this.getActiveAlerts()
    };
  }

  private checkThresholds(profile: PerformanceProfile): void {
    const operationName = profile.operationName;
    const duration = profile.duration || 0;

    let threshold: { maxLatency: number; errorRate: number } | undefined;

    // Map operation names to thresholds
    if (operationName.includes('quality') || operationName.includes('assess')) {
      threshold = this.thresholds.qualityAssessment;
    } else if (operationName.includes('duplicate') || operationName.includes('similarity')) {
      threshold = this.thresholds.duplicateDetection;
    } else if (operationName.includes('workflow') || operationName.includes('orchestrat')) {
      threshold = this.thresholds.workflowOrchestration;
    } else if (operationName.includes('metadata')) {
      threshold = this.thresholds.metadataGeneration;
    } else if (operationName.includes('end-to-end') || operationName.includes('capture')) {
      threshold = this.thresholds.endToEnd;
    }

    if (threshold && duration > threshold.maxLatency) {
      this.generateAlert({
        severity: duration > threshold.maxLatency * 2 ? 'error' : 'warning',
        message: `Operation ${operationName} exceeded latency threshold`,
        metric: `${operationName}.latency`,
        threshold: threshold.maxLatency,
        actualValue: duration
      });
    }
  }

  private generateAlert(alertData: {
    severity: 'info' | 'warning' | 'error' | 'critical';
    message: string;
    metric: string;
    threshold: number;
    actualValue: number;
  }): void {
    const alert: PerformanceAlert = {
      id: `alert-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      resolved: false,
      ...alertData
    };
    
    this.alerts.push(alert);
  }

  private getCurrentMemoryUsage(): number {
    // In a real implementation, this would use actual memory monitoring
    return Math.floor(Math.random() * 1000000); // Mock memory usage
  }

  updateThresholds(newThresholds: Partial<PerformanceThresholds>): void {
    this.thresholds = { ...this.thresholds, ...newThresholds };
  }

  clearMetrics(): void {
    this.metrics = [];
  }

  clearAlerts(): void {
    this.alerts = [];
  }
}

// Instrumented workflow class for performance testing
class InstrumentedCaptureWorkflow {
  private monitor: PerformanceMonitor;

  constructor(monitor: PerformanceMonitor) {
    this.monitor = monitor;
  }

  async processCapture(content: string, metadata: any = {}): Promise<{
    result: any;
    performanceProfile: PerformanceProfile | null;
  }> {
    const profileId = this.monitor.startOperation('end-to-end-capture', {
      contentLength: content.length,
      hasMetadata: Object.keys(metadata).length > 0
    });

    try {
      // Simulate quality assessment
      const qualityProfileId = this.monitor.startOperation('quality-assessment');
      await this.simulateDelay(10, 20); // 10-20ms
      const qualityProfile = this.monitor.endOperation(qualityProfileId);

      // Simulate duplicate detection
      const duplicateProfileId = this.monitor.startOperation('duplicate-detection');
      await this.simulateDelay(5, 15); // 5-15ms
      const duplicateProfile = this.monitor.endOperation(duplicateProfileId);

      // Simulate workflow orchestration
      const workflowProfileId = this.monitor.startOperation('workflow-orchestration');
      await this.simulateDelay(2, 8); // 2-8ms
      const workflowProfile = this.monitor.endOperation(workflowProfileId);

      // Simulate metadata generation
      const metadataProfileId = this.monitor.startOperation('metadata-generation');
      await this.simulateDelay(5, 12); // 5-12ms
      const metadataGenProfile = this.monitor.endOperation(metadataProfileId);

      const result = {
        quality: qualityProfile?.duration,
        duplicate: duplicateProfile?.duration,
        workflow: workflowProfile?.duration,
        metadata: metadataGenProfile?.duration
      };

      const endToEndProfile = this.monitor.endOperation(profileId);
      
      return { result, performanceProfile: endToEndProfile };

    } catch (error) {
      this.monitor.recordError('end-to-end-capture', error as Error);
      this.monitor.endOperation(profileId);
      throw error;
    }
  }

  private async simulateDelay(min: number, max: number): Promise<void> {
    const delay = Math.random() * (max - min) + min;
    return new Promise(resolve => setTimeout(resolve, delay));
  }
}

describe('TDD Cycle 1.4 - Performance Monitoring Framework', () => {
  let performanceMonitor: PerformanceMonitor;
  let instrumentedWorkflow: InstrumentedCaptureWorkflow;

  beforeEach(() => {
    performanceMonitor = new PerformanceMonitor();
    instrumentedWorkflow = new InstrumentedCaptureWorkflow(performanceMonitor);
    performanceMonitor.startMonitoring();
  });

  afterEach(() => {
    performanceMonitor.stopMonitoring();
  });

  describe('Performance Metrics Collection', () => {
    it('should collect latency metrics for all operations', async () => {
      const content = 'Performance monitoring test content';
      
      const { performanceProfile } = await instrumentedWorkflow.processCapture(content);
      
      const metrics = performanceMonitor.getMetrics();
      const latencyMetrics = metrics.filter(m => m.category === 'latency');

      expect(latencyMetrics.length).toBeGreaterThanOrEqual(5); // end-to-end + 4 sub-operations
      expect(latencyMetrics.some(m => m.name.includes('quality-assessment'))).toBe(true);
      expect(latencyMetrics.some(m => m.name.includes('duplicate-detection'))).toBe(true);
      expect(latencyMetrics.some(m => m.name.includes('workflow-orchestration'))).toBe(true);
      expect(latencyMetrics.some(m => m.name.includes('metadata-generation'))).toBe(true);
      expect(latencyMetrics.some(m => m.name.includes('end-to-end-capture'))).toBe(true);

      console.log(`✅ Collected ${latencyMetrics.length} latency metrics`);
    });

    it('should collect memory usage metrics', async () => {
      const content = 'Memory monitoring test content';
      
      await instrumentedWorkflow.processCapture(content);
      
      const metrics = performanceMonitor.getMetrics();
      const memoryMetrics = metrics.filter(m => m.category === 'memory');

      expect(memoryMetrics.length).toBeGreaterThan(0);
      memoryMetrics.forEach(metric => {
        expect(metric.unit).toBe('bytes');
        expect(metric.value).toBeGreaterThanOrEqual(0);
      });

      console.log(`✅ Collected ${memoryMetrics.length} memory metrics`);
    });

    it('should track operation metadata', async () => {
      const content = 'A'.repeat(5000); // Large content
      const metadata = { source: 'test', type: 'large-content' };
      
      const { performanceProfile } = await instrumentedWorkflow.processCapture(content, metadata);
      
      expect(performanceProfile?.metadata).toBeDefined();
      expect(performanceProfile?.metadata?.contentLength).toBe(5000);
      expect(performanceProfile?.metadata?.hasMetadata).toBe(true);

      console.log(`✅ Operation metadata captured: ${JSON.stringify(performanceProfile?.metadata)}`);
    });
  });

  describe('Performance Threshold Monitoring', () => {
    it('should generate alerts when operations exceed thresholds', async () => {
      // Set very strict thresholds to trigger alerts
      performanceMonitor.updateThresholds({
        qualityAssessment: { maxLatency: 1, errorRate: 0.01 }, // 1ms - very strict
        duplicateDetection: { maxLatency: 1, errorRate: 0.01 },
        endToEnd: { maxLatency: 10, errorRate: 0.01 }
      });

      const content = 'Threshold monitoring test';
      
      await instrumentedWorkflow.processCapture(content);
      
      const alerts = performanceMonitor.getActiveAlerts();
      
      expect(alerts.length).toBeGreaterThan(0);
      alerts.forEach(alert => {
        expect(alert.severity).toMatch(/warning|error|critical/);
        expect(alert.actualValue).toBeGreaterThan(alert.threshold);
        expect(alert.resolved).toBe(false);
      });

      console.log(`✅ Generated ${alerts.length} performance alerts`);
    });

    it('should categorize alerts by severity', async () => {
      // Set different threshold levels
      performanceMonitor.updateThresholds({
        qualityAssessment: { maxLatency: 5, errorRate: 0.01 },
        endToEnd: { maxLatency: 20, errorRate: 0.01 }
      });

      // Process multiple operations to get various alert levels
      for (let i = 0; i < 5; i++) {
        await instrumentedWorkflow.processCapture(`Test content ${i}`);
      }
      
      const alerts = performanceMonitor.getActiveAlerts();
      const severityLevels = [...new Set(alerts.map(a => a.severity))];

      expect(severityLevels.length).toBeGreaterThan(0);
      severityLevels.forEach(severity => {
        expect(['info', 'warning', 'error', 'critical']).toContain(severity);
      });

      console.log(`✅ Alert severities: ${severityLevels.join(', ')}`);
    });

    it('should allow alert resolution', () => {
      // Manually create an alert for testing
      const testAlert: PerformanceAlert = {
        id: 'test-alert-123',
        severity: 'warning',
        message: 'Test alert',
        metric: 'test.latency',
        threshold: 50,
        actualValue: 75,
        timestamp: new Date().toISOString(),
        resolved: false
      };

      performanceMonitor['alerts'].push(testAlert);

      expect(performanceMonitor.getActiveAlerts()).toHaveLength(1);
      
      const resolved = performanceMonitor.resolveAlert('test-alert-123');
      expect(resolved).toBe(true);
      expect(performanceMonitor.getActiveAlerts()).toHaveLength(0);

      console.log(`✅ Alert resolution working correctly`);
    });
  });

  describe('Performance Reporting', () => {
    it('should generate comprehensive performance reports', async () => {
      // Process multiple operations for meaningful statistics
      const testCases = [
        'Short content',
        'Medium length content with more details',
        'A'.repeat(1000) + ' - Very long content for performance testing'
      ];

      for (const content of testCases) {
        await instrumentedWorkflow.processCapture(content);
      }

      const report = performanceMonitor.getPerformanceReport();

      // Validate report structure
      expect(report.summary).toBeDefined();
      expect(report.operationBreakdown).toBeDefined();
      expect(report.alerts).toBeDefined();

      // Validate summary metrics
      expect(report.summary.totalOperations).toBeGreaterThan(0);
      expect(report.summary.averageLatency).toBeGreaterThan(0);
      expect(report.summary.errorRate).toBeGreaterThanOrEqual(0);

      // Validate operation breakdown
      expect(Object.keys(report.operationBreakdown).length).toBeGreaterThan(0);
      Object.values(report.operationBreakdown).forEach(opData => {
        expect(opData.count).toBeGreaterThan(0);
        expect(opData.avgLatency).toBeGreaterThanOrEqual(0);
        expect(opData.minLatency).toBeGreaterThanOrEqual(0);
        expect(opData.maxLatency).toBeGreaterThanOrEqual(opData.minLatency);
      });

      console.log(`✅ Performance report: ${report.summary.totalOperations} ops, ${report.summary.averageLatency.toFixed(2)}ms avg`);
      console.log(`✅ Operation breakdown: ${Object.keys(report.operationBreakdown).join(', ')}`);
    });

    it('should calculate accurate performance statistics', async () => {
      // Process operations with known characteristics
      const iterations = 10;
      for (let i = 0; i < iterations; i++) {
        await instrumentedWorkflow.processCapture(`Test iteration ${i}`);
      }

      const report = performanceMonitor.getPerformanceReport();

      // Each iteration should have 5 operations (4 sub + 1 end-to-end)
      expect(report.summary.totalOperations).toBe(iterations * 5);

      // Validate statistics for each operation type
      Object.entries(report.operationBreakdown).forEach(([operation, stats]) => {
        expect(stats.count).toBe(iterations);
        expect(stats.avgLatency).toBeGreaterThan(0);
        expect(stats.maxLatency).toBeGreaterThanOrEqual(stats.avgLatency);
        expect(stats.minLatency).toBeLessThanOrEqual(stats.avgLatency);
        
        console.log(`✅ ${operation}: ${stats.count} ops, ${stats.avgLatency.toFixed(2)}ms avg, ${stats.minLatency.toFixed(2)}-${stats.maxLatency.toFixed(2)}ms range`);
      });
    });
  });

  describe('Performance Monitoring Configuration', () => {
    it('should allow dynamic threshold updates', () => {
      const originalThresholds = performanceMonitor['thresholds'];
      
      const newThresholds = {
        qualityAssessment: { maxLatency: 25, errorRate: 0.005 },
        endToEnd: { maxLatency: 75, errorRate: 0.01 }
      };

      performanceMonitor.updateThresholds(newThresholds);
      
      const updatedThresholds = performanceMonitor['thresholds'];
      
      expect(updatedThresholds.qualityAssessment.maxLatency).toBe(25);
      expect(updatedThresholds.qualityAssessment.errorRate).toBe(0.005);
      expect(updatedThresholds.endToEnd.maxLatency).toBe(75);
      
      // Should preserve unchanged thresholds
      expect(updatedThresholds.duplicateDetection).toEqual(originalThresholds.duplicateDetection);

      console.log(`✅ Dynamic threshold update successful`);
    });

    it('should support monitoring start/stop controls', async () => {
      expect(performanceMonitor['isMonitoring']).toBe(true);
      
      // Process operation while monitoring
      await instrumentedWorkflow.processCapture('Monitoring control test');
      const metricsWithMonitoring = performanceMonitor.getMetrics().length;
      expect(metricsWithMonitoring).toBeGreaterThan(0);

      // Stop monitoring and clear
      performanceMonitor.stopMonitoring();
      performanceMonitor.clearMetrics();
      
      // Process operation without monitoring
      await instrumentedWorkflow.processCapture('No monitoring test');
      const metricsWithoutMonitoring = performanceMonitor.getMetrics().length;
      expect(metricsWithoutMonitoring).toBe(0);

      // Restart monitoring
      performanceMonitor.startMonitoring();
      await instrumentedWorkflow.processCapture('Restart monitoring test');
      const metricsAfterRestart = performanceMonitor.getMetrics().length;
      expect(metricsAfterRestart).toBeGreaterThan(0);

      console.log(`✅ Monitoring controls: ${metricsWithMonitoring}→${metricsWithoutMonitoring}→${metricsAfterRestart} metrics`);
    });
  });

  describe('Error Tracking Integration', () => {
    it('should record and track operation errors', () => {
      const testError = new Error('Test operation failure');
      
      performanceMonitor.recordError('test-operation', testError);
      
      const metrics = performanceMonitor.getMetrics();
      const errorMetrics = metrics.filter(m => m.category === 'error');
      
      expect(errorMetrics.length).toBe(1);
      expect(errorMetrics[0].name).toBe('test-operation.errors');
      expect(errorMetrics[0].value).toBe(1);
      expect(errorMetrics[0].labels?.errorType).toBe('Error');
      expect(errorMetrics[0].labels?.errorMessage).toBe('Test operation failure');

      console.log(`✅ Error tracking: ${errorMetrics[0].name} recorded`);
    });

    it('should include error rates in performance reports', () => {
      // Record some successful operations and some errors
      for (let i = 0; i < 8; i++) {
        performanceMonitor.recordMetric({
          name: 'test-operation.latency',
          value: 10 + Math.random() * 5,
          unit: 'ms',
          timestamp: new Date().toISOString(),
          category: 'latency',
          labels: { operation: 'test-operation' }
        });
      }

      // Record 2 errors out of 10 total operations (20% error rate)
      performanceMonitor.recordError('test-operation', new Error('Error 1'));
      performanceMonitor.recordError('test-operation', new Error('Error 2'));

      const report = performanceMonitor.getPerformanceReport();
      
      expect(report.summary.errorRate).toBeCloseTo(0.2, 1); // 20% error rate
      expect(report.operationBreakdown['test-operation'].errorCount).toBe(2);

      console.log(`✅ Error rate tracking: ${(report.summary.errorRate * 100).toFixed(1)}% error rate`);
    });
  });

  describe('Real-world Performance Scenarios', () => {
    it('should handle high-throughput scenarios efficiently', async () => {
      const startTime = performance.now();
      
      // Process 50 operations rapidly
      const promises = Array.from({ length: 50 }, (_, i) => 
        instrumentedWorkflow.processCapture(`High throughput test ${i}`)
      );
      
      await Promise.all(promises);
      
      const totalTime = performance.now() - startTime;
      const report = performanceMonitor.getPerformanceReport();
      
      expect(report.summary.totalOperations).toBe(250); // 50 * 5 operations each
      expect(totalTime).toBeLessThan(5000); // Should complete in under 5 seconds
      
      const throughput = report.summary.totalOperations / (totalTime / 1000);
      expect(throughput).toBeGreaterThan(50); // At least 50 ops/sec

      console.log(`✅ High throughput: ${throughput.toFixed(1)} ops/sec, ${totalTime.toFixed(0)}ms total`);
    });

    it('should maintain performance under varying load conditions', async () => {
      const loadLevels = [1, 5, 10, 20];
      const performanceResults: number[] = [];

      for (const load of loadLevels) {
        performanceMonitor.clearMetrics();
        const startTime = performance.now();
        
        const promises = Array.from({ length: load }, (_, i) => 
          instrumentedWorkflow.processCapture(`Load test ${load}-${i}`)
        );
        
        await Promise.all(promises);
        
        const endTime = performance.now();
        const avgLatency = (endTime - startTime) / load;
        performanceResults.push(avgLatency);
      }

      // Performance should scale reasonably (shouldn't degrade exponentially)
      const performanceDegradation = performanceResults[3] / performanceResults[0];
      expect(performanceDegradation).toBeLessThan(5); // Should not be more than 5x slower

      console.log(`✅ Load scaling: ${performanceResults.map(r => r.toFixed(1)).join('→')}ms avg latency`);
      console.log(`✅ Performance degradation: ${performanceDegradation.toFixed(2)}x at 20x load`);
    });
  });
});