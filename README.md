# Numora

> Challenge your intuition. Master the number.

## 📌 Overview

Numora is a web-based number guessing game designed to combine
simple gameplay with a modern full-stack architecture.

The application provides multiple game modes, customizable number
ranges, higher/lower hints, scoring, player statistics, and
competitive gameplay.

Numora is a personal portfolio project built to demonstrate
practical full-stack development using Python, Flask, JavaScript,
SQLAlchemy, and SQLite.

## 🎯 Project Goals

Numora is being developed with the following goals:

- Build a complete web-based number guessing experience.
- Implement multiple gameplay modes with different game mechanics.
- Apply a modular and maintainable software architecture.
- Separate frontend, backend, game logic, and database responsibilities.
- Implement persistent player and game data using a relational database.
- Provide a foundation for statistics and game history.
- Demonstrate practical use of Python, Flask, JavaScript, SQLAlchemy, and Git.
- Develop the project incrementally as a portfolio-quality application.


## ✨ Features

### 🎮 Gameplay

- Single Player mode
- Two Player mode
- Two Player with computer-generated number
- Player vs Computer mode
- Customizable number range
- Higher/lower guessing hints
- Attempt-based scoring
- Rematch support

### 🤖 Intelligent Gameplay

- Computer opponent uses binary search in Player vs Computer mode.
- Backend controls game rules and game state.
- Secret numbers are kept on the backend rather than exposed to the frontend.

### 📊 Player & Game Data

- Player registration
- Persistent game records
- Player scores and attempts
- Game history
- Player statistics
- Win, loss, and draw tracking

### 🛠️ Application

- Modular Flask backend
- REST-style API endpoints
- SQLAlchemy database integration
- SQLite persistence
- Modular frontend templates
- Responsive web interface
- Git/GitHub version control

## 🎮 Game Modes

Numora provides multiple game modes, each designed around a different
gameplay experience.


### 👤 Single Player

The computer generates a secret number within the selected range.

The player repeatedly submits guesses and receives a higher/lower hint
until the correct number is found.

**Flow:**

1. Select the number range.
2. Start a Single Player game.
3. Submit a guess.
4. Receive a higher/lower hint.
5. Continue until the number is guessed.
6. Receive a score based on the number of attempts.


### 👥 Two Player — Player Chooses Number

Two players compete across two rounds.

**Round 1**

- Player 1 chooses the secret number.
- Player 2 attempts to guess it.
- Player 2 receives a score based on their attempts.

**Round 2**

- Player 2 chooses the secret number.
- Player 1 attempts to guess it.
- Player 1 receives a score based on their attempts.

The scores from both rounds are compared to determine the winner.


### 👥 Two Player — Computer Generates Number

The computer generates one secret number for both players.

Players take turns making guesses.

When one player correctly guesses the number, that player is marked
as finished, but the game continues so the other player can also
complete their attempt.

Once both players have guessed the number, their scores are compared
to determine the winner.

This ensures that one player's early correct guess does not
automatically end the competition.


### 🤖 Player vs Computer

In this mode, the player chooses the secret number and the computer
attempts to discover it.

The computer uses a **binary search strategy** rather than random
guessing.

After each computer guess, the player provides one of three responses:

- `Higher` — the secret number is higher than the computer's guess.
- `Lower` — the secret number is lower than the computer's guess.
- `Correct` — the computer has found the number.

The search range is progressively reduced after each response.

## 🛠️ Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Frontend | HTML5 | Page structure and UI |
| Styling | CSS3 | Responsive and modern interface |
| Client-side Logic | JavaScript | User interaction and API communication |
| Backend | Python | Application and game logic |
| Web Framework | Flask | Routing and REST-style API |
| ORM | SQLAlchemy / Flask-SQLAlchemy | Database interaction |
| Database | SQLite | Persistent game and player data |
| Version Control | Git | Source-code version control |
| Repository | GitHub | Remote repository and project hosting |

## 🏗️ System Architecture

