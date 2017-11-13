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
sudo python manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/schema.xml
