# AWS Well-Architected Framework

A set of best practices for designing cloud systems, organized into **six pillars**. The SAA exam
frames many scenario questions around these trade-offs.

## The six pillars
1. **Operational Excellence** — run and monitor systems, improve processes. Automate changes,
   respond to events, define standards (IaC, runbooks, observability).
2. **Security** — protect data and systems. Least-privilege IAM, encryption at rest/in transit,
   traceability (CloudTrail), defense in depth.
3. **Reliability** — recover from failure, scale to meet demand. Multi-AZ, health checks, auto
   scaling, backups, loosely coupled components, graceful degradation.
4. **Performance Efficiency** — use resources efficiently. Right-size instances, use serverless/
   managed services, caching (CloudFront, ElastiCache, DAX), pick the right storage/database.
5. **Cost Optimization** — avoid unnecessary spend. Right purchasing model (Spot/Reserved/Savings
   Plans), turn off idle resources, S3 lifecycle policies, pay-for-what-you-use.
6. **Sustainability** — minimize environmental impact. Efficient resource use, managed services,
   right-sizing.

## How to use it on the exam
When a question asks for the "best" design, it's usually testing a pillar trade-off:
- "Most cost-effective" → Cost Optimization (Spot, S3-IA, serverless, right-sizing).
- "Highly available / fault tolerant" → Reliability (Multi-AZ, ASG, failover routing).
- "Most secure" → Security (least privilege, encryption, private subnets, no public access).
- "Best performance / lowest latency" → Performance Efficiency (caching, edge, read replicas).

Ask: *which pillar is this scenario optimizing for?* — the wording usually tells you.
