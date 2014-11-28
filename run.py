__author__ = 'matthieu'

from docker import Client
import argparse
from cStringIO import StringIO


parser = argparse.ArgumentParser(description='PGXL startpack')
parser.add_argument('--ip', dest="ip", action="store_true", help="print container IP")
parser.add_argument('--ncontainers', dest="ncontainers", action="store", type=int, default=4, help="N containers")
parser.add_argument('--conf', dest='conf', action="store", type=str, help="generate configuration file")

args = parser.parse_args()
dcl = Client()

def get_containers(dcl):
    containers = dcl.containers()
    cts = []
    for c in containers:
        info = dcl.inspect_container(c)
        name = info['Name']
        ip = info['NetworkSettings']['IPAddress']
        cts.append({"name": name, "ip": ip})
    return cts

def get_conf(dcl):
    ctn = get_containers(dcl)
    datanodes = ["PGXL%d" %i for i in range(len(ctn))]
    datanodes_ip = [c["ip"] for c in ctn]
    gtm_server = datanodes_ip[0]
    gtm_port = 20001
    coord_server = datanodes_ip[0]
    conf = StringIO()
    conf.write("""
pgxcOwner=pom
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
    conf.write("""
coordMasterDir=$HOME/pgxc/nodes/coord
coordSlaveDir=$HOME/pgxc/nodes/coord_slave
coordArchLogDir=$HOME/pgxc/nodes/coord_archlog
coordNames=(coord1)
coordPorts=(5432)
poolerPorts=(20010)
coordPgHbaEntries=(all)
coordMasterServers=({0})
coordMasterDirs=($coordMasterDir)
coordMaxWALsernder=0
coordMaxWALSenders=($coordMaxWALsernder)
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
""".format(coord_server))
    conf.write("""
datanodeMasterDir=$HOME/pgxc/nodes/dn_master
datanodeSlaveDir=$HOME/pgxc/nodes/dn_slave
datanodeArchLogDir=$HOME/pgxc/nodes/datanode_archlog
primaryDatanode={0}
datanodeNames=({1})
datanodePorts=({2})
datanodePoolerPorts=({3})
datanodePgHbaEntries=(all)
""".format(datanodes[0], ' '.join(datanodes), ' '.join(["21000"] * len(datanodes)), ' '.join(["21010"] * len(datanodes))))
    conf.write("""
datanodeMasterServers=({0})
datanodeMasterDirs=({1})
datanodeMaxWalSender=5
datanodeMaxWALSenders=({3})
datanodeSlave=n
datanodeExtraConfig=none
datanodeSpecificExtraConfig=({2})
datanodeExtraPgHba=none
datanodeSpecificExtraPgHba=({2})
datanodeAdditionalSlaves=n
""".format(' '.join(ip for ip in datanodes_ip), ' '.join("$datanodeMasterDir/%d" %i for i in range(len(datanodes))),
           ' '.join(["none"] * len(datanodes)), ' '.join(["$datanodeMaxWalSender"] * len(datanodes))))
    return conf

if args.ip:
    print get_containers(dcl)

if args.conf:
    conf = get_conf(dcl)
    with open(args.conf, "w+") as fp:
        fp.write(conf.getvalue())
    conf.close()

