## Sync Linear -> Asana

It's a one-way sync from Linear to Asana.

### Mapping of objects

| Linear    | Asana     |
| --------- | --------- |
| Team      | Team      |
| Milestone | Portfolio |
| Project   | Project   |
| Issue     | Task      |

### Testing locally

Create a virtual environment:

    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt

Run the sync:

    flask sync asana-projects "Q1 2022"

Create milestone portfolio:

    flask create milestone-portfolio "Q1 2022"

To run the quarterly update:

```
flask info asana-team-ids
flask info asana-custom-team-ids
flask info linear-team-ids
flask create milestone-portfolio "Q2 2022"
flask sync asana-projects "Q2 2022"

```
