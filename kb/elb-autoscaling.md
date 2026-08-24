# Elastic Load Balancing and Auto Scaling

Together these give you **high availability** and **elasticity** — distribute traffic and add/remove
capacity automatically.

## Load balancer types
- **Application Load Balancer (ALB)**: Layer 7 (HTTP/HTTPS). Routes by **path, host, headers, query**.
  Targets: EC2, IP, Lambda, containers. Best for web apps and microservices.
- **Network Load Balancer (NLB)**: Layer 4 (TCP/UDP/TLS). Ultra-high performance, low latency,
  **static IP / Elastic IP**. Millions of requests/sec. Best for extreme performance or non-HTTP.
- **Gateway Load Balancer (GWLB)**: deploy/scale third-party virtual appliances (firewalls, IDS).
- **Classic Load Balancer**: legacy, avoid for new designs.

## Key ELB concepts
- **Target groups** with **health checks** — unhealthy targets are removed from rotation.
- **Cross-zone load balancing** spreads traffic evenly across AZs.
- Terminate **TLS/SSL** at the load balancer; integrate with **ACM** for free certificates.
- **Sticky sessions** pin a client to a target when needed.

## EC2 Auto Scaling Groups (ASG)
- Maintain a target number of instances across AZs; replace unhealthy ones automatically.
- **Launch template** defines what to launch (AMI, type, SG, user data).
- Scaling policies: **target tracking** (e.g. keep CPU at 50%), **step**, **scheduled**, **predictive**.
- Set **min / desired / max** capacity. Combine ASG + ELB for a self-healing, elastic tier.
