# Project Status Monitor

An AI-powered project status monitor that connects to Azure DevOps, identifies overdue and at-risk projects, and sends automated Slack notifications every Monday morning.

## Problem Statement
Program Managers tracking 30-40+ projects manually struggle to catch schedule slips before they become critical. This tool automates that monitoring and delivers proactive alerts directly to Slack.

## How It Works
1. Connects to Azure DevOps via API and fetches all work items
2. Checks each project's target date against today's date
3. Flags projects that are overdue or due within the next 7 days
4. Sends a formatted Slack notification with actionable alerts
5. Runs automatically every Monday at 9:00 AM PST via GitHub Actions

## Alerts
- 🔴 **OVERDUE** — project has passed its target date
- ⚠️ **DUE SOON** — project is due within the next 7 days

## Tech Stack
- Python 3.9
- Azure DevOps REST API
- Slack Incoming Webhooks
- GitHub Actions (automated scheduling)

## Setup

### Prerequisites
- Azure DevOps account with a project and work items
- Slack workspace with an Incoming Webhook configured
- Python 3.9+

### Installation
1. Clone the repository
   ```
   git clone https://github.com/PreshitaJain/project-status-monitor.git
   cd project-status-monitor
   ```

2. Create and activate a virtual environment
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies
   ```
   pip install requests
   ```

4. Set environment variables
   ```
   export AZURE_DEVOPS_PAT=your_azure_devops_token
   export SLACK_WEBHOOK_URL=your_slack_webhook_url
   ```

5. Run the script
   ```
   python3 project_monitor.py
   ```

## Automated Scheduling
This project uses GitHub Actions to run every Monday at 9:00 AM PST automatically. To enable this in your own repository, add the following secrets in GitHub Settings → Secrets:
- `AZURE_DEVOPS_PAT`
- `SLACK_WEBHOOK_URL`

## Author
Preshita Jain — [LinkedIn](https://linkedin.com/in/preshitajain1) | [GitHub](https://github.com/PreshitaJain)
