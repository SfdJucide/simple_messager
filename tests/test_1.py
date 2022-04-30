# import unittest
# import time
#
# from server import get_response, parse_argv
# from client import build_message, check_server_answer, parse_client_argv
#
#
# class ServerTestCase(unittest.TestCase):
#     args1 = ['server.py', '-a', '127.0.0.2', '-p', '7776']
#     args2 = ['server.py']
#
#     response_good = {
#         'response': 200
#     }
#     response_bad = {
#         'response': 400,
#         'error': 'Bad Request'
#     }
#     message1 = {
#         'action': 'presence',
#         'time': time.time(),
#         'user': 'guest'
#     }
#     message2 = {
#         'action': 'presence',
#         'time': time.time(),
#         'user': 'enemy'
#     }
#
#     def test_parsing_argv(self):
#         self.assertEqual(type(parse_argv(args=self.args2)), tuple)
#         self.assertEqual(parse_argv(args=self.args2), ('', 7777))
#         self.assertEqual(parse_argv(args=self.args1), ('127.0.0.2', 7776))
#
#     def test_get_response(self):
#         self.assertEqual(get_response(self.message1), self.response_good)
#         self.assertEqual(get_response(self.message2), self.response_bad)
#
#
# class ClientTestCase(unittest.TestCase):
#     args1 = ['client.py', '127.0.0.2', '7776']
#     args2 = ['client.py']
#
#     message1 = {
#         'action': 'presence',
#         'time': time.time(),
#         'user': 'guest'
#     }
#     message2 = {
#         'action': 'presence',
#         'time': time.time(),
#         'user': 'enemy'
#     }
#
#     response1 = {
#         'response': 404
#     }
#
#     response2 = {
#         'response': 200
#     }
#
#     def test_build_message(self):
#         self.assertEqual(build_message('enemy')['user'], self.message2['user'])
#
#     def test_parse_client(self):
#         self.assertEqual(parse_client_argv(args=self.args2), ('localhost', 7777))
#         self.assertEqual(parse_client_argv(args=self.args1), ('127.0.0.2', 7776))
#
#     def test_check_server_answer(self):
#         self.assertEqual(check_server_answer(self.response1), '400: Bad Request')
#         self.assertEqual(check_server_answer(self.response2), '200: OK')
#
#
# if __name__ == '__main__':
#     unittest.main()
