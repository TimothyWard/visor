from bigbrother import index
import unittest
import json


class BigBrotherTrackingTests(unittest.TestCase):

    def setUp(self):
        index.app.testing = True
        self.app = index.app.test_client()

    def tearDown(self):
        index.tracks.clear()

    def test_app_is_available(self):
        response = self.app.get('/')
        assert b'Welcome to Big Brother, you\'re ad-tracking solution!' in response.data

    def test_post_track_hover(self):

        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="HOVER",
            x_pixel=20,
            y_pixel=100
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data

        response2 = self.app.get('/track')
        data = json.loads(response2.data)
        assert len(data) == 1
        data = data[0]
        assert data['ad_format'] == 'MOBILE'
        assert data['ad_name'] == 'Cialis'
        assert data['ip'] == '1.1.1.1'
        assert data['track_type'] == 'HOVER'
        assert data['x_pixel'] == 20
        assert data['y_pixel'] == 100

    def test_post_track_generic(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data

        response2 = self.app.get('/track')
        data = json.loads(response2.data)
        assert len(data) == 1
        data = data[0]
        assert data['ad_format'] == 'MOBILE'
        assert data['ad_name'] == 'Cialis'
        assert data['ip'] == '1.1.1.1'
        assert data['track_type'] == 'CLICK'

    def test_conversion_rate(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="IMPRESSION"
        ))
        track_json2 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="IMPRESSION"
        ))
        track_json3 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data
        response3 = self.app.post('/track', data=track_json3, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response3.data

        response4 = self.app.get('/track/statistics')
        data = json.loads(response4.data)
        assert data['conversion_rate'] == 0.5

    def test_tracking_counts(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="SCROLL"
        ))
        track_json2 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="SCROLL"
        ))
        track_json3 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data
        response3 = self.app.post('/track', data=track_json3, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response3.data

        response4 = self.app.get('/track/statistics')
        data = json.loads(response4.data)
        assert data['tracking_counts'] == {'CLICK': 1, 'CLOSE': 0, 'HOVER': 0, 'IMPRESSION': 0, 'SCROLL': 2}

    def test_heatmap_data(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="HOVER",
            x_pixel=10,
            y_pixel=12
        ))
        track_json2 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="HOVER",
            x_pixel=10,
            y_pixel=12
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data

        response4 = self.app.get('/track/statistics')
        data = json.loads(response4.data)
        assert data['heatmap_data'] == [[10.0, 12.0], [10.0, 12.0]]

    def test_ip_filter(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        track_json2 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="2.2.2.2",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data

        response4 = self.app.get('/track?start_ip=2.2.2.2&end_ip=2.2.2.2')
        data = json.loads(response4.data)
        assert len(data) == 1

    def test_name_filter(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        track_json2 = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Viagra",
            ip="2.2.2.2",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data

        response4 = self.app.get('/track?ad_name=Viagra')
        data = json.loads(response4.data)
        assert len(data) == 1

    def test_ad_format_filter(self):
        track_json = json.dumps(dict(
            ad_format="MOBILE",
            ad_name="Cialis",
            ip="1.1.1.1",
            track_type="CLICK"
        ))
        track_json2 = json.dumps(dict(
            ad_format="DESKTOP",
            ad_name="Viagra",
            ip="2.2.2.2",
            track_type="CLICK"
        ))
        response = self.app.post('/track', data=track_json, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response.data
        response2 = self.app.post('/track', data=track_json2, content_type='application/json')
        assert b'New Tracking Event Successfully Added' in response2.data

        response4 = self.app.get('/track?ad_format=MOBILE')
        data = json.loads(response4.data)
        assert len(data) == 1


if __name__ == '__main__':
    unittest.main()