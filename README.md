# horus_resteasy
(Cloud) Rest Service for RASA and Webhook for Dialogflow

## Interface

- "/"
  - Rest Service Up?
  
- "/sick", methods=['POST']
  - Post that a user is sick

- "/sick", methods=['GET']
  - Get sickness entry for one user, for testing purpose only
  
- "/sick/all", methods=['GET']
  - Get all sickness entries, for testing purpose only
  
- "/vacation/all", methods=['GET']
  - Get all vacation entries, for testing purpose only
  
- "/dialogflow/requests", methods=['GET']
  - Look at the Dialogflow requests in detail, for develoment purpose only
  
- '/dialogflow/webhook', methods=['GET', 'POST']
  - Entry point for all Dialogflow requests

- '/watson/webhook', methods=['POST']
  - Entry point for all Watson requests

- '/watson/requests', methods=['GET']
  - Look at the Watson requests in detail, for develoment purpose only

## Deployment

The following environment variables have to be set:

- `MONGODB_NAME`: name of the mongoDB user
- `MONGODB_PASS`: password of the mongoDB user
- `MONGODB_LINK`: link to the mongoDB server(s)
  (If using Atlas, use the Python 3.4 or later string and only the server part excluding
    '@', but including '/dbname')
- `FLASK_APP`: path to rest.py
- `FLASK_ENV`: flask environment (`development` or `production`)

Then start it with

```sh
flask run
```

To fill the database with dummy data, you can also execute `python insert_dummy_data.py`.
This still needs all of the `MONGODB_*` variables to be set correctly.

## Database

This api needs a mongoDB instance in the cloud with a database called `horus` and two
collections `user` and `sickness`.
