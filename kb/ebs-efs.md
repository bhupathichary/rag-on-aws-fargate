# AWS Storage: EBS vs EFS vs Instance Store

Three block/file storage options that are easy to confuse on the exam.

## EBS (Elastic Block Store)
- Network-attached **block** storage for a single EC2 instance (one AZ).
- Persists independently of the instance lifecycle. Can be detached/reattached (same AZ).
- **Volume types**: gp3/gp2 (general SSD), io1/io2 (provisioned IOPS SSD, high performance/databases),
  st1 (throughput HDD, big data), sc1 (cold HDD, archival).
- **Snapshots** are incremental backups stored in S3; can copy across regions and create AMIs.
- Can be encrypted with KMS (encrypts data at rest, in transit to instance, and snapshots).

## EFS (Elastic File System)
- Managed **NFS** file system, **shared across many EC2 instances and AZs** simultaneously.
- Elastic — grows/shrinks automatically. Linux only.
- Modes: Standard vs One Zone; lifecycle to Infrequent Access for cost savings.
- Use when multiple instances need a shared filesystem (content management, shared config).

## Instance Store
- **Ephemeral** physical disk attached to the host. Fastest IO, but **data is lost when the
  instance stops/terminates**. Use for caches, scratch, buffers — never durable data.

## Quick chooser
- One instance, persistent block volume → **EBS**
- Many instances share files → **EFS**
- Temporary high-speed scratch → **Instance Store**
