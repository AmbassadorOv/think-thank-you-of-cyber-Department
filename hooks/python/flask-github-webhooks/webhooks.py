import logging
import time
from sys import stderr, hexversion
import hmac
from json import loads, dumps
from subprocess import Popen, PIPE
from tempfile import mkstemp
from os import access, X_OK, remove, fdopen
from os.path import isfile, abspath, normpath, dirname, join, basename

import requests
from ipaddress import ip_address, ip_network
from flask import Flask, request, abort

logging.basicConfig(stream=stderr)

application = Flask(__name__)

# Load the config file once at startup to avoid redundant disk I/O on every request
PATH = normpath(abspath(dirname(__file__)))
CONFIG = {}
try:
    with open(join(PATH, 'config.json'), 'r') as cfg:
        CONFIG = loads(cfg.read())
except FileNotFoundError:
    logging.warning("config.json not found, using defaults")

# In-memory cache for GitHub IP whitelist to avoid redundant network requests
GHP_IP_CACHE = {
    'networks': None,
    'last_updated': 0
}
CACHE_TTL = 86400  # 24 hours (GitHub IPs don't change frequently)


def get_github_networks():
    """
    Fetch and cache GitHub's IP whitelist, pre-parsing them into network objects.
    """
    now = time.time()
    if GHP_IP_CACHE['networks'] is None or now - GHP_IP_CACHE['last_updated'] > CACHE_TTL:
        try:
            # Performance optimization: avoids ~0.6s network request on every call
            whitelist = requests.get('https://api.github.com/meta').json()['hooks']
            GHP_IP_CACHE['networks'] = [ip_network(u'{}'.format(ip)) for ip in whitelist]
            GHP_IP_CACHE['last_updated'] = now
        except Exception as e:
            if GHP_IP_CACHE['networks'] is None:
                raise e
            logging.error("Failed to refresh GitHub IP whitelist: {}".format(e))
    return GHP_IP_CACHE['networks']


@application.route('/', methods=['GET', 'POST'])
def index():
    """
    Main WSGI application entry.
    """
    # Only POST is implemented
    if request.method != 'POST':
        abort(501, "only POST is supported")

    hooks = CONFIG.get('hooks_path', join(PATH, 'hooks'))
    # Allow Github IPs only
    if CONFIG.get('github_ips_only', True):
        src_ip = ip_address(u'{}'.format(request.remote_addr))
        networks = get_github_networks()

        for network in networks:
            if src_ip in network:
                break
        else:
            abort(403, "Unable to validate source IP")

    # Enforce secret, so not just anybody can trigger these hooks
    secret = CONFIG.get('enforce_secret', '')
    if secret:
        # Only SHA1 is supported
        header_signature = request.headers.get('X-Hub-Signature')
        if header_signature is None:
            abort(403, "No header signature found")

        sha_name, signature = header_signature.split('=')
        if sha_name != 'sha1':
            abort(501, "Only SHA1 is supported")

        # HMAC requires the key to be bytes. In Python 3, we must encode the string.
        secret_bytes = secret.encode('utf-8') if isinstance(secret, str) else secret
        mac = hmac.new(secret_bytes, msg=request.data, digestmod='sha1')

        # Python does not have hmac.compare_digest prior to 2.7.7
        if hexversion >= 0x020707F0:
            if not hmac.compare_digest(str(mac.hexdigest()), str(signature)):
                abort(403)
        else:
            # What compare_digest provides is protection against timing
            # attacks; we can live without this protection for a web-based
            # application
            if not str(mac.hexdigest()) == str(signature):
                abort(403)

    # Implement ping
    event = request.headers.get('X-GitHub-Event', 'ping')
    if event == 'ping':
        return dumps({'msg': 'pong'})

    # Gather data
    try:
        payload = request.get_json()
    except Exception:
        logging.warning('Request parsing failed')
        abort(400, "Request parsing failed")

    # Determining the branch can be tricky, as it only appears for certain event
    # types, and at different levels
    branch = None
    try:
        # Case 1: a ref_type indicates the type of ref.
        # This true for create and delete events.
        if 'ref_type' in payload:
            if payload['ref_type'] == 'branch':
                branch = payload['ref']

        # Case 2: a pull_request object is involved. This is pull_request and
        # pull_request_review_comment events.
        elif 'pull_request' in payload:
            # This is the TARGET branch for the pull-request, not the source
            # branch
            branch = payload['pull_request']['base']['ref']

        elif event in ['push']:
            # Push events provide a full Git ref in 'ref' and not a 'ref_type'.
            branch = payload['ref'].split('/', 2)[2]

    except KeyError:
        # If the payload structure isn't what we expect, we'll live without
        # the branch name
        pass

    # All current events have a repository, but some legacy events do not,
    # so let's be safe
    name = payload['repository']['name'] if 'repository' in payload else None
    meta = {
        'name': name,
        'branch': branch,
        'event': event
    }
    logging.info('Metadata:\n{}'.format(dumps(meta)))
    # Skip push-delete
    if event == 'push' and payload['deleted']:
        logging.info('Skipping push-delete event for {}'.format(dumps(meta)))
        return dumps({'status': 'skipped'})

    # Possible hooks
    scripts = []
    if branch and name:
        scripts.append(join(hooks, '{event}-{name}-{branch}'.format(**meta)))
    if name:
        scripts.append(join(hooks, '{event}-{name}'.format(**meta)))
    scripts.append(join(hooks, '{event}'.format(**meta)))
    scripts.append(join(hooks, 'all'))

    # Check permissions
    scripts = [s for s in scripts if isfile(s) and access(s, X_OK)]
    if not scripts:
        return dumps({'status': 'nop'})

    # Save payload to temporal file
    osfd, tmpfile = mkstemp()
    with fdopen(osfd, 'w') as pf:
        pf.write(dumps(payload))

    # Run scripts
    ran = {}
    for s in scripts:
        proc = Popen(
            [s, tmpfile, event],
            stdout=PIPE, stderr=PIPE
        )
        stdout, stderr = proc.communicate()
        ran[basename(s)] = {
            'returncode': proc.returncode,
            'stdout': stdout.decode('utf-8'),
            'stderr': stderr.decode('utf-8'),
        }
        # Log errors if a hook failed
        if proc.returncode != 0:
            logging.error('{} : {} \n{}'.format(
                s, proc.returncode, stderr
            ))

    # Remove temporal file
    remove(tmpfile)
    info = CONFIG.get('return_scripts_info', False)
    if not info:
        return dumps({'status': 'done'})

    output = dumps(ran, sort_keys=True, indent=4)
    logging.info(output)
    return output


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0')
