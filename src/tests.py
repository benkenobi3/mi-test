import app
import unittest
from unittest import mock
from mongomock import MongoClient
from fastapi.testclient import TestClient


def simple_generation_req(app):
    return app.request(
        method='POST',
        url='/generate',
        json={
            "secret_text": "secret text",
            "phrase": "secret phrase"
        }
    )


def simple_getting_req(app, secret_key):
    return app.request(
        method='GET',
        url='/secrets/' + secret_key,
        params={'secret_phrase': 'secret phrase'}
    )


class FastApiTestCase(unittest.TestCase):

    @mock.patch('app.collection', MongoClient().db.collection)
    def setUp(self):
        self.app: TestClient = TestClient(app.app)

    def tearDown(self):
        pass

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_not_found_error(self):
        res = self.app.request(method='GET', url='/secrets/123')
        assert res.status_code == 404

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_generation(self):
        res = simple_generation_req(self.app)
        assert res.status_code == 201

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_getting_secret(self):
        res = simple_generation_req(self.app)
        assert res.status_code == 201

        secret_key = res.json()['secret_key']
        res = simple_getting_req(self.app, secret_key)
        assert res.status_code == 200
        assert res.json() == {'secret': 'secret text'}

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_del_after_read(self):
        res = simple_generation_req(self.app)
        assert res.status_code == 201

        secret_key = res.json()['secret_key']
        res = simple_getting_req(self.app, secret_key)
        assert res.status_code == 200

        res = simple_getting_req(self.app, secret_key)
        assert res.status_code == 404

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_wrong_secret_phrase(self):
        res = simple_generation_req(self.app)
        assert res.status_code == 201

        secret_key = res.json()['secret_key']
        res = self.app.request(
            method='GET',
            url='/secrets/' + secret_key,
            params={'secret_phrase': 'wrong secret phrase'}
        )
        assert res.status_code == 401

    @mock.patch('app.collection', MongoClient().db.collection)
    def test_validation_error(self):
        res = self.app.request(
            method='POST',
            url='/generate',
            json={
                "secret_text": "",
                "phrase": "secret phrase"
            }
        )
        assert res.status_code == 422

        res = self.app.request(
            method='POST',
            url='/generate',
            json={
                "secret_text": "secret text",
                "phrase": ""
            }
        )
        assert res.status_code == 422


if __name__ == '__main__':
    unittest.main()
