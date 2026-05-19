import requests
import os
from datetime import datetime, timedelta

# Azure DevOps configuration
ORGANIZATION = "Preshita91"
PROJECT = "Project-Status-Monitor"
PAT = os.environ.get("AZURE_DEVOPS_PAT")

# Slack configuration
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

# Date thresholds
TODAY = datetime.today().date()
NEXT_WEEK = TODAY + timedelta(days=7)

def get_work_items():
    url = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/wit/wiql?api-version=7.0"

    query = {
        "query": "SELECT [System.Id], [System.Title], [Microsoft.VSTS.Scheduling.TargetDate], [System.State] FROM WorkItems WHERE [System.TeamProject] = @project"
    }

    response = requests.post(
        url,
        json=query,
        auth=("", PAT)
    )

    if response.status_code != 200:
        raise RuntimeError(f"Azure DevOps API error {response.status_code}: {response.text}")

    work_items = response.json().get("workItems", [])
    return [item["id"] for item in work_items]

def get_work_item_details(item_id):
    url = f"https://dev.azure.com/{ORGANIZATION}/{PROJECT}/_apis/wit/workitems/{item_id}?api-version=7.0"

    response = requests.get(url, auth=("", PAT))

    if response.status_code != 200:
        raise RuntimeError(f"Azure DevOps API error {response.status_code} for item {item_id}: {response.text}")

    return response.json()

def check_status(item):
    fields = item.get("fields", {})
    title = fields.get("System.Title", "Unknown")
    due_date_str = fields.get("Microsoft.VSTS.Scheduling.TargetDate")

    if not due_date_str:
        return None

    due_date = datetime.strptime(due_date_str[:10], "%Y-%m-%d").date()

    if due_date < TODAY:
        return f":red_circle: *OVERDUE:* '{title}' was due on {due_date}"
    elif due_date <= NEXT_WEEK:
        return f":warning: *DUE SOON:* '{title}' is due on {due_date}"
    else:
        return None

def send_slack_notification(alerts):
    message = "*Project Status Monitor Alert*\n\n"
    message += "\n".join(alerts)
    message += "\n\n_Please review and take action._"

    response = requests.post(
        SLACK_WEBHOOK_URL,
        json={"text": message}
    )

    if response.status_code == 200:
        print("Slack notification sent successfully.")
    else:
        print(f"Failed to send Slack notification: {response.status_code}")

def main():
    if not PAT:
        raise RuntimeError("AZURE_DEVOPS_PAT secret is not set in GitHub repository secrets.")
    if not SLACK_WEBHOOK_URL:
        raise RuntimeError("SLACK_WEBHOOK_URL secret is not set in GitHub repository secrets.")

    print("Checking project statuses...\n")

    item_ids = get_work_items()
    alerts = []

    for item_id in item_ids:
        item = get_work_item_details(item_id)
        alert = check_status(item)
        if alert:
            alerts.append(alert)

    if alerts:
        print("Projects needing attention:\n")
        for alert in alerts:
            print(alert)
        send_slack_notification(alerts)
    else:
        print("All projects are on track!")

if __name__ == "__main__":
    main()
