from PIL import Image, ExifTags
from uuid import uuid4
import cStringIO
from google.cloud import storage
from app import app

def google_storage_upload(source_file):
    # Rotate it properly
    image_buffer = cStringIO.StringIO(source_file.read())
    fixed_image_buffer = fix_image_rotation(image_buffer)

    # Connect to google cloud datastore and upload file
    fixed_image_buffer.seek(0)
    client = storage.Client()
    bucket = client.get_bucket(app.config['CLOUD_STORAGE_BUCKET'])
    name = str(uuid4())
    blob = bucket.blob(name)
    blob.upload_from_string(fixed_image_buffer.read())
    blob.make_public()

    return app.config['CLOUD_STORAGE_URL'] + '/' + name

def fix_image_rotation(image_buffer):
    try:
        image = Image.open(image_buffer)
        orientation = None
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
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
