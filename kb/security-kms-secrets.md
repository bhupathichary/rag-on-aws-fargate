# Security: KMS, Secrets Manager, and Parameter Store

## AWS KMS (Key Management Service)
- Managed **encryption keys**. Most AWS services integrate with KMS to encrypt data at rest
  (S3, EBS, RDS, DynamoDB, Secrets Manager).
- **Customer Managed Keys (CMK)** give you control over rotation and key policies; AWS-managed keys are simpler.
- **Envelope encryption**: KMS encrypts a data key, which encrypts your data. All key use is logged in **CloudTrail**.
- Automatic annual key rotation available for CMKs.

## Secrets Manager vs Parameter Store
Both store configuration/secrets, but differ:
- **Secrets Manager**: purpose-built for secrets (DB passwords, API keys). Supports **automatic
  rotation** (e.g. rotate an RDS password on a schedule via Lambda). Encrypted with KMS. Has a cost per secret.
- **SSM Parameter Store**: store config values and secrets (SecureString via KMS). **Free** standard tier,
  no built-in rotation. Good for plain config and simple secrets.

**Chooser**: need rotation / it's a real credential → **Secrets Manager**. Simple config or
budget-sensitive → **Parameter Store**.

## For your flagship
Store the **Anthropic API key** in **Secrets Manager** (or Parameter Store SecureString). The
Fargate **task role** is granted permission to read just that secret at runtime — the key never
sits in your code, image, or environment file in plaintext.

## Broader security services (know the names)
- **WAF** (web app firewall), **Shield** (DDoS), **GuardDuty** (threat detection),
  **Inspector** (vuln scanning), **Macie** (sensitive data in S3), **IAM Identity Center** (SSO).
