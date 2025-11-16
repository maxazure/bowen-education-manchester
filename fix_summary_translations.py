#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正文章、活动摘要的英文翻译
"""

import sqlite3


def fix_post_summaries():
    """修正文章摘要的英文翻译"""

    # 文章摘要翻译映射
    post_summaries = {
        19: "Bowen Chess Club held its 2024 Annual Gala in December, recognizing outstanding students and unveiling plans for 2025.",
        20: "Chronicles Zhang Ming's journey from complete beginner to inter-school chess champion.",
        21: "An in-depth explanation of one of the most important tactical themes in chess - the double attack, helping students improve their tactical skills.",
        18: "Sunday's doubles practice match provided valuable practical experience and technical exchange opportunities for students.",
        17: "The 2025 Spring Badminton League is about to begin, welcoming players of all levels to register.",
        16: "Bowen Badminton Club successfully hosted the annual friendly invitational, with nearly 100 players participating in this badminton event.",
        15: "Saturday Rapid Chess Tournament Report - Fierce battles and exciting performances.",
        14: "2025 Spring ECF Rating Tournament Registration Notice.",
        13: "2024 Autumn Inter-School Chess Championship Successfully Concluded.",
        12: "2025 Bowen Holiday Camp - Drama and Sports Activities.",
        11: "GCSE Cantonese Examination Class.",
        10: "Introductory Cantonese Class.",
        9: "Chinese Proficiency Test.",
        8: "A-Level Chinese Course.",
        7: "GCSE Chinese Examination Class.",
        6: "Elementary Chinese Class.",
        5: "Beginner Chinese Class.",
        4: "Bowen Chess Club achieved excellent results in the Manchester Regional Tournament.",
        3: "2024 HAF Program Successfully Concluded, benefiting over 200 children.",
        2: "2024 Autumn Term enrollment is now open.",
        1: "Bowen Education Group has established a strategic partnership with Henan University.",
    }

    db_path = "instance/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 60)
    print("修正文章摘要翻译")
    print("=" * 60)
    print()

    for post_id, summary_en in post_summaries.items():
        cursor.execute("""
            UPDATE post
            SET summary_en = ?
            WHERE id = ?
        """, (summary_en, post_id))

        if cursor.rowcount > 0:
            cursor.execute("SELECT title FROM post WHERE id = ?", (post_id,))
            title = cursor.fetchone()[0]
            print(f"✓ #{post_id}: {title}")
            print(f"  → {summary_en}\n")

    conn.commit()
    conn.close()

    print("=" * 60)
    print("✅ 文章摘要翻译修正完成！")
    print("=" * 60)


if __name__ == "__main__":
    fix_post_summaries()
