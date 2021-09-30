# 3. Docker Support Engineer Test

# Machine Used

    AWS Light Sail Virtual Machine
    Version Ubuntu 20.04 LTS (GNU/Linux 5.4.0-1018-aws x86_64)

## Docker Install
Here are the commands to install the latest Docker

1. `sudo apt-get update`
2. `sudo apt-get install -y --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common`
4. `curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg`
5. `echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
6. `sudo apt-get update`
7. `sudo apt-get install docker-ce docker-ce-cli containerd.io`
8. `docker --version`
    - output: `Docker version 20.10.8, build 3967b7d`

    We have now installed the latest Docker ✅

## Docker-compose install

Here are the commands to install docker-compose version `1.25.3`

1. `sudo curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose`
2. `sudo chmod +x /usr/local/bin/docker-compose`
3. `docker-compose --version`
   - output: `docker-compose version 1.25.3, build d4d1b42b`

    We have now installed the latest docker-compose version `1.25.3` ✅

## Start a `postgres 12` instance using `docker-compose`

1. First we need to create a `docker-compose.yml` file and fill it to config our instance.

    1. First type `touch docker-compose.yml` to create an empty `docker-compose.yml` file
    2. Then type `vi docker-compose.yml` to edit that empty yml file
        1. Start editing by pressing `a`
        2. Then we are writing the docker-compose config like this:
            ![Image of screenshot](https://github.com/gh15hidalgo/gh_carto_test/blob/master/part_3/images/config_screenshot.png)
        3. Finally to save and quit, press `esc` key, press `:`, type `x` and press `enter`.
            - output: `"docker-compose.yml" 12L, 270C written`
        4. To check if you edited the yml correctly type `cat docker-compose.yml` 
            - output
```
        version: '3.7'
        services:
           postgres:
              image: postgres:10.5
              volumes:
                - ./data/db:/var/lib/postgresql/data
              environment:
                - POSTGRES_DB=postgres
                - POSTGRES_USER=postgres
                - POSTGRES_PASSWORD=postgres
        volumes:
           data_volume:
```

2. Then start the instance by pressing `sudo docker-compose up -d` which will run the postgres instance on detached mode to be able to keep using the terminal.
    - output
```
    ubuntu@ip-172-26-6-187:~$ sudo docker-compose up -d
    Creating network "ubuntu_default" with the default driver
    Creating volume "ubuntu_data_volume" with default driver
    Pulling postgres (postgres:10.5)...
    10.5: Pulling from library/postgres
    f17d81b4b692: Pull complete
    c1f213be5edb: Pull complete
    9c79723dc510: Pull complete
    603a66804109: Pull complete
    b4f1b901e523: Pull complete
    99d9650419de: Pull complete
    02d87bb25bad: Pull complete
    333a24caa91e: Pull complete
    9cab7935ece2: Pull complete
    5977bf28967d: Pull complete
    74ddd26cf783: Pull complete
    07b76fcb42dd: Pull complete
    7da7962ee038: Pull complete
    0ddc5f8e0873: Pull complete
    Digest: sha256:e19acdab213d6318565a6da5fb824ca5161e99fe63dbc37036557aacb35fae51
    Status: Downloaded newer image for postgres:10.5
    Creating ubuntu_postgres_1 ... done
```

We have successfully started the instance 🚀
    

## Check docker volume location

Now that the instance is up we need to check where the location for the instance's volume data will be stored.

Typing the command `sudo docker volume ls` you can see each volumes' name.
  - output
```
    DRIVER    VOLUME NAME
    local     ubuntu_data_volume
```

Then taking that volume name we run the command `sudo docker volume inspect VOLUME_NAME` to get the location.

Which in our case would be `sudo docker volume inspect ubuntu_data_volume`
- output

```
    ubuntu@ip-172-26-6-187:~$ sudo docker volume inspect ubuntu_data_volume
    [
        {
            "CreatedAt": "2021-09-30T18:59:19Z",
            "Driver": "local",
            "Labels": {
                "com.docker.compose.project": "ubuntu",
                "com.docker.compose.version": "1.25.3",
                "com.docker.compose.volume": "data_volume"
            },
            "Mountpoint": "/var/lib/docker/volumes/ubuntu_data_volume/_data",
            "Name": "ubuntu_data_volume",
            "Options": null,
            "Scope": "local"
        }
    ]
