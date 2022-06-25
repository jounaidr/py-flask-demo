## py-flask-demo
A demo project to explore the flask framework and Python webserver development. All server code in contained within ```server.py```, which consists of two endpoints. 

```GET /scores/x/``` will return the user and score at the ranking specified by x, and ```POST /scores/``` can be used to add/update a players score using the following format JSON payload:```{"name": "jeff", "score": 20}```. Caching is implemented within the GET endpoint, as sort is somewhat expensive, if cache is not used an error message will print to console.

The server can be ran using the following command: ```Python3 server.py```. Alternativly the server can be enabled as a systemd service using the service file. To do this, the following commands can be ran:

```cmd
> cp scores-server.service /lib/systemd/system/

> systemctl enable scores-server.service

> systemctl start scores-server.service
```

Once ran, the server can be accessed on the host ip and port set as variables in ```server.py```, by defualt it will be running on port 8888. A live demo of the server is running on the following host: [159.65.87.227:8888](http://159.65.87.227:8888/scores/1/)

### TODOs
- Add logging functionality (timestamp, logging level, log to file)
