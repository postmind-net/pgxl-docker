### SSH USER KEY FOR LOCAL SSH
ssh-keygen -t rsa -C "pom@pgxl" -f pom/.ssh/id_rsa -q -N ""
cp pom/.ssh/id_rsa.pub pom/.ssh/authorized_keys

