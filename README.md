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

```
    python3 -m venv ./venv
    source ./venv/bin/activate
    pip install -r requirements.txt
```

Create a `.env` file with all of the following values set :

```
FLASK_APP=src.app
FLASK_RUN_HOST=0.0.0.0
FLASK_RUN_PORT=5580
FLASK_ENV=development
LINEAR_PERSONAL_TOKEN=YOUR_PERSONAL_LINEAR_TOKEN
ASANA_PERSONAL_TOKEN=YOUR_PERSONAL_ASANA_TOKEN
```

Create the `Q1_2022` Linear milestone portfolio in Asana based on a template portfolio:

```
    flask create milestone-portfolio "Q1 2022"
```

When syncing for the first time, use the `asana-projects-by-template` to use the master portfolio template :

```
    flask sync asana-projects-by-template "Q1 2022"
```

The template portfolio should be set by changing `ASANA_PORTFOLIO_TEMPLATE_ID` in `config.py`.

Run a common sync:

```
    flask sync asana-projects "Q1 2022"
```

### Usage for a quarterly update

```
flask create milestone-portfolio "Q2 2022"
```

Add the output portfolio `gid` to the `LINEAR_MILESTONE_ASANA_PORTFOLIO` variable in `config.py`.

After that run :

```
flask sync asana-projects-by-template "Q2 2022"
```

### Cleaning up after testing features locally

```
flask delete milestone-portfolio "Q2 2022"
```

### Update team ids

#### Asana

You can find the team ids by running:

```
flask info asana-custom-team-ids
```

Update the team ids in sync in the `ASANA_CUSTOM_FIELD_TEAM` map `config.py` with the relevant ids.

#### Linear

Likewise, you can find the team ids by running:

```
flask info linear-team-ids
```

Update the team ids in sync in the `LINEAR_TEAMS` map `config.py` with the relevant ids.

### Updating the milestone portfolio members

To add any new users to a portfolio after creation:

Add any Asana user id to the `ASANA_PORTFOLIO_USERS_IDS` list in `config.py`

```
flask info update-milestone-portfolio-members "Q2 2022"
```
