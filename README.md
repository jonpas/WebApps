# FERI-WebApps

Various web applications built at Web Technologies (slo. Spletne Tehnologije) using [Django](https://www.djangoproject.com/) and [Bootstrap](https://getbootstrap.com/), showcasing different systems and technologies in 4 distinct applications.


## Applications

### Todo

_`todo` (requires: `core`)_

Todo application featuring lists and items with deadlines and reminders, tags and dynamic completion status.

### Doodle (game)

_`doodle` (requires: `core`, `rooms`, login)_

Drawing game application featuring draw and guess chat-based multiplayer game with lobbies, login and statistics tracking, animations and sound effects.

### Ludo (game)

_`ludo` (requires: `core`, `rooms`, login)_

Turn-based game application featuring interactive multiplayer board game [ludo](https://en.wikipedia.org/wiki/Ludo_(board_game)) with lobbies, login, statistics tracking, animations and sound effects.

### Transporter

_`transport` (requires: `core`, login)_

Transportation helper application allowing registered users to offer transportation, search all offers using advanced search features, reservations, ability to track real-time GPS location of the transporter and grading.


## Helper Applications

### Core

_`core`_

Core systems application, providing login and registration services, base template with navigation bar, font page and linking all pages together.

### Rooms

_`rooms` (requires: `core`)_

Abstracted application used by `doodle` and `ludo`, providing room creation and joining services as well as live chat (messaging).


## Setup

- `$ python -m venv venv` (virtual environment)
- `$ source venv/bin/activate`
- `$ pip install -r requirements.txt` (`$ pip freeze > requirements.txt` to update dependencies)
    - _Installs [Django](https://www.djangoproject.com/) and additional packages._
