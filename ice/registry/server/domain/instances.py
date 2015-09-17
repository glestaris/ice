from .domain import Domain


class InstancesDomain(Domain):
    # Domain configuration
    DEFAULT_ENDPOINT = 'instances'
    DEFAULT_ITEM_TITLE = 'instance'
    DEFAULT_ITEM_METHODS = ['GET', 'DELETE']

    def get_schema(self):
        return {
            # Session
            'session_id': {
                'type': 'objectid',
                'data_relation': {
                    'resource': 'sessions',
                    'field': '_id',
                    'embeddable': True
                },
                'required': True
            },

            # Networking
            'networks': {
                'type': 'list',
                'schema': {
                    'type': 'dict',
                    'schema': {
                        'addr': {
                            'type': 'string',
                            'required': True
                        },
                        'iface': {
                            'type': 'string',
                            'required': False
                        },
                        'bcast_addr': {
                            'type': 'ip',
                            'required': False
                        }
                    }
                },
            },

            # Public networking
            'public_ip_addr': {
                'required': True,
                'type': 'ip'
            },
            'public_reverse_dns': {
                'required': True,
                'type': 'string'
            },

            # Cloud info
            'cloud_id': {
                'required': False,
                'type': 'url'
            },
            'vpc_id': {
                'required': False,
                'type': 'string'
            },

            # SSH options
            'ssh_username': {
                'required': False,
                'type': 'string',
                'default': 'root'
            },
            'ssh_authorized_fingerprint': {
                'required': True,
                'type': 'string'
            },

            # Status
            'status': {
                'required': False,
                'type': 'string',
                'default': 'running'
            },
            'failed_pings_count': {
                'required': False,
                'type': 'integer',
                'default': 0
            }
        }
