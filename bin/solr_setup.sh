#!/bin/bash
# Apache Solr Setup
APP_NAME="pianosite"
SOLR_VERSION=4.10.2
SOLR_DIRECTORY=solr-$SOLR_VERSION/example/solr/collection1

wget http://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
tar xzf solr-$SOLR_VERSION.tgz
sudo cp -R $SOLR_DIRECTORY/conf $SOLR_DIRECTORY/conf.original
sudo cp $SOLR_DIRECTORY/build
workon $APP_NAME
# This may not work because the latest django-haystack doesn't support creating
# schema.xml files for solr 4.X, instead we need to copy the local dev one until we
# update to solr 6.x
# Open issue: https://github.com/django-haystack/django-haystack/issues/1546
./manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/conf/schema.xml
