#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正和优化英文翻译内容
提供更自然的英文翻译
"""

import sqlite3


def fix_translations():
    """手动修正关键内容的英文翻译"""

    # 文章标题翻译映射
    post_translations = {
        "博文集团与河南大学建立战略合作伙伴关系": "Bowen Education Group Establishes Strategic Partnership with Henan University",
        "2024年秋季学期招生现已开放": "2024 Autumn Term Enrollment Now Open",
        "2024年HAF项目圆满结束，惠及200余名儿童": "2024 HAF Program Successfully Concluded, Benefiting Over 200 Children",
        "博文国际象棋俱乐部在曼彻斯特地区赛事中斩获佳绩": "Bowen Chess Club Achieves Excellent Results in Manchester Regional Tournament",
        "Foundation Mandarin / 基础中文启蒙班": "Foundation Mandarin / Beginner Chinese Class",
        "Primary Mandarin / 小学中文进阶班": "Primary Mandarin / Elementary Chinese Class",
        "GCSE Chinese / GCSE中文考试班": "GCSE Chinese / GCSE Chinese Examination Class",
        "A-Level Chinese / A-Level中文课程": "A-Level Chinese / A-Level Chinese Course",
        "HSK Preparation / HSK汉语水平考试": "HSK Preparation / Chinese Proficiency Test",
        "Beginner Cantonese / 粤语初级班": "Beginner Cantonese / Introductory Cantonese Class",
        "GCSE Cantonese / GCSE粤语考试班": "GCSE Cantonese / GCSE Cantonese Examination Class",
        "2025年博文假期营 - 戏剧运动活动": "2025 Bowen Holiday Camp - Drama and Sports Activities",
        "2024年秋季校际国际象棋锦标赛圆满落幕": "2024 Autumn Inter-School Chess Championship Successfully Concluded",
        "2025年春季ECF等级赛报名通知": "2025 Spring ECF Rating Tournament Registration Notice",
        "周六快棋赛战报 - 激烈对决，精彩纷呈": "Saturday Rapid Chess Tournament Report - Exciting Battles",
        "2024年羽毛球友谊邀请赛成功举办": "2024 Badminton Friendly Invitational Successfully Held",
        "2025年春季羽毛球联赛报名开始": "2025 Spring Badminton League Registration Now Open",
        "周日双打练习赛精彩回顾": "Sunday Doubles Practice Match Highlights",
        "博文国际象棋俱乐部2024年度盛典圆满落幕": "Bowen Chess Club 2024 Annual Gala Successfully Concluded",
        "从零基础到冠军：张明的国际象棋成长之路": "From Beginner to Champion: Zhang Ming's Chess Journey",
        '国际象棋中的"战术主题"：双重攻击详解': "Tactical Themes in Chess: Understanding Double Attacks",
    }

    # 活动标题翻译映射
    event_translations = {
        "2025春节联欢晚会": "2025 Chinese New Year Gala",
        "国际象棋夏季训练营": "Chess Summer Training Camp",
        "HSK汉语水平考试模拟测试": "HSK Chinese Proficiency Mock Test",
        "羽毛球友谊邀请赛": "Badminton Friendly Invitational",
        "家长教育讲座：如何帮助孩子学好中文": "Parent Education Seminar: How to Help Your Child Learn Chinese",
        "暑期中文文化体验营": "Summer Chinese Culture Experience Camp",
    }

    # 单页标题翻译映射
    page_translations = {
        "中文学校": "Chinese School",
        "补习中心": "Tutoring Center",
        "国际象棋俱乐部": "Chess Club",
        "政府项目": "Government Programs",
        "博文活动": "Bowen Events",
        "博文新闻": "Bowen News",
        "羽毛球俱乐部": "Badminton Club",
        "学期日期": "Term Dates",
        "PTA家长教师协会": "PTA - Parent-Teacher Association",
        "训练时间表": "Training Schedule",
        "HAF项目": "HAF Program",
        "河南大学合作": "Henan University Partnership",
        "博文集团": "Bowen Education Group",
        "博文图库": "Bowen Gallery",
        "常见问题解答": "Frequently Asked Questions",
        "俱乐部简介": "Club Introduction",
        "课程设置": "Course Curriculum",
        "学习资源": "Learning Resources",
    }

    db_path = "instance/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("修正英文翻译")
    print("=" * 60)
    print()

    # 修正文章翻译
    print("📰 修正文章翻译...")
    for zh_title, en_title in post_translations.items():
        cursor.execute("""
            UPDATE post
            SET title_en = ?,
                seo_title_en = ?
            WHERE title = ?
        """, (en_title, en_title, zh_title))
        if cursor.rowcount > 0:
            print(f"   ✓ {zh_title}")
            print(f"     → {en_title}")

    # 修正活动翻译
    print("\n🎉 修正活动翻译...")
    for zh_title, en_title in event_translations.items():
        cursor.execute("""
            UPDATE event
            SET title_en = ?,
                seo_title_en = ?
            WHERE title = ?
        """, (en_title, en_title, zh_title))
        if cursor.rowcount > 0:
            print(f"   ✓ {zh_title}")
            print(f"     → {en_title}")

    # 修正单页翻译
    print("\n📄 修正单页翻译...")
    for zh_title, en_title in page_translations.items():
        cursor.execute("""
            UPDATE single_page
            SET title_en = ?,
                seo_title_en = ?
            WHERE title = ?
        """, (en_title, en_title, zh_title))
        if cursor.rowcount > 0:
            print(f"   ✓ {zh_title}")
            print(f"     → {en_title}")

    # 对于已经是英文的内容，确保 en 字段与原字段相同
    print("\n📝 处理已有英文内容...")

    # Products
    cursor.execute("""
        UPDATE product
        SET name_en = name,
            summary_en = summary,
            description_html_en = description_html,
            price_text_en = price_text,
            seo_title_en = COALESCE(seo_title, name),
            seo_description_en = COALESCE(seo_description, summary)
        WHERE name LIKE '%English%'
           OR name LIKE '%GCSE%'
           OR name LIKE '%A-Level%'
           OR name LIKE '%HSK%'
           OR name LIKE '%Foundation%'
           OR name LIKE '%Cantonese%'
           OR name LIKE '%Primary%'
           OR name LIKE '%Mathematics%'
           OR name LIKE '%Physics%'
    """)
    print(f"   ✓ 已更新 {cursor.rowcount} 个产品的英文字段")

    # Posts (已经是英文的)
    cursor.execute("""
        UPDATE post
        SET title_en = title,
            summary_en = summary,
            content_html_en = content_html,
            seo_title_en = COALESCE(seo_title, title),
            seo_description_en = COALESCE(seo_description, summary)
        WHERE title LIKE 'Foundation Mandarin%'
           OR title LIKE 'Primary Mandarin%'
           OR title LIKE 'GCSE%'
           OR title LIKE 'A-Level%'
           OR title LIKE 'HSK%'
           OR title LIKE 'Beginner Cantonese%'
    """)
    print(f"   ✓ 已更新 {cursor.rowcount} 篇文章的英文字段")

    # Events (已经是英文的)
    cursor.execute("""
        UPDATE event
        SET title_en = title,
            description_en = description,
            summary_en = summary,
            seo_title_en = COALESCE(seo_title, title),
            seo_description_en = COALESCE(seo_description, summary)
        WHERE title LIKE '%English%'
           OR title LIKE 'Chinese New Year%'
           OR title LIKE 'HSK%'
    """)
    print(f"   ✓ 已更新 {cursor.rowcount} 个活动的英文字段")

    # Single Pages (已经是英文的)
    cursor.execute("""
        UPDATE single_page
        SET title_en = title,
            subtitle_en = subtitle,
            content_html_en = content_html,
            seo_title_en = COALESCE(seo_title, title),
            seo_description_en = COALESCE(seo_description, subtitle)
        WHERE title IN ('About Us', 'Contact Us', 'Privacy Policy',
                       'Terms of Service', 'Cookie Policy', 'Safeguarding Policy')
    """)
    print(f"   ✓ 已更新 {cursor.rowcount} 个单页的英文字段")

    conn.commit()
    conn.close()

    print("\n" + "=" * 60)
    print("✅ 翻译修正完成！")
    print("=" * 60)
    print("\n现在可以访问英文页面查看效果了。")
    print("建议通过管理后台进一步优化和完善翻译内容。")


if __name__ == "__main__":
    fix_translations()
