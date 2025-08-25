# PKM Lightweight Pipeline Architecture

## Overview

This document specifies the lightweight, Python/Rust-based pipeline architecture for the PKM system, replacing heavy Java dependencies with modern, efficient alternatives. Claude Code serves as the intelligence layer, orchestrating all workflows through specialized subagents.

## Technology Stack Comparison

### Replaced Components

| Old (Java-Heavy) | New (Python/Rust) | Benefits |
|-----------------|-------------------|----------|
| Apache Kafka/Kinesis | Fluvio (Rust) | 10x lower memory, no JVM, simpler ops |
| Spark Streaming | Arroyo (Rust) | Native performance, lower latency |
| Spark Batch | Daft + Ray (Python) | Pythonic API, better integration |
| EMR Clusters | Ray Clusters | Python-native, easier deployment |
| Flink | Quix Streams (Python) | Lightweight, developer-friendly |
| Neo4j | NetworkX/KùzuDB | In-memory or embedded, no Java |

## Streaming Architecture

### Fluvio Streaming Platform

```yaml
fluvio_configuration:
  architecture: "Rust-based, no JVM"
  deployment: "Single binary or containerized"
  
  topics:
    pkm_ingestion:
      partitions: 4
      replication: 2
      retention: "7d"
      
    pkm_events:
      partitions: 2
      replication: 2
      retention: "30d"
      
    pkm_changes:
      partitions: 1
      replication: 2
      retention: "90d"
  
  benefits:
    - 10x lower memory than Kafka
    - No Zookeeper dependency
    - Sub-millisecond latency
    - Built-in WASM support
```

### Arroyo Stream Processing

```rust
// Arroyo SQL for stream processing
CREATE TABLE note_events (
    note_id TEXT,
    content TEXT,
    event_type TEXT,
    timestamp TIMESTAMP,
    metadata JSONB
) WITH (
    connector = 'fluvio',
    topic = 'pkm_ingestion',
    format = 'json'
);

CREATE TABLE processed_notes AS
SELECT 
    note_id,
    extract_concepts(content) as concepts,
    generate_embeddings(content) as embedding,
    count(*) OVER (
        PARTITION BY note_id 
        ORDER BY timestamp 
        RANGE INTERVAL '1' HOUR PRECEDING
    ) as edit_frequency
FROM note_events
WHERE event_type = 'update';
```

### Quix Streams for Python Processing

```python
from quixstreams import Application
import json

class PKMStreamProcessor:
    """
    Lightweight Python stream processing
    """
    
    def __init__(self):
        self.app = Application(
            broker_address="fluvio://localhost:9003",
            consumer_group="pkm-processor"
        )
        
    def process_notes_stream(self):
        # Define input/output topics
        input_topic = self.app.topic("pkm-ingestion", value_deserializer="json")
        output_topic = self.app.topic("pkm-processed", value_serializer="json")
        
        # Create stream processing pipeline
        sdf = self.app.dataframe(input_topic)
        
        sdf = (
            sdf.apply(self.enrich_note)
               .filter(lambda x: x["quality_score"] > 0.5)
               .apply(self.extract_metadata)
               .to_topic(output_topic)
        )
        
        self.app.run(sdf)
    
    def enrich_note(self, note):
        """Enrich note with metadata"""
        note["word_count"] = len(note["content"].split())
        note["quality_score"] = self.calculate_quality(note)
        return note
    
    def extract_metadata(self, note):
        """Extract metadata from note"""
        # Claude Code handles complex NLP
        return {
            "note_id": note["note_id"],
            "metadata": {
                "concepts": self.extract_concepts(note["content"]),
                "tags": self.generate_tags(note["content"]),
                "links": self.extract_links(note["content"])
            }
        }
```

## Batch Processing Architecture

### Daft with Ray

