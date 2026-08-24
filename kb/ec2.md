# Amazon EC2 (Elastic Compute Cloud)

EC2 provides resizable virtual servers ("instances") in the cloud. You choose an AMI (machine
image), an instance type (CPU/memory/network profile), and networking, then launch.

## Instance families
- **General purpose** (t3, t4g, m6i): balanced CPU/memory. Burstable T-family uses CPU credits.
- **Compute optimized** (c6i): high CPU — batch, gaming, HPC.
- **Memory optimized** (r6i, x2): in-memory databases, large caches.
- **Storage optimized** (i4i, d3): high sequential/random disk IO.
- **Accelerated** (p4, g5): GPUs for ML/graphics.

## Purchasing options (exam-critical)
- **On-Demand**: pay per second/hour, no commitment. Use for short/unpredictable workloads.
- **Reserved Instances / Savings Plans**: commit 1 or 3 years for up to ~72% discount. Steady-state workloads.
- **Spot Instances**: up to ~90% off spare capacity, but AWS can reclaim with a 2-minute warning.
  Use for fault-tolerant, interruption-tolerant work (batch, CI, big data).
- **Dedicated Hosts / Dedicated Instances**: physical isolation for licensing/compliance.

## Key facts
- Instances live in a **subnet** inside a **VPC** and are protected by **security groups**.
- **User data** scripts run at first boot to bootstrap the instance.
- **Instance metadata** is available at `http://169.254.169.254/latest/meta-data/`.
- Attach an **IAM role** to an instance so code on it gets temporary credentials — never store keys on the instance.
- **Placement groups**: cluster (low latency), spread (hardware isolation), partition (large distributed systems).
