printf 'build prestart.cpp ? (y/n)'
read a
if [[ $a == 'y' ||  $a == 'Y' || $a == '' ]]
then
    g++ -Wall -o prestart.out hooks/prestart.cpp
fi
printf 'copy init.sh to rootfs/ ? (y/n)'
read a
if [[ $a == 'y' ||  $a == 'Y' || $a == '' ]]
then
    sudo cp init.sh rootfs/
fi
echo 'starting <helo>'
sudo runc run helo
