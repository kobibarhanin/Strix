from flask import Flask
import os
import pymongo

from api.submitter import submitter_api
from api.executor import executor_api
from api.orchestrator import orchestrator_api
from api.infra import infra_api
from api.common import common_api
from infra.utils import set_global

app = Flask(__name__)
app.register_blueprint(submitter_api)
app.register_blueprint(executor_api)
app.register_blueprint(orchestrator_api)
app.register_blueprint(infra_api)
app.register_blueprint(common_api)

set_global('agent_name', os.environ['AGENT_NAME'])
set_global('agent_url', os.environ['AGENT_URL'])
port = os.environ['PORT'] if 'PORT' in os.environ else '5000'
set_global('agent_port', port)
set_global('agent_status', 'connected')
set_global('tracker_host', os.environ['TRACKER_HOST'] if 'TRACKER_HOST' in os.environ else 'tracker')

# TODO >> MIGRATION
db_global = pymongo.MongoClient(f'mongodb://{os.environ["DB_HOST"]}:27017/')['agent']['global']
global_entry = {
        'type': 'properties',
        'agent_name': os.environ['AGENT_NAME'],
        'agent_url': os.environ['AGENT_URL'],
        'agent_port': port,
        'agent_status': 'connected',
        'tracker_host': os.environ['TRACKER_HOST'] if 'TRACKER_HOST' in os.environ else 'tracker'
}
db_global.update({'type': 'properties'}, global_entry, upsert=True)

app.run(debug=True, host='0.0.0.0', port=port)