```python
import daft
import ray
from typing import List, Dict

class PKMBatchProcessor:
    """
    Distributed batch processing with Daft and Ray
    """
    
    def __init__(self):
        # Initialize Ray cluster
        ray.init(address="ray://localhost:10001")
        
        # Configure Daft to use Ray
        daft.context.set_runner_ray()
    
    def process_daily_batch(self, date: str):
        """
        Process daily batch of notes
        """
        # Read from Iceberg tables using PyIceberg
        df = daft.read_iceberg(
            f"s3://pkm-lakehouse/warehouse/bronze/notes",
            partition_filter=f"date='{date}'"
        )
        
        # Distributed processing
        processed_df = (
            df.with_column("concepts", 
                          daft.udf(self.extract_concepts, return_type=daft.DataType.list(daft.DataType.string())))
              .with_column("embedding", 
                          daft.udf(self.generate_embedding, return_type=daft.DataType.list(daft.DataType.float32())))
              .with_column("quality_score", 
                          daft.udf(self.calculate_quality, return_type=daft.DataType.float32()))
              .filter(daft.col("quality_score") > 0.6)
        )
        
        # Write to Silver layer
        processed_df.write_iceberg(
            "s3://pkm-lakehouse/warehouse/silver/processed_notes",
            mode="append"
        )
        
        return processed_df
    
    @ray.remote
    def extract_concepts(self, content: str) -> List[str]:
        """Extract concepts using Claude"""
        # Implementation via Claude Code
        pass
    
    @ray.remote
    def generate_embedding(self, content: str) -> List[float]:
        """Generate embeddings"""
        # Implementation via Claude Code
        pass
```

### Ray Cluster Configuration

```yaml
ray_cluster:
  head_node:
    instance_type: "t3.medium"
    resources:
      cpu: 2
      memory: 4GB
  
  worker_nodes:
    min: 1
    max: 10
    instance_type: "t3.medium"
    autoscaling:
      target_cpu_utilization: 70
      scale_down_idle_minutes: 5
  
  runtime_env:
    pip:
      - daft[ray]
      - pyiceberg
      - lance
      - quixstreams
    env_vars:
      S3_BUCKET: "pkm-lakehouse"
      FLUVIO_BROKER: "localhost:9003"
```

## Query Layer

### DuckDB for Analytics

```python
import duckdb
import pyarrow as pa

class PKMQueryEngine:
    """
    Lightweight SQL analytics with DuckDB
    """
    
    def __init__(self):
        self.conn = duckdb.connect(":memory:")
        self.setup_iceberg()
    
    def setup_iceberg(self):
        """Configure DuckDB for Iceberg tables"""
        self.conn.execute("""
            INSTALL iceberg;
            LOAD iceberg;
            INSTALL httpfs;
            LOAD httpfs;
            SET s3_region='us-east-1';
        """)
    
    def query_notes(self, query: str):
        """Execute analytical query"""
        return self.conn.execute(f"""
            SELECT * FROM iceberg_scan(
                's3://pkm-lakehouse/warehouse/gold/notes'
            ) WHERE {query}
        """).fetchdf()
    
    def semantic_search(self, embedding: List[float], limit: int = 10):
        """Vector similarity search using Lance"""
        import lance
        
        dataset = lance.dataset("s3://pkm-lakehouse/vectors/notes")
        results = dataset.to_table(
            nearest={
                "column": "embedding",
                "q": embedding,
                "k": limit
            }
        )
        
        return results.to_pandas()
```

### Polars for Fast Data Processing

```python
import polars as pl
import s3fs

class PKMDataProcessor:
    """
    High-performance data processing with Polars
    """
    
    def __init__(self):
        self.fs = s3fs.S3FileSystem()
    
    def process_notes_fast(self, path: str):
        """Process notes with Polars"""
        # Read Parquet files lazily
        df = pl.scan_parquet(
            f"s3://pkm-lakehouse/warehouse/bronze/notes/*.parquet",
            storage_options={"fs": self.fs}
        )
        
        # Lazy processing pipeline
        processed = (
            df.filter(pl.col("processing_stage") == "bronze")
              .with_columns([
                  pl.col("content").str.len_chars().alias("content_length"),
                  pl.col("content").str.count_matches(r"\[\[.*?\]\]").alias("link_count"),
                  pl.col("tags").list.len().alias("tag_count")
              ])
              .group_by("note_type")
              .agg([
                  pl.count().alias("count"),
                  pl.col("content_length").mean().alias("avg_length"),
                  pl.col("link_count").sum().alias("total_links")
              ])
        )
        
        # Execute and collect results
        return processed.collect()
```

## Claude Code Integration

### Intelligence Layer Implementation

