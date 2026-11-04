# Shop Platform

E-commerce for our stores. Customers buy in the web app, store staff manage the catalog.

## Architecture

The web frontend talks to the API. The API publishes order events to **Kafka**, and the notifications service consumes them to send email.
