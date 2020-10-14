

# Trade Snake
A classic situation: there you are, in space, empty cargo hold and some liquid capital burning a hole in your space pockets. 
What should you buy near your current location, and where should you sell it to maximize your profit? 
This is the forbidden knowledge the oligarchs of New Eden don't want you to know, and it has a provider: **Trade Snake**.

Trade Snake is a real-time trade identification and tasking system for EVE Online. 
Trade Snake uses Apache Pulsar to carry out data ingestion of market orders and stream processing of ETL tasks. 
Redis is used to cache static data required by the ingestion framework,
but also to identify and serve trades to connected clients.
Flask acts as a backend API for the ReactJS frontend.


![Banner 1](https://github.com/garden-of-delete/trade-snake/blob/master/images/1.gif)

The key design features of this project:
- Enterprise architecture can handle very high message velocity (5000 > new orders / sec).
- Parallelized ingestion framework uses Pulsar functions to implement a microservice architecture.
- Asynchronous and distributed trade-identification algorithm, while basic, is highly horizontally scalable.
- Redis implemented as a caching / state service for Pulsar functions, and as a cache for my API.

![Banner 3](https://github.com/garden-of-delete/trade-snake/blob/master/images/3.gif)

# Setup
During development this project configured on EC2 instances in AWS and required deployment of Apache Pulsar 2.6.1, Redis, Flask, Node, and all dependencies. The node layout used in this project (shown below) is only one possibility and can be adjusted to meet the needs of other projects.

Start by installing git on each machine (as needed), and pull this repo to your home directory. 

![node layout](https://github.com/garden-of-delete/trade-snake/blob/master/images/node_layout.png)

## AWS and Environment
1. Set up the AWS cluster. Either Ubuntu 18/20 or Amazon's AMI 1.x is fine. The node layout referenced by the .conf files included in this repository is:  
    - 3x t2.large Zookeeper nodes on `10.0.0.11`,`10.0.0.13`, and `10.0.0.6`  
    - 3x i3.xlarge Bookkeeper nodes on `10.0.0.4`,`10.0.0.8`, and `10.0.0.10`  
    - 3x c5n.large Broker nodes on `10.0.0.12`,`10.0.0.14`, and `10.0.0.7`  
    - 1x c5n.xlarge node for Redis, Flask, and Node.js on `10.0.0.5`  
    - 1x t2.micro Market producer node on `10.0.0.9`

2. Prepare the environment (All pulsar nodes. Special instructions for Redis/Flask/Node.js node below):  
    - Install Java JDK8 (OpenJDK8 will work unless you plan to use PulsarSQL/Presto, in which case you need Oracle JDK8)  
    - Install python3. Pulsar refers internally to '`python`, so link the python3 executable to the python command with: `sudo ln -sf /usr/bin/python3 /usr/bin/python`
    - Install pip, then use pip to get the `pulsar`,`pulsar-client`, and any dependancies.  
    - Additionally, use pip to install the `requests`, and `asyncio` packages on the market producer node.

## Apache Pulsar
1. Follow the Apache Pulsar 2.6.1 bare-metal setup [here](https://pulsar.apache.org/docs/en/deploy-bare-metal/). 
    - Care should be taken to follow the specific instructions for the Zookeeper, Bookkeeper, and Broker nodes.
    - Reference configurations can be found in the `/pulsar-config` subdirectory of this repository. They are:
        - `zookeeper.conf` (`apache-pulsar-2.6.1/conf/zookeeper.conf`): Zookeeper configuration
        - `bookkeeper.conf` (`apache-pulsar-2.6.1/conf/bookkeeper.conf): Bookie configuration
        - `broker.conf` (`apache-pulsar-2.6.1/conf/broker.conf): Broker configuration
        - `functions-worker.yml` (`apache-pulsar-2.6.1/conf/functions-worker.yml`): Functions worker configuration
2. Create pulsar functions.
    - Use .yml


## Redis
1. Download Redis [here](https://download.redis.io/releases/redis-6.0.8.tar.gz).
2. Configure Redis by editing the `Redis`

## Flask
    - Navigate to the backend API subdirectory (`cd ~/trade_snake/trade-snake-flask`)
    - Use pip to install `flask` and `flask-cors`
    - Run the backend API with `python application.py`

## Node + React
    - Navigate to the webclient subdirectory (`cd ~/trade_snake/trade-snake-gui`)
    - Install node.js (`sudo apt install nodejs`)
    - Install the Node Package Manager (`sudo apt install npm` followed by `npm i`)
    - Build the webapp (`npm run build`)
    - Run the webapp (`npm start`)

![Banner 2](https://github.com/garden-of-delete/trade-snake/blob/master/images/2.gif)

## Start-up
To start the system, first, the pulsar cluster should be started

# Future
I would like to explore better algorithms for trade identification that take advantage of Trade Snake's distributed archetecture. If that algorithm relies on trees, even better (gotta stick with the metaphor). 

This is an enterprise archetecture, and I would like to 

