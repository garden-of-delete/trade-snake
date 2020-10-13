#Trade Snake
A classic situation: there you are, in your space ship, empty cargo hold and some capital burning a hole in your space pockets. 
What should you buy near your current location, and where should you sell it to maximize your profit per unit distance? 
This is the forbidden knowledge the oligarchs of New Eden don't want you to know, and it has a provider: **Trade Snake**.  

Trade Snake is a real-time trade identification and tasking system for EVE Online. 
Trade Snake uses Apache Pulsar to carry out data ingestion, stream processing. 
Redis is used to cache static data required by the ingestion framework,
but also to identify and serve trades to connected clients.
Flask provides a web-facing API service, and I am using React (Node.js) as my front-end.

The key design features of this project:
- Enterprise architecture can handle very high message velocity (>5000 messages / sec)
- Parallelized ingestion framework uses Pulsar functions to implement a microservice architecture
- Asynchronous and distributed trade-identification algorithm, while basic, is highly horizontally scalable.
- Redis implemented as a caching / state service for Pulsar functions, and as a cache for my API.

###Features

###Future


###Setup
This is focused on a bare-metal deployment of Apache Pulsar 2.6.1 to an AWS cluster. 

First, follow the bare-metal setup [here](https://pulsar.apache.org/docs/en/deploy-bare-metal/).
Some notes:
- 
