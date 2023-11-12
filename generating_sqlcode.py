import os,sys, sqlitescripting
import sqlacodegen.main  as sqlcodegen_main

#https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/quickstart/

base_sqlite = 'DataBase_Modeler.sql'
output_db = 'DataBase_Modeler.db'
output_file = 'DataBase_Modeler.py'

sqlitescripting.execute_scripts(output_db, base_sqlite)

base_string = str(
	'--outfile {1} sqlite:///{0}'.format(
	output_db,output_file
))

for x in [
	'{0} -m pip install --upgrade flask-sqlacodegen'.format(sys.executable),
	'{0} -m sqlacodegen.main --flask {1}'.format(sys.executable, base_string),
]:
	os.system(x)

table_string = None
tables = []

if os.path.exists(output_file):
	from fileinput import FileInput as finput
	with finput(output_file,inplace=True) as foil:
		for line in foil:
			if ' = db.Table(' in line:
				tables += [
					line.replace(' = db.Table(','').strip()
				]

			print(line,end='')

		table_string = '\nAllTables = [{0}]'.format(','.join(tables))
		print(table_string)

views = [
	x.replace('t_','').lower() for x in tables
]

if table_string is not None:
	if os.path.exists('DataBase.py'):
		os.remove('DataBase.py')
	with open('DataBase.py','a+') as writer:
		app = lambda x:writer.write(x+'\n')
		app("""#!/usr/bin/env python3
##region Imports
import os,sys,base64,json,xcyl,threading
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from flask_openapi3 import OpenAPI, Tag, Info, APIView
from flask import make_response

if sys.version_info[0] < 3:
	from StringIO import StringIO
else:
	from io import StringIO
try:
	import pandas as pd,pytz
except:
	[os.system("{0} -m pip install --upgrade {1} >/dev/null".format(sys.executable, x)) for x in ['pandas', 'pytz']]
	import pandas as pd,pytz
##endregion
##region prep_lambdas
def internal_wrap(data):
	return base64.b64encode(bytes(data.to_json(), 'utf-8'))
def internal_unwrap(data):
	return pd.read_json(StringIO(base64.b64decode(data).decode('utf-8')))

internal_from_input = lambda data: internal_unwrap(bytes(os.fsencode(data)))
external_unwrap = lambda data: pd.DataFrame.from_dict([json.load(StringIO(data[0].data.decode('utf-8')))])

eastern,eastern_to_utc,date_format = pytz.timezone('US/Eastern'), lambda x:x.astimezone(pytz.utc), "%Y-%m-%dT%H:%M:%S"
date_print = lambda x: str(x.strftime(date_format))

get_now = lambda: datetime.now(eastern);nice_now = lambda: date_print(get_now())
##endregion
##region Global Information
sqlite_name, base_table_name, core_port,sem = "cryptolation_run.sqlite", "current_running", 8899, threading.Semaphore()
info = Info(title='Testing API', version='0.0.0')
app = OpenAPI(__name__, info=info)
##endregion
""")
		#app(""+table_string)
		for table,view in zip(tables,views):
			app("##region {0}".format(view))
			app("""{0}_view = APIView(url_prefix="/{0}",view_tags=[Tag(name="{0}", description="Auto Generating Stuff")])""".format(view))
			app("""@{0}_view.route("/")
class {1}:
	table = "{0}"

	@{0}_view.doc(summary="Auto generated summary")
	def get(self):
		global sem
		with xcyl.sqlobj(sqlite_name, threadLock=sem) as sql:
			tabel = sql.load_table(self.table)
			raw_output = tabel.to_json()
			data = internal_wrap(tabel)
		return {{
			"code":0,
			"message":True,
			"data":data,
			"raw_data":None
		}}

	@{0}_view.doc(summary="Auto generated summary")
	def post(self):
		global sem
		\"\"\"
		Sample Post used in the request
		:post(self, form:BasePost)

		class BasePost(BaseModel):
			data: Optional[str] = Field(None, description="The wrapped pandas frame")
			uuid: Optional[str] = Field(None, description='The UUID Number of the scan')
		\"\"\"

		with xcyl.sqlobj(sqlite_name, threadLock=sem) as sql:
			if self.table in sql.table_names():
				data['idx'] = int(len(sql.load_table(self.table).index))
			else:
				data['idx'] = 0

			data = pd.DataFrame.from_dict([data])

			data.to_sql(self.table, sql.connection, if_exists='append')
		return {{
			"code":0,
			"message":True,
			"data":True,
			"raw_data":None
		}}
\n\n""".format(view, view.title()))
			app("##endregion")

		app('')
		app("views = [{0}_view]".format('_view,'.join(views)))
		app("""[app.register_api_view(x) for x in views]

if "--server" in ' '.join(sys.argv):
	app.run(debug=True, port=core_port, host='0.0.0.0',use_reloader=True)

def client(ipaddress):
	global core_port;import hugg
	utils = hugg.face('frantzme/TBD','')
	zip_location = utils['python-client-generated.zip']
	sys.path.insert(0, zip_location)

	import swagger_client as crypto_test

	config = crypto_test.configuration.Configuration()
	config.host = "http://{0}:{1}".format(ipaddress,core_port)
	apiclient = crypto_test.ApiClient(config)
	crypto_test.myapi = apiclient
	crypto_test.args =  {
	    '_return_http_data_only':False,
	    '_preload_content':False
	}

	def new_args(kwargs):
	    base = {
	        '_return_http_data_only':False,
	        '_preload_content':False
	    }

	    for key,value in kwargs.items():
	        base[key] = value

	    return base


	crypto_test.new_args = new_args
	return crypto_test
""")

##Generate the views using Swagger.io
##https://app.swaggerhub.com/welcome
