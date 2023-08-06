# remotecv_redis
Redis image loader for RemoteCV which is an OpenCV worker for facial and feature recognition

## Use with Thumbor
This loader is intended to be compatible with the Thumbor Storage plugin `tc_redis.storage.redis_storage` from [thumbor-community/redis](https://github.com/thumbor-community/redis).

## Config

Set the following enviroment variables before running RemoteCV:
```
## Redis server host to connect
## defaults to localhost
REMOTECV_REDIS_HOST = localhost

## Redis server port to connect
## defaults to 6379
REMOTECV_REDIS_PORT = 6379

## Redis database id to query
## defaults to 0
REMOTECV_REDIS_DATABASE = 0

## Redis serverpassword
#REMOTECV_REDIS_PASSWORD

## What user agent should we send when requesting images from HTTP fallback
## defaults to True
REMOTECV_REDIS_HTTP_FALLBACK = True

## What user agent should we send when requesting images from HTTP fallback
## defaults to RemoteCV/1
REMOTECV_REDIS_HTTP_USER_AGENT = "RemoteCV/1"
```

## Running RemoteCV

See [RemoteCV repo](https://github.com/thumbor/remotecv)
Or use the Docker container maintaned by [MinimalCompact](https://github.com/MinimalCompact/thumbor/tree/master/remotecv) as a base image...
