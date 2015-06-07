# Prerequisites #

  * a [turbogears 2](http://www.turbogears.org/2.0/) environment (currently we use 2.0b2)
  * [pysmbc](http://cyberelk.net/tim/software/pysmbc/) in version 1.09 or up
  * libsmbclient
  * smbclient (currently required for the crawler. We hope to get rid of this dependency soon)
**nice to have:**
  * a decent sql database like mysql
  * apache2 with mod\_wsgi

# Installation #

  1. checkout noodle via [svn](http://code.google.com/p/noodle-ng/source/checkout) to /opt/noodle or any other directory that suits you. We assume /opt/noodle in this guide.
  1. copy the development\_template.ini to development.ini and do the same with production\_template.ini and edit the files according to your environment (url to database, ...)
  1. run "paster setup-app development.ini" to setup the database. Currently you use a sqlite db in the noodle directory.
  1. edit the hcrawler.py to scan the ip range you are interested in. This has to be done in code, but we will make this easier in the future.
  1. now you can run "paster serve development.ini" and see the result in your browser on port 8080

# What to do next #
sqlite is not a very fast database solution and should be substituted with something more decent like mysql or postgresql.

paster is nice for development but not a very performing web server. You can use apache2 with mod\_wsgi instead. (Instructions on that follow.)

setup a cron job that runs hcrawler and statsd on a regular basis.