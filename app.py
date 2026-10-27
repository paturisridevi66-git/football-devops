
from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

# Demo match data. These are illustrative fixtures, not live results.
# Keep "home" and "away" for compatibility with the existing tests.
matches = [
    {
        "id": 1,
        "home": "Manchester City",
        "away": "Arsenal",
        "date": "2026-10-25",
        "time": "17:30",
        "status": "Completed",
        "home_score": 2,
        "away_score": 1,
    },
    {
        "id": 2,
        "home": "Liverpool",
        "away": "Chelsea",
        "date": "2026-10-25",
        "time": "20:00",
        "status": "Completed",
        "home_score": 1,
        "away_score": 1,
    },
    {
        "id": 3,
        "home": "Manchester United",
        "away": "Tottenham",
        "date": "2026-10-29",
        "time": "18:00",
        "status": "Upcoming",
        "home_score": None,
        "away_score": None,
    },
    {
        "id": 4,
        "home": "Newcastle United",
        "away": "Aston Villa",
        "date": "2026-10-30",
        "time": "19:30",
        "status": "Upcoming",
        "home_score": None,
        "away_score": None,
    },
]

# Illustrative league standings.
standings = [
    {
        "position": 1,
        "team": "Manchester City",
        "played": 10,
        "won": 8,
        "drawn": 1,
        "lost": 1,
        "points": 25,
    },
    {
        "position": 2,
        "team": "Arsenal",
        "played": 10,
        "won": 7,
        "drawn": 2,
        "lost": 1,
        "points": 23,
    },
    {
        "position": 3,
        "team": "Liverpool",
        "played": 10,
        "won": 7,
        "drawn": 1,
        "lost": 2,
        "points": 22,
    },
    {
        "position": 4,
        "team": "Chelsea",
        "played": 10,
        "won": 5,
        "drawn": 3,
        "lost": 2,
        "points": 18,
    },
    {
        "position": 5,
        "team": "Tottenham",
        "played": 10,
        "won": 5,
        "drawn": 2,
        "lost": 3,
        "points": 17,
    },
]

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Football Match Center</title>

    <style>
        :root {
            --background: #0b1410;
            --surface: #14221b;
            --green: #83f28f;
            --text: #f2f7f3;
            --muted: #9eafa3;
            --border: #2b4033;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            background: var(--background);
            color: var(--text);
            font-family: Arial, Helvetica, sans-serif;
            line-height: 1.5;
        }

        header {
            padding: 20px 6%;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            border-bottom: 1px solid var(--border);
            background: #101c15;
        }

        .brand {
            font-size: 1.15rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }

        .brand span {
            color: var(--green);
        }

        .demo-label {
            font-size: 0.75rem;
            color: var(--green);
            border: 1px solid #426b4a;
            border-radius: 20px;
            padding: 5px 10px;
            white-space: nowrap;
        }

        main {
            max-width: 1200px;
            margin: auto;
            padding: 34px 6% 60px;
        }

        .hero {
            margin-bottom: 28px;
        }

        .eyebrow {
            color: var(--green);
            font-size: 0.78rem;
            font-weight: bold;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        h1 {
            font-size: clamp(2rem, 5vw, 3.2rem);
            line-height: 1.1;
            margin: 10px 0;
            letter-spacing: -1.5px;
        }

        .subtitle,
        .muted {
            color: var(--muted);
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 14px;
            margin: 28px 0 38px;
        }

        .stat,
        .panel,
        .match-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
        }

        .stat {
            padding: 18px;
        }

        .stat strong {
            display: block;
            color: var(--green);
            font-size: 1.8rem;
        }

        .stat span {
            color: var(--muted);
            font-size: 0.85rem;
        }

        .section-heading {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 16px;
        }

        h2 {
            font-size: 1.35rem;
            margin: 0;
        }

        .filters {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 18px;
        }

        input,
        select {
            background: var(--surface);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 11px 13px;
            border-radius: 9px;
            font-size: 0.9rem;
        }

        input {
            flex: 1;
            min-width: 180px;
        }

        select {
            max-width: 100%;
        }

        .match-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 15px;
        }

        .match-card {
            padding: 20px;
        }

        .match-top {
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 22px;
        }

        .status {
            font-size: 0.72rem;
            font-weight: bold;
            border-radius: 20px;
            padding: 5px 9px;
        }

        .completed {
            color: var(--green);
            background: #213d29;
        }

        .upcoming {
            color: #f4d58b;
            background: #40351e;
        }

        .teams {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 12px;
        }

        .team {
            font-weight: bold;
            overflow-wrap: anywhere;
        }

        .team:last-child {
            text-align: right;
        }

        .score {
            font-size: 1.5rem;
            font-weight: 800;
            white-space: nowrap;
        }

        .match-meta {
            margin-top: 18px;
            padding-top: 12px;
            border-top: 1px solid var(--border);
            color: var(--muted);
            font-size: 0.82rem;
        }

        .section {
            margin-top: 42px;
        }

        .panel {
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            white-space: nowrap;
        }

        th,
        td {
            padding: 14px 16px;
            border-bottom: 1px solid var(--border);
        }

        th {
            color: var(--muted);
            font-size: 0.75rem;
            text-transform: uppercase;
        }

        tbody tr:last-child td {
            border-bottom: none;
        }

        td:first-child {
            color: var(--green);
            font-weight: bold;
        }

        .points {
            color: var(--green);
            font-weight: bold;
        }

        .empty {
            grid-column: 1 / -1;
            padding: 28px;
            text-align: center;
            color: var(--muted);
            background: var(--surface);
            border-radius: 12px;
        }

        footer {
            text-align: center;
            padding: 24px;
            color: var(--muted);
            border-top: 1px solid var(--border);
            font-size: 0.82rem;
        }

        @media (max-width: 650px) {
            header {
                padding: 16px 5%;
            }

            main {
                padding: 26px 5% 40px;
            }

            .stats {
                gap: 8px;
            }

            .stat {
                padding: 12px 9px;
            }

            .stat strong {
                font-size: 1.4rem;
            }

            .stat span {
                font-size: 0.72rem;
            }

            .match-grid {
                grid-template-columns: 1fr;
            }

            .match-card {
                padding: 16px;
            }

            .teams {
                gap: 8px;
            }
        }
    </style>
</head>

<body>
<header>
    <div class="brand">⚽ FOOTBALL <span>MATCH CENTER</span></div>
    <span class="demo-label">DEMO DATA</span>
</header>

<main>
    <section class="hero">
        <div class="eyebrow">Your football dashboard</div>
        <h1>Football Match Center</h1>
        <p class="subtitle">
            Explore match results, upcoming fixtures and league standings.
        </p>
        <p class="muted">
            Educational demo · Scores and standings are illustrative
        </p>
    </section>

    <section class="stats" aria-label="Dashboard summary">
        <div class="stat">
            <strong id="total-count">{{ matches|length }}</strong>
            <span>Total matches</span>
        </div>

        <div class="stat">
            <strong id="completed-count">
                {{ matches|selectattr("status", "equalto", "Completed")|list|length }}
            </strong>
            <span>Completed</span>
        </div>

        <div class="stat">
            <strong id="upcoming-count">
                {{ matches|selectattr("status", "equalto", "Upcoming")|list|length }}
            </strong>
            <span>Upcoming</span>
        </div>
    </section>

    <section>
        <div class="section-heading">
            <h2>Matches &amp; Fixtures</h2>
        </div>

        <div class="filters">
            <input
                id="search"
                type="search"
                placeholder="Search a team..."
                aria-label="Search teams"
            >

            <select id="status-filter" aria-label="Filter matches by status">
                <option value="all">All matches</option>
                <option value="completed">Completed</option>
                <option value="upcoming">Upcoming</option>
            </select>
        </div>

        <div class="match-grid" id="match-list">
            {% for match in matches %}
            <article
                class="match-card"
                data-status="{{ match.status|lower }}"
                data-teams="{{ (match.home ~ ' ' ~ match.away)|lower }}"
            >
                <div class="match-top">
                    <span class="status {{ match.status|lower }}">
                        {{ match.status }}
                    </span>
                    <span class="muted">Match {{ match.id }}</span>
                </div>

                <div class="teams">
                    <div class="team">{{ match.home }}</div>

                    {% if match.status == "Completed" %}
                    <div class="score">
                        {{ match.home_score }} - {{ match.away_score }}
                    </div>
                    {% else %}
                    <div class="score">VS</div>
                    {% endif %}

                    <div class="team">{{ match.away }}</div>
                </div>

                <div class="match-meta">
                    {{ match.date }} · {{ match.time }}
                </div>
            </article>
            {% endfor %}

            <div class="empty" id="no-results" hidden>
                No matches found. Try a different search or filter.
            </div>
        </div>
    </section>

    <section class="section">
        <div class="section-heading">
            <h2>League Standings</h2>
            <span class="demo-label">Sample table</span>
        </div>

        <div class="panel">
            <table>
                <thead>
                    <tr>
                        <th>Pos</th>
                        <th>Team</th>
                        <th>Played</th>
                        <th>Won</th>
                        <th>Drawn</th>
                        <th>Lost</th>
                        <th>Points</th>
                    </tr>
                </thead>

                <tbody>
                    {% for team in standings %}
                    <tr>
                        <td>{{ team.position }}</td>
                        <td>{{ team.team }}</td>
                        <td>{{ team.played }}</td>
                        <td>{{ team.won }}</td>
                        <td>{{ team.drawn }}</td>
                        <td>{{ team.lost }}</td>
                        <td class="points">{{ team.points }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </section>
</main>

<footer>
    Football Match Center · Built with Flask, Docker and GitHub Actions
</footer>

<script>
    const searchInput = document.getElementById("search");
    const statusFilter = document.getElementById("status-filter");
    const cards = Array.from(document.querySelectorAll(".match-card"));
    const noResults = document.getElementById("no-results");

    function filterMatches() {
        const query = searchInput.value.trim().toLowerCase();
        const status = statusFilter.value;
        let visible = 0;

        cards.forEach(card => {
            const matchesTeam = card.dataset.teams.includes(query);
            const matchesStatus =
                status === "all" || card.dataset.status === status;

            const show = matchesTeam && matchesStatus;
            card.hidden = !show;

            if (show) {
                visible++;
            }
        });

        noResults.hidden = visible !== 0;
    }

    searchInput.addEventListener("input", filterMatches);
    statusFilter.addEventListener("change", filterMatches);
</script>
</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(
        HTML_PAGE,
        matches=matches,
        standings=standings,
    )


@app.route("/api/matches")
def get_matches():
    return jsonify(matches)


@app.route("/health")
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)