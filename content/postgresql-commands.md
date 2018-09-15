---
date: 2018-05-24
location: Kathmandu, Nepal
title: Postgres Commands
description: List of postgres commands that I always end up having to look up
draft: false
code: true
---

Since I primarily [il:about-keshab-paudel:use Django], I don't have
the need to write SQL or even use the database shell very often. But
once in a while there comes a time when I have to resort to using the
dear old `pgshell`.


## Administration

### Starting pgshell

```bash

# switch to `postgres` user
sudo su postgres

# just run
psql

# OR: with Django project's manage.py for database specific task
./manage.py dbshell

```

### Info about the tables

#### List of columns and their data types of a table.

If the schema is anything other than the default one, append `AND
table_schema = '<schema_name>'` at the end of the query.

```sql
SELECT column_name, data_type FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = '<table_name>';
```

The result will be something like this:

```
 id                   | integer
 password             | character varying
 last_login           | timestamp with time zone
```

#### Find the primary key

To know the primary key of a table:

```sql
SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = '<tablename>'::regclass
AND    i.indisprimary;
```


## In Docker

If there's a need to run a version of postgresql that is not in the
system packages repository then Docker is probably the best option.


### Pull and run the image

Pull the required image, see docker hub page for
[postgres](https://hub.docker.com/_/postgres/) and find the version
you desire.

```bash
docker run --name <FANCY_NAME> -e POSTGRES_USER=<USER> -e POSTGRES_PASSWORD=<PASSWORD> -d -p 5433:5432 postgres:9.6.9
```

* `--name <FANCY_NAME>`: Something unique, short and descriptive to
  refer to the instance of the created container.
* `-e POSTGRES_USER=<USER>`: If provided, the user will be created.
* `-e POSTGRES_PASSWORD=<PASSWORD>`: Password for the user.
* `-d`: Detach the container, i.e. run in the background
* `-p 5433:5432`: Postgres runs on `5432` by default, we are mapping
  `5433` on host to the `5432` on the container because `5432` might
  be already in use on the host system.
* `postgres:9.6.9`: Name of the image.


### Restore from other instances

Create a dump by running this command:


```bash
pg_dumpall -h localhost -p 5432 -U postgres -c >  "/home/something/backup.sql"
```

To restore, run the following command:

```bash
cat /home/something/backup.sql | docker exec -i <FANCY_NAME> psql -Upostgres
```

* `<FANCY_NAME>`: This is the name of the container.


## Read

* [pg_dump and restore a db in a container](http://durandom.de/docker/postgres/2016/12/20/pg_dump/)
* [Backup, restore postgres in docker container](https://gist.github.com/gilyes/525cc0f471aafae18c3857c27519fc4b)
* [Dockerized Postgresql Development Environment](https://ryaneschinger.com/blog/dockerized-postgresql-development-environment/)
* [Backup & Restore Database in PostgreSQL (pg_dump,pg_restore)](https://www.mkyong.com/database/backup-restore-database-in-postgresql-pg_dumppg_restore/)
* [Dump and restore of PostgreSQL: version compatibility FAQ](https://pgolub.wordpress.com/2013/11/19/dump-and-restore-of-postgresql-version-compatibility-faq/)
* [Gist: PostgreSQL command line cheatsheet](https://gist.github.com/Kartones/dd3ff5ec5ea238d4c546)
* [Jason Meridth: PostgreSQL Command Line Cheat Sheet](https://blog.jasonmeridth.com/posts/postgresql-command-line-cheat-sheet/)
* [Retrieve primary key columns](https://wiki.postgresql.org/wiki/Retrieve_primary_key_columns)
