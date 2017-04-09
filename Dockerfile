FROM python:3.6-alpine

# RUN apk add --no-cache \
#		pcre-dev
# 		build-base
		# python3-dev

RUN addgroup -S uwsgi && adduser -S -g uwsgi uwsgi

WORKDIR /project

COPY requirements/requirements-main.txt /project/
COPY requirements/requirements-dev.txt /project/

RUN set -e && \
	apk add --no-cache --virtual .build-deps \
		gcc \
		libc-dev \
		linux-headers \
	&& \
	pip install -r requirements-main.txt && \
	pip install -r requirements-dev.txt && \
	apk del .build-deps

COPY setup.py /project/
COPY setup.cfg /project/
COPY .coveragerc /project/
COPY tox.ini /project/
COPY pytest.ini /project/
COPY README.rst /project/
COPY docker-entrypoint.sh /usr/local/bin/

COPY rabbitChat /project/rabbitChat
COPY tests /project/tests/


EXPOSE 5001 9091

CMD ["docker-entrypoint.sh"]