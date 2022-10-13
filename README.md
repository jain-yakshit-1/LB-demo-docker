# LB-demo-docker

1) Build Docker image of Flask app server

 Go into app/ directory in terminal

 Let's build a two different docker image in which app_server is serving on two different ports 8031 and 8032

```
docker build -t app_server_01 --build-arg port_no=8031 .
```
```
docker build -t app_server_02 --build-arg port_no=8032 .
```


2) Run the app_server image in detached mode on port 8031 and 8032
```
docker run -d --name server_01 -p 8031:8031 app_server_01
```
```
docker run -d --name server_02 -p 8032:8032 app_server_02
```

Check if both the containers are running
```
docker ps -a
```
```
CONTAINER ID   IMAGE           COMMAND                  CREATED          STATUS          PORTS                    NAMES
206b49bc3b1c   app_server_02   "/bin/sh -c 'python …"   6 seconds ago    Up 5 seconds    0.0.0.0:8032->8032/tcp   server_02
026b1237114a   app_server_01   "/bin/sh -c 'python …"   23 seconds ago   Up 23 seconds   0.0.0.0:8031->8031/tcp   server_01
```


3) Find out the IP Address of both these containers using `docker inspect <container_id> | grep IPAddress`

```
docker inspect server_01 | grep IPAddress
```
```
docker inspect server_02 | grep IPAddress
```

Output must look like in this format
```
            "SecondaryIPAddresses": null,
            "IPAddress": "172.17.0.2",
                    "IPAddress": "172.17.0.2",
```


4) Collect this ips and change the config in `haproxy.cfg` present in haproxy/ folder
For eg:- 
```
backend application_nodes
    balance roundrobin # A load balancing strategy to serve client in round robin fashion.
    server server01 172.17.0.2:8031 weight 2 check
    server server02 172.17.0.3:8032 check
```

5) Build Docker image of HAProxy server

 Go into haproxy/ directory in terminal and type below command

```
docker build -t haproxy_lb .
```

6) Run the haproxy image on port 3030. We also expose the stats page on 3035.

```
docker run --rm --name haproxy_lb_0 -p 3030:3000 -p 3035:8404 haproxy_lb
```

7) Gitpod will show a pop-up to preview the page of port 3030 and 3035. Click on both the preview button.
   3035 URL will show the stats page
   3030 URL will show output from one of the app servers.

8) Stop server_01 using below command.
```
docker stop server_01
```
In the stats page, you will start seeing the red mark on server_01 after 10 sec.

9) Re-start server_01 using below command.
```
docker start server_01
```

In the stats page, you will start seeing the green mark on server_01 after 10 sec.

### Note

If you make any change in haproxy.cfg file and want to re-work then you will have to do the following steps.
```
i) Stop / Remove any existing haproxy container
ii) Remove the image of haproxy
iii) Re-build the haproxy Image
iv) Re-run the haproxy container as per the instructions specified previously.
```




## References

1) https://www.tecmint.com/name-docker-containers/#:~:text=How%20to%20Name%20a%20Docker,print%20the%20new%20container%20ID.
2) https://www.mend.io/free-developer-tools/blog/docker-expose-port/
3) https://foxutech.com/how-to-load-balancing-applications-with-haproxy-and-docker/
4) https://www.tutorialworks.com/container-networking/
5) https://vsupalov.com/docker-env-vars/
6) https://www.baeldung.com/ops/dockerfile-env-variable