pkg_dnf = {
    'telegraf': {
        'needs': ['action:dnf_makecache'],
    },
}

svc_systemd = {
    'telegraf': {
        'needs': ['pkg_dnf:telegraf'],
    },
}

files = {
    '/etc/telegraf/telegraf.conf': {
        'mode': '0444',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
        'context': {
            'telegraf': node.metadata.get('telegraf', {}),
        },
    },
}

directories = {}

git_deploy = {}

if node.has_bundle('nginx'):
    files['/etc/telegraf/telegraf.d/nginx.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('php'):
    files['/etc/telegraf/telegraf.d/php-fpm.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('chrony'):
    files['/etc/telegraf/telegraf.d/chrony.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('haproxy'):
    files['/etc/telegraf/telegraf.d/haproxy.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('hddtemp'):
    files['/etc/telegraf/telegraf.d/hddtemp.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('influxdb'):
    files['/etc/telegraf/telegraf.d/influxdb.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('kapacitor'):
    files['/etc/telegraf/telegraf.d/kapacitor.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('lm-sensors'):
    files['/etc/telegraf/telegraf.d/lm-sensors.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('smartmontools'):
    files['/etc/telegraf/telegraf.d/smartmontools.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('postgresql'):
    files['/etc/telegraf/telegraf.d/postgresql.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence') or node.has_bundle('atlassian-bitbucket') or node.has_bundle('atlassian-bamboo') or node.metadata.get('telegraf', {}).get('collect_java', False):
    files['/etc/telegraf/telegraf.d/java.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence') or node.has_bundle('atlassian-bamboo') or node.metadata.get('telegraf', {}).get('collect_tomcat', False):
    files['/etc/telegraf/telegraf.d/tomcat.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('atlassian-confluence'):
    files['/etc/telegraf/telegraf.d/atlassian-confluence.conf'] = {
        'owner': 'telegraf',
        'mode': '0400',
        'content_type': 'mako',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }

if node.has_bundle('xmr-stak'):
    directories['/usr/local/src/PyMinerMonitor'] = {
        'mode': '0700',
        'owner': 'telegraf',
    }

    git_deploy['/usr/local/src/PyMinerMonitor'] = {
        'needs': ['directory:/usr/local/src/PyMinerMonitor'],
        'repo': 'https://github.com/Jamesits/PyMinerMonitor.git',
        'rev': 'master',
        'triggers': ['svc_systemd:telegraf:restart'],
    }

    files['/usr/local/src/PyMinerMonitor/config.json'] = {
        'mode': '0600',
        'source': '{}.xmr-stak.config.json'.format(node.name),
        'owner': 'telegraf',
        'triggers': ['svc_systemd:telegraf:restart'],
        'needs': ['git_deploy:/usr/local/src/PyMinerMonitor'],
    }

    files['/etc/telegraf/telegraf.d/pyminermonitor.conf'] = {
        'mode': '0444',
        'needs': ['pkg_dnf:telegraf'],
        'triggers': ['svc_systemd:telegraf:restart'],
    }
