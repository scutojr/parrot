#!/usr/bin/env python

import time
import json
import urllib.request as urlReq
from unittest import TestCase, main


class TestEvent(TestCase):

    def setUp(self):
        self.host = 'localhost'
        self.port = 12213
        self.url = 'http://%s:%s/parrot/api/v1/events' % (self.host, self.port)

    def test_basic_event(self):
        headers = {
            'Content-Type': 'application/json'
        }
        topic = ['example1', 'example2', 'example3']
        data = {
            'topic': '',
            'hostname': 'jayce.test.001',
            'service': 'Worker',
            'status': 'CRITICAL',
            'output': 'some output of the detecting program',
            'timestampt': int(time.time()*1000),
            'tags': {
                'cluster': 'tiny01',
                'testMode': True
            }
        }
        try:
            for t in topic:
                data['topic'] = t
                payload = json.dumps(data).encode()
                req = urlReq.Request(self.url, payload, headers)
                rsp = urlReq.urlopen(req)
        except urlReq.HTTPError as e:
            self.assertTrue(False, 'Failed to post event: ' + str(e))


if __name__ == '__main__':
    main()
