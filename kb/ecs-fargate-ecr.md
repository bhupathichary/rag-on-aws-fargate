# Containers on AWS: ECS, Fargate, and ECR

This is the deployment path for your flagship RAG service.

## ECR (Elastic Container Registry)
- Managed **Docker image registry**. You `docker build`, tag, and `docker push` images here.
- Private by default; access controlled via IAM. Integrates with ECS/EKS and image scanning.

## ECS (Elastic Container Service)
- AWS-native container orchestration. You define a **task definition** (which image, CPU/memory,
  ports, environment, IAM **task role**) and run it as a **task** or a long-running **service**.
- **Service** keeps N tasks running, integrates with an **ALB** and **Auto Scaling**.
- Two launch types:
  - **Fargate** — **serverless**: AWS runs the containers, no EC2 to manage. Pay per vCPU/memory/second. Simplest.
  - **EC2** — you manage a cluster of EC2 container hosts (more control, cheaper at scale).

## Fargate (the recommended default)
- No servers to patch or scale; you just specify CPU/memory and run tasks.
- Runs in your **VPC**; give it an **IAM task role** for least-privilege access to S3/DynamoDB/Secrets Manager.
- Put an **ALB** in front for a public endpoint + health checks; scale with Service Auto Scaling.

## EKS (Elastic Kubernetes Service)
- Managed **Kubernetes** for teams standardizing on K8s. More power and portability, more complexity.
- Your post-exam "stretch": redeploy the same container on EKS and note the ECS-vs-EKS trade-offs.

## Typical flow for your project
`docker build` → **ECR** → **ECS task definition** → **Fargate service** behind an **ALB** →
public URL, with **CloudWatch** logs and **Secrets Manager** for the API key.
