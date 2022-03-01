import unittest
from ..client.message import Message


class TestMessageMethods(unittest.TestCase):

    def test_to_string(self):
        msg = Message()
        msg.set_message("hi")
        msg.set_sender("idan")
        msg.set_receiver("alon")
        msg.set_seq(1)
        msg_string = msg.to_string()
        self.assertEqual(msg_string, "<m:hi><s:idan><r:alon><q:1>")

    def test_load(self):
        msg = Message()
        msg.set_message("hi")
        msg.set_sender("idan")
        msg.set_receiver("alon")
        msg.set_seq(1)
        msg_string = msg.to_string()

        msg_copy = Message()
        msg_copy.load(msg_string)
        self.assertEqual(msg_copy.get_message(), "hi")
        self.assertEqual(msg_copy.get_sender(), "idan")
        self.assertEqual(msg_copy.get_receiver(), "alon")
        self.assertEqual(msg_copy.get_seq(), "1")
        self.assertEqual(msg_copy.get_response(), None)
        self.assertEqual(msg_copy.get_request(), None)


if __name__ == '__main__':
    unittest.main()
