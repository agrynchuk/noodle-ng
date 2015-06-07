# Notes while installing Turbogears 2.1 for upgrading Noodle NG #
```
* paster quickstart -s -n --disable-migrations
(-s enables sqlalchemy, -n disables authentication)
Name: Noodle NG
Package: noodle
No mako templates
* python setup.py develop
- nosetests fail, need to install tw.forms (ToscaWidgets) by adding "tw.forms", to setup.py in Noodle-NG folder
* python setup.py develop
- And of course we also need the database driver, e.g. 
* easy_install MySQL-python (which requires to have mysql development files, hehe)
- and pysqlite for development
* easy_install pysqlite
- and we are going to need pysmbc and ftputil (or only one of them) for the crawler and proxyDownloader
* easy_install pysmbc, easy_install ftputil (where pysmbc needs the samba development files)
* paster setup-app development.ini
- Creating apache mod_wsgi configuration using modwsgi_deploy (from http://pypi.python.org/pypi/modwsgideploy/)
* paster modwsgi_deploy
```