from . import app
from .models import *
import base64


image_folder = app.config['IMAGE_FOLDER']


# category(user, post)とファイル名を受け取り、画像のbase64エンコードを返す関数
def getImage(category: str, filename: str) -> object:
    if not category in ['post', 'user']:
        message = "invalid category " + category
        return {"result": "error", "message": message}

    extension = filename.split('.')[-1]
    if not extension in ['jpg', 'jpeg', 'png', 'gif', 'svg', 'JPG', 'JPEG', 'PNG', 'GIF', 'SVG']:
        message = "invalid extenstion of " + filename
        return {"result": "error", "message": message}

    path = "{}/{}/{}".format(image_folder, category, filename)
    try:
        with open(path, 'rb') as f:
            img_base64 = "data:image/{};base64,{}".\
                format(extension, base64.b64encode(f.read()).decode('utf-8'))

    except BaseException as e:
        print(e)
        return {"result": "error", "message": "not found image"}

    return img_base64


# 画像を保存するAPI written by Keisuke Toyoda
def saveImage(base64image: str, category: str, filename: str, ext: str):
    """
    :param base65file:input image data, base64でエンコードされたやつ
    :param filename: 保存するときのファイル名
    :param ext; 拡張子
    :return:
    """

    i = 7
    for i in range(7, len(base64image)):
        if base64image[i - 7:i] == "base64,":
            break

    base64image = base64image[i::]

    try:
        rowimage = base64.b64decode(base64image)
    except BaseException:
        return "error: decode error"

    path = "{}/{}/{}.{}".format(image_folder, category, filename, ext)

    try:
        with open(path, 'wb') as f:
            f.write(rowimage)
    except BaseException as e:
        return "failed"

    return "success"


# いいね数を取得する関数 (Tomofumi Kondo)
def countLike(post_id):
    if not post_id > 0:
        return "invalid post_id"

    count_like = len(
        db.session.query(Like.post_id).
        filter(Like.post_id == post_id).all()
    )

    return count_like
