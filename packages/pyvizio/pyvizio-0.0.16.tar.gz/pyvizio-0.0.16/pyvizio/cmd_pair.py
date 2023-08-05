from .protocol import CommandBase, get_json_obj, ProtoConstants, Endpoints


class PairCommandBase(CommandBase):
    def __init__(self, device_id, device_type, endpoint):
        super(PairCommandBase, self).__init__()
        CommandBase.url.fset(self, Endpoints.ENDPOINTS[device_type][endpoint])
        self.DEVICE_ID = device_id


class BeginPairResponse(object):
    def __init__(self, ch_type, token):
        self.ch_type = ch_type
        self.token = token


class BeginPairCommand(PairCommandBase):
    """Initiating pairing process"""

    def process_response(self, json_obj):
        item = get_json_obj(json_obj, ProtoConstants.RESPONSE_ITEM)
        response = BeginPairResponse(
            get_json_obj(item, ProtoConstants.CHALLENGE_TYPE),
            get_json_obj(item, ProtoConstants.PAIRING_REQ_TOKEN),
        )
        return response

    def __init__(self, device_id, device_name, device_type):
        super().__init__(device_id, device_type, "BEGIN_PAIR")
        self.DEVICE_NAME = str(device_name)


class PairChallengeResponse(object):
    def __init__(self, auth_token):
        self.auth_token = auth_token


class PairChallengeCommand(PairCommandBase):
    """Finish pairing"""

    def process_response(self, json_obj):
        item = get_json_obj(json_obj, ProtoConstants.RESPONSE_ITEM)
        response = PairChallengeResponse(get_json_obj(item, ProtoConstants.AUTH_TOKEN))
        return response

    def __init__(self, device_id, challenge_type, pairing_token, pin, device_type):
        super().__init__(device_id, device_type, "FINISH_PAIR")
        self.CHALLENGE_TYPE = int(challenge_type)
        self.RESPONSE_VALUE = str(pin)
        self.PAIRING_REQ_TOKEN = int(pairing_token)


class CancelPairCommand(BeginPairCommand):
    """Cancel pairing process"""

    def process_response(self, json_obj):
        return None

    def __init__(self, device_id, device_name, device_type):
        super().__init__(device_id, device_name, device_type, "CANCEL_PAIR")
