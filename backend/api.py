from flask import Blueprint, jsonify, request
from sqlalchemy import or_, func
from .models import db
from .models import *
from .util import *
import datetime
import uuid

api = Blueprint('api', __name__)


# 検索結果を返すAPI
@api.route("/result", methods=["GET"])
def retrieval_result():
    keyword = None
    transportation = None
    stayed_date = None

    # GETメソッドで値をもらうようにしました (Shingo Watanabe)
    args = request.args
    for key, value in args.items():

        if "keyword" == key:
            keyword = value

            if keyword == "":
                keyword = None

        if "transportation" == key:
            if value == "":
                transportation = None
            else:
                transportation = value

        if "stayed_date" == key:
            if value == "":
                stayed_date = None
            else:
                stayed_date = value

    post_list = db.session.query(Post).\
        join(Schedule, Post.id == Schedule.post_id)

    if keyword is not None:
        post_list = post_list.filter(or_(
            Post.post_name.like("%" + keyword + "%"),
            Schedule.title.like("%" + keyword + "%"),))

    if transportation is not None:
        post_list = post_list.filter(
            Post.transportation_flag == transportation)

    if stayed_date is not None:
        post_list = post_list.filter(Post.period == stayed_date)

    post_list = post_list.order_by(db.desc(Post.id)).all()

    post_dict = [post.to_dict() for post in post_list]

    for post in post_dict:
        image_base64 = getImage("post", post['image_name'])
        post['image_base64'] = image_base64

        count_like = countLike(post["id"])
        post["count_like"] = count_like

    return jsonify(post_dict)


# トップページに投稿の一覧を返すAPI (Shingo Watanabe)
@api.route("/posts")
def get_top_posts():
    # クエリでlimitが指定されていたらその数の投稿データを返す
    limit = request.args.get("limit", default=100, type=int)

    top_post_list = db.session.query(Post).\
        order_by(db.desc(Post.id)).\
        limit(limit).\
        all()

    top_post_dict = [post.to_dict() for post in top_post_list]
    for post in top_post_dict:
        image_base64 = getImage("post", post['image_name'])
        post['image_base64'] = image_base64

        count_like = countLike(post["id"])
        post["count_like"] = count_like

    return jsonify(top_post_dict)


# user_name or user_idを指定するとその人の投稿一覧を返すAPI written by Keisuke Toyoda
@api.route("/getpersonalposts", methods=["GET"])
def get_personal_posts():
    user_id = -1
    user_name = ""
    user_id = request.args.get("user_id", default=-1, type=int)
    user_name = request.args.get("user_name", default="", type=str)

    if user_id == -1 and user_name == "":
        return "error: not found user"

    if user_id == -1:
        user_id = db.session.query(
            User.id).filter(
            User.user_name == user_name).all()
        if len(user_id) == 0:
            return "error: not found user"
        user_id = user_id[0]

    personal_posts = db.session.query(Post).\
        filter(Post.user_id == user_id).\
        all()

    personal_posts_dic = [post.to_dict() for post in personal_posts]

    for post in personal_posts_dic:
        image_base64 = getImage("post", post['image_name'])
        post['image_base64'] = image_base64

        count_like = countLike(post["id"])
        post["count_like"] = count_like

    return jsonify(personal_posts_dic)
    # return str(user_id)


# コメント一覧を取得するAPI written by Keisuke Toyoda
@api.route("/allcomments")
def get_all_comment():
    comment_list = db.session.query(Comment).all()

    comment_dict = [post.to_dict() for post in comment_list]
    return jsonify(comment_dict)


# コメントを追加するAPI written by Keisuke Toyoda
@api.route("/addcomment", methods=["POST"])
def add_comment():
    commenter_id = -1
    commenter_name = ""
    comment = ""
    post_id = -1
    if "commenter_id" in request.form:
        commenter_id = int(request.form["commenter_id"])
    elif "commenter_name" in request.form:
        commenter_name = request.form["commenter_name"]
        commenter_id = db.session.query(
            User.id).filter(
            User.user_name == commenter_name).all()
        if len(commenter_id) == 0:
            return "error:not found user"
        commenter_id = commenter_id[0]

    if "post_id" in request.form:
        post_id = request.form["post_id"]
    elif "post_name" in request.form:
        post_name = request.form["post_name"]
        post_id = db.session.query(
            Post.id).filter(
            Post.name == post_name).all()
        if len(post_name) == 0:
            return "error: not found post"
        post_id = post_id[0]

    if len(db.session.query(Post).filter(Post.id == post_id).all()) == 0:
        return "error: not found post"

    if "comment" in request.form:
        comment = request.form["comment"]

    if (commenter_id == -1 and commenter_name == "") or comment == "":
        return "error:not enough information"

    comment_date = datetime.datetime.now()

    comment_data = [Comment(
        commenter_id=commenter_id,
        comment_time=comment_date,
        comment=comment,
        post_id=post_id
    )]

    db.session.add_all(comment_data)
    db.session.commit()

    return "added comment"


