SOLR_VERSION=4.10.2

wget http://archive.apache.org/dist/lucene/solr/$SOLR_VERSION/solr-$SOLR_VERSION.tgz
tar xzf solr-$SOLR_VERSION.tgz
cd solr-$SOLR_VERSION/example/solr/collection1
cp -R conf conf.original
cp build
workon pianosite
python manage.py build_solr_schema > solr-$SOLR_VERSION/example/solr/collection1/schema.xml
cd solr-$SOLR_VERSION/example
java -jar start.jar
