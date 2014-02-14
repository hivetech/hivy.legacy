# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright (C) 2014 Hive Tech, SAS.


import time
import os
import unittest
from flask.ext.testing import TestCase
from werkzeug.datastructures import Headers
from werkzeug.test import Client

from hivy.app import app
from hivy import DOCKER_ON, SERF_ON
from hivy.node.factory import NodeFactory
from hivy.node.foundation import NodeFoundation


#TODO Test RestNode._node_name()
class RestfulNodeTestCase(TestCase):

    default_user = 'chuck'
    invalid_test_token = '4321'
    valid_test_token = 'd2a879423e53ddbb6788bbc286647a793440f3db'
    node_resource_path = '/v0/node'

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_node_resource_is_locked(self):
        rv = self.client.get(self.node_resource_path)
        self.assert_401(rv)
        self.assertTrue('WWW-Authenticate' in rv.headers)
        self.assertTrue('Token' in rv.headers['WWW-Authenticate'])

    def test_node_invalid_token_rejected(self):
        h = Headers()
        h.add('Authorization', self.invalid_test_token)
        rv = Client.open(self.client, path=self.node_resource_path, headers=h)
        self.assert_401(rv)

    def test_get_absent_node_informations(self):
        if DOCKER_ON:
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.get(self.node_resource_path, headers=h)
            self.assertTrue('error' in rv.data)
        else:
            pass

    def test_create_node(self):
        if DOCKER_ON:
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.post(self.node_resource_path, headers=h)
            assert 'error' not in rv.data
            assert 'Id' in rv.data
            assert 'name' in rv.data
        else:
            pass

    def test_get_existing_node_informations(self):
        if DOCKER_ON:
            time.sleep(5)
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.get(self.node_resource_path, headers=h)
            for info in ['ip', 'node', 'state', 'name']:
                self.assertTrue(info in rv.data)
        else:
            pass

    def test_delete_node(self):
        if DOCKER_ON:
            # Wait for the container to be correctly started
            time.sleep(5)
            h = Headers()
            h.add('Authorization', self.valid_test_token)
            rv = self.client.delete(self.node_resource_path, headers=h)
            assert 'error' not in rv.data
            assert 'name' in rv.data
            assert 'destroyed' in rv.data
        else:
            pass


class NodeFactoryTestCase(unittest.TestCase):

    servers_test = '*'
    image_test = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    role_test = 'test'
    name_test = 'test-node-factory'

    def setUp(self):
        self.node = NodeFactory(
            self.image_test, self.name_test, self.role_test)

    def test_inspect_absent_node(self):
        if DOCKER_ON:
            description = self.node.inspect()
            assert 'error' in description
        else:
            pass

    def test_activate_node(self):
        if DOCKER_ON:
            feedback = self.node.activate()
            assert 'error' not in feedback
            assert 'Id' in feedback
            assert 'name' in feedback
        else:
            pass

    def test_inspect_node(self):
        if DOCKER_ON:
            time.sleep(5)
            description = self.node.inspect()
            for info in ['ip', 'node', 'state', 'name']:
                self.assertTrue(info in description)
        else:
            pass

    def test_destroy_node(self):
        if DOCKER_ON:
            # Wait for the container to be correctly started
            time.sleep(5)
            feedback = self.node.destroy()
            assert 'error' not in feedback
            assert 'name' in feedback
            assert 'destroyed' in feedback
        else:
            pass


class NodeFoundationTestCase(unittest.TestCase):

    image_test = os.environ.get('NODE_IMAGE', 'quay.io/hackliff/node')
    role_test = 'test'
    name_test = 'test-node-foundation'

    def setUp(self):
        self.node = NodeFoundation(
            self.image_test, self.name_test, self.role_test)

    # Avoiding salt dependency for now
    #def test_check(self):
        #report = self.node.check(self.servers_test)
        #assert report
        #assert report['home']

    def test_register_node(self):
        if SERF_ON:
            pass
        else:
            pass

    def test_forget_node(self):
        if SERF_ON:
            pass
        else:
            pass
