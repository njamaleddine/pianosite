#!/bin/bash
# Apache Solr Setup
APP_NAME="pianosite"
SOLR_VERSION=4.10.2
SOLR_DIRECTORY=solr-$SOLR_VERSION/example/solr/collection1
source `which virtualenvwrapper.sh`

wget http://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
tar xzf solr-$SOLR_VERSION.tgz
cp -R $SOLR_DIRECTORY/conf SOLR_DIRECTORY/conf.original
cp $SOLR_DIRECTORY/build
workon $APP_NAME
python manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/schema.xml
