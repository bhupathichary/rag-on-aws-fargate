# Amazon VPC (Virtual Private Cloud)

A VPC is a logically isolated virtual network in AWS where you launch resources. You control IP
ranges (CIDR), subnets, route tables, and gateways.

## Core components
- **Subnets**: a range of IPs in one Availability Zone. **Public** subnet = has a route to an
  Internet Gateway. **Private** subnet = no direct internet route.
- **Internet Gateway (IGW)**: allows public subnets to reach the internet (inbound + outbound).
- **NAT Gateway**: lets **private** subnet resources make **outbound** internet calls (e.g. pull
  updates) without being reachable inbound. Managed, highly available per AZ. **Bills hourly + per GB** — a common surprise cost.
- **Route tables**: control where subnet traffic goes.

## Security layers (exam favorite comparison)
| | Security Group | Network ACL |
|---|---|---|
| Level | Instance (ENI) | Subnet |
| State | **Stateful** (return traffic auto-allowed) | **Stateless** (must allow both directions) |
| Rules | Allow only | Allow **and** deny |
| Evaluation | All rules | Rules in number order |

## Connectivity options
- **VPC Peering**: connect two VPCs privately (no transitive routing).
- **Transit Gateway**: hub-and-spoke connecting many VPCs and on-prem.
- **VPC Endpoints**: private access to AWS services without going over the internet.
  **Gateway endpoints** (S3, DynamoDB — free) vs **Interface endpoints** (PrivateLink, hourly cost).
- **Site-to-Site VPN** (over internet, encrypted) and **Direct Connect** (dedicated private line).
