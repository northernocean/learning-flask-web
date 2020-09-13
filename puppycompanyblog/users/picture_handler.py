import os
from PIL import Image
from flask import current_app


def add_profile_image(image_to_upload: str, username: str) -> str:

    filename, file_extension = os.path.splitext(os.path.basename(image_to_upload.filename))
    new_filepath = os.path.join(current_app.root_path, "static",
                                "profile_images", username + file_extension)

    picture = Image.open(image_to_upload)
    picture.thumbnail((200, 200))
    picture.save(new_filepath)

    return os.path.basename(new_filepath)
