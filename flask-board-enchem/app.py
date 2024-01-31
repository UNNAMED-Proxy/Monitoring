from flask import Flask, render_template, session, url_for, request, redirect, flash, send_file
from datetime import datetime
import os
import pymysql
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
import logging

app = Flask(__name__)
app.secret_key = 'ajkdjfkajdkfdjfhjafkwekk112sdfakfkadfafdf'

def connectsql():
    conn = pymysql.connect(host='localhost', user='root', passwd='enchem135!', db='userlist', charset='utf8')
    return conn

# 게시물 조회수 증가 함수
def increase_view_count(post_id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "UPDATE board SET view = view + 1 WHERE id = %s"
    value = post_id
    try:
        cursor.execute(query, value)
        conn.commit()
        cursor.close()
        conn.close()
        logging.info(f"View count increased for post {post_id}")
    except Exception as e:
        logging.error(f"Error increasing view count: {str(e)}")
        conn.rollback()
        cursor.close()
        conn.close()


# 게시글 세부 정보 가져오기
def fetch_post_content(post_id):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT id, title, content FROM board WHERE id = %s"
    value = post_id
    cursor.execute(query, value)
    post_content = cursor.fetchall()
    conn.close()
    return post_content


# 댓글 삽입
def insert_comment(post_id, username, comment_text):
    conn = connectsql()
    cursor = conn.cursor()
    query = "INSERT INTO comments (post_id, user_name, comment) VALUES (%s, %s, %s)"
    values = (post_id, username, comment_text)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


# 댓글에 대한 게시물 ID를 가져오는 함수 구현
def get_post_id_for_comment(comment_id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "SELECT post_id FROM comments WHERE id = %s"
    value = comment_id
    cursor.execute(query, value)
    post_id = cursor.fetchone()[0]  # 댓글 ID에 대한 게시물 ID가 하나만 있다고 가정합니다
    cursor.close()
    conn.close()
    return post_id


# 댓글 삭제
def delete_comment(id, comment_id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM comments WHERE post_id = %s AND id = %s"
    values = (id, comment_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


# 댓글 가져오기
def fetch_comments(post_id):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = """
        SELECT board.id, board.title, board.content, comments.id as comment_id ,comments.user_name, comments.comment, comments.wdate
        FROM board
        LEFT JOIN comments ON board.id = comments.post_id
        WHERE board.id = %s
    """
    value = post_id
    cursor.execute(query, value)
    comments = cursor.fetchall()
    conn.close()
    # 댓글이 없으면 빈 값으로 리턴 시킨다.
    comments = [
        {
            'id': comment['id'],
            'user_name': comment['user_name'] or '',
            'comment': comment['comment'] or '',
            'wdate': comment['wdate'] or '',
            'comment_id': comment['comment_id'] or ''
        }
        for comment in comments if comment['user_name'] is not None
    ]
    return comments


# 업로드된 파일을 저장할 디렉토리 설정
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 파일 업로드 허용 확장자 설정 (예: 이미지 파일을 업로드하려면 허용되는 확장자를 추가할 수 있습니다.)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


# 허용되는 파일 확장자인지 확인하는 함수
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# DB에서 Major목록을 가져오는 함수
def get_major_list():
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM major"
    cursor.execute(query)
    majors = cursor.fetchall()
    conn.close()
    return majors

# DB에서 Minor목록을 가져오는 함수
def get_minor_list():
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT * FROM minor"
    cursor.execute(query)
    minors = cursor.fetchall()
    conn.close()
    return minors

@app.route('/')
# 세션유지를 통한 로그인 유무 확인
def index():
    if 'username' in session:
        username = session['username']

        return render_template('index.html', logininfo=username)
    else:
        username = None
        return render_template('index.html', logininfo=username)


@app.route('/post')
# board테이블의 게시판 제목리스트 역순으로 출력
def post():
    if 'username' in session:
        username = session['username']
    else:
        username = None
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    query = "SELECT board.id, board.name, board.title, board.wdate, count(comments.comment) comment, board.view, board.post_password FROM board LEFT JOIN comments ON board.id = comments.post_id group by board.id ORDER BY id DESC;"  # ORDER BY 컬럼명 DESC : 역순출력, ASC : 순차출력
    cursor.execute(query)
    post_list = cursor.fetchall()

    # None을 빈 문자열로 처리
    for post in post_list:
        if post['post_password'] is None:
            post['post_password'] = ''

    cursor.close()
    conn.close()

    return render_template('post.html', postlist=post_list, logininfo=username)


# 파일 다운로드 라우트 함수
@app.route('/post/file/<id>')
def download_file(id):
    file_info = get_file_info(id)

    if file_info:
        file_path = file_info['file_path']
        return send_file(file_path, as_attachment=True)
    else:
        return render_template('error.html', error_message='File not found')


# 파일 정보를 가져오는 함수
def get_file_info(id):
    conn = connectsql()
    cursor = conn.cursor(dictionary=True)

    file_query = "SELECT * FROM files WHERE post_id = %s"
    cursor.execute(file_query, id)
    file_info = cursor.fetchone()
    cursor.close()
    conn.close()

    return file_info


# 이전 코멘트를 카운터
def comments_count_before(id):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    comments_count_before_query = "SELECT COUNT(comments.post_id) FROM comments WHERE comments.post_id = %s"
    value = id
    cursor.execute(comments_count_before_query, value)
    comments_count_before = cursor.fetchone()
    conn.close()
    return comments_count_before['COUNT(comments.post_id)']


def comments_count_after(id):
    conn = connectsql()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    comments_count_before_query = "SELECT COUNT(comments.post_id) FROM comments WHERE comments.post_id = %s"
    value = id
    cursor.execute(comments_count_before_query, value)
    comments_count_after = cursor.fetchone()
    conn.close()
    return comments_count_after['COUNT(comments.post_id)']


@app.route('/post/content/<id>', methods=['GET', 'POST'])
def content(id):
    if 'username' in session:
        username = session['username']
        should_increase = request.args.get('should_increase', True)
        comments_after_count = int(request.args.get('comments_after_count', 0))
        comments_before_count = int(request.args.get('comments_before_count', 0))

        # 댓글을 추가하기 전에 게시글 세부 정보(조회수 포함) 가져오기
        post_content_before_comment = fetch_post_content(id)

        # 댓글을 추가한 후에 댓글 가져오기
        comments = fetch_comments(id)

        # 해당 게시물이 비밀번호가 설정되어있는지 체크
        conn = connectsql()
        cursor = conn.cursor()
        post_password_query = "SELECT post_password FROM board WHERE id = %s"
        post_password_value = id
        cursor.execute(post_password_query, post_password_value)
        correct_password = cursor.fetchone()[0]

        # 비밀번호 확인 로직을 추가합니다.
        entered_password = request.form.get('entered_password')

        if ((comments_after_count == comments_before_count + 1) or (comments_after_count + 1 == comments_before_count)):
            return render_template('content.html', content=post_content_before_comment, comments=comments,
                                   username=username)

        if str(entered_password) != str(correct_password):
            # 비밀번호가 일치하지 않는 경우
            return redirect(url_for('password_check', id=id, entered_password=entered_password))

        # Convert 'should_increase' to boolean
        should_increase = str(should_increase).lower() != 'false'

        if should_increase:
            # 조회수 증가
            increase_view_count(id)
        return render_template('content.html', content=post_content_before_comment, comments=comments,
                               username=username)
    else:
        return render_template('Error.html')


# Flask 뷰 함수 수정
@app.route('/password_check/<id>', methods=['GET', 'POST'])
def password_check(id):
    print('/password_check/<id>')
    if 'username' in session:
        username = session['username']
        should_increase = request.args.get('should_increase', True)

        # 해당 게시물이 비밀번호가 설정되어있는지 체크
        conn = connectsql()
        cursor = conn.cursor()
        post_password_query = "SELECT post_password FROM board WHERE id = %s"
        post_password_value = id
        cursor.execute(post_password_query, post_password_value)
        correct_password = cursor.fetchone()[0]
        entered_password = request.form.get('entered_password')

        if request.method == 'POST':  # 변경된 부분
            if str(entered_password) != str(correct_password):
                flash('비밀번호가 일치하지 않습니다. 다시 시도해주세요.', 'error')
            else:
                # Convert 'should_increase' to boolean
                should_increase = str(should_increase).lower() != 'false'

                if should_increase:
                    # 조회수 증가
                    increase_view_count(id)
                # 비밀번호가 일치하는 경우, 해당 게시물 내용 페이지로 이동
                return redirect(url_for('content', id=id, should_increase='false', correct_password=correct_password,
                                        entered_password=entered_password), code=307)

        return render_template('password_check.html', id=id, logininfo=username)
    else:
        return render_template('Error.html'), 200


@app.route('/post/comment/<id>', methods=['GET', 'POST'])
def add_comment(id):
    if 'username' in session:
        username = session['username']
        comment_text = request.form['comment']

        comments_before_count = comments_count_before(id)

        conn = connectsql()
        cursor = conn.cursor()
        query = "INSERT INTO comments (post_id, user_name, comment) VALUES (%s, %s, %s)"
        values = (id, username, comment_text)
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()

        comments_after_count = comments_count_after(id)

        return redirect(url_for('content', id=id, should_increase='false', comments_before_count=comments_before_count,
                                comments_after_count=comments_after_count))
    else:
        return render_template('Error.html')


@app.route('/post/edit/<id>', methods=['GET', 'POST'])
# GET -> 유지되고있는 username 세션과 현재 접속되어진 id와 일치시 edit페이지 연결
# POST -> 접속되어진 id와 일치하는 title, content를 찾아 UPDATE
def edit(id):
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']

            edittitle = request.form['title']
            editcontent = request.form['content']

            conn = connectsql()
            cursor = conn.cursor()
            query = "UPDATE board SET title = %s, content = %s WHERE id = %s"
            value = (edittitle, editcontent, id)
            cursor.execute(query, value)
            conn.commit()
            cursor.close()
            conn.close()

            return render_template('editSuccess.html')
    else:
        if 'username' in session:
            username = session['username']
            conn = connectsql()
            cursor = conn.cursor()
            query = "SELECT name FROM board WHERE id = %s"
            value = id
            cursor.execute(query, value)
            data = [post[0] for post in cursor.fetchall()]
            cursor.close()
            conn.close()

            if username in data:
                conn = connectsql()
                cursor = conn.cursor(pymysql.cursors.DictCursor)
                query = "SELECT id, title, content FROM board WHERE id = %s"
                value = id
                cursor.execute(query, value)
                postdata = cursor.fetchall()
                cursor.close()
                conn.close()
                return render_template('edit.html', data=postdata, logininfo=username)
            else:
                return render_template('editError.html')
        else:
            return render_template('Error.html')


@app.route('/post/delete/<id>')
# 유지되고 있는 username 세션과 id 일치시 삭제확인 팝업 연결
def delete(id):
    if 'username' in session:
        username = session['username']

        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT name FROM board WHERE id = %s"
        value = id
        cursor.execute(query, value)
        data = [post[0] for post in cursor.fetchall()]
        cursor.close()
        conn.close()

        if username in data:
            return render_template('delete.html', id=id)
        else:
            return render_template('editError.html')
    else:
        return render_template('Error.html')


@app.route('/post/delete/success/<id>')
# 삭제 확인시 id와 일치하는 컬럼 삭제, 취소시 /post 페이지 연결
def deletesuccess(id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM board WHERE id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM comments WHERE post_id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM files WHERE post_id = %s"
    value = id
    cursor.execute(query, value)
    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for('post'))


@app.route('/post/comment/delete/<int:id>/<int:comment_id>', methods=['GET'])
def delete_comment_route(id, comment_id):
    if 'username' in session:
        comments_before_count = comments_count_before(id)
        # 게시물 내용 페이지에서 댓글 삭제 시 id와 comment_id를 전달하여 delete_comment 함수 호출
        delete_comment(id, comment_id)
        comments_after_count = comments_count_after(id)
        # 삭제 완료 후 다시 해당 게시물의 내용 페이지로 리디렉션
        return redirect(url_for('content', id=id, should_increase='false', comments_before_count=comments_before_count,
                                comments_after_count=comments_after_count))
    else:
        return render_template('Error.html')

# 댓글 삭제 함수
def delete_comment(post_id, comment_id):
    conn = connectsql()
    cursor = conn.cursor()
    query = "DELETE FROM comments WHERE post_id = %s AND id = %s"
    values = (post_id, comment_id)
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/write', methods=['GET', 'POST'])
# GET -> write 페이지 연결
# POST -> username, password를 세션으로 불러온 후, form에 작성되어진 title, content를 테이블에 입력
def write():
    if request.method == 'POST':
        if 'username' in session:
            username = session['username']
            password = session['password']

            usertitle = request.form['title']
            usercontent = request.form['content']
            post_password = request.form['post_password']
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # 게시물 post_id 채번
            conn = connectsql()
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(id) + 1 FROM board")
            post_id = cursor.fetchone()
            cursor.close()
            conn.close()

            # 게시물이 없으면 1
            post_id = 1 if str(post_id[0]) == 'None' else str(post_id[0])
            # 게시물 Password가 없으면 NULL
            post_password = None if post_password == '' else post_password

            # 현재 스크립트 파일의 경로를 얻기
            current_directory = os.path.dirname(os.path.realpath(__file__))

            # UPLOAD_FOLDER를 현재 디렉토리를 기준으로 한 상대 경로로 지정
            UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            # 파일 처리
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                # 파일 정보를 데이터베이스에 저장
                conn = connectsql()
                cursor = conn.cursor()
                query = "INSERT INTO files (file_name, file_path, upload_date, post_id) VALUES (%s, %s, %s, %s)"
                values = (filename, os.path.join(app.config['UPLOAD_FOLDER'], filename), timestamp, post_id)
                cursor.execute(query, values)
                conn.commit()
                cursor.close()
                conn.close()

            # 게시글 정보를 데이터베이스에 저장
            conn = connectsql()
            cursor = conn.cursor()
            query = "INSERT INTO board (id, name, password, title, content, wdate, view, post_password) values (%s, %s, %s, %s, %s, %s, %s, %s)"
            values = (post_id, username, password, usertitle, usercontent, timestamp, 0, post_password)
            cursor.execute(query, values)
            conn.commit()
            cursor.close()
            conn.close()


            return redirect(url_for('post'))
        else:
            return render_template('errorpage.html')
    else:
        if 'username' in session:
            username = session['username']
            # DB에서 majors 목록 가져오기
            majors = get_major_list()
            minors = get_minor_list()
            return render_template('write.html', logininfo=username, majors=majors, minors=minors)
        else:
            return render_template('Error.html')


@app.route('/logout')
# username 세션 해제
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        logininfo = request.form['id']
        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT user_password FROM tbl_user WHERE user_name = %s"
        value = userid
        cursor.execute(query, value)
        hashed_password = cursor.fetchone()

        if hashed_password and check_password_hash(hashed_password[0], userpw):
            session['username'] = request.form['id']
            return render_template('index.html', logininfo=logininfo)
        else:
            return render_template('loginError.html')
    else:
        return render_template('login.html')


@app.route('/regist', methods=['GET', 'POST'])
def regist():
    if request.method == 'POST':
        userid = request.form['id']
        userpw = request.form['pw']

        conn = connectsql()
        cursor = conn.cursor()
        query = "SELECT * FROM tbl_user WHERE user_name = %s"
        value = userid
        cursor.execute(query, value)
        existing_user = cursor.fetchall()

        if existing_user:
            conn.rollback()
            return render_template('registError.html')
        else:
            # 해시된 비밀번호 저장
            hashed_password = generate_password_hash(userpw, method='pbkdf2:sha256')
            query = "INSERT INTO tbl_user (user_name, user_password, user_password1) values (%s, %s, %s)"
            value = (userid, hashed_password, userpw)
            cursor.execute(query, value)
            conn.commit()
            return render_template('registSuccess.html')
    else:
        return render_template('regist.html')


if __name__ == '__main__':
    app.run(debug=True)
