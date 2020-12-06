# Copyright (c) 2020 Sharvil Kekre skekre98
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import unittest

from app import app
from preprocess import funnel_name


# Test case for data preprocess
class TestPreprocess(unittest.TestCase):

    # Method to test funnel name
    def test_get_random_player_names(self):
        names = ["Bud Acton", "Gary Alexander", "Steven Adams"]
        for i in range(3):
            player_name = funnel_name(names[i])
            self.assertTrue(player_name in " ".join(names))


# Test cases for URL routing
class TestRouting(unittest.TestCase):
    # Method to test <blank> routing
    def test_blank_routing(self):
        with app.test_client() as c:
            response = c.get("")
            # 308: permanent redirect
            self.assertEqual(response.status_code, 308)

    # Method to test <some> routing
    def test_invalid_routing(self):
        with app.test_client() as c:
            response = c.get("/some/path/that/doesnt/exist")
            # 404: page not found
            self.assertEqual(response.status_code, 404)

    def test_authors_routing(self):
        with app.test_client() as c:
            response = c.get("/authors")
            # 200: response is OK
            self.assertEqual(response.status_code, 200)

    def test_blog_routing(self):
        with app.test_client() as c:
            response = c.get("/blog")
            self.assertEqual(response.status_code, 200)

    def test_chat_routing(self):
        with app.test_client() as c:
            response = c.get("/chat")
            self.assertEqual(response.status_code, 200)

    def test_download_routing(self):
        with app.test_client() as c:
            # expected response code is a 302 ('Moved Temporarily') because of the 'redirect'
            response = c.get("/download/1")
            self.assertEqual(response.status_code, 302)

            response = c.get("/download/2")
            self.assertEqual(response.status_code, 302)

            response = c.get("/download/3")
            self.assertEqual(response.status_code, 302)

    def test_download_routing_invalid_url(self):
        with app.test_client() as c:
            # invalid URL
            response = c.get("/download")
            self.assertEqual(response.status_code, 404)

    def test_get_bot_response_routing(self):
        with app.test_client() as c:
            response = c.post("/bot-msg", data={"msg": "test message"})
            self.assertEqual(response.status_code, 200)

    def test_get_bot_response_routing_get_not_supported(self):
        with app.test_client() as c:
            # GET not supported
            response = c.get("/bot-msg")
            self.assertEqual(response.status_code, 405)

    def test_get_bot_response_routing_missing_param(self):
        with app.test_client() as c:
            # Bad request: missing param
            response = c.post("/bot-msg")
            self.assertEqual(response.status_code, 400)

    def test_home_routing(self):
        with app.test_client() as c:
            response = c.get("/")
            self.assertEqual(response.status_code, 200)

    def test_home2_routing(self):
        with app.test_client() as c:
            response = c.get("/home")
            self.assertEqual(response.status_code, 200)

    def test_predictions_routing(self):
        with app.test_client() as c:
            response = c.get("/predictions")
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