# 指定した投稿を取得するAPI written by Keisuke Toyoda
@api.route("/getpost", methods=["GET"])
def get_a_post():
    post_id = request.args.get("post_id", default=-1, type=int)
    post_name = request.args.get("post_name", default="", type=str)
    post_user = request.args.get("post_user", default="", type=str)
    post = {}

    if post_id == -1 and post_name == "" and post_user == "":
        return "error: not inputed post information"

    if post_id != -1:
        post = db.session.query(Post).\
            filter(Post.id == post_id).\
            all()
    elif post_name != "":
        post = db.session.query(Post).\
            filter(Post.post_name == post_name).\
            all()
    elif post_user != "":
        user_id = db.session.query(User.id).\
            filter(User.user_name == post_user).\
            all()
        if len(user_id) == 0:
            return {}
        post = db.session.query(Post).\
            filter(Post.user_id == user_id).\
            limit(1).\
            all()

    if post == {} or len(post) == 0:
        return {}

    post = post[0].to_dict()

    if post_name == "":
        post_name = db.session.query(Post.post_name).filter(Post.id == post_id)

    if post_user == "":
        post_user = db.session.query(
            User.user_name).filter(
            User.id == post["user_id"])

    post_name = post_name[0]
    post["post_name"] = post_name[0]
    post_user = post_user[0]
    post["user_name"] = post_user[0]

    image_base64 = getImage("post", post['image_name'])
    post['image_base64'] = image_base64

    schedules = db.session.query(Schedule).\
        filter(Schedule.post_id == post["id"]).\
        all()

    schedules_dict = [schedule.to_dict() for schedule in schedules]

    for i in range(len(schedules_dict)):
        start_time = schedules_dict[i]["start_time"]
        schedules_dict[i]["start_year"] = start_time.year
        schedules_dict[i]["start_month"] = start_time.month
        schedules_dict[i]["start_date"] = start_time.day
        schedules_dict[i]["start_hour"] = start_time.hour
        schedules_dict[i]["start_min"] = start_time.minute

        end_time = schedules_dict[i]["end_time"]
        schedules_dict[i]["end_year"] = end_time.year
        schedules_dict[i]["end_month"] = end_time.month
        schedules_dict[i]["end_date"] = end_time.day
        schedules_dict[i]["end_hour"] = end_time.hour
        schedules_dict[i]["end_min"] = end_time.minute

        if schedules_dict[i]['longitude'] == float(1000):
            schedules_dict[i]['longitude'] = ""
            schedules_dict[i]['latitude'] = ""

    return jsonify({"post_information": post,
                    "schedule_information": schedules_dict})
# ここまでwritten by KeisukeToyoda


# コメントを取得するする written by Keisuke Toyoda
@api.route("/getcomments", methods=["GET"])
def get_comments():
    """
    post_nameかpost_idをパラメータで渡すと、その記事についているコメント一覧をjson形式で返す
    :return:
    """
    post_id = request.args.get("post_id", default=-1, type=int)
    post_name = request.args.get("post_name", default="", type=str)

    if post_id == -1 and post_name == "":
        return {}

    if post_id == -1:
        post_id = db.session.query(Post.id).\
            filter(Post.post_name == post_name).\
            all()

    comments = db.session.query(Comment).\
        filter(Comment.post_id == post_id).\
        all()

    comments_list = [comment.to_dict() for comment in comments]
    for comment in comments_list:
        commenter_name = db.session.query(User.user_name).\
            filter(User.id == comment['commenter_id']).\
            all()

        if commenter_name is not None:
            comment['commenter_name'] = commenter_name[0][0]
        else:
            comment['commenter_name'] = "no member"

    if not len(comments_list):
        return {}

    return jsonify(comments_list)


# いいね機能 written by Keisuke Toyoda
@api.route("/toggleLike", methods=["POST"])
def toggleLike():
    if "post_id" in request.form:
        post_id = request.form["post_id"]
    else:
        return "not sent post_id"

    if 'liker_name' in request.form:
        liker_name = request.form["liker_name"]
        liker_id = db.session.query(User.id)\
            .filter(User.user_name == liker_name)\
            .first()
    else:
        return "not sent liker_name"

    if len(db.session.query(Post.id).filter(Post.id == post_id).all()) == 0:
        return "not found post"

    if len(db.session.query(User.id).filter(User.id == liker_id).all()) == 0:
        return "not found liker"

    already_like = db.session.query(Like).\
        filter(Like.liker_id == liker_id, Like.post_id == post_id)\
        .all()

    # いいねを解除する場合
    if len(already_like) > 0:
        db.session.delete(already_like[0])
        db.session.commit()

        return "remove like"

    # いいねを登録する場合
    else:
        new_like = Like(
            liker_id=liker_id,
            post_id=post_id
        )

        db.session.add(new_like)
        db.session.commit()

        return "add like"


