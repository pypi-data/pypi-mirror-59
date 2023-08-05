
'''
This is auto-generated file,
which includes metadata for module Cisco_IOS_XR_ipv4_telnet_cfg
'''

from ydk._core._dm_meta_info import _MetaInfoClassMember, _MetaInfoClass, _MetaInfoEnum
from ydk._core._dm_meta_info import ATTRIBUTE, REFERENCE_LIST, REFERENCE_LEAFLIST, REFERENCE_BITS, REFERENCE_UNION
from ydk._core._dm_meta_info import REFERENCE_CLASS, REFERENCE_IDENTITY_CLASS, REFERENCE_ENUM_CLASS, ANYXML_CLASS
from ydk._core._importer import _yang_ns

_meta_table = {
    'Ipv6Telnet.Client' : {
        'meta_info' : _MetaInfoClass('Ipv6Telnet.Client', REFERENCE_CLASS,
            '''Telnet client configuration''',
            False, 
            [
            _MetaInfoClassMember('source-interface', ATTRIBUTE, 'str', 'xr:Interface-name',
                None, None,
                [], [b'[a-zA-Z0-9._/-]+'],
                '''                Source interface for telnet sessions
                ''',
                'source_interface',
                'Cisco-IOS-XR-ipv4-telnet-cfg', False),
            ],
            'Cisco-IOS-XR-ipv4-telnet-cfg',
            'client',
            _yang_ns.NAMESPACE_LOOKUP['Cisco-IOS-XR-ipv4-telnet-cfg'],
            'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg',
        ),
    },
    'Ipv6Telnet' : {
        'meta_info' : _MetaInfoClass('Ipv6Telnet', REFERENCE_CLASS,
            '''IPv6 telnet configuration''',
            False, 
            [
            _MetaInfoClassMember('client', REFERENCE_CLASS, 'Client', '',
                'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg', 'Ipv6Telnet.Client',
                [], [],
                '''                Telnet client configuration
                ''',
                'client',
                'Cisco-IOS-XR-ipv4-telnet-cfg', False),
            ],
            'Cisco-IOS-XR-ipv4-telnet-cfg',
            'ipv6-telnet',
            _yang_ns.NAMESPACE_LOOKUP['Cisco-IOS-XR-ipv4-telnet-cfg'],
            'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg',
        ),
    },
    'Ipv4Telnet.Client' : {
        'meta_info' : _MetaInfoClass('Ipv4Telnet.Client', REFERENCE_CLASS,
            '''Telnet client configuration''',
            False, 
            [
            _MetaInfoClassMember('source-interface', ATTRIBUTE, 'str', 'xr:Interface-name',
                None, None,
                [], [b'[a-zA-Z0-9._/-]+'],
                '''                Source interface for telnet sessions
                ''',
                'source_interface',
                'Cisco-IOS-XR-ipv4-telnet-cfg', False),
            ],
            'Cisco-IOS-XR-ipv4-telnet-cfg',
            'client',
            _yang_ns.NAMESPACE_LOOKUP['Cisco-IOS-XR-ipv4-telnet-cfg'],
            'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg',
        ),
    },
    'Ipv4Telnet' : {
        'meta_info' : _MetaInfoClass('Ipv4Telnet', REFERENCE_CLASS,
            '''ipv4 telnet''',
            False, 
            [
            _MetaInfoClassMember('client', REFERENCE_CLASS, 'Client', '',
                'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg', 'Ipv4Telnet.Client',
                [], [],
                '''                Telnet client configuration
                ''',
                'client',
                'Cisco-IOS-XR-ipv4-telnet-cfg', False),
            ],
            'Cisco-IOS-XR-ipv4-telnet-cfg',
            'ipv4-telnet',
            _yang_ns.NAMESPACE_LOOKUP['Cisco-IOS-XR-ipv4-telnet-cfg'],
            'ydk.models.cisco_ios_xr.Cisco_IOS_XR_ipv4_telnet_cfg',
        ),
    },
}
_meta_table['Ipv6Telnet.Client']['meta_info'].parent =_meta_table['Ipv6Telnet']['meta_info']
_meta_table['Ipv4Telnet.Client']['meta_info'].parent =_meta_table['Ipv4Telnet']['meta_info']