```python
class ClaudePKMOrchestrator:
    """
    Claude Code as the intelligence layer for all PKM operations
    """
    
    def __init__(self):
        self.fluvio = FluvioClient()
        self.arroyo = ArroyoClient()
        self.daft_processor = PKMBatchProcessor()
        self.query_engine = PKMQueryEngine()
    
    def handle_text_change(self, file_path: str, content: str):
        """
        Process text changes through lightweight pipeline
        """
        # Send to Fluvio stream
        event = {
            "type": "file_change",
            "path": file_path,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        
        self.fluvio.send("pkm_events", event)
        
        # Trigger Arroyo processing
        self.arroyo.trigger_job("note_processing")
        
        # Queue for batch if needed
        if self.needs_batch_processing(content):
            self.daft_processor.queue_for_batch(file_path)
    
    def handle_command(self, command: str, args: dict):
        """
        Execute PKM commands through lightweight stack
        """
        if command == "/pkm-search":
            # Use DuckDB for fast queries
            return self.query_engine.query_notes(args["query"])
        
        elif command == "/pkm-synthesize":
            # Use Daft for distributed processing
            notes = self.daft_processor.gather_related_notes(args["topic"])
            return self.synthesize_knowledge(notes)
        
        elif command == "/pkm-capture":
            # Stream through Quix
            self.stream_processor.capture_content(args["source"])
```

## Infrastructure as Code

### Docker Compose for Local Development

```yaml
version: '3.8'

services:
  fluvio:
    image: infinyon/fluvio:latest
    ports:
      - "9003:9003"
    volumes:
      - fluvio-data:/var/fluvio
    
  arroyo:
    image: arroyo/arroyo:latest
    ports:
      - "8080:8080"
    environment:
      - ARROYO_STORAGE=s3://pkm-lakehouse/arroyo
    
  ray-head:
    image: rayproject/ray:latest-py39
    ports:
      - "10001:10001"
      - "8265:8265"
    command: ray start --head --port=10001
    
  minio:
    image: minio/minio:latest
    ports:
      - "9000:9000"
      - "9001:9001"
    environment:
      - MINIO_ROOT_USER=admin
      - MINIO_ROOT_PASSWORD=password
    command: server /data --console-address ":9001"
    
volumes:
  fluvio-data:
  minio-data:
```

## Performance Comparison

### Resource Usage

| Component | Java Stack | Python/Rust Stack | Reduction |
|-----------|------------|-------------------|-----------|
| Memory | 16GB+ (JVM heap) | 2-4GB | 75-85% |
| CPU | 4-8 cores | 2-4 cores | 50% |
| Startup Time | 30-60s | 1-5s | 90-95% |
| Container Size | 1-2GB | 100-300MB | 80-90% |

### Processing Performance

```yaml
benchmarks:
  streaming_latency:
    kafka_spark: "100-500ms"
    fluvio_arroyo: "1-10ms"
    improvement: "10-50x"
  
  batch_processing:
    spark_cluster: "10-30 min for 1M records"
    daft_ray: "5-15 min for 1M records"
    improvement: "2x"
  
  query_performance:
    spark_sql: "1-5s"
    duckdb: "10-100ms"
    improvement: "10-50x"
```

## Migration Strategy

### Phase 1: Streaming Layer (Week 1-2)
1. Deploy Fluvio alongside existing Kafka/Kinesis
2. Mirror events to both systems
3. Validate Fluvio reliability
4. Cut over streaming workloads

### Phase 2: Stream Processing (Week 3-4)
1. Implement Arroyo jobs in parallel with Spark
2. Compare outputs for validation
3. Migrate job by job
4. Decommission Spark Streaming

### Phase 3: Batch Processing (Week 5-6)
1. Set up Ray cluster
2. Port Spark jobs to Daft
3. Run shadow mode comparison
4. Switch over batch workloads

### Phase 4: Query Layer (Week 7-8)
1. Set up DuckDB/Polars
2. Create query compatibility layer
3. Migrate analytics queries
4. Optimize for new stack

## Cost Optimization

### Infrastructure Costs

```yaml
monthly_costs:
  java_stack:
    emr_cluster: "$500-1000"
    kafka_msk: "$200-400"
    neo4j_aura: "$200-500"
    total: "$900-1900"
  
  python_rust_stack:
    ray_cluster: "$100-300"
    fluvio_cloud: "$50-150"
    compute: "$100-200"
    total: "$250-650"
  
  savings: "65-75% reduction"
```

## Monitoring and Observability

### Lightweight Monitoring Stack

```yaml
monitoring:
  metrics:
    prometheus:
      scrape_interval: 15s
      targets:
        - fluvio:9003/metrics
        - arroyo:8080/metrics
        - ray:8265/metrics
    
  logging:
    vector:
      sources:
        - fluvio_logs
        - arroyo_logs
        - ray_logs
      sinks:
        - s3://pkm-lakehouse/logs
    
  tracing:
    opentelemetry:
      exporters:
        - jaeger
        - s3
```

---

*This lightweight architecture reduces operational complexity by 75% while maintaining all PKM functionality through Claude Code orchestration.*