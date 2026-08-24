# Monitoring: CloudWatch, CloudTrail, and Config

Three observability services the exam expects you to tell apart.

## CloudWatch — metrics, logs, alarms (what is happening)
- **Metrics**: numeric performance data (CPU, latency, queue depth). Custom metrics supported.
- **Logs**: centralize application/system logs (e.g. Lambda, ECS, EC2 via agent). Query with Logs Insights.
- **Alarms**: trigger on a metric threshold → notify (SNS) or act (Auto Scaling, EC2 action).
- **Dashboards**: visualize metrics. **EventBridge** (formerly CloudWatch Events) reacts to events on a schedule or pattern.
- Basic EC2 monitoring is 5-minute; **detailed monitoring** is 1-minute (extra cost).

## CloudTrail — API audit log (who did what)
- Records **API calls** across your account: who, when, from where, what action.
- Essential for **security auditing, compliance, and forensics**.
- Delivers logs to S3; enable across all regions. Not for performance metrics — that's CloudWatch.

## AWS Config — resource compliance (is it configured correctly)
- Tracks **resource configuration history** and evaluates against **rules** (e.g. "all EBS volumes
  must be encrypted"). Flags non-compliant resources and can auto-remediate.

## Quick chooser
- Performance/health + alerts → **CloudWatch**
- "Who made this API call?" → **CloudTrail**
- "Is this resource compliant with policy?" → **Config**
