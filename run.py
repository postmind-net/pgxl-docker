__author__ = 'matthieu'

import argparse
from cStringIO import StringIO

from docker import Client
dcl = Client()


parser = argparse.ArgumentParser(description='PGXL startpack')
parser.add_argument('--ip', dest="ip", action="store_true", help="print container IP")
parser.add_argument('--ncontainers', dest="ncontainers", action="store", type=int, default=4, help="N containers")
parser.add_argument('--conf', dest='conf', action="store", type=str, help="generate configuration file")
parser.add_argument('--static', dest='static', action="store", type=str, default=None, help="generate configuration file")
parser.add_argument('--local', dest='local', action="store", type=int, default=0, help="local mode")
parser.add_argument('--gtmproxy', dest='gtmproxy', action="store_true", help="enable gtm proxies (distributed mode)")


args = parser.parse_args()

def get_containers(dcl):
    containers = dcl.containers()
    cts = []
    for c in containers:
        info = dcl.inspect_container(c)
        name = info['Name']
        ip = info['NetworkSettings']['IPAddress']
        cts.append({"name": name, "ip": ip})
    return cts

def get_conf(ips, local_mode=False, gtmproxy=False):
    servers = ["PGXL%d" %i for i in range(len(ips))]
    servers_ip = ips
    datanodes = servers
    datanodes_ip = servers_ip
    nnodes = len(datanodes)
    gtm_server = servers_ip[0]
    gtm_port = 20001
    #coord_server = datanodes_ip[0]
    conf = StringIO()
    conf.write("""
pgxcOwner=$USER
pgxcUser=$pgxcOwner
tmpDir=/tmp
localTmpDir=$tmpDir
configBackup=n
""")
    conf.write("""
gtmName=gtm
gtmMasterServer={0}
gtmMasterPort={1}
gtmMasterDir=$HOME/pgxc/nodes/gtm
gtmExtraConfig=none
gtmMasterSpecificExtraConfig=none
""".format(gtm_server, gtm_port))

    if gtmproxy:
        conf.write("""
gtmProxyDir=$HOME/pgxc/nodes/gtm_pxy
gtmProxy=y
gtmProxyNames=({0})
gtmProxyServers=({1})
gtmProxyPorts=({2})
gtmProxyDirs=({3})
gtmPxyExtraConfig=none
gtmPxySpecificExtraConfig=({4})
""".format(' '.join(["PROXY%d" %i for i in range(nnodes)]),
           ' '.join(datanodes_ip),
           ' '.join(["20001"] * nnodes),
           ' '.join(["$gtmProxyDir"] * nnodes),
           ' '.join(["none"] * nnodes)))

    if local_mode:
        conf.write("""
coordMasterDir=$HOME/pgxc/nodes/coord
coordSlaveDir=$HOME/pgxc/nodes/coord_slave
coordArchLogDir=$HOME/pgxc/nodes/coord_archlog
coordNames=(COORD)
coordPorts=(5432)
poolerPorts=(20010)
coordPgHbaEntries=(all)
coordMasterServers=(127.0.0.1)
coordMasterDirs=($coordMasterDir)
coordMaxWALSenders=(5)
coordSlave=n
coordExtraConfig=coordExtraConfig
cat > $coordExtraConfig <<EOF
#================================================
# Added to all the coordinator postgresql.conf
# Original: $coordExtraConfig
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
listen_addresses = '*'
max_connections = 100
log_filename = 'coordinator.log'
EOF
coordSpecificExtraConfig=(none)
coordExtraPgHba=none
coordSpecificExtraPgHba=(none)
""")
    else:
        conf.write("""
coordMasterDir=$HOME/pgxc/nodes/coord
coordSlaveDir=$HOME/pgxc/nodes/coord_slave
coordArchLogDir=$HOME/pgxc/nodes/coord_archlog
coordNames=({0})
coordPorts=({1})
poolerPorts=({2})
coordPgHbaEntries=({3})
coordMasterServers=({4})
coordMasterDirs=({5})
coordMaxWALsender=5
coordMaxWALSenders=({6})
coordSlave=n
coordExtraConfig=coordExtraConfig
cat > $coordExtraConfig <<EOF
#================================================
# Added to all the coordinator postgresql.conf
# Original: $coordExtraConfig
log_destination = 'stderr'
logging_collector = on
log_directory = 'pg_log'
listen_addresses = '*'
max_connections = 100
log_filename = 'coordinator.log'
EOF
coordSpecificExtraConfig=({7})
coordExtraPgHba=none
coordSpecificExtraPgHba=({7})
""".format(' '.join("COORD%d" %node for node in range(nnodes)),
           ' '.join(["5432"] * nnodes),
           ' '.join(["20010"] * nnodes),
           ' '.join(["all"] * nnodes),
           ' '.join(datanodes_ip),
           ' '.join("$coordMasterDir/%d" %i for i in range(nnodes)),
           ' '.join(["$coordMaxWALsender"] * nnodes),
           ' '.join(["none"] * nnodes)))
    conf.write("""
datanodeMasterDir=$HOME/pgxc/nodes/dn_master
datanodeSlaveDir=$HOME/pgxc/nodes/dn_slave
datanodeArchLogDir=$HOME/pgxc/nodes/datanode_archlog
primaryDatanode={0}
datanodeNames=({1})
datanodePorts=({2})
datanodePoolerPorts=({3})
datanodePgHbaEntries=(all)
""".format(datanodes[0], ' '.join(datanodes),
           ' '.join(map(str, range(21000, 21000 + nnodes))),
           ' '.join(map(str, range(22000, 22000 + nnodes)))))
    conf.write("""
datanodeMasterServers=({0})
datanodeMasterDirs=({1})
datanodeMaxWalSender=5
datanodeMaxWALSenders=({3})
datanodeSlave=n
datanodeExtraConfig=node.conf
datanodeSpecificExtraConfig=({2})
datanodeExtraPgHba=none
datanodeSpecificExtraPgHba=({2})
datanodeAdditionalSlaves=n
""".format(' '.join(ip for ip in datanodes_ip), ' '.join("$datanodeMasterDir/%d" %i for i in range(nnodes)),
           ' '.join(["none"] * nnodes),
           ' '.join(["$datanodeMaxWalSender"] * nnodes)))
    return conf

