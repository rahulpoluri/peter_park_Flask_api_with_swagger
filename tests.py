import json
import unittest
from unittest.mock import Mock, patch
import app
from datetime import datetime

class plateGetOutput():
    plate_num = "M-PP124"
    created_at = datetime.utcnow()


class platePostOutput():
    plate_num = "M-PP124"
    created_at = datetime.utcnow()


class TestPlate(unittest.TestCase):
    def testApiGetMethod_200(self):
        mock1 = app.NumberPlate = Mock()
        mock1.query.all.return_value = [plateGetOutput()]
        url = "/plate"
        client = app.app.test_client()
        response = client.get(url)
        assert(response.status_code == 200)

    def testApiPostMethod_200(self):
        mock2 = app.NumberPlate = Mock()
        mock2_1 = app.db = Mock()
        a = platePostOutput()
        mock2.query.filter_by.return_value.first.return_value = a
        url = "/plate"
        header = {}
        body = {'plate': 'M-PP123'}
        client = app.app.test_client()
        response = client.post(url, json=body, headers=header)
        assert response.status_code == 200

    def testPostKeyError_400(self):
        mock3 = app.NumberPlate = Mock()
        mock3_1 = app.db = Mock()
        a = platePostOutput()
        mock3.query.filter_by.return_value.first.return_value = a
        url = "/plate"
        header = {}
        body = {'plate_changed': 'M-PP123'}
        client = app.app.test_client()
        response = client.post(url, json=body, headers=header)
        assert response.status_code == 400
        assert response.get_data() == b'Not a valid request/plate field not found'

    def testPostValidPlateValue_422(self):
        mock4 = app.NumberPlate = Mock()
        mock4_1 = app.db = Mock()
        a = platePostOutput()
        mock4.query.filter_by.return_value.first.return_value = a
        url = "/plate"
        header = {}
        body = {'plate': 'MPP123'}
        client = app.app.test_client()
        response = client.post(url, json=body, headers=header)
        assert response.status_code == 422
        assert response.get_data() == b'Not a valid Plate Number'

    def testPostEmptyJson_400(self):
        mock5 = app.NumberPlate = Mock()
        mock5_1 = app.db = Mock()
        a = platePostOutput()
        mock5.query.filter_by.return_value.first.return_value = a
        url = "/plate"
        header = {}
        body = {}
        client = app.app.test_client()
        response = client.post(url, json=body, headers=header)
        assert response.status_code == 400
        assert response.get_data() == b'Not a valid request/plate field not found'

    def testDbFailure_500(self):
        mock6 = app.NumberPlate = Mock()
        mock6.query.all.side_effect = Exception("Oops something went wrong")
        url = "/plate"
        client = app.app.test_client()
        response = client.get(url)
        assert response.status_code == 500
        assert response.get_data() == b'Oops something went wrong'


class TestSearchPlate(unittest.TestCase):
    def testSearchGet_200(self):
        mock1 = app.NumberPlate = Mock()
        mock1.query.all.return_value = [plateGetOutput()]
        url = "/search-plate?key=MPP124&levenshtein=1"
        client = app.app.test_client()
        response = client.get(url)
        assert(response.status_code == 200)

    def testSearchGet_400(self):
        mock2 = app.NumberPlate = Mock()
        mock2.query.all.return_value = [plateGetOutput()]
        url = "/search-plate?key=MPP124&levenshtein=a"
        client = app.app.test_client()
        response = client.get(url)
        assert(response.status_code == 400)

    def testSearchGet_500(self):
        mock2 = app.NumberPlate = Mock()
        mock2.query.all.side_effect = Exception("Oops something went wrong")
        url = "/search-plate?key=MPP124&levenshtein=1"
        client = app.app.test_client()
        response = client.get(url)
        assert(response.status_code == 500)


if __name__ == '__main__':
    unittest.main()

