# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


from flask import Flask, request
from flask.ext import restful
import os

import hivy.settings as settings
from hivy.logger import logger


log = logger(__name__)


app = Flask(__name__)
app.config.update(
    PROPAGATE_EXCEPTIONS=False,
    PRESERVE_CONTEXT_ON_EXCEPTION=True,
    ENV=os.environ.get('APP_ENV', 'development')
)

api = restful.Api(app)
for endpoint, resource in settings.ROUTES.iteritems():
    api.add_resource(resource, endpoint)


#TODO Use it for logging and perfs
@app.before_request
def before_request():
    log.debug(request)


@app.after_request
def after_request(response):
    log.debug(request)
    return response