Numora follows a modular full-stack architecture that separates the
user interface, API layer, game logic, and data persistence.

```text
┌──────────────────────────────┐
│          Frontend            │
│      HTML + CSS + JS         │
└──────────────┬───────────────┘
               │
               │ HTTP / API
               ▼
┌──────────────────────────────┐
│        Flask Backend         │
│       Routes / API Layer     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Game Service          │
│    Game State Management     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Game Engines          │
│                              │
│  Single Player               │
│  Two Player                  │
│  Two Player + Computer       │
│  Player vs Computer          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       SQLAlchemy ORM         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          SQLite              │
│                              │
│ Players                      │
│ Games                        │
│ Game Players                 │
│ Guesses                      │
└──────────────────────────────┘
```

## 📁 Project Structure

Numora follows a modular project structure where frontend, backend,
game logic, database models, and application services are separated
by responsibility.

```text
number-guessing-game/
│
├── app/
│   ├── __init__.py
│   │
│   ├── game/
│   │   ├── __init__.py
│   │   ├── base_game.py
│   │   ├── single_player.py
│   │   ├── two_player.py
│   │   ├── two_player_computer.py
│   │   └── player_vs_computer.py
│   │   
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── player.py
│   │   ├── game.py
│   │   ├── game_player.py
│   │   └── guess.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── game_routes.py
│   │   └── page_routes.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── game_service.py
│   │
│   ├── templates/
│   │   ├── index.html
│   │   ├── statistics.html
│   │   ├── history.html
│   │   │
│   │   └── games/
│   │       ├── single_player.html
│   │       ├── two_player.html
│   │       ├── two_player_choose.html
│   │       ├── two_player_computer.html
│   │       └── player_vs_computer.html
│   │
│   └── static/
│       ├── css/
│       │   ├── style.css
│       │   ├── dashboard.css
│       │   │
│       │   └── games/
│       │       ├── game.css
│       │       ├── single_player.css
│       │       ├── two_player.css
│       │       └── player_vs_computer.css
│       │
│       └── js/
│           ├── app.js
│           ├── statistics.js
│           ├── history.js
│           │
│           └── games/
│               ├── single_player.js
│               ├── two_player_choose.js
│               ├── two_player_computer.js
│               └── player_vs_computer.js
│
├── instance/
│   └── game.db
│
├── run.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 🧠 Game Logic

Numora uses separate game logic for each game mode. The game rules
are handled by the Python backend rather than by the frontend.

### 👤 Single Player

In Single Player mode:

1. The computer generates a secret number.
2. The player enters a guess.
3. Numora checks the guess against the secret number.
4. If the guess is too low, Numora tells the player to guess higher.
5. If the guess is too high, Numora tells the player to guess lower.
6. The game continues until the player guesses correctly.
7. The player's attempts are used to calculate the score.

### 👥 Two Player — Player Chooses Number

This mode is played in two rounds.

**Round 1:**
- Player 1 chooses the secret number.
- Player 2 tries to guess it.
- Player 2 receives a score based on their attempts.

**Round 2:**
- Player 2 chooses the secret number.
- Player 1 tries to guess it.
- Player 1 receives a score based on their attempts.

After both rounds, the two scores are compared and the player with
the higher score wins.

### 👥 Two Player — Computer Generates Number

In this mode, the computer generates one secret number.

Player 1 and Player 2 take turns guessing the number.

When a player guesses correctly, that player finishes their part of
the game. The other player continues guessing until they also find
the number.

After both players finish, their scores are compared to determine
the winner.

### 🤖 Player vs Computer

In this mode, the player chooses the secret number and the computer
tries to find it.

Instead of making random guesses, the computer uses **binary search**.

The computer starts with the complete number range and guesses the
middle number.

The player tells the computer whether the secret number is:

- **Higher** than the computer's guess
- **Lower** than the computer's guess
- **Correct**

Based on the response, the computer removes the numbers that cannot
be the answer and searches the remaining range.

This allows the computer to find the number efficiently.

## 🗄️ Database Design

Numora uses **SQLite** as its database and **SQLAlchemy** as the
Object-Relational Mapper (ORM).

The database stores information about players, games, participation,
and individual guesses.

### Database Tables

| Table | Purpose |
|---|---|
| `players` | Stores player information |
| `games` | Stores information about each game |
| `game_players` | Connects players with games and stores their game-specific data |
| `guesses` | Stores individual guesses made during games |

### 👤 Players

The `players` table stores basic information about each player.

Important fields include:

- Player ID
- Username
- Account creation time

### 🎮 Games

The `games` table stores the main information about each game.

It includes information such as:

- Game ID
- Game mode
- Number source
- Number range
- Game status
- Winner
- Start and end time

The table also stores game-state information required by specific
game modes.

### 👥 Game Players

The `game_players` table connects players to games.

It stores information such as:

- Which player participated in a game
- Their role in the game
- Their score
- Their number of attempts
- Whether they have finished

This table allows Numora to support games involving multiple players.

### 🎯 Guesses

The `guesses` table records individual guesses made during a game.

It stores:

- Game
- Player
- Guess value
- Result
- Attempt number
- Time of the guess

This information can later be used for game history, statistics,
and gameplay analysis.

### 🔗 Database Relationship

The basic relationship can be represented as:

```text
Player
   │
   │
   ▼
