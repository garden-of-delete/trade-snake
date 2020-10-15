# Trade Snake
A classic situation: there you are, in space, empty cargo hold and some liquid capital burning a hole in your space pocket. 
What should you buy near your current location, and where should you sell it to maximize your profit? 
This is the forbidden knowledge the oligarchs of New Eden don't want you to know, and it has a provider: **Trade Snake**.

Trade Snake is a real-time trade identification and tasking system for EVE Online. 
Trade Snake uses Apache Pulsar to carry out data ingestion of market orders and stream processing of ETL tasks. 
Redis is used to cache static data required by the ingestion framework,
but also to identify and serve trades to connected clients.
Flask acts as a backend API for the ReactJS web client.


![Banner 1](https://github.com/garden-of-delete/trade-snake/blob/master/images/1.gif)

The key design features of this project:
- Enterprise architecture can handle very high message velocity (5000 > new orders/sec).
- Parallelized ingestion framework uses Pulsar functions to implement a microservice architecture.
- Asynchronous and distributed trade-identification algorithm, while basic, is highly horizontally scalable.
- Redis implemented as a caching / state service for Pulsar functions, and as a cache for the API.

![Banner 3](https://github.com/garden-of-delete/trade-snake/blob/master/images/3.gif)

# Related Repositories
### [Trade Snake React Webapp](https://github.com/garden-of-delete/trade-snake-react)  
### [Trade Snake Flask Backend API](https://github.com/garden-of-delete/trade-snake-flask)

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
2. Create pulsar functions using the pulsar-admin cli. Each function in the pipeline can be found at `~/trade_snake/trade-snake-scripts/pf-*.py`. 
   An example:  
   ```
   ~/apache-pulsar-2.6.1/bin/pulsar-admin functions create \`  
   --tenant public \
   --namespace default \
   --name pyexclamation \
   --py exclamation.py \
   --classname exclamation.ExclamationFunction \
   --inputs persistent://public/default/raw-orders \
   --output persistent://public/default/exclamation-output
   ```

## Redis
Follow these steps:
    1. Follow the redis setup instructions [here](https://redis.io/topics/quickstart)  

## Flask
Follow these steps:
    1. Navigate to the backend API subdirectory (`cd ~/trade_snake/trade-snake-flask`)
    2. Use pip to install `flask` and `flask-cors`
    3. Run the backend API with `python application.py`

## Node + React
Follow these steps:
    1. Navigate to the webclient subdirectory (`cd ~/trade_snake/trade-snake-gui`)
    2. Install node.js (`sudo apt install nodejs`)
    3. Install the Node Package Manager (`sudo apt install npm` followed by `npm i`)
    4. Build the webapp (`npm run build`)
    5. Run the webapp (`npm start`)

![Banner 2](https://github.com/garden-of-delete/trade-snake/blob/master/images/2.gif)

## Start-up
To start the system:
1. Start the redis/node/flask node. Run `~/trade_snake/redis-config/redis-static-data-load.py` to load the eve online static data.
2. Start the pulsar nodes and run pulsar services (Zookeeper nodes -> Bookie Nodes -> Broker Nodes).
3. Start the market producer node. Run `~trade_snake/trade-snake-scripts/eve-market-producer.py` to start pulling orders from Eve Online.
4. Start Flask and React the servers as described in the final step of the "Node + React" and "Flask" sections above.