```
This is the location of the volume 👆

## Stop the instance
To stop the instance we need to find the `CONTAINER ID` and then stop it.

1. To find the CONTAINER ID of the instance we need to use the command `sudo docker ps`. This command list out all running containers.
    ```
    CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS         PORTS      NAMES
    ada8c5617cd5   postgres:10.5   "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   5432/tcp   ubuntu_postgres_1
    ```
2. Now that we have the name of the instance we can use the `sudo docker stop CONTAINER_ID`.
   In my case it would be `sudo docker stop 7427864121e0`
3. Now let us run `sudo docker ps -a` to check for all instances including spoted ones.
```
CONTAINER ID   IMAGE           COMMAND                  CREATED         STATUS                      PORTS     NAMES
ada8c5617cd5   postgres:10.5   "docker-entrypoint.s…"   4 minutes ago   Exited (0) 33 seconds ago             ubuntu_postgres_1
```

Yep this instance has been stopped 🛑 as seen by the STATUS column


### Bonus Track

However, let us start up this instance to find the postgres db port plus version.

We run `sudo docker start ada8c5617cd5` to start the instance again.

1. Then let us enter this postgres instance through psql using `docker exec -it CONTAINER_NAME psql -U USER_NAME`

    For us it would be `docker exec -it ubuntu_postgres_1 psql -U postgres -W postgres`
    - output
    ```
    ubuntu@ip-172-26-6-187:~$ docker exec -it ubuntu_postgres_1 psql -U postgres
    Got permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock: Get "http://%2Fvar%2Frun%2Fdocker.sock/v1.2
    4/containers/ubuntu_postgres_1/json": dial unix /var/run/docker.sock: connect: permission denied
    ubuntu@ip-172-26-6-187:~$ sudo docker exec -it ubuntu_postgres_1 psql -U postgres
    psql (10.5 (Debian 10.5-2.pgdg90+1))
    Type "help" for help.
    ```
2. Check for the postgres port using sql
    We are going to check the postgres settings specifically for the port via `SELECT * FROM pg_settings WHERE name = 'port';`.
    - output
```
    postgres=# SELECT * FROM pg_settings WHERE name = 'port';
 name | setting | unit |                       category                       |                short_desc                | extra_desc |  context   | vartype | source  | min_val | max_val |
 enumvals | boot_val | reset_val | sourcefile | sourceline | pending_restart 
------+---------+------+------------------------------------------------------+------------------------------------------+------------+------------+---------+---------+---------+---------+
----------+----------+-----------+------------+------------+-----------------
 port | 5432    |      | Connections and Authentication / Connection Settings | Sets the TCP port the server listens on. |            | postmaster | integer | default | 1       | 65535   |
          | 5432     | 5432      |            |            | f
(1 row)
```
Looking at the column `port` the database is using port `5432`

3. Then check the postgresql version using `SELECT version();`, which is `PostgreSQL 10.5`. That correctly matches what we configed in our docker-compose.yml file.
```
postgres=# SELECT version();
                                                             version                                                              
----------------------------------------------------------------------------------------------------------------------------------
 PostgreSQL 10.5 (Debian 10.5-2.pgdg90+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 6.3.0-18+deb9u1) 6.3.0 20170516, 64-bit
(1 row)
```

Now let us get out of the instance via `\q` command


## Destroy any trace of Docker instances 🔥

Finally, let us remove any trace of this instance.


1. To remove the volume, image, and instance we will use the command `sudo docker-compose down -v --rmi all`.
    * `down`: Removes the instance
    * `-v` : Will remove all the volume data of the instance
    * `-rmi all` : Remove all images used by any service like postgres
   - output
`
    ubuntu@ip-172-26-6-187:~$ sudo docker-compose down -v --rmi all
    Stopping ubuntu_postgres_1 ... done
    Removing ubuntu_postgres_1 ... done
    Removing network ubuntu_default
    Removing volume ubuntu_data_volume
    Removing image postgres:10.5
`

2. Let us check the status of all instances again with `sudo docker ps -a`.
   If you get the output below then the instance should gone
```
    ubuntu@ip-172-26-6-187:~$ sudo docker ps -a
    CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```
  Now let us check if the volume of the instance is also gone via the command `sudo docker volume ls` that shows all volumes for every instance.
    - output
    ```
    DRIVER    VOLUME NAME
    ```
3. Finally let us remove all the files/directories created from `sudo docker-compose up -d` command like `data` and `docker-compose.yml`.
    Here using `ls` we see these files
    - output:
    ```
    ubuntu@ip-172-26-6-187:~$ ls
    data  docker-compose.yml
    ```
    1. We will remove the `data` directory via `sudo rm -rf data` since data is a directory. 
    2. To remove `docker-compose.yml` we will use ``sudo rm docker-compose.yml``.

Finally, another `ls` to double check.
- output:
        ```
        ubuntu@ip-172-26-6-187:~$ ls
        ubuntu@ip-172-26-6-187:~$
        ```
        
We have successful deleted all traces of the instance 🔥

