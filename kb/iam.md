# AWS IAM (Identity and Access Management)

IAM controls **who** can do **what** on **which** resources. It is global (not region-scoped) and free.

## Core entities
- **Users**: a person or app with long-term credentials. Avoid using the root user for daily work.
- **Groups**: collections of users; attach policies to a group to manage many users at once.
- **Roles**: temporary credentials assumed by trusted entities — EC2 instances, Lambda functions,
  other AWS accounts, or federated users. **Preferred over long-term keys.**
- **Policies**: JSON documents granting/denying permissions. Attach to users, groups, or roles.

## Policy structure
```json
{ "Effect": "Allow", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::my-bucket/*" }
```
- **Effect**: Allow or Deny (explicit Deny always wins).
- **Action**: the API calls permitted.
- **Resource**: which ARNs it applies to.
- **Condition**: optional constraints (IP, MFA, time).

## Best practices (exam themes)
- **Least privilege** — grant only what's needed.
- Use **roles for workloads** (EC2/Lambda), never embed access keys in code or on instances.
- Enable **MFA**, especially on the root account.
- Evaluation logic: default deny → explicit Allow grants → explicit Deny overrides everything.
- **IAM Identity Center (SSO)** for workforce/multi-account access; **STS** issues temporary tokens.