# 新規登録用API written by Keisuke Toyoda
@api.route("/registration", methods=["POST"])
def new_regstration():
    if "name" in request.form:
        user_name = request.form["name"]
    else:
        return "error: not found name"

    if len(db.session.query(User.user_name).filter(
            User.user_name == user_name).all()) != 0:
        return "this user name is exist"

    if "email" in request.form:
        user_email = request.form["email"]
    else:
        return "error: not found email"

    if len(db.session.query(User.user_name).filter(
            User.e_mail == user_email).all()) != 0:
        return "this email address is exist"

    if "password" in request.form:
        password = request.form["password"]
    else:
        return "error: not found password"

    user_data = [User(
        e_mail=user_email,
        user_name=user_name,
        password=password
    )]

    db.session.add_all(user_data)
    db.session.commit()

    return "complete registration"


# login認証をするAPI written by Keisuke Toyoda
@api.route("/login", methods=["POST"])
def login():
    user_email = ""
    password = ""
    if "email" in request.form:
        user_email = request.form["email"]
    else:
        return "error: not found email"

    if "password" in request.form:
        password = request.form["password"]
    else:
        return "error: not found password"

    user_name = db.session.query(
        User.user_name).filter(
        User.e_mail == user_email,
        User.password == password).all()
    if len(user_name) == 0:
        return "permission denied"

    user_name = user_name[0][0]
    return str(user_name)


#　ここからスケジュールや投稿全体を登録するAPIのための関数 (Shingo Watanabe)
#　登録するためのフラグなどを立てる関数 (Shingo Watanabe)
def calc_flag():
    data = request.get_json()
    post_data = data['post_information']
    schedule_data = data['schedule_information']

    period_list = []
    transportation_list = []
    index = 0
    time_info = None

    for schedule in schedule_data:
        start_time = datetime.datetime(
            int(schedule['start_year']), int(
                schedule['start_month']), int(schedule['start_date']),
            int(schedule['start_hour']), int(schedule['start_min']))

        end_time = datetime.datetime(
            int(schedule['end_year']), int(
                schedule['end_month']), int(schedule['end_date']),
            int(schedule['end_hour']), int(schedule['end_min']))

        period_list.append(start_time)
        period_list.append(end_time)

        if index == 0:
            time_info = datetime.date(int(schedule['start_year']), int(
                schedule['start_month']), int(schedule['start_date']))
        index += 1

        transportation_list.append(schedule['transportation'])

    traveled_flag = 0
    if len(period_list) >= 2:
        period = (period_list[-1] - period_list[0]).days
        if time_info < datetime.date.today():
            traveled_flag = 1
    else:
        period = 0
        if time_info < datetime.date.today():
            traveled_flag = 1

    car = '車'
    transportation_flag = 1
    for transportation in transportation_list:
        if transportation == car:
            transportation_flag = 0

    return [traveled_flag, transportation_flag, period]


# user_nameからuser_idを返す関数 (Shingo Watanabe)
def user_check():
    data = request.get_json()
    post_data = data['post_information']
    user_name = post_data['user_name']

    user_id = db.session.query(
        User.id).filter(
        User.user_name == user_name).all()
    if not user_id:
        return "Not found user"
    else:
        user_id = user_id[0][0]

    return user_id


