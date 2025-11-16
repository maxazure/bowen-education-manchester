#!/usr/bin/env python3
"""
扩充团队成员信息脚本
将教师照片导入媒体库并创建团队成员记录
"""

import sqlite3
import os
from datetime import datetime
from PIL import Image

# 数据库路径
DB_PATH = 'instance/database.db'
TEACHERS_DIR = 'templates/static/images/teachers/'

# 教师照片列表及其信息
TEACHER_PHOTOS = [
    'andrew-toft.jpg',
    'catherine-zhu.png',
    'david-chess.jpg',
    'ellen-cantonese.jpg',
    'jenny-mei.png',
    'jessica-headmaster.jpg',
    'johnathan-carter.png',
    'josh-teacher.png',
    'katie-wong.jpg',
    'kirsty-dicken.jpg',
    'lewis-assistant.png',
    'lin-li.jpg',
    'ms-wong-piano.png',
    'qian-cai.jpg',
    'simon-english.jpg',
    'steve-chan.jpg',
    'tim-english.jpg',
    'william-english.jpg',
    'xirong-li.webp'
]

# 团队成员数据
TEAM_MEMBERS = [
    {
        'name': 'Miss Catherine Zhu',
        'name_cn': '朱凯瑟琳',
        'title': 'Senior Chinese Teacher',
        'department': 'Chinese School',
        'photo': 'catherine-zhu.png',
        'qualifications': 'MA Chinese Literature (Beijing Normal University), PGCE (University of Manchester)',
        'bio': '''<p>Catherine has over 10 years of experience teaching Mandarin to students of all ages. She specializes in GCSE and A-Level Chinese, with an impressive track record of students achieving top grades.</p>
<p>A native Mandarin speaker from Beijing, Catherine holds a Master's degree in Chinese Literature and a PGCE from the University of Manchester. Her teaching approach combines traditional methods with modern technology to create engaging and effective lessons.</p>
<p>Catherine is passionate about Chinese culture and regularly organizes cultural workshops and events for students.</p>''',
        'sort_order': 4
    },
    {
        'name': 'Miss Lin Li',
        'name_cn': '李琳',
        'title': 'Chinese Language Teacher',
        'department': 'Chinese School',
        'photo': 'lin-li.jpg',
        'qualifications': 'BA Chinese Language & Culture (Nanjing University), International Chinese Teacher Certificate',
        'bio': '''<p>Lin Li brings 8 years of teaching experience from both China and the UK. She specializes in teaching young learners and foundation level Mandarin, making Chinese language learning fun and accessible.</p>
<p>With a background in Chinese language and culture from Nanjing University, Lin Li holds the prestigious International Chinese Teacher Certificate. Her creative teaching methods incorporate songs, games, and storytelling to engage young learners.</p>
<p>She is particularly skilled at teaching Chinese characters using innovative memory techniques.</p>''',
        'sort_order': 5
    },
    {
        'name': 'Miss Ellen Wong',
        'name_cn': '黄爱伦',
        'title': 'Cantonese Language Teacher',
        'department': 'Chinese School',
        'photo': 'ellen-cantonese.jpg',
        'qualifications': 'BA Linguistics (University of Hong Kong), Certificate in Teaching Cantonese',
        'bio': '''<p>Ellen is a native Cantonese speaker from Hong Kong with 6 years of teaching experience. She specializes in teaching Cantonese language and culture to students of all levels.</p>
<p>With a degree in Linguistics from the University of Hong Kong, Ellen has deep knowledge of Cantonese phonetics and grammar. Her lessons focus on practical conversation skills and understanding Hong Kong culture.</p>
<p>Ellen is passionate about preserving Cantonese language and regularly organizes cultural events featuring Cantonese cuisine, films, and traditions.</p>''',
        'sort_order': 6
    },
    {
        'name': 'Miss Jenny Mei',
        'name_cn': '梅珍妮',
        'title': 'Chinese Teacher & HSK Coordinator',
        'department': 'Chinese School',
        'photo': 'jenny-mei.png',
        'qualifications': 'MA Teaching Chinese as a Foreign Language (Shanghai International Studies University), HSK Examiner Certificate',
        'bio': '''<p>Jenny is our HSK examination coordinator with 12 years of experience in teaching Chinese as a foreign language. She has successfully prepared hundreds of students for HSK examinations at all levels.</p>
<p>Holding a Master's degree from Shanghai International Studies University and an HSK Examiner Certificate, Jenny has comprehensive understanding of the HSK examination system and requirements.</p>
<p>Her systematic approach and detailed exam strategies have helped students achieve excellent results in HSK examinations.</p>''',
        'sort_order': 7
    },
    {
        'name': 'Miss Qian Cai',
        'name_cn': '蔡倩',
        'title': 'Junior Chinese Teacher',
        'department': 'Chinese School',
        'photo': 'qian-cai.jpg',
        'qualifications': 'BA Chinese Language Education (East China Normal University), Certificate in Teaching Young Learners',
        'bio': '''<p>Qian Cai is an enthusiastic young teacher who specializes in teaching Chinese to children aged 4-11. She has 5 years of teaching experience and is known for her energetic and creative teaching style.</p>
<p>With a degree in Chinese Language Education and specialized training in teaching young learners, Qian creates a fun and supportive learning environment for children.</p>
<p>She uses a variety of interactive activities, including arts and crafts, songs, and games, to make learning Chinese enjoyable for young students.</p>''',
        'sort_order': 8
    },
    {
        'name': 'Mr. Simon Harris',
        'name_cn': None,
        'title': 'English Language Tutor',
        'department': 'Tuition Centre',
        'photo': 'simon-english.jpg',
        'qualifications': 'BA English Literature (University of Oxford), PGCE, QTS',
        'bio': '''<p>Simon is an experienced English teacher with 15 years of teaching experience. He specializes in GCSE and A-Level English Language and Literature, with exceptional results year after year.</p>
<p>A graduate of Oxford University, Simon holds Qualified Teacher Status and has taught in several outstanding schools in Greater Manchester. His deep knowledge of English literature and language helps students develop critical thinking and analytical skills.</p>
<p>Simon is particularly skilled at preparing students for examinations and has a proven track record of helping students achieve top grades.</p>''',
        'sort_order': 9
    },
    {
        'name': 'Mr. Tim Anderson',
        'name_cn': None,
        'title': 'English Tutor',
        'department': 'Tuition Centre',
        'photo': 'tim-english.jpg',
        'qualifications': 'BA English & Creative Writing (University of Manchester), TEFL Certificate',
        'bio': '''<p>Tim is a creative and enthusiastic English tutor with 7 years of experience. He specializes in creative writing and English language development for students aged 11-16.</p>
<p>With a background in Creative Writing from the University of Manchester, Tim brings a unique approach to English teaching, encouraging students to express themselves creatively while developing essential language skills.</p>
<p>He is passionate about inspiring young writers and regularly runs creative writing workshops.</p>''',
        'sort_order': 10
    },
    {
        'name': 'Mr. William Thompson',
        'name_cn': None,
        'title': 'Senior English & Literature Tutor',
        'department': 'Tuition Centre',
        'photo': 'william-english.jpg',
        'qualifications': 'MA English Literature (University of Cambridge), PGCE, QTS',
        'bio': '''<p>William is a highly qualified English teacher with over 20 years of experience. He has taught at some of the most prestigious schools in the UK and specializes in A-Level English Literature.</p>
<p>A Cambridge graduate with a Master's in English Literature, William has exceptional knowledge of classic and contemporary literature. His analytical approach helps students develop sophisticated literary criticism skills.</p>
<p>William has been an examiner for A-Level English Literature and provides invaluable insights into examination requirements and techniques.</p>''',
        'sort_order': 11
    },
    {
        'name': 'Mr. Jonathan Carter',
        'name_cn': None,
        'title': 'Mathematics Tutor',
        'department': 'Tuition Centre',
        'photo': 'johnathan-carter.png',
        'qualifications': 'BSc Mathematics (Imperial College London), MSc Applied Mathematics, PGCE',
        'bio': '''<p>Jonathan is an exceptional mathematics tutor with 10 years of teaching experience. He specializes in GCSE and A-Level Mathematics, Further Mathematics, and entrance exam preparation.</p>
<p>With degrees from Imperial College London, Jonathan has a strong academic background in mathematics. He is skilled at breaking down complex mathematical concepts into understandable steps.</p>
<p>Jonathan has successfully prepared numerous students for Oxbridge entrance exams and has an excellent track record of A* grades at A-Level.</p>''',
        'sort_order': 12
    },
    {
        'name': 'Mr. Josh Mitchell',
        'name_cn': None,
        'title': 'Mathematics & Science Tutor',
        'department': 'Tuition Centre',
        'photo': 'josh-teacher.png',
        'qualifications': 'BSc Physics (University of Manchester), PGCE in Mathematics & Science',
        'bio': '''<p>Josh is a versatile tutor who teaches both Mathematics and Science subjects. With 8 years of experience, he specializes in GCSE level Mathematics, Physics, and Chemistry.</p>
<p>Holding a Physics degree from the University of Manchester and a PGCE in Mathematics & Science, Josh brings a practical, real-world approach to teaching. He excels at showing students how mathematical and scientific concepts apply to everyday life.</p>
<p>His patient and methodical teaching style helps students build confidence in subjects they may find challenging.</p>''',
        'sort_order': 13
    },
    {
        'name': 'Mr. Steve Chan',
        'name_cn': '陈思齐',
        'title': 'Science Tutor',
        'department': 'Tuition Centre',
        'photo': 'steve-chan.jpg',
        'qualifications': 'BSc Biochemistry (University of Leeds), MSc Biotechnology, QTS',
        'bio': '''<p>Steve is a dedicated science tutor with 9 years of teaching experience. He specializes in GCSE and A-Level Biology and Chemistry, with a particular focus on practical applications.</p>
<p>With advanced degrees in Biochemistry and Biotechnology, Steve brings cutting-edge scientific knowledge to his teaching. He is skilled at making complex biological and chemical concepts accessible and engaging.</p>
<p>Steve regularly incorporates hands-on experiments and demonstrations to bring science to life for his students.</p>''',
        'sort_order': 14
    },
    {
        'name': 'Mr. David Richardson',
        'name_cn': None,
        'title': 'Chess Coach & Director',
        'department': 'Chess Club',
        'photo': 'david-chess.jpg',
        'qualifications': 'FIDE Master, ECF International Chess Arbiter, DBS Certified Coach',
        'bio': '''<p>David is a FIDE Master with over 25 years of chess playing and coaching experience. He has represented England in international tournaments and has coached students to national and international success.</p>
<p>As an ECF International Chess Arbiter, David has officiated at numerous prestigious tournaments. His systematic coaching approach focuses on developing tactical skills, strategic thinking, and competitive mindset.</p>
<p>David has coached several students to county and national championship titles. He is passionate about using chess as a tool to develop critical thinking and problem-solving skills in young people.</p>''',
        'sort_order': 15
    },
    {
        'name': 'Miss Katie Wong',
        'name_cn': '黄嘉迪',
        'title': 'Chess Coach',
        'department': 'Chess Club',
        'photo': 'katie-wong.jpg',
        'qualifications': 'FIDE Candidate Master, ECF Coach Level 2, BSc Mathematics',
        'bio': '''<p>Katie is a FIDE Candidate Master and experienced chess coach with 6 years of teaching experience. She specializes in coaching beginners and intermediate players, particularly young children.</p>
<p>With a Mathematics degree and ECF Level 2 coaching qualification, Katie combines analytical thinking with patient, encouraging teaching methods. She is particularly skilled at teaching chess to children aged 5-12.</p>
<p>Katie believes chess is an excellent tool for developing concentration, patience, and logical thinking in young learners.</p>''',
        'sort_order': 16
    },
    {
        'name': 'Mr. Andrew Toft',
        'name_cn': None,
        'title': 'Badminton Coach',
        'department': 'Sports',
        'photo': 'andrew-toft.jpg',
        'qualifications': 'Badminton England Level 2 Coach, First Aid Certified, DBS Enhanced Check',
        'bio': '''<p>Andrew is a qualified badminton coach with 12 years of coaching experience. He has competed at county level and has coached players of all ages and abilities, from complete beginners to competitive players.</p>
<p>Holding a Badminton England Level 2 coaching qualification, Andrew focuses on developing proper techniques, footwork, and game strategies. His coaching has helped numerous students compete successfully in local and regional tournaments.</p>
<p>Andrew is passionate about promoting badminton as a fun, social sport that improves fitness, coordination, and mental agility.</p>''',
        'sort_order': 17
    },
    {
        'name': 'Miss Kirsty Dicken',
        'name_cn': None,
        'title': 'Administrative Manager',
        'department': 'Administration',
        'photo': 'kirsty-dicken.jpg',
        'qualifications': 'BA Business Administration (Manchester Metropolitan University), Office Management Diploma',
        'bio': '''<p>Kirsty is our dedicated Administrative Manager with 8 years of experience in educational administration. She oversees all administrative operations, enrollment processes, and customer service.</p>
<p>With a degree in Business Administration and extensive experience in the education sector, Kirsty ensures smooth day-to-day operations of all our programs. She is the first point of contact for parents and handles inquiries with professionalism and care.</p>
<p>Kirsty is committed to providing excellent service and creating a welcoming environment for all students and families.</p>''',
        'sort_order': 18
    },
    {
        'name': 'Mr. Lewis Bennett',
        'name_cn': None,
        'title': 'Administrative Assistant',
        'department': 'Administration',
        'photo': 'lewis-assistant.png',
        'qualifications': 'BTEC Business Studies, Customer Service Certification',
        'bio': '''<p>Lewis is our friendly Administrative Assistant who supports daily operations and student services. With 4 years of experience in educational administration, he helps ensure everything runs smoothly.</p>
<p>Lewis handles class schedules, facility bookings, communications with parents, and various administrative tasks. His organizational skills and attention to detail help maintain efficient operations across all our programs.</p>
<p>Known for his helpful and approachable manner, Lewis is always ready to assist students, parents, and staff with any queries or concerns.</p>''',
        'sort_order': 19
    },
    {
        'name': 'Miss Jessica Chen',
        'name_cn': '陈杰西卡',
        'title': 'Academic Coordinator',
        'department': 'Administration',
        'photo': 'jessica-headmaster.jpg',
        'qualifications': 'MA Education Management (University of Birmingham), BA Chinese Studies',
        'bio': '''<p>Jessica is our Academic Coordinator who oversees curriculum development and quality assurance across all programs. She has 10 years of experience in education management and teaching.</p>
<p>With a Master's in Education Management from the University of Birmingham, Jessica ensures all our courses meet high academic standards. She coordinates between different departments and develops new educational initiatives.</p>
<p>Jessica's bilingual background allows her to bridge effectively between Chinese and British educational approaches, creating programs that combine the best of both systems.</p>''',
        'sort_order': 20
    }
]


