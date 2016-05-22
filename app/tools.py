import boto
import os.path
from uuid import uuid4
from flask import current_app as app
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
from config import basedir
import cStringIO

def s3_upload(source_file, acl='public-read'):
    source_filename = secure_filename(source_file.filename)
    source_extension = os.path.splitext(source_filename)[1]
    # Rotate it properly
    image_buffer = cStringIO.StringIO(source_file.read())
    fixed_image_buffer = fix_image_rotation(image_buffer)

    destination_filename = uuid4().hex + source_extension

    # Connect to S3 and upload file
    conn = boto.connect_s3(app.config["AWS_ACCESS_KEY_ID"], app.config["AWS_SECRET_ACCESS_KEY"])
    b = conn.get_bucket(app.config["S3_BUCKET_NAME"])

    key = b.new_key("/".join([app.config["S3_UPLOAD_DIRECTORY"], destination_filename]))
    fixed_image_buffer.seek(0)
    key.set_contents_from_string(fixed_image_buffer.read())
    key.set_acl(acl)
    url = key.generate_url(expires_in=0, query_auth=False)

    return url

def fix_image_rotation(image_buffer):
    try:
        image = Image.open(image_buffer)
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif = dict(image._getexif().items())

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
        output = cStringIO.StringIO()
        image.save(output, format="JPEG")
        image.close()
        return output

    except (AttributeError, KeyError, IndexError) as e:
        # cases: image don't have getexif
        return image_buffer
