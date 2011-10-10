#!/usr/bin/env sh

crawler="134.93.48.211"
frontend="134.93.48.204"
privatekey="$HOME/.ssh/nag"
keydir=`dirname $0`/public_keys
configdir=`dirname $0`/cfg

function deploy {
	server=$1
	echo "deploying config to $server"
	echo "=================================="
	scp -i $privatekey $keydir/authorized_keys2 root@$server:.ssh/authorized_keys2
	rsync -Hrvz -e "ssh -i $privatekey" $configdir/ root@$server:/
	#restart sshd
	ssh -i $privatekey -l root $server "/etc/init.d/sshd restart"
}


echo "generating authorized_keys2"
touch $keydir/authorized_keys2
rm $keydir/authorized_keys2
for key in $(find $keydir -name "*.pub"); do
	cat $key >> $keydir/authorized_keys2
done

deploy $crawler
deploy $frontend

# some handy work on crawler and server ...
ssh -i $privatekey -l root $crawler "chkconfig httpd off && /etc/init.d/httpd stop"
ssh -i $privatekey -l root $frontend "chkconfig httpd on && /etc/init.d/httpd restart"

ssh -i $privatekey -l root $frontend "rm -f /etc/cron.d/99noodle-crawler"
