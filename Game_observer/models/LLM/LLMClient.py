import requests
import json

class LLMClient:
    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "llama3.1"

    def is_available(self):
        try:
            requests.get("http://localhost:11434", timeout=1)
            return True
        except:
            return False

    def analyze(self, log_text):

        base_prompt = "You are a soulslike game analyzer, please read the following logs about a gameplay, where" \
                      "every section is an action with a logo, the name of the action (like Stamina increased), the change itself" \
                      "as previous state -> current state and the exact time, when the action took place. I need you to write " \
                      "a small analysis, what could possibly happen in the game, for example if stamina is very low (like lower " \
                      "than 5-8%) at the moment and in the next moment the HP is decreased, the player may hit by an enemy due " \
                      "to lack of stamina to dodge, or if the players HP is very high (like more than 75-80%) and suddenly dies from one hit, " \
                      "the player may died from falling down or by a big hit (like from a boss) that he should dodge. Here are some crucial informations " \
                      "about the player status: the player's stamina decreases if the player use an attack, dodge, sprint or parry, the player's stamina " \
                      "increases if the player's stamina did not decrease recently. I want you to try to build up a scenario what could happen in the game, I need " \
                      "you to analyze every action found in the log and try to find coincidences. The log contains the following: "

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3.1",
                "prompt": base_prompt + log_text,
                "stream": True
            },
            stream=True
        )

        full_response = ""

        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))

                if "response" in data:
                    full_response += data["response"]

                if data.get("done"):
                    break

        return full_response