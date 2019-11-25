# horus_resteasy
(Cloud) Rest Service for RASA and Webhook for Dialogflow

- "/"
  - Rest Service Up?

- "/authenticate", methods=['POST']
  - checks if a user exists

- "/sick", methods=['POST']
  - Post that a user is sick

- "/sick", methods=['GET']
  - Get sickness entry for one user, for testing purpose only
- "/sick/all", methods=['GET']
  - Get all sickness entries, for testing purpose only
  
- "/dialogflow/requests", methods=['GET']
  - Look at the dialogflow requests in detail, for develoment purpose only
  
- '/dialogflow/webhook', methods=['GET', 'POST']
  - Entry point for all Dialogflow requests
