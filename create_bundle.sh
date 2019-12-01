# remove 
rootfs_src=~/tmp/alpine-bundle/rootfs/
tomcat_src=~/images/sample_tomcat/tomcat-9.0.29
rootfs_dst=~/images/sample_tomcat/alpine-bundle/rootfs/
p_rootfs_dst=~/images/sample_tomcat/alpine-bundle/
p_tomcat_dst=~/images/sample_tomcat/alpine-bundle/rootfs/

printf 'create bundle from %s to %s\n' $rootfs_src $rootfs_dst
# remove rootfs
sudo rm -r $rootfs_dst
sudo mkdir $rootfs_dst
echo 'old rootfs removed'

# create rootfs
sudo cp -r ${rootfs_src} ${p_rootfs_dst}
echo 'new rootfs copied'
sudo cp -r $tomcat_src $p_tomcat_dst
echo 'tomcat copied'

# change owner and mode
sudo chmod -R 755 $rootfs_dst
sudo chown 0:0 -R $rootfs_dst