# データを挿入するためのリストを作成する関数 (Shingo Watanabe)
def create_insert_list():
    data = request.get_json()
    post_data = data['post_information']
    schedule_data = data['schedule_information']
    traveled_flag = calc_flag()[0]
    transportation_flag = calc_flag()[1]
    period = calc_flag()[2]
    user_id = user_check()

    if not 'image' in post_data:
        to_post_insert = [
            {
                'user_id': user_id,
                # 'user_name': post_data['user_name'],
                'post_name': post_data['post_name'],
                'content': post_data['content'],
                'posted_date': datetime.date.today(),
                'traveled_flag': traveled_flag,
                'transportation_flag': transportation_flag,
                'period': period,
                'image_name': "default.jpeg"
            }
        ]
    else:
        extension = list(post_data['image_name'].split('.'))[-1]
        image_name = str(uuid.uuid4())
        if saveImage(post_data['image'], 'post',
                     image_name, extension) == "success":
            to_post_insert = [
                {
                    'user_id': user_id,
                    # 'user_name': post_data['user_name'],
                    'post_name': post_data['post_name'],
                    'content': post_data['content'],
                    'posted_date': datetime.date.today(),
                    'traveled_flag': traveled_flag,
                    'transportation_flag': transportation_flag,
                    'period': period,
                    'image_name': image_name + '.' + extension
                }
            ]
        else:
            to_post_insert = [
                {
                    'user_id': user_id,
                    # 'user_name': post_data['user_name'],
                    'post_name': post_data['post_name'],
                    'content': post_data['content'],
                    'posted_date': datetime.date.today(),
                    'traveled_flag': traveled_flag,
                    'transportation_flag': transportation_flag,
                    'period': period,
                    'image_name': "default.jpeg"
                }
            ]

    post_id = -1
    to_schedule_insert = []
    for schedule in schedule_data:
        # 位置情報が登録されていないデータを受け取るときの処理 (マップ上にピンが立たないように存在しない値を入れておく)
        if schedule['latitude'] == "" or schedule['longitude'] == "":
            schedule['latitude'] = float(1000)
            schedule['longitude'] = float(1000)
        if 'memo' in schedule:
            memo = schedule['memo']
        else:
            memo = ''
        to_schedule_insert.append(
            {
                'post_id': post_id,
                'title': schedule['title'],
                'latitude': float(schedule['latitude']),
                'longitude': float(schedule['longitude']),
                'start_time': datetime.datetime(
                    int(schedule['start_year']), int(
                        schedule['start_month']), int(schedule['start_date']),
                    int(schedule['start_hour']), int(schedule['start_min'])
                ),
                'end_time': datetime.datetime(
                    int(schedule['end_year']), int(
                        schedule['end_month']), int(schedule['end_date']),
                    int(schedule['end_hour']), int(schedule['end_min'])
                ),
                'transportation': schedule['transportation'],
                'memo': memo
            }
        )

    return [to_post_insert, to_schedule_insert]


# スケジュールや投稿全体を登録するAPI (Shingo Watanabe)
@api.route("/postschedule", methods=["POST"])
def register_schedule():
    to_post_insert, to_schedule_insert = create_insert_list()

    db.session.execute(Post.__table__.insert(), to_post_insert)
    db.session.commit()

    post_id = db.session.query(Post.id).\
        order_by(db.desc(Post.id)).\
        limit(1).\
        all()[0][0]

    for schedule in to_schedule_insert:
        schedule['post_id'] = post_id
        db.session.execute(Schedule.__table__.insert(), schedule)
        db.session.commit()

    return "Suceeded!"


# 投稿を削除するAPI (Shingo Watanabe)
@api.route("/postdelete", methods=["POST"])
def delete_post():
    post_id = request.form["post_id"]
    user_name = request.form["user_name"]

    user_id = db.session.query(
        User.id).filter(
        User.user_name == user_name).all()
    if not user_id:
        return "Not found user"
    else:
        user_id = user_id[0][0]

    post_id = db.session.query(
        Post.id).filter(
        Post.id == post_id,
        Post.user_id == user_id).all()
    if not post_id:
        return "error: posted user and deleted user are not same."
    post_id = post_id[0][0]

    schedule_delete_querys = db.session.query(
        Schedule).filter(Schedule.post_id == post_id).all()
    for query in schedule_delete_querys:
        db.session.delete(query)
        db.session.commit()

    post_delete_query = db.session.query(
        Post).filter(Post.id == post_id).first()
    db.session.delete(post_delete_query)
    db.session.commit()

    return "Deleted"


# 投稿を編集するAPI (Shingo Watanabe)
@api.route("/postedit", methods=["POST"])
def edit_post():
    data = request.get_json()
    post_data = data['post_information']
    schedule_data = data['schedule_information']

    post_id = post_data['post_id']
    user_name = post_data['user_name']
    user_id = db.session.query(
        User.id).filter(
        User.user_name == user_name).all()
    if not user_id:
        return "Not found user"
    else:
        user_id = user_id[0][0]

    traveled_flag = calc_flag()[0]
    transportation_flag = calc_flag()[1]
    period = calc_flag()[2]

    check = db.session.query(Post).filter(
        Post.id == post_id, Post.user_id == user_id).all()
    if len(check) == 0:
        return "error: posted user and edit user are not same. "

    schedule_delete_querys = db.session.query(
        Schedule).filter(Schedule.post_id == post_id).all()
    for query in schedule_delete_querys:
        db.session.delete(query)
        db.session.commit()

    post_delete_query = db.session.query(
        Post).filter(Post.id == post_id).first()
    db.session.delete(post_delete_query)
    db.session.commit()

    to_post_insert = create_insert_list()[0]
    to_schedule_insert = create_insert_list()[1]

    db.session.execute(Post.__table__.insert(), to_post_insert)
    db.session.commit()

    new_post_id = db.session.query(Post.id).\
        order_by(db.desc(Post.id)).\
        limit(1).\
        all()[0][0]

    for schedule in to_schedule_insert:
        schedule['post_id'] = new_post_id
        db.session.execute(Schedule.__table__.insert(), schedule)
        db.session.commit()

    return "Updated"
