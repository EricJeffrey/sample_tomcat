printf 'this operation will copy init.sh to rootfs/, continue?'
read a
sudo cp init.sh rootfs/
sudo runc run helo
