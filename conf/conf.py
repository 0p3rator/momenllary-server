api_host = 'http://10.2.131.240:3000'

api_username = "jingwei@momenta.ai"
api_password = "zuojingwei"


api_host = 'http://mapeditor.momenta.works'

api_username = "jingwei"
api_password = "HDmapjw"

db_host = "10.2.131.240"
db_databaseName= "test"
db_username='jingwei'
db_password='zuo'

db_host = "mapeditor.momenta.works"
db_databaseName= "test"
db_username='postgres'
db_password='zuojingwei'
db_port = 5432

api_headers = {
    'User-Agent': 'bulk_upload_sax.py',
}

api_get_changesets = "/api/0.6/changesets"

api_query_box = '/api/0.6/map?bbox={},{},{},{}'
api_query_changeset = '/api/0.6/changeset/{}/download'
api_delete_element = "/api/0.6/{}/{}" #[node|way|relation]



s3_host="http://s3.momenta.works"
s3_key="2AOP8OZF6542K3ROFD5P"
s3_secret="gR8j2IssVJKm90XWEgz421aispgdQ1Ph8EYIQ59x"