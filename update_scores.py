import requests
from datetime import datetime
from zoneinfo import ZoneInfo
from ics import Calendar

TEAM_ID = 8498  # Scotland in FotMob

def get_matches():
    url = f"https://www.fotmob.com/api/teams?id={TEAM_ID}&tab=fixtures"
    data = requests.get(url).json()

    matches = []
    fixtures = data.get("fixtures", {}).get("allFixtures", {}).get("fixtures", [])
    for m in fixtures:
        status = m.get("status", {})
        if not status.get("finished"):
            continue

        matches.append({
            "date": datetime.fromtimestamp(status["utcTimeStamp"]).date(),
            "score": f'{m["result"]["homeScore"]}-{m["result"]["awayScore"]}'
        })

    return matches

def main():
    with open("scotland.ics", "r") as f:
        cal = Calendar(f.read())

    # UK local time
    today = datetime.now(ZoneInfo("Europe/London")).date()

    matches = get_matches()
    matches_today = [m for m in matches if m["date"] == today]

    if not matches_today:
        print("No matches today. Exiting.")
        return

    updated = False

    for event in cal.events:
        event_date = event.begin.date()
        match = next((m for m in matches_today if m["date"] == event_date), None)
        if not match:
            continue
        if "(" in event.name:
            continue  # already updated

        # Update SUMMARY only
        event.name = f"{event.name} ({match['score']})"
        updated = True

    if updated:
        with open("scotland.ics", "w") as f:
            f.writelines(cal)
        print("Updated scores.")
    else:
        print("No updates needed.")

if __name__ == "__main__":
    main()
