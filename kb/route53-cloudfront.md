# Route 53 (DNS) and CloudFront (CDN)

## Amazon Route 53 — DNS + routing
Managed, highly available DNS. Also registers domains and health-checks endpoints.

**Record types**: A, AAAA, CNAME, MX, TXT, and **Alias** records (map a name to an AWS resource
like an ALB, CloudFront, or S3 website — free, and works at the zone apex where CNAME can't).

**Routing policies** (common exam questions):
- **Simple**: one record, no logic.
- **Weighted**: split traffic by percentage (A/B testing, gradual rollout).
- **Latency-based**: send users to the lowest-latency region.
- **Failover**: primary/secondary with health checks (active-passive DR).
- **Geolocation**: route by user's location (compliance, localization).
- **Geoproximity**: route by geographic distance, with bias.
- **Multivalue answer**: return several healthy IPs (basic load spreading).

## Amazon CloudFront — CDN
Caches content at **edge locations** worldwide for low latency and offloads your origin.
- **Origins**: S3 buckets, ALB, EC2, or any HTTP server.
- **Origin Access Control (OAC)**: lock an S3 origin so it's only reachable via CloudFront.
- Integrates with **AWS WAF** and **Shield** for DDoS/web protection, and **ACM** for TLS certs.
- Supports caching policies, signed URLs/cookies for private content, and Lambda@Edge/CloudFront Functions.
- Use it to speed up static + dynamic content globally and reduce load/cost on the origin.
