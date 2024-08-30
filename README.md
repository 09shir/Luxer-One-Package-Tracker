# Luxer One Package Delivery Tracker

A package delivery tracker website specifically for Luxer One built in Angular for myself to keep track of deliveries in package locker.
- Utilizes Gmail API to create scheduled batch jobs in a Flask server to query automated package reminder emails into a PostgresSQL table for storage and retrieval
- Hosted frontend and backend servers in an AWS EC2 Ubuntu cloud VM with Nginx configured to proxy requests from the backend