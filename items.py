pkg_dnf = {}

actions = {}

files = {}

symlinks = {}

users = {}

svc_systemd = {}

if node.metadata.get('telegraf', {}).get('binary_install', False) == False:
    telegraf_dependency = 'pkg_dnf:telegraf'
    pkg_dnf['telegraf'] = {
        'needs': ['action:dnf_makecache'],
    }
else:
    telegraf_dependency = 'action:chmod_telegraf_binary'
    telegraf_version = node.metadata.get('telegraf', {}).get('version', '1.7.2')
    telegraf_arch = node.metadata.get('telegraf', {}).get('arch', 'armhf')
    files['/usr/local/bin/install_telegraf_binary'] = {
        'mode': '0700',
        'content_type': 'mako',
        'context': {
            'telegraf_version': telegraf_version,
            'telegraf_arch': telegraf_arch,
        },
        'needs': ['pkg_dnf:wget'],
    }
    actions['symlink_systemd_service'] = {
        'command': '/usr/bin/systemctl link /usr/lib/telegraf/scripts/telegraf.service',
        'unless': 'file -E /etc/systemd/system/telegraf.service',
        'needs': ['file:/usr/local/bin/install_telegraf_binary'],
        'triggered': True,
        'triggers': ['action:systemd-daemon-reload'],
        'needed_by': ['svc_systemd:telegraf'],
    }
    actions['deploy_telegraf_binary'] = {
        'command': '/usr/local/bin/install_telegraf_binary',
        'unless': '/usr/bin/telegraf --version | grep {}'.format(telegraf_version),
        'needs': ['file:/usr/local/bin/install_telegraf_binary'],
        'triggers': ['action:symlink_systemd_service'],
    }
    users['telegraf'] = {
        'home': '/etc/telegraf',
        'shell': "/bin/false",
        'needed_by': ['svc_systemd:telegraf'],
    }
    actions['chmod_telegraf_binary'] = {
        'command': 'chown root:telegraf /usr/bin/telegraf',
        'unless': 'ls /usr/bin/telegraf -l | grep \'root telegraf\'',
        'needs': ['action:deploy_telegraf_binary'],
    }

svc_systemd['telegraf'] = {
    'needs': [telegraf_dependency],
}

directories = {
    '/etc/telegraf/telegraf.d': {
        'mode': '0700',
        'owner': 'telegraf',
        'triggers': ['svc_systemd:telegraf:restart'],
    },
}

files['/etc/telegraf/telegraf.conf'] = {
    'mode': '0400',
    'owner': 'telegraf',
    'content_type': 'mako',
    'needs': [telegraf_dependency],
    'triggers': ['svc_systemd:telegraf:restart'],
    'context': {
        'telegraf': node.metadata.get('telegraf', {}),
    },
}

git_deploy = {}

