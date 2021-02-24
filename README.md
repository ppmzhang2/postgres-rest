# Redshift REST Service

An `aiohttp` based REST service on querying Amazon Redshift. The sample data can be found via the Redshift [Getting Started Guide](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-create-sample-db.html).

## Usage

After installing `docker engine` and `docker-compose`, build via `docker-compose.yml`:

```shell
docker-compose up
```

It is recommended to create a `systemd` script `/etc/systemd/system/docker-redshift-rest.service` to auto-start service on boot. Change the `WorkingDirectory` parameter with your project path:

```ini
[Unit]
Description=Docker Compose Application Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ec2-user/redshift-rest
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service to start automatically:

```shell
sudo systemctl enable docker-redshift-rest
```

## API

### Total Sales

Get total sales quantity at a given date.

* **Method**: `GET`
* **Example**: `/api/v1/sales?date=2008-01-05`
* **Arguments**
    + date: date string in `yyyy-mm-dd` format
* **Response Attributes**
    + sales: total sales on that day

## Reference

1. https://docs.aws.amazon.com/redshift/latest/dg/c_sampledb.html
2. http://mmariani.github.io/poss2016-aiohttp/