GamePlayer
   │
   │
   ▼
Game
   │
   │
   ▼
Guess
```

## 🔌 API

Numora uses Flask to provide API endpoints that allow the frontend
to communicate with the backend game system.

The frontend sends requests to the Flask API, and the backend
processes the request using the appropriate game logic and database
operations.

### API Flow

```text
Frontend
   │
   │ HTTP Request
   ▼
Flask API
   │
   ▼
Game Service
   │
   ▼
Game Engine
   │
   ▼
Database
   │
   ▼
JSON Response
   │
   ▼
Frontend
```

## 🎨 Frontend Architecture

Numora uses HTML, CSS, and JavaScript for the frontend.

The frontend is organized into separate files based on their
responsibilities rather than placing the entire application in a
single HTML file.

### Frontend Structure

```text
templates/
│
├── index.html
├── statistics.html
├── history.html
│
└── games/
    ├── single_player.html
    ├── two_player.html
    ├── two_player_choose.html
    ├── two_player_computer.html
    └── player_vs_computer.html


static/
│
├── css/
│   ├── style.css
│   ├── dashboard.css
│   │
│   └── games/
│       ├── game.css
│       ├── single_player.css
│       ├── two_player.css
│       └── player_vs_computer.css
│
└── js/
    ├── app.js
    ├── statistics.js
    ├── history.js
    │
    └── games/
        ├── single_player.js
        ├── two_player_choose.js
        ├── two_player_computer.js
        └── player_vs_computer.js
```

## 🏆 Scoring System

Numora currently uses an attempt-based scoring system.

Players receive a higher score when they find the secret number using
fewer attempts.

### Current Formula

```text
Base Score = 1000

Attempt Penalty = Attempts × 50

Final Score = max(Base Score − Attempt Penalty, 0)
```

### Example

If a player finds the number in 4 attempts:

```text
Base Score = 1000
Penalty = 4 × 50
Penalty = 200

Final Score = 1000 − 200
Final Score = 800
```

### Current Score Table

| Attempts | Score |
|---:|---:|
| 1 | 950 |
| 2 | 900 |
| 3 | 850 |
| 4 | 800 |
| 5 | 750 |
| 10 | 500 |
| 20 | 0 |


## 🧪 Testing & Validation

Numora's backend and game logic have been tested during development
to verify that the different game states, API operations, and scoring
behavior work as expected.

### Game Logic Testing

The following gameplay scenarios have been tested:

- Correct and incorrect guesses.
- Higher/lower hints.
- Attempt counting.
- Score calculation.
- Game completion.
- Two-player round progression.
- Two-player score comparison.
- Both players completing the computer-generated-number mode.
- Binary search behavior in Player vs Computer mode.
- Invalid game and player states.

### API Testing

The Flask API has been tested for:

- Player creation.
- Duplicate player validation.
- Game creation.
- Game state retrieval.
- Guess submission.
- Computer-generated guesses.
- Computer feedback.
- Two-player round creation.
- Player history retrieval.
- Player statistics retrieval.

### Database Validation

Database records have been checked to ensure that gameplay information
is correctly persisted, including:

- Players
- Games
- Game participants
- Attempts
- Scores
- Individual guesses
- Game status
- Winners

### Frontend Testing

The Single Player frontend has been tested for:

- Game creation from the home page.
- Loading a game using its game ID.
- Submitting guesses.
- Displaying higher/lower feedback.
- Displaying attempts and score.
- Completing a game.
- Rematch functionality.
- Navigation back to the home page.

Testing is being performed incrementally as new features are added.

## 📊 Current Development Status

Numora is currently under active development. The project is being
built incrementally, with the backend architecture and core game
logic being developed before completing all frontend game interfaces.

### ✅ Implemented

- Flask application structure
- SQLite database integration
- SQLAlchemy ORM
- Player model
- Game model
- Game-player relationship model
- Guess tracking model
- Modular game-engine architecture
- Single Player game logic
- Two Player game logic
- Two Player with computer-generated number logic
- Player vs Computer logic
- Binary search computer strategy
- Attempt tracking
- Basic scoring system
- Game state persistence
- Player game history API
- Player statistics API
- Modular frontend structure
- Single Player frontend
- Single Player API integration
- Single Player rematch flow
- Git and GitHub integration

### 🚧 In Progress

- Complete frontend implementation for all game modes
- Two Player user interface
- Two Player round-selection flow
- Two Player with computer interface
- Player vs Computer interface
- Complete frontend navigation
- Timer functionality
- Sound effects
- Theme support
- Final scoring system

### 🔮 Planned

- Improve the overall UI/UX
- Add more detailed statistics
- Improve game history presentation
- Add stronger validation and error handling
- Add automated testing
- Improve accessibility and responsiveness
- Refine the scoring algorithm
- Add additional gameplay improvements

The project status will be updated as development progresses.

## 🔀 Git & GitHub

Git is used for version control throughout the development of Numora.

The local project working directory is connected to a remote GitHub
repository, allowing changes to be tracked and synchronized throughout
development.

### Repository Setup

The local Git repository was initialized and connected to the GitHub
remote repository using:

```bash
git init
git remote add origin <repository-url>
git branch -M main
```

### Development Workflow

After making changes, the project can be updated using:

```bash
git status
git add .
git commit -m "Describe the change"
git push origin main
```

### Workflow

```text
Make changes
     ↓
git status
     ↓
git add .
     ↓
git commit
     ↓
git push origin main
     ↓
GitHub Repository
```


## 🔮 Future Enhancements

Numora is designed to be extended beyond its current implementation.
The following improvements are planned as development continues.

### 🎮 Gameplay

- Complete all game-mode interfaces.
- Improve the rematch experience across all modes.
- Add more gameplay customization options.
- Improve the overall game flow and user experience.

### ⏱️ Game Experience

- Add a game timer.
- Add sound effects and optional audio controls.
- Add dark and light themes.
- Improve animations and visual feedback.
- Further improve responsive design.

### 📊 Statistics & History

- Expand player statistics.
- Improve game history visualization.
- Add more detailed gameplay insights.
- Track additional performance metrics.

### 🧠 Game Intelligence

- Further improve the computer opponent experience.
- Add additional algorithm-based gameplay features.
- Explore different difficulty levels for computer opponents.

### 🧪 Quality & Engineering

- Add automated unit and integration tests.
- Improve API validation and error handling.
- Improve security and session management.
- Refine the scoring system using additional gameplay factors.
- Improve overall code quality and maintainability.

### 🚀 Deployment

- Prepare Numora for cloud deployment.
- Configure production-ready application settings.
- Explore a production database solution when required.