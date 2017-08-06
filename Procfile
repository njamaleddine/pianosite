web: gunicorn -w 4 -b 0.0.0.0:$PORT wsgi:application
search: sh -c 'cd ./solr-4.10.2/example/ && java -jar start.jar'
celery_worker: celery -A pianosite worker -l info
celery_beat: celery -A pianosite beat
celery_flower: flower -A pianosite --port=5555
