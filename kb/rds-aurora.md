# Amazon RDS and Aurora (Relational Databases)

RDS is managed relational database hosting (patching, backups, failover handled by AWS). Engines:
MySQL, PostgreSQL, MariaDB, Oracle, SQL Server, and Amazon Aurora.

## Multi-AZ vs Read Replicas (the classic exam trap)
- **Multi-AZ deployment** = **high availability / disaster recovery**. A synchronous standby in
  another AZ. Automatic failover on outage. **Not** for scaling reads — the standby isn't readable.
- **Read Replicas** = **read scaling**. Asynchronous copies you can direct read traffic to. Up to
  15 for Aurora, 5 for RDS. Can be cross-region. Can be promoted to standalone.

Remember: **Multi-AZ = availability; Read Replicas = performance/scaling.**

## Amazon Aurora
- AWS-built engine, MySQL- and PostgreSQL-compatible. ~5x MySQL / ~3x PostgreSQL throughput.
- Storage auto-scales to 128 TB; **6 copies of data across 3 AZs**, self-healing.
- **Aurora Serverless** auto-scales capacity for variable/unpredictable workloads.
- **Aurora Global Database** for cross-region DR with ~1s replication.

## Backups
- **Automated backups** with point-in-time recovery (retention up to 35 days).
- **Manual snapshots** kept until you delete them.

## When not to use RDS
- Need single-digit-ms NoSQL at massive scale → **DynamoDB**.
- Data warehousing / analytics on petabytes → **Redshift**.