def get_haproxy(ips):
    conf = StringIO()
    conf.write("""
global
    log         127.0.0.1 local2 debug

    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    maxconn     4000
    user        haproxy
    group       haproxy
    daemon

    # turn on stats unix socket
    stats socket /var/lib/haproxy/stats

defaults
    timeout client 1m
    timeout server 1m
    timeout connect 10s

listen stats 0.0.0.0:9000
    mode http
    stats uri /stats

listen PGSQL 0.0.0.0:5432
    mode tcp
    option tcplog
    balance static-rr
""")

    for i in range(1, len(ips)):
        conf.write("""    server s%d %s:5432 check\n""" %(i, ips[i]))
    return conf

if args.ip:
    print get_containers(dcl)

if args.conf:
    local_mode = False
    gtmproxy = args.gtmproxy
    if args.local > 0:
        ips = ["127.0.0.1"] * args.local
        local_mode = True
	gtmproxy = False
    elif args.static == None:
	   from docker import Client

	   dcl = Client()
	   ctn = get_containers(dcl)
	   ips = [c["ip"] for c in ctn]
    else:
        ips = args.static.split(",")
    conf = get_conf(ips, local_mode, gtmproxy)
    with open("%s/pgxc_ctl.conf" %args.conf, "w+") as fp:
        fp.write(conf.getvalue())
    with open("%s/haproxy.cfg" %args.conf, "w+") as fp:
        fp.write(get_haproxy(ips).getvalue())
    conf.close()

