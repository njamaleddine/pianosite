wget http://archive.apache.org/dist/lucene/solr/4.7.2/solr-4.7.2.tgz
tar xzf solr-4.7.2.tgz
cd solr-4.7.2/example/solr/collection1
cp -R conf conf.original
cp build
python manage.py build_solr_schema > schema.xml
mv pianosite/schema.xml pianosite/solr-4.7.2/example/solr/collection1/conf/schema.xml
cd pianosite/solr-4.7.2/solr-4.7.2/example
java -jar start.jar