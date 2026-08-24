# Decoupling: SQS, SNS, and Kinesis

Messaging services let components communicate without being directly connected — the core of
**loosely coupled, resilient** architectures.

## SQS (Simple Queue Service) — queues
- **Pull**-based message queue. A producer sends messages; consumers poll and process them.
- **Standard queues**: nearly unlimited throughput, at-least-once delivery, best-effort ordering.
- **FIFO queues**: exactly-once processing, strict ordering, lower throughput.
- **Visibility timeout**: a message is hidden while being processed; reappears if not deleted in time.
- **Dead-Letter Queue (DLQ)**: capture messages that fail repeatedly for later inspection.
- Classic use: **decouple** a web tier from a worker tier; smooth out spikes (buffer).

## SNS (Simple Notification Service) — pub/sub
- **Push**-based publish/subscribe. Publish once to a **topic**; **fan out** to many subscribers
  (SQS queues, Lambda, HTTP, email, SMS).
- Pattern: **SNS → multiple SQS queues** so several systems each get their own copy of an event.

## Kinesis — real-time streaming
- **Data Streams**: ingest and process large **real-time** streams (clickstream, logs, IoT).
  Data split into **shards**; records retained (up to 365 days) and can be re-read.
- **Data Firehose**: load streaming data into S3, Redshift, OpenSearch with minimal code.
- Choose Kinesis when you need ordered, replayable, high-throughput streaming — not just decoupling.

## Chooser
- Decouple + buffer work → **SQS**. Fan-out one event to many → **SNS**. Real-time analytics stream → **Kinesis**.
