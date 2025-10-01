# mcp/context_protocol.py

import uuid
import datetime

class MCPMessage:
    def __init__(self, sender, receiver, msg_type, payload):
        self.message = {
            "sender": sender,
            "receiver": receiver,
            "type": msg_type,
            "trace_id": str(uuid.uuid4()),
            "timestamp": str(datetime.datetime.utcnow()),
            "payload": payload
        }

    def get_message(self):
        return self.message
