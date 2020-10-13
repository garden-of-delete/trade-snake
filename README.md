

# Trade Snake
A classic situation: there you are, in space, empty cargo hold and some capital burning a hole in your space pockets. 
What should you buy near your current location, and where should you sell it to maximize your profit per unit distance? 
This is the forbidden knowledge the oligarchs of New Eden don't want you to know, and it has a provider: **Trade Snake**.  

Trade Snake is a real-time trade identification and tasking system for EVE Online. 
Trade Snake uses Apache Pulsar to carry out data ingestion, stream processing. 
Redis is used to cache static data required by the ingestion framework,
but also to identify and serve trades to connected clients.
Flask provides a web-facing API service, and the React (Node.js) provides a RESTful web client front-end.


![Banner 1](https://github.com/garden-of-delete/trade-snake/blob/master/images/1.gif)

The key design features of this project:
- Enterprise architecture can handle very high message velocity (5000 > new orders / sec).
- Parallelized ingestion framework uses Pulsar functions to implement a microservice architecture.
- Asynchronous and distributed trade-identification algorithm, while basic, is highly horizontally scalable.
- Redis implemented as a caching / state service for Pulsar functions, and as a cache for my API.

![Banner 3](https://github.com/garden-of-delete/trade-snake/blob/master/images/3.gif)

# Setup
## AWS and Environment
This is focused on a bare-metal deployment of Apache Pulsar 2.6.1 to an AWS cluster. 
1. Set up the AWS cluster. Either Ubuntu 18/20 or Amazon's AMI 1.x is fine. The node layout referenced by the .conf files included in this repository is:  
3x t2.large Zookeeper nodes on `10.0.0.11`,`10.0.0.13`, and `10.0.0.6`  
3x i3.xlarge Bookkeeper nodes on `10.0.0.4`,`10.0.0.8`, and `10.0.0.10`  
3x c5n.large Broker nodes on `10.0.0.12`,`10.0.0.14`, and `10.0.0.7`  
1x c5n.xlarge node for Redis, Flask, and Node.js on `10.0.0.5`  
1x t2.micro Market producer node on `10.0.0.9`


2. Prepare the environment (All pulsar nodes. Special instructions for Redis/Flask/Node.js node below):  
Install Java JDK8 (OpenJDK8 will do unless you plan to use PulsarSQL/Presto, in which case you need Oracle JDK8)  
Install python3. Link the python3 executable to the python command with: `sudo ln -s /usr/bin/python3 /usr/bin/python`
Install pip, then use pip to get the `pulsar`,`pulsar-client`, `redis`, and any dependancies. 
Additionally, install the `requests` package on the market producer node.

## Apache Pulsar
2. Follow the Apache Pulsar 2.6.1 bare-metal setup [here](https://pulsar.apache.org/docs/en/deploy-bare-metal/). 
- Note, this guide has specific instructions for the Zookeeper, Bookkeeper, and Broker nodes.
- Examples of the relevant configuration files for pulsar can be found in the `/pulsar-config` subdirectory of this repository.

3. Clone this repo into your home directory. Copy

## Redis

## Flask

## Node + React
![Banner 2](https://github.com/garden-of-delete/trade-snake/blob/master/images/2.gif)

