/**
 * Performance Monitor
 * TDD Cycle 1.4 - Real-time performance tracking and metrics collection
 * 
 * SOLID Principles:
 * - SRP: Single responsibility for performance monitoring and metrics collection
 * - OCP: Open for extension through custom metrics and thresholds
 * - ISP: Interface segregation with focused monitoring capabilities
 * - DIP: Depends on performance data abstractions
 */

export interface PerformanceMetric {
  name: string;
  value: number;
  unit: 'ms' | 'bytes' | 'count' | 'percent' | 'ops/sec';
  timestamp: string;
  category: 'latency' | 'throughput' | 'memory' | 'cpu' | 'error';
  labels?: Record<string, string>;
}

export interface PerformanceAlert {
  id: string;
  severity: 'info' | 'warning' | 'error' | 'critical';
  message: string;
  metric: string;
  threshold: number;
  actualValue: number;
  timestamp: string;
  resolved: boolean;
}

export interface PerformanceProfile {
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

export interface PerformanceThresholds {
  qualityAssessment: { maxLatency: number; errorRate: number };
  duplicateDetection: { maxLatency: number; errorRate: number };
  workflowOrchestration: { maxLatency: number; errorRate: number };
  metadataGeneration: { maxLatency: number; errorRate: number };
  endToEnd: { maxLatency: number; errorRate: number };
}

export class PerformanceMonitor {
  private metrics: PerformanceMetric[] = [];
  private alerts: PerformanceAlert[] = [];
  private activeProfiles: Map<string, PerformanceProfile> = new Map();
  private thresholds: PerformanceThresholds;
  private isMonitoring: boolean = false;

  constructor(thresholds?: Partial<PerformanceThresholds>) {
    // KISS: Simple default thresholds based on TDD Cycle 1.4 requirements
    this.thresholds = {
      qualityAssessment: { maxLatency: 50, errorRate: 0.01 },
      duplicateDetection: { maxLatency: 50, errorRate: 0.01 },
      workflowOrchestration: { maxLatency: 20, errorRate: 0.005 },
      metadataGeneration: { maxLatency: 30, errorRate: 0.005 },
      endToEnd: { maxLatency: 100, errorRate: 0.02 },
      ...thresholds
    };
  }

  // SRP: Monitoring lifecycle management
  startMonitoring(): void {
    this.isMonitoring = true;
    this.metrics = [];
    this.alerts = [];
    this.activeProfiles.clear();
  }

  stopMonitoring(): void {
    this.isMonitoring = false;
  }

  // SRP: Operation profiling
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

    // Record metrics - DRY principle
    this.recordLatencyMetric(profile);
    this.recordMemoryMetric(profile);

    // Check thresholds and generate alerts
    this.checkThresholds(profile);

    return profile;
  }

  // SRP: Metrics recording
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

  // SRP: Data retrieval
  getMetrics(): PerformanceMetric[] {
    return [...this.metrics]; // Return copy for encapsulation
  }

  getAlerts(): PerformanceAlert[] {
    return [...this.alerts]; // Return copy for encapsulation
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

  // SRP: Performance reporting
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
    
    // Group by operation - DRY principle applied
    this.groupLatencyMetrics(latencyMetrics, operationBreakdown);
    this.groupErrorMetrics(errorMetrics, operationBreakdown);
    this.calculateOperationStatistics(operationBreakdown);

    const totalOperations = latencyMetrics.length;
    const totalErrors = errorMetrics.reduce((sum, m) => sum + m.value, 0);

    return {
      summary: {
        totalOperations,
        averageLatency: this.calculateAverageLatency(latencyMetrics),
        errorRate: totalOperations > 0 ? totalErrors / totalOperations : 0,
        memoryUsage: this.getCurrentMemoryUsage(),
        activeAlerts: this.getActiveAlerts().length
      },
      operationBreakdown,
      alerts: this.getActiveAlerts()
    };
  }

  // OCP: Configuration management
  updateThresholds(newThresholds: Partial<PerformanceThresholds>): void {
    this.thresholds = { ...this.thresholds, ...newThresholds };
  }

  clearMetrics(): void {
    this.metrics = [];
  }

  clearAlerts(): void {
    this.alerts = [];
  }

  // DRY: Extracted helper methods
  private recordLatencyMetric(profile: PerformanceProfile): void {
    this.recordMetric({
      name: `${profile.operationName}.latency`,
      value: profile.duration || 0,
      unit: 'ms',
      timestamp: new Date().toISOString(),
      category: 'latency',
      labels: { operation: profile.operationName }
    });
  }

  private recordMemoryMetric(profile: PerformanceProfile): void {
    this.recordMetric({
      name: `${profile.operationName}.memory_peak`,
      value: profile.memoryPeak - profile.memoryStart,
      unit: 'bytes',
      timestamp: new Date().toISOString(),
      category: 'memory',
      labels: { operation: profile.operationName }
    });
  }

  private checkThresholds(profile: PerformanceProfile): void {
    const operationName = profile.operationName;
    const duration = profile.duration || 0;

    let threshold = this.findThreshold(operationName);
    
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

  private findThreshold(operationName: string): { maxLatency: number; errorRate: number } | undefined {
    // KISS: Simple threshold mapping
    if (operationName.includes('quality') || operationName.includes('assess')) {
      return this.thresholds.qualityAssessment;
    } else if (operationName.includes('duplicate') || operationName.includes('similarity')) {
      return this.thresholds.duplicateDetection;
    } else if (operationName.includes('workflow') || operationName.includes('orchestrat')) {
      return this.thresholds.workflowOrchestration;
    } else if (operationName.includes('metadata')) {
      return this.thresholds.metadataGeneration;
    } else if (operationName.includes('end-to-end') || operationName.includes('capture')) {
      return this.thresholds.endToEnd;
    }
    return undefined;
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
    // For GREEN phase, using mock data with realistic variations
    return Math.floor(Math.random() * 500000 + 1000000); // 1MB to 1.5MB range
  }

  // DRY: Extracted report calculation methods
  private groupLatencyMetrics(latencyMetrics: PerformanceMetric[], operationBreakdown: Record<string, any>): void {
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
  }

  private groupErrorMetrics(errorMetrics: PerformanceMetric[], operationBreakdown: Record<string, any>): void {
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
  }

  private calculateOperationStatistics(operationBreakdown: Record<string, any>): void {
    Object.keys(operationBreakdown).forEach(operation => {
      const data = operationBreakdown[operation];
      const latencies = data.latencies;
      
      operationBreakdown[operation] = {
        count: latencies.length,
        avgLatency: latencies.length > 0 ? latencies.reduce((a: number, b: number) => a + b, 0) / latencies.length : 0,
        minLatency: latencies.length > 0 ? Math.min(...latencies) : 0,
        maxLatency: latencies.length > 0 ? Math.max(...latencies) : 0,
        errorCount: data.errorCount
      };
    });
  }

  private calculateAverageLatency(latencyMetrics: PerformanceMetric[]): number {
    if (latencyMetrics.length === 0) return 0;
    return latencyMetrics.reduce((sum, m) => sum + m.value, 0) / latencyMetrics.length;
  }
}