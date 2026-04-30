import json
import os
from typing import Any, Dict, List, Tuple

import openai

SUPPORTED_SPORTS = {
    "football": {
        "Arsenal": 88,
        "Chelsea": 84,
        "Liverpool": 90,
        "Manchester City": 93,
        "Manchester United": 80,
        "Real Madrid": 92,
        "Barcelona": 91,
        "Bayern Munich": 94,
    },
    "basketball": {
        "Lakers": 89,
        "Warriors": 92,
        "Bucks": 88,
        "Nets": 86,
        "Celtics": 90,
    },
}


def get_team_rating(sport: str, team: str) -> int:
    return SUPPORTED_SPORTS.get(sport, {}).get(team, 50)


def compute_prediction(team_a: str, team_b: str, sport: str) -> Tuple[str, str]:
    rating_a = get_team_rating(sport, team_a)
    rating_b = get_team_rating(sport, team_b)
    if rating_a == rating_b:
        probability = 0.5
    else:
        probability = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    winner = team_a if probability >= 0.5 else team_b
    confidence = int(max(50, min(99, round(abs(probability - 0.5) * 200 + 50))))
    return f"{winner} Win", f"{confidence}%"


def generate_ai_prediction(team_a: str, team_b: str, sport: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY must be set for AI predictions")

    openai.api_key = api_key
    prompt = (
        "You are a sports analyst. Given a matchup, return a JSON object with keys: "
        "prediction, confidence, analysis, and key_factors. "
        "Use the teams and sport provided. "
        "Do not include any markdown or explanation outside of the JSON object."
    )
    user_message = (
        f"Matchup: {team_a} vs {team_b}\nSport: {sport}\n"
        "Provide a short prediction and supporting factors."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    text = response.choices[0].message.content.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # fallback for minor formatting issues
        text = text[text.find("{") : text.rfind("}") + 1]
        return json.loads(text)
