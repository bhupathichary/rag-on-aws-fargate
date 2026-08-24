# AWS Lambda and Serverless

Lambda runs your code without provisioning servers. You upload a function; AWS runs it in response
to **events** and bills per request + compute time (GB-seconds). Idle = no cost.

## Key facts
- **Event-driven**: triggered by S3 uploads, API Gateway, DynamoDB Streams, SQS, EventBridge, etc.
- **Max timeout 15 minutes**; memory 128 MB–10 GB (CPU scales with memory).
- **Stateless**; `/tmp` gives ephemeral scratch space. Store state in S3/DynamoDB.
- **Concurrency**: scales automatically; set **reserved concurrency** to cap, **provisioned
  concurrency** to eliminate cold starts for latency-sensitive apps.
- Package as zip or **container image**. Attach an **execution role** for permissions.

## API Gateway (front door for serverless APIs)
- **REST API**, **HTTP API** (cheaper/faster), and **WebSocket API**.
- Handles throttling, auth (IAM, Cognito, Lambda authorizers), caching, request/response mapping.
- Common pattern: **API Gateway → Lambda → DynamoDB**, a fully serverless backend.

## When serverless fits
- Spiky/unpredictable traffic, event processing, glue code, lightweight APIs — you avoid paying for
  idle servers. Not ideal for long-running (>15 min) or steady high-throughput compute (use ECS/EC2).

## Related serverless services
- **Step Functions**: orchestrate multi-step workflows with state.
- **EventBridge**: event bus for decoupled, event-driven architectures.
- **Fargate**: serverless containers (see ecs-fargate-ecr).
