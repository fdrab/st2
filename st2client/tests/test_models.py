import mock
import json
import logging
import unittest2

from tests import base

from st2client import models
from st2client.utils import httpclient


LOG = logging.getLogger(__name__)


class TestSerialization(unittest2.TestCase):

    def test_resource_serialize(self):
        instance = base.FakeResource(id='123', name='abc')
        self.assertDictEqual(instance.serialize(), base.RESOURCES[0])

    def test_resource_deserialize(self):
        instance = base.FakeResource.deserialize(base.RESOURCES[0])
        self.assertEqual(instance.id, '123')
        self.assertEqual(instance.name, 'abc')


class TestResourceManager(unittest2.TestCase):

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES), 200, 'OK')))
    def test_resource_get_all(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resources = mgr.get_all()
        actual = [resource.serialize() for resource in resources]
        expected = json.loads(json.dumps(base.RESOURCES))
        self.assertListEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES), 200, 'OK')))
    def test_resource_get_all_with_limit(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resources = mgr.get_all(limit=50)
        actual = [resource.serialize() for resource in resources]
        expected = json.loads(json.dumps(base.RESOURCES))
        self.assertListEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_get_all_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        self.assertRaises(Exception, mgr.get_all)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES[0]), 200, 'OK')))
    def test_resource_get_by_id(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resource = mgr.get_by_id('123')
        actual = resource.serialize()
        expected = json.loads(json.dumps(base.RESOURCES[0]))
        self.assertEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 404, 'NOT FOUND')))
    def test_resource_get_by_id_404(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resource = mgr.get_by_id('123')
        self.assertIsNone(resource)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_get_by_id_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        self.assertRaises(Exception, mgr.get_by_id)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps([base.RESOURCES[0]]), 200, 'OK')))
    def test_resource_query(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resources = mgr.query(name='abc')
        actual = [resource.serialize() for resource in resources]
        expected = json.loads(json.dumps([base.RESOURCES[0]]))
        self.assertEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps([base.RESOURCES[0]]), 200, 'OK')))
    def test_resource_query_with_limit(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resources = mgr.query(name='abc', limit=50)
        actual = [resource.serialize() for resource in resources]
        expected = json.loads(json.dumps([base.RESOURCES[0]]))
        self.assertEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 404, 'NOT FOUND')))
    def test_resource_query_404(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resources = mgr.query(name='abc')
        self.assertListEqual(resources, [])

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_query_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        self.assertRaises(Exception, mgr.query, name='abc')

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps([base.RESOURCES[0]]), 200, 'OK')))
    def test_resource_get_by_name(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resource = mgr.get_by_name('abc')
        actual = resource.serialize()
        expected = json.loads(json.dumps(base.RESOURCES[0]))
        self.assertEqual(actual, expected)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 404, 'NOT FOUND')))
    def test_resource_get_by_name_404(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        resource = mgr.get_by_name('abc')
        self.assertIsNone(resource)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES), 200, 'OK')))
    def test_resource_get_by_name_ambiguous(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        self.assertRaises(Exception, mgr.get_by_name, 'abc')

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_get_by_name_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        self.assertRaises(Exception, mgr.get_by_name)

    @mock.patch.object(
        httpclient.HTTPClient, 'post',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES[0]), 200, 'OK')))
    def test_resource_create(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        instance = base.FakeResource.deserialize('{"name": "abc"}')
        resource = mgr.create(instance)
        self.assertIsNotNone(resource)

    @mock.patch.object(
        httpclient.HTTPClient, 'post',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_create_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        instance = base.FakeResource.deserialize('{"name": "abc"}')
        self.assertRaises(Exception, mgr.create, instance)

    @mock.patch.object(
        httpclient.HTTPClient, 'put',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps(base.RESOURCES[0]), 200, 'OK')))
    def test_resource_update(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        text = '{"id": "123", "name": "cba"}'
        instance = base.FakeResource.deserialize(text)
        resource = mgr.update(instance)
        self.assertIsNotNone(resource)

    @mock.patch.object(
        httpclient.HTTPClient, 'put',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_update_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        text = '{"id": "123", "name": "cba"}'
        instance = base.FakeResource.deserialize(text)
        self.assertRaises(Exception, mgr.update, instance)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps([base.RESOURCES[0]]), 200, 'OK')))
    @mock.patch.object(
        httpclient.HTTPClient, 'delete',
        mock.MagicMock(return_value=base.FakeResponse('', 204, 'NO CONTENT')))
    def test_resource_delete(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        instance = mgr.get_by_name('abc')
        mgr.delete(instance)

    @mock.patch.object(
        httpclient.HTTPClient, 'delete',
        mock.MagicMock(return_value=base.FakeResponse('', 404, 'NOT FOUND')))
    def test_resource_delete_404(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        instance = base.FakeResource.deserialize(base.RESOURCES[0])
        mgr.delete(instance)

    @mock.patch.object(
        httpclient.HTTPClient, 'get',
        mock.MagicMock(return_value=base.FakeResponse(json.dumps([base.RESOURCES[0]]), 200, 'OK')))
    @mock.patch.object(
        httpclient.HTTPClient, 'delete',
        mock.MagicMock(return_value=base.FakeResponse('', 500, 'INTERNAL SERVER ERROR')))
    def test_resource_delete_failed(self):
        mgr = models.ResourceManager(base.FakeResource, base.FAKE_ENDPOINT)
        instance = mgr.get_by_name('abc')
        self.assertRaises(Exception, mgr.delete, instance)