if node.has_bundle('nginx'):
    files['/etc/telegraf/telegraf.d/nginx.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('php'):
    files['/etc/telegraf/telegraf.d/php-fpm.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('chrony'):
    files['/etc/telegraf/telegraf.d/chrony.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('haproxy'):
    files['/etc/telegraf/telegraf.d/haproxy.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('hddtemp'):
    files['/etc/telegraf/telegraf.d/hddtemp.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('influxdb'):
    files['/etc/telegraf/telegraf.d/influxdb.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('kapacitor'):
    files['/etc/telegraf/telegraf.d/kapacitor.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('lm-sensors'):
    files['/etc/telegraf/telegraf.d/lm-sensors.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('smartmontools'):
    files['/etc/telegraf/telegraf.d/smartmontools.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('postgresql'):
    files['/etc/telegraf/telegraf.d/postgresql.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence') or node.has_bundle('atlassian-bitbucket') or node.has_bundle('atlassian-bamboo') or node.metadata.get('telegraf', {}).get('collect_java', False):
    files['/etc/telegraf/telegraf.d/java.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence') or node.has_bundle('atlassian-bamboo') or node.metadata.get('telegraf', {}).get('collect_tomcat', False):
    files['/etc/telegraf/telegraf.d/tomcat.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence'):
    files['/etc/telegraf/telegraf.d/atlassian-confluence.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('xmr-stak'):
    files['/etc/telegraf/telegraf.d/xmr-stak.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.metadata.get('telegraf', {}).get('rtorrent', {}):
    files['/etc/telegraf/telegraf.d/rtorrent.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }
    files['/usr/local/bin/telegraf_rtorrent'] = {
        'source': 'rtorrent.py',
        'owner': 'telegraf',
        'mode': '0700',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.metadata.get('telegraf', {}).get('collectd_input', {}):
    files['/etc/telegraf/telegraf.d/collectd.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
        'context': {
            'server': node.metadata.get('telegraf', {}).get('collectd_input', {}),
        },
    }
    files['/etc/telegraf/collectd_auth_file'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
        'context': {
            'server': node.metadata.get('telegraf', {}).get('collectd_input', {}),
        },
    }
    files['/etc/telegraf/collectd_types.db'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

    if node.has_bundle('firewalld'):
        if node.metadata.get('telegraf', {}).get('firewalld_permitted_zones'):
            for zone in node.metadata.get('telegraf', {}).get('firewalld_permitted_zones'):
                actions['firewalld_add_telegraf_collectd_zone_{}'.format(zone)] = {
                    'command': 'firewall-cmd --permanent --zone={} --add-port=25826/udp'.format(zone),
                    'unless': 'firewall-cmd --zone={} --list-ports | grep "25826/udp"'.format(zone),
                    'cascade_skip': False,
                    'needs': ['pkg_dnf:firewalld'],
                    'triggers': ['action:firewalld_reload'],
                }
        elif node.metadata.get('firewalld', {}).get('default_zone'):
            default_zone = node.metadata.get('firewalld', {}).get('default_zone')
            actions['firewalld_add_telegraf_collectd_zone_{}'.format(default_zone)] = {
                'command': 'firewall-cmd --permanent --zone={} --add-port=25826/udp'.format(default_zone),
                'unless': 'firewall-cmd --zone={} --list-ports | grep "25826/udp"'.format(default_zone),
                'cascade_skip': False,
                'needs': ['pkg_dnf:firewalld'],
                'triggers': ['action:firewalld_reload'],
            }
        elif node.metadata.get('firewalld', {}).get('custom_zones', False):
            for interface in node.metadata['interfaces']:
                custom_zone = node.metadata.get('interfaces', {}).get(interface).get('firewalld_zone')
                actions['firewalld_add_telegraf_collectd_zone_{}'.format(custom_zone)] = {
                    'command': 'firewall-cmd --permanent --zone={} --add-port=25826/udp'.format(custom_zone),
                    'unless': 'firewall-cmd --zone={} --list-ports | grep "25826/udp"'.format(custom_zone),
                    'cascade_skip': False,
                    'needs': ['pkg_dnf:firewalld'],
                    'triggers': ['action:firewalld_reload'],
                }
        else:
            actions['firewalld_add_telegraf_collectd'] = {
                'command': 'firewall-cmd --permanent --add-port=25826/udp',
                'unless': 'firewall-cmd --list-ports | grep "25826/udp"',
                'cascade_skip': False,
                'needs': ['pkg_dnf:firewalld'],
                'triggers': ['action:firewalld_reload'],
            }

if node.metadata.get('telegraf', {}).get('synology', False):
    files['/etc/telegraf/telegraf.d/synology.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }
    synology_mibs = ['HOST-RESOURCES-MIB.txt', 'IF-MIB.txt', 'RFC1213-MIB.txt', 'SYNOLOGY-DISK-MIB.txt', 'SYNOLOGY-ISCSILUN-MIB.txt', 'SYNOLOGY-RAID-MIB.txt', 'SYNOLOGY-SERVICES-MIB.txt', 'SYNOLOGY-SMART-MIB.txt', 'SYNOLOGY-SPACEIO-MIB.txt', 'SYNOLOGY-STORAGEIO-MIB.txt', 'SYNOLOGY-SYSTEM-MIB.txt', 'SYNOLOGY-UPS-MIB.txt', 'UCD-DEMO-MIB.txt', 'UCD-DISKIO-MIB.txt', 'UCD-DLMOD-MIB.txt', 'UCD-IPFILTER-MIB.txt', 'UCD-IPFWACC-MIB.txt', 'UCD-SNMP-MIB-OLD.txt', 'UCD-SNMP-MIB.txt']
    for mib in synology_mibs:
        files['/usr/share/snmp/mibs/{}'.format(mib)] = {
            'source': 'synology_mibs/{}'.format(mib),
            'mode': '0444',
            'triggers': ['svc_systemd:telegraf:restart'],
        }

for config in node.metadata.get('telegraf', {}).get('custom_configs', {}):
    files['/etc/telegraf/telegraf.d/{}.conf'.format(config)] = {
        'source': '{}.{}'.format(node.name, config),
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': [telegraf_dependency],
        'triggers': ['svc_systemd:telegraf:restart'],
    }
