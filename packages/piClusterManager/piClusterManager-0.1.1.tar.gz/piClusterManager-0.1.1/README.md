# piClusterManager
Open source Manager for PI clusters

## install
```sh
pip3 install piClusterManager
```
## fisrt run
you can setup cluster manager only when you have **new instalation of raspberian**, **not change passwords** and  **enabled SSH**

then you can write
```sh
picluster --setup
```

**for everything to work properly, you must have runned command ```piclusterdeamon``` at all nodes**

## usage
```sh
usage: picluster [-h] [--setup] [--update] [--dockerSwarmSetup] [--passwd]
                 [--execute EXECUTE]

PI Cluster manager

optional arguments:
  -h, --help          show this help message and exit
  --setup             setup pi cluster
  --update            make update && upgrade in all nodes
  --dockerSwarmSetup  setup docker swarm in cluster
  --passwd            change password of cluster (same password in all nodes)
  --execute EXECUTE   execute command in all nodes (--execute="rm -rf
                      /home/pi/example")

```
