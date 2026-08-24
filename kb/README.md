# AWS Knowledge Base (for the RAG flagship)

A small corpus of AWS reference docs, written SAA-exam-flavored so that building/querying your
RAG service also reinforces your exam study. Each file is one topic — good chunk boundaries for
retrieval.

## Contents
- `ec2.md` — EC2 instances, families, purchasing options
- `vpc.md` — VPC, subnets, gateways, security groups vs NACLs
- `s3.md` — S3 storage classes, versioning, encryption
- `iam.md` — users, groups, roles, policies
- `ebs-efs.md` — block vs file vs instance-store storage
- `rds-aurora.md` — relational DBs, Multi-AZ vs read replicas, Aurora
- `dynamodb.md` — NoSQL, capacity modes, DAX, GSI/LSI, streams
- `elb-autoscaling.md` — ALB/NLB/GWLB, Auto Scaling Groups
- `lambda-serverless.md` — Lambda, API Gateway, serverless patterns
- `sqs-sns-kinesis.md` — decoupling and streaming
- `cloudwatch-cloudtrail.md` — monitoring, auditing, Config
- `route53-cloudfront.md` — DNS routing policies, CDN
- `ecs-fargate-ecr.md` — containers (your deployment path)
- `security-kms-secrets.md` — KMS, Secrets Manager, Parameter Store
- `well-architected.md` — the six pillars

## How the RAG uses these
1. Load each `.md` as a document (or chunk longer ones).
2. Embed locally with `sentence-transformers` (all-MiniLM-L6-v2).
3. Index with FAISS.
4. On a question, embed it, retrieve the top-k relevant docs, and pass them to Claude as context.

## Notes
- These are learning-grade summaries, **not** authoritative AWS docs. For exam truth, confirm
  against the official AWS service FAQs and documentation.
- Content is synthetic/original — safe to use in a personal project (no proprietary material).
- Grow the corpus as you study: add a doc per new topic; the RAG improves as your notes do.
