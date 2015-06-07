Since Noodle NG requires quite some time and knowledge to setup from srcatch we want to provide you a fast and simple way.

## How To Get Started ##
[Download](http://www.staff.uni-mainz.de/hwinther/noodle/) the latest appliance image. You will get an [Open Virtualization Format](http://en.wikipedia.org/wiki/Open_Virtualization_Format) package. Import the package into the virtualization software of your choice.

The root password is "ketchup".

**Change the root password!**

edit the file /opt/noodle-ng/crawler.ini to fit your needs and run the crawler by starting the /opt/noodle-ng/start\_crawler.sh shell script. This will populate the database. You find the webserver of your appliance at port 80.

## Follow Up ##
**Set up a real database for Noodle NG.**
> The sqlite database of the appliance is a good start but quickly reaches performance limits. Since the appliance is not intended to be upgradable you should set up an external database host. This can be any db supported by [sqlalchemy](http://www.sqlalchemy.org/). Common are postgres and mysql. Then edit the files /opt/noodle-ng/production.ini and /opt/noodle-ng/crawler.ini and look for the sqlalchemy.url. Now you need to create the database scheme. Change your current working directory to /opt/noodle-ng and run

> `paster setup-app production.ini`

**Set up a Cron job for crawling**
> Edit the file /etc/cron.d/99noodle-crawler to fit your needs. The script start\_crawler.sh takes care that no more than one instance of the crawler is running. So you could use `* * * * *` in the cron file if you want to scan aggressive.


## Technical Details ##
The basesystem of the appliance is scientific linux 6.

You will find Noodle NG at /opt/noodle-ng. There is also a apache config file we added at /etc/httpd/conf.d/noodle.conf.