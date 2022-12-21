# https://github.com/cherkavi/cheat-sheet/blob/master/microsoft-applications.md#teams-send-message
def send_teams_message_with_text(message: str):
        response: Response = requests.post(
                        f"https://graph.microsoft.com/v1.0/teams/{TEAMS_TEAM_ID}/channels/{TEAMS_CHANNEL_ID}/messages",
                                json={"body": {"content": f"{message}"}},
                                        headers={"Authorization": f"Bearer {TEAMS_TOKEN}", "Content-type": "application/json"})
            return response.content
