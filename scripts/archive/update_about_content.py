#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新博文教育集团的简介内容（中英文）
"""

import sqlite3


def update_about_content():
    """更新关于博文的所有相关内容"""

    # 中文简介
    about_zh = """<div class="about-intro">
    <h2 class="section-subtitle">立足英国 · 服务社区 · 传承文化 · 联通中外</h2>

    <p class="lead">博文教育（Bowen Education）创立于2020年，总部位于英国曼彻斯特，是一所经Ofsted（英国教育标准局）注册认证、并具备Tax-Free Childcare 政府育儿补贴资质的综合性中文教育与文化机构。我们致力于为华裔青少年及其他族裔儿童提供系统、专业的中文语言与文化教育，帮助他们在多元社会中建立自信的文化身份与全球化视野。</p>

    <h3>我们的教育理念</h3>
    <p>秉持"<strong>Learn · Share · Bridge（学习 · 分享 · 桥梁）</strong>"的教育理念，博文教育通过语言教学、文化推广与社会项目三大体系，构建了一个融合学术成长、人格培养与文化认同的教育生态。</p>

    <h3>我们的使命</h3>
    <blockquote class="mission-quote">
        <p>"让中华文化在英国深深扎根"，不仅是一句口号，而是一份代代相传的责任。</p>
    </blockquote>

    <p>正是这份事业，让我们能够不遗余力地将中文教育融入英国主流教育体系。通过华文学校，我们正在影响和启发下一代，帮助他们认识自我、理解根源、连接世界。这份成就感，丝毫不亚于科技创新带来的震撼——因为我们塑造的，是无数孩子的精神世界。</p>

    <h3>我们的资质</h3>
    <ul class="qualification-list">
        <li><strong>Ofsted 注册认证</strong> - 英国教育标准局官方认证</li>
        <li><strong>Tax-Free Childcare 资质</strong> - 政府育儿补贴合格机构</li>
        <li><strong>专业教师团队</strong> - 所有教师均持有相关教学资格</li>
        <li><strong>系统化课程</strong> - 完整的中文教育体系</li>
    </ul>
</div>"""

    # 英文简介
    about_en = """<div class="about-intro">
    <h2 class="section-subtitle">Rooted in the UK · Serving Communities · Passing on Culture · Bridging East and West</h2>

    <p class="lead">Bowen Education was founded in 2020 and is headquartered in Manchester, UK. We are a comprehensive Chinese language and cultural education institution registered and accredited by Ofsted (Office for Standards in Education) with Tax-Free Childcare government subsidy eligibility. We are committed to providing systematic and professional Chinese language and cultural education for Chinese heritage children and children of other ethnic backgrounds, helping them build confident cultural identities and global perspectives in a diverse society.</p>

    <h3>Our Educational Philosophy</h3>
    <p>Guided by our educational philosophy of "<strong>Learn · Share · Bridge</strong>," Bowen Education has built an educational ecosystem that integrates academic growth, character development, and cultural identity through three core systems: language teaching, cultural promotion, and community programs.</p>

    <h3>Our Mission</h3>
    <blockquote class="mission-quote">
        <p>"Deeply rooting Chinese culture in the UK" is not just a slogan, but a responsibility passed down through generations.</p>
    </blockquote>

    <p>It is this mission that drives us to spare no effort in integrating Chinese language education into the UK mainstream education system. Through our Chinese school, we are influencing and inspiring the next generation, helping them understand themselves, recognize their roots, and connect with the world. This sense of achievement is no less profound than the impact of technological innovation—because what we shape is the spiritual world of countless children.</p>

    <h3>Our Qualifications</h3>
    <ul class="qualification-list">
        <li><strong>Ofsted Registered</strong> - Officially accredited by the Office for Standards in Education</li>
        <li><strong>Tax-Free Childcare Eligible</strong> - Approved government childcare subsidy provider</li>
        <li><strong>Professional Teaching Team</strong> - All teachers hold relevant teaching qualifications</li>
        <li><strong>Systematic Curriculum</strong> - Comprehensive Chinese education system</li>
    </ul>
</div>"""

    db_path = "instance/database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    print("=" * 70)
    print("更新博文教育简介内容")
    print("=" * 70)
    print()

    # 1. 更新"博文集团"单页 (ID: 16, slug: about-company)
    print("1. 更新'博文集团'单页...")
    cursor.execute("""
        UPDATE single_page
        SET content_html = ?,
            content_html_en = ?,
            title = '关于博文教育',
            title_en = 'About Bowen Education',
            subtitle = '立足英国 · 服务社区 · 传承文化 · 联通中外',
            subtitle_en = 'Rooted in the UK · Serving Communities · Passing on Culture · Bridging East and West'
        WHERE id = 16
    """, (about_zh, about_en))
    print(f"   ✓ 已更新 (ID: 16)")
    print()

    # 2. 更新首页 About 区块的内容
    print("2. 检查首页 About 区块...")
    # 首页的 About 区块通常是硬编码在模板中的，需要更新模板文件
    print("   ⚠️  首页 About 区块需要更新模板文件")
    print()

    conn.commit()
    conn.close()

    print("=" * 70)
    print("✅ 数据库内容更新完成！")
    print("=" * 70)
    print()
    print("接下来需要手动更新的文件:")
    print("1. templates/zh/home.html - 首页中文 About 区块")
    print("2. templates/en/home.html - 首页英文 About 区块")
    print()


if __name__ == "__main__":
    update_about_content()
