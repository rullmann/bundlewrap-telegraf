@metadata_processor
def dnf(metadata):
    if node.has_bundle('dnf'):
        metadata.setdefault('dnf', {})
        metadata['dnf'].setdefault('repositories', {})
        metadata['dnf']['repositories'].setdefault('influxdb', {})
        metadata['dnf']['repositories']['influxdb'].setdefault(
            'name',
            'InfluxDB Repository - RHEL 7',
        )
        metadata['dnf']['repositories']['influxdb'].setdefault(
            'baseurl',
            'https://repos.influxdata.com/rhel/7/x86_64/stable',
        )
        metadata['dnf']['repositories']['influxdb'].setdefault(
            'gpgkey',
            'https://repos.influxdata.com/influxdb.key',
        )
    return metadata, DONE

@metadata_processor
def firewalld(metadata):
    if node.has_bundle('firewalld'):
        metadata.setdefault('firewalld', {})
        metadata['firewalld'].setdefault('ports')
        for port in ['25826/udp']:
            if port not in metadata['firewalld']['ports']:
                metadata['firewalld']['ports'].append(port)

    return metadata, DONE

@metadata_processor
def sudo(metadata):
    if node.has_bundle('sudo') and node.has_bundle('smartmontools'):
        metadata.setdefault('sudo', {})
        metadata['sudo'].setdefault('extras', {})
        metadata['sudo']['extras'].setdefault(
            'smartctl',
            'telegraf ALL=(ALL) NOPASSWD: /usr/sbin/smartctl',
        )

    return metadata, DONE

@metadata_processor
def pip(metadata):
    if node.has_bundle('python') and node.has_bundle('xmr-stak'):
        metadata.setdefault('python', {})
        metadata['python'].setdefault('pip_packages', [])
        for package in ['requests']:
            if package not in metadata['python']['pip_packages']:
                metadata['python']['pip_packages'].append(package)
    return metadata, DONE
