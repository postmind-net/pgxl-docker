### SSH USER KEY FOR LOCAL SSH
mkdir pom/.ssh
ssh-keygen -t rsa -C "pom@pgxl" -f pom/.ssh/id_rsa -q -N ""
cat pom/.ssh/id_rsa.pub >> pom/.ssh/authorized_keys

