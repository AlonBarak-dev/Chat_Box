import unittest
from message import Message

class TestMessage(unittest.TestCase):

    def test_load(self):
        msg_string = "<s:alon><r:server:192.168.56.1><t:connect>"
        msg_test = Message()
        msg_test.load(msg_string)
        msg_result = Message()
        msg_result.set_sender("alon")
        msg_result.set_receiver("server:192.168.56.1")
        msg_result.set_request('connect')
        assert msg_result.get_sender() == msg_test.get_sender(), "load failed"
        assert msg_result.get_receiver() == msg_test.get_receiver(), "load failed"
        assert msg_result.get_request() == msg_test.get_request(), "load failed"

        msg_string = "<s:alon><r:server:127.0.0.1><p:message_received><m:hello World!>"
        msg_test = Message()
        msg_test.load(msg_string)
        msg_result = Message()
        msg_result.set_sender("alon")
        msg_result.set_receiver("server:192.168.56.1")
        msg_result.set_response('message_received')
        msg_result.set_message("hello World!")
        assert msg_result.get_sender() == msg_test.get_sender(), "load failed"
        assert not msg_result.get_receiver() == msg_test.get_receiver(), "different addresses "
        assert msg_result.get_response() == msg_test.get_response(), "load failed"
        assert msg_result.get_message() == msg_test.get_message(), "load failed"

    def test_to_string(self):
        msg_result = Message()
        msg_result.set_sender("alon")
        msg_result.set_receiver("server:192.168.56.1")
        msg_result.set_request('connect')
        msg_string = msg_result.to_string()
        msg_test = Message()
        msg_test.load(msg_string)
        assert msg_result.get_sender() == msg_test.get_sender(), "to_string failed"
        assert msg_result.get_receiver() == msg_test.get_receiver(), "to_string failed"
        assert msg_result.get_request() == msg_test.get_request(), "to_string failed"

        msg_result.set_sender("alon")
        msg_result.set_receiver("server:192.168.56.1")
        msg_result.set_response('message_received')
        msg_result.set_message("hello World!")
        msg_string = msg_result.to_string()
        msg_test = Message()
        msg_test.load(msg_string)
        assert msg_result.get_sender() == msg_test.get_sender(), "to_string failed"
        assert msg_result.get_receiver() == msg_test.get_receiver(), "different addresses "
        assert msg_result.get_response() == msg_test.get_response(), "to_string failed"
        assert msg_result.get_message() == msg_test.get_message(), "to_string failed"

if __name__ == "__main__":
    unittest.main()

