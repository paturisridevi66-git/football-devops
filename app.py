
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

matches = [
    {
        "home": "Manchester City",
        "away": "Arsenal",
        "home_score": 2,
        "away_score": 1,
        "status": "Completed"
    },
    {
        "home": "Liverpool",
        "away": "Chelsea",
        "home_score": 1,
        "away_score": 1,
        "status": "Completed"
    },
    {
        "home": "Real Madrid",
        "away": "Barcelona",
        "home_score": None,
        "away_score": None,
        "status": "Upcoming"
    },
    {
        "home": "Bayern Munich",
        "away": "Borussia Dortmund",
        "home_score": None,
        "away_score": None,
        "status": "Upcoming"
    }
]

standings = [
    {"team": "Manchester City", "played": 10, "points": 24},
    {"team": "Arsenal", "played": 10, "points": 22},
    {"team": "Liverpool", "played": 10, "points": 21},
    {"team": "Chelsea", "played": 10, "points": 17}
]

PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Football Match Center</title>
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f1f5f9;
            color: #172033;
        }
        header {
            background: #123524;
            color: white;
            padding: 24px;
            text-align: center;
        }
        main {
            max-width: 900px;
            margin: 25px auto;
            padding: 0 16px;
        }
        h2 { color: #176b43; }
        .card {
            background: white;
            padding: 18px;
            margin-bottom: 12px;
            border-radius: 12px;
            box-shadow: 0 2px 8px #0000000d;
        }
        .match {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }
        .score { font-size: 20px; font-weight: bold; }
        .status { color: #64748b; font-size: 13px; }
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 12px; text-align: left; }
        th { background: #e2eee7; }
        tr:not(:last-child) td { border-bottom: 1px solid #e2e8f0; }
        footer { text-align: center; padding: 20px; color: #64748b; }
    </style>
</head>
<body>
    <header>
        <h1>⚽ Football Match Center</h1>
        <p>Matches, results and league standings</p>
    </header>
    <main>
        <h2>Match Center</h2>
        {% for match in matches %}
        <section class="card">
            <div class="match">
                <strong>{{ match.home }}</strong>
                <span class="score">
                    {% if match.home_score is not none %}
                        {{ match.home_score }} - {{ match.away_score }}
                    {% else %}
                        VS
                    {% endif %}
                </span>
                <strong>{{ match.away }}</strong>
            </div>
            <p class="status">{{ match.status }}</p>
        </section>
        {% endfor %}

        <h2>League Standings</h2>
        <section class="card">
            <table>
                <thead>
                    <tr><th>Team</th><th>Played</th><th>Points</th></tr>
                </thead>
                <tbody>
                    {% for team in standings %}
                    <tr>
                        <td>{{ team.team }}</td>
                        <td>{{ team.played }}</td>
                        <td>{{ team.points }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </section>
    </main>
    <footer>Football DevOps Project | Demo data for academic use</footer>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        PAGE, matches=matches, standings=standings
    )


@app.route("/api/matches")
def get_matches():
    return jsonify(matches)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
