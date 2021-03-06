# PostgreSQL REST Service

An `aiohttp` based REST service on querying PostgreSQL. The sample data can be found [here](https://www.dropbox.com/s/cl08mf38i222fio/postgres-rest-tickitdb.zip?dl=0), modified from the Amazon Redshift [Getting Started Guide](https://docs.aws.amazon.com/redshift/latest/gsg/rs-gsg-create-sample-db.html).

## Usage

After installing `docker engine` and `docker-compose`, build via `docker-compose.yml`:

```shell
docker-compose up
```

It is recommended to create a `systemd` script `/etc/systemd/system/docker-postgres-rest.service` to auto-start service on boot. Change the `WorkingDirectory` parameter with your project path:

```ini
[Unit]
Description=Docker Compose Application Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ec2-user/postgres-rest
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

Enable the service to start automatically:

```shell
sudo systemctl enable docker-postgres-rest
```

## API

### Config - Initialization

Initializing DB by recreating all tables.

* **Method**: `POST`
* **Example**: `/api/v1/config/init`
* **Response Attributes**
    + message: "success" if succeeded

### Config - Load

Loading into DB data in the text files.

* **Method**: `POST`
* **Example**: `/api/v1/config/load`
* **Response Attributes**
    + message: "success" if succeeded

### Config - Count

Couting records in tables.

* **Method**: `GET`
* **Example**: `/api/v1/config/count/{table}`
* **Arguments**
    + table: table name
* **Response Attributes**
    + result: number of records in that table

### Summary - Total Sales

Get total sales quantity at a given date.

* **Method**: `GET`
* **Example**: `/api/v1/summary/sales?date=2008-01-05`
* **Arguments**
    + date: date string in `yyyy-mm-dd` format
* **Response Attributes**
    + sales: total sales on that day

## Reference

1. https://docs.aws.amazon.com/redshift/latest/dg/c_sampledb.html
2. http://mmariani.github.io/poss2016-aiohttp/