def get_image_dimensions(image_path):
    """获取图片尺寸"""
    try:
        with Image.open(image_path) as img:
            return img.size  # 返回 (width, height)
    except Exception as e:
        print(f"Error reading image {image_path}: {e}")
        return (800, 600)  # 默认尺寸


def get_file_size(file_path):
    """获取文件大小（字节）"""
    return os.path.getsize(file_path)


def get_mime_type(filename):
    """根据文件扩展名获取MIME类型"""
    ext = filename.split('.')[-1].lower()
    mime_types = {
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'webp': 'image/webp',
        'gif': 'image/gif'
    }
    return mime_types.get(ext, 'image/jpeg')


def import_teacher_photos(conn):
    """将教师照片导入媒体文件表"""
    cursor = conn.cursor()
    photo_media_map = {}

    print("\n开始导入教师照片...")

    for photo in TEACHER_PHOTOS:
        photo_path = os.path.join(TEACHERS_DIR, photo)

        if not os.path.exists(photo_path):
            print(f"警告: 照片文件不存在 - {photo_path}")
            continue

        # 获取文件信息
        file_size = get_file_size(photo_path)
        width, height = get_image_dimensions(photo_path)
        mime_type = get_mime_type(photo)

        # 构建路径
        path_original = f'/static/images/teachers/{photo}'

        # 检查是否已存在
        cursor.execute(
            "SELECT id FROM media_file WHERE path_original = ?",
            (path_original,)
        )
        existing = cursor.fetchone()

        if existing:
            photo_media_map[photo] = existing[0]
            print(f"照片已存在: {photo} (ID: {existing[0]})")
            continue

        # 插入媒体文件记录
        now = datetime.now().isoformat()
        cursor.execute("""
            INSERT INTO media_file (
                filename_original, mime_type, size_bytes, width, height,
                path_original, file_type, is_public, usage_count,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            photo, mime_type, file_size, width, height,
            path_original, 'image', 1, 0,
            now, now
        ))

        media_id = cursor.lastrowid
        photo_media_map[photo] = media_id
        print(f"导入照片: {photo} (ID: {media_id})")

    conn.commit()
    print(f"\n成功导入 {len(photo_media_map)} 张照片")
    return photo_media_map


def create_team_members(conn, photo_media_map):
    """创建团队成员记录"""
    cursor = conn.cursor()
    created_count = 0

    print("\n开始创建团队成员...")

    for member in TEAM_MEMBERS:
        # 获取照片的media_id
        photo_media_id = photo_media_map.get(member['photo'])

        if not photo_media_id:
            print(f"警告: 找不到照片 {member['photo']} 的media_id，跳过成员 {member['name']}")
            continue

        # 检查是否已存在
        cursor.execute(
            "SELECT id FROM team_member WHERE name = ?",
            (member['name'],)
        )
        existing = cursor.fetchone()

        if existing:
            print(f"成员已存在: {member['name']} (ID: {existing[0]})")
            continue

        # 插入团队成员记录
        now = datetime.now().isoformat()

        # 准备specialties（将名字和中文名组合）
        specialties = member['name']
        if member.get('name_cn'):
            specialties += f" ({member['name_cn']})"

        cursor.execute("""
            INSERT INTO team_member (
                name, title, department, photo_media_id,
                bio, qualifications, specialties,
                sort_order, is_featured, is_active,
                created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            member['name'],
            member['title'],
            member['department'],
            photo_media_id,
            member['bio'],
            member['qualifications'],
            specialties,
            member['sort_order'],
            1,  # is_featured
            1,  # is_active
            now,
            now
        ))

        created_count += 1
        print(f"创建成员: {member['name']} - {member['title']}")

    conn.commit()
    print(f"\n成功创建 {created_count} 个团队成员")
    return created_count


def main():
    """主函数"""
    print("=" * 60)
    print("扩充博文教育团队成员信息")
    print("=" * 60)

    # 连接数据库
    conn = sqlite3.connect(DB_PATH)

    try:
        # 1. 导入教师照片
        photo_media_map = import_teacher_photos(conn)

        # 2. 创建团队成员
        created_count = create_team_members(conn, photo_media_map)

        # 3. 显示所有团队成员
        print("\n" + "=" * 60)
        print("当前所有团队成员列表")
        print("=" * 60)

        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, title, department, sort_order
            FROM team_member
            ORDER BY sort_order
        """)

        all_members = cursor.fetchall()
        print(f"\n总共 {len(all_members)} 位团队成员:\n")

        for member in all_members:
            print(f"{member[4]:2d}. {member[1]:30s} - {member[2]:40s} ({member[3]})")

        print("\n" + "=" * 60)
        print(f"任务完成! 新增了 {created_count} 位团队成员")
        print("=" * 60)

    except Exception as e:
        print(f"\n错误: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == '__main__':
    main()
