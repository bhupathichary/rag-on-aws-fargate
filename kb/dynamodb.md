# Amazon DynamoDB (NoSQL)

Fully managed, serverless key-value and document database. **Single-digit-millisecond** latency at
any scale. No servers to manage; scales automatically. Multi-AZ by default.

## Data model
- **Tables** contain **items** (rows); items have **attributes**.
- **Primary key**: partition key alone, or partition key + sort key (composite).
- The partition key is hashed to distribute data — choose a high-cardinality key to avoid "hot partitions".

## Capacity modes
- **On-Demand**: pay per request, auto-scales instantly. Unpredictable/spiky workloads.
- **Provisioned**: set read/write capacity units (RCU/WCU); cheaper for steady, predictable load.
  Add auto scaling to adjust within bounds.

## Performance and access patterns
- **DAX (DynamoDB Accelerator)**: in-memory cache, microsecond reads for read-heavy workloads.
- **Global Secondary Index (GSI)**: query on non-key attributes; different partition/sort key.
- **Local Secondary Index (LSI)**: same partition key, alternate sort key (defined at table creation).
- **DynamoDB Streams**: ordered change log — trigger Lambda on inserts/updates/deletes.
- **Global Tables**: multi-region, active-active replication.

## When to choose it
- High-scale, low-latency lookups with known access patterns (session stores, user profiles,
  IoT, shopping carts). Not for complex joins/ad-hoc queries — that's relational/Redshift territory.
