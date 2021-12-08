FROM python:3.9.5

RUN pip install git+git://github.com/doublethinklab/youtube-api.git

ENTRYPOINT ["jupyter notebook", "--ip 0.0.0.0", "--port 8888", "--allow-root", "--no-browser"]
