import boto
import os.path
from uuid import uuid4
from flask import current_app as app
from werkzeug.utils import secure_filename

def s3_upload(source_file, acl='public-read'):
	source_filename = secure_filename(source_file.data.filename)
	source_extension = os.path.splitext(source_filename)[1]
	destination_filename = uuid4().hex + source_extension

	# Connect to S3 and upload file
	conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], app.config["AWS_SECRET_ACCESS_KEY"])
	b = conn.get_bucket(app.config["S3_BUCKET_NAME"])

	key = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"], destination_filename]))
	key.set_contents_from_string(source_file.data.read())
	key.set_acl(acl)
	url = key.generate_url(expires_in=0, query_auth=False)

	return url
