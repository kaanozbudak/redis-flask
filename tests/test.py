import app
import unittest
import time


class TestMyApp(unittest.TestCase):
    # set up --> when test start
    def setUp(self):
        self.app = app.app.test_client()

    # tear down --> when test over
    def tearDown(self):
        del self.app

    # test main domain
    def test_main(self):
        rv = self.app.get('/')
        assert rv.status == '404 NOT FOUND'

    # test all keys
    def test_get_keys(self):
        rv = self.app.get('/keys/')
        assert rv.status == '200 OK'
        # print(rv.allow)
        # assert sorted(rv.allow) == ['GET', 'PUT', 'DELETE']

    # test get a key
    def test_get_key(self):
        rv = self.app.put('/keys/', json={
            'key': 'phone',
            'value': 'telefon'
        })
        _rv = self.app.get('/keys/phone/')
        assert _rv.status == '200 OK'

    # test get key fail
    def test_get_key_fail(self):
        rv = self.app.get('/keys/something/')
        assert rv.status == '204 NO CONTENT'

    # test not allowed method
    def test_patch_key(self):
        rv = self.app.patch('/keys/')
        assert rv.status == '405 METHOD NOT ALLOWED'

    # test create new key
    def test_put_key(self):
        rv = self.app.put('/keys/', json={
            'key': 'phone',
            'value': 'telefon'
        })
        json_data = rv.get_json()
        assert json_data['result']
        assert rv.status == '201 CREATED'

    # test is key exist
    def test_key_is_exist(self):
        _rv = self.app.put('/keys/', json={
            'key': 'phone',
            'value': 'telefon'
        })
        rv = self.app.head('/keys/phone/')
        assert not rv.data
        assert rv.status == '200 OK'

    # test is key exist fail
    def test_key_is_exist_fail(self):
        rv = self.app.head('/keys/pencil/')
        assert rv.status == '204 NO CONTENT'

    # test delete a key
    def test_delete_key(self):
        rv = self.app.delete('/keys/phone/')
        assert rv.status == '200 OK'

    # test delete all keys
    def test_delete_all_keys(self):
        rv = self.app.delete('/keys/')
        assert rv.status == '200 OK'
        json_data = rv.get_json()
        assert json_data['result']

    # test expire time
    def test_put_key_expire(self):
        rv = self.app.put('/keys/?expire_in=3', json={
            'key': 'keyboard',
            'value': 'klavye'
        })
        json_data = rv.get_json()
        assert json_data['result']
        assert rv.status == '201 CREATED'
        _rv = self.app.get('/keys/keyboard/')
        assert _rv.status == '200 OK'
        time.sleep(7)
        # wait until expire time over
        __rv = self.app.get('/keys/keyboard/')
        assert __rv.status == '204 NO CONTENT'

    def test_put_key_expire_fail(self):
        rv = self.app.put('/keys/?expire_in=3', json={
            'key': 'keyboard',
            'value': 'klavye'
        })
        json_data = rv.get_json()
        assert json_data['result']
        assert rv.status == '201 CREATED'
        _rv = self.app.get('/keys/keyboard/')
        assert _rv.status == '200 OK'
        # time.sleep(7)
        # do not wait until expire time over so it can failed
        __rv = self.app.get('/keys/keyboard/')
        assert __rv.status != '204 NO CONTENT'

    # test wildcard prefix
    def test_get_key_wildcard(self):
        rv = self.app.put('/keys/', json={
            'key': 'phone',
            'value': 'telefon'
        })
        _rv = self.app.get('/keys/?filter=["pho[n,k]e"]')
        assert _rv.status == '200 OK'

    # test wildcard prefix fail
    def test_get_key_wildcard_fail(self):
        rv = self.app.put('/keys/', json={
            'key': 'phone',
            'value': 'telefon'
        })
        _rv = self.app.get('/keys/?filter=pho[q,a]e')
        assert _rv.status == '200 OK'
        assert _rv.get_json()['result'] == []
