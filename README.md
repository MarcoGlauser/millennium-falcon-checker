# Millennium Falcon Checker
The purpose of this little project is to regularly check the LEGO online shop and
detect then the LEGO UCS Millennium Falcon is in stock.
When it is back in stock it sends a pushbullet notification.

## Requirements
* redis

## Configuration
The script can be configured by using environment variables.
The environment variable PUSHBULLET_API_KEY is required.


|Env Variable        |Description                                                           | Default                                             |
|--------------------|----------------------------------------------------------------------|-----------------------------------------------------|
|PUSHBULLET_API_KEY  | API key to use Pushbullet. Worker won't start without a valid api key|                                                     |
|URL                 | Defines the URL to regularly poll. change this to your country       | https://shop.lego.com/en-CH/Millennium-Falcon-75192 |
|REDIS_HOST          | Redis host to connect to                                             | localhost                                           |
|REDIS_PORT          | Redis port to connect to                                             | 6379                                                |
|REDIS_DB            | Redis db to connect to                                               | 0                                                   |

## Docker
You can also run it with docker.
The image is available at Dockerhub mglauser/millennium-falcon-checker.

Beware that when you link redis you have to set the environment variable REDIS_PORT.
Otherwise it will use the environment variable of the redis container.

## Usage
### Python
Clone repo and create venv
```python
huey_consumer checker.huey
```

### Docker
```
docker run -e PUSHBULLET_API_KEY=1234 -e REDIS_HOST=someredis.host -d mglauser/millennium-falcon-checker:latest
```