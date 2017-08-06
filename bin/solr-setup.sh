# Apache Solr Setup
APP_NAME="pianosite"
SOLR_VERSION=4.10.2

wget http://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
tar xzf solr-$SOLR_VERSION.tgz
cd solr-$SOLR_VERSION/example/solr/collection1
cp -R conf conf.original
cp build
workon $APP_NAME
python manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/schema.xml
cd solr-$SOLR_VERSION/example

# solr will start when invoked with honcho (Procfile)
# java -jar start.jar
