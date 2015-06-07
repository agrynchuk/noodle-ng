#Dev doku on how to automatically generate appliance for multiple targets


You can use the following script to automatically generate vms for the targets: Virtualbox, VMWare, HyperV

```
#!/usr/bin/env sh

vmID="3fb768da-f38d-40a8-b5f9-f53545bf90a6"   #specifiy the vm (VBoxManage list vms)
hdID=`VBoxManage showvminfo $vmID --machinereadable | grep "Controller-ImageUUID-0-0" | sed 's/.*"="\(.*\)"/\1/'`
product="Noodle NG"
producturl="https://code.google.com/p/noodle-ng/"
vendor="Noodle NG Team"
vendorurl="https://code.google.com/p/noodle-ng/people/list"
version="1.0rc3"
suffix="Spaghetti_Aglio_et_Olio"
filename="Noodle-NG--$version--$suffix--appliance"  #target file name without extension
exportDir=`dirname $0`/export

echo "vmID: $vmID"
echo "hdID: $hdID"

echo "clean target dir"
mkdir -p $exportDir
touch $exportDir/somefile
rm $exportDir/*

echo "exporting VM:$vmID as ova"
VBoxManage export $vmID --vsys 0 --product "$product" --producturl "$producturl" --vendor "$vendor" --vendorurl "$vendorurl" --version "$version" --output $exportDir/$filename.ova

echo "exporting hd:$hdID as vhd"
VBoxManage clonehd $hdID --format VHD $exportDir/$filename.vhd
```