-- ================================================================
-- 国际象棋俱乐部栏目重组 SQL 脚本
-- ================================================================
-- 目标：重新组织国际象棋俱乐部的子栏目结构
--
-- 新栏目结构：
-- 1. 俱乐部简介 (SINGLE_PAGE)
-- 2. 课程设置 (SINGLE_PAGE) - 包含注册表单
-- 3. 活动与赛事 (POST)
-- 4. 学习资源 (SINGLE_PAGE)
-- 5. 新闻与精彩回顾 (POST)
-- ================================================================

BEGIN TRANSACTION;

-- ================================================================
-- 第一步：删除旧的子栏目
-- ================================================================
-- 删除相册栏目（id=18，已不再需要）
DELETE FROM site_column WHERE id = 18;

-- 删除棋手信息栏目（id=17，改为课程设置）
DELETE FROM single_page WHERE column_id = 17;
DELETE FROM site_column WHERE id = 17;

-- 保留"我们的比赛"栏目（id=16），但将其改名为"活动与赛事"
UPDATE site_column SET name = '活动与赛事', slug = 'chess-events', sort_order = 3 WHERE id = 16;

-- ================================================================
-- 第二步：创建新的栏目
-- ================================================================

-- 1. 俱乐部简介 (id=26)
INSERT INTO site_column (id, name, slug, column_type, parent_id, menu_location, sort_order, show_in_nav, is_enabled, created_at, updated_at)
VALUES (26, '俱乐部简介', 'chess-about', 'SINGLE_PAGE', 5, 'BOTH', 1, 1, 1, datetime('now'), datetime('now'));

-- 2. 课程设置 (id=27)
INSERT INTO site_column (id, name, slug, column_type, parent_id, menu_location, sort_order, show_in_nav, is_enabled, created_at, updated_at)
VALUES (27, '课程设置', 'chess-courses', 'SINGLE_PAGE', 5, 'BOTH', 2, 1, 1, datetime('now'), datetime('now'));

-- 3. 学习资源 (id=28)
INSERT INTO site_column (id, name, slug, column_type, parent_id, menu_location, sort_order, show_in_nav, is_enabled, created_at, updated_at)
VALUES (28, '学习资源', 'chess-resources', 'SINGLE_PAGE', 5, 'BOTH', 4, 1, 1, datetime('now'), datetime('now'));

-- 4. 新闻与精彩回顾 (id=29)
INSERT INTO site_column (id, name, slug, column_type, parent_id, menu_location, sort_order, show_in_nav, is_enabled, created_at, updated_at)
VALUES (29, '新闻与精彩回顾', 'chess-news', 'POST', 5, 'BOTH', 5, 1, 1, datetime('now'), datetime('now'));

-- ================================================================
-- 第三步：创建页面内容 (SINGLE_PAGE)
-- ================================================================

-- 1. 俱乐部简介 (single_page id=19)
INSERT INTO single_page (id, column_id, title, subtitle, content_html, status, published_at, created_at, updated_at)
VALUES (19, 26, '俱乐部简介', 'About Bowen Chess Club',
'<h2>欢迎来到博文国际象棋俱乐部</h2>
<p>博文国际象棋俱乐部成立于2018年，是大曼彻斯特地区领先的青少年国际象棋培训机构。我们致力于通过国际象棋教育培养孩子们的逻辑思维能力、专注力和决策能力。</p>

<h3>我们的使命</h3>
<p>我们相信国际象棋不仅是一项竞技运动，更是一种教育工具。通过国际象棋，孩子们可以学会：</p>
<ul>
    <li><strong>逻辑思维</strong>：培养分析问题和解决问题的能力</li>
    <li><strong>战略规划</strong>：学会提前思考和制定计划</li>
    <li><strong>专注力</strong>：提高注意力集中的时间和质量</li>
    <li><strong>抗压能力</strong>：在竞争中学会冷静应对压力</li>
    <li><strong>体育精神</strong>：尊重对手，胜不骄败不馁</li>
</ul>

<h3>俱乐部特色</h3>
<div class="row mt-4">
    <div class="col-md-6">
        <h4><i class="fas fa-certificate"></i> 专业认证</h4>
        <p>俱乐部与英格兰国际象棋联合会（ECF）合作，为学员提供官方等级认证服务。学员可以参加ECF等级赛，获得国际认可的棋力等级。</p>
    </div>
    <div class="col-md-6">
        <h4><i class="fas fa-users"></i> 小班教学</h4>
        <p>我们采用小班制教学，确保每个学员都能得到充分的关注和指导。师生比例控制在1:8以内。</p>
    </div>
</div>

<div class="row mt-3">
    <div class="col-md-6">
        <h4><i class="fas fa-trophy"></i> 优异成绩</h4>
        <p>俱乐部学员在各级比赛中屡获佳绩。2023年，我们的学员在曼彻斯特地区青少年锦标赛中获得多个组别的冠亚军。</p>
    </div>
    <div class="col-md-6">
        <h4><i class="fas fa-calendar-alt"></i> 灵活安排</h4>
        <p>提供周末和平日班次，家长可以根据孩子的时间灵活选择。同时提供在线和线下两种授课方式。</p>
    </div>
</div>

<h3>训练理念</h3>
<p>我们的教学以<strong>兴趣培养</strong>为起点，通过<strong>系统训练</strong>提升棋力，最终帮助学员<strong>建立自信</strong>。我们不仅教授国际象棋技术，更注重培养学员的思维方式和品格。</p>

<h3>成绩与荣誉</h3>
<ul>
    <li>2023年曼彻斯特地区青少年锦标赛 - 团体第二名</li>
    <li>2023年ECF等级赛 - 多名学员获得组别前三名</li>
    <li>2022年校际国际象棋联赛 - 冠军</li>
    <li>俱乐部现有注册会员超过80人</li>
    <li>20+名学员获得ECF官方等级认证</li>
</ul>

<h3>联系我们</h3>
<div class="contact-info mt-4">
    <p><i class="fas fa-map-marker-alt"></i> <strong>地址：</strong>Sale Sports Centre, Sale Road, Sale, Manchester M33 3SL</p>
    <p><i class="fas fa-envelope"></i> <strong>邮箱：</strong>chess@boweneducation.org</p>
    <p><i class="fas fa-phone"></i> <strong>电话：</strong>07123 456789</p>
    <p><i class="fas fa-clock"></i> <strong>训练时间：</strong>周六、周日 10:00-12:00, 14:00-17:00</p>
</div>

<div class="alert alert-success mt-4">
    <h4>现在加入我们！</h4>
    <p>博文国际象棋俱乐部常年招收新会员，欢迎5-16岁的青少年加入。无论您的孩子是零基础还是已有一定水平，我们都有适合的课程。</p>
    <p><strong>首次体验课免费！</strong></p>
</div>',
'published', datetime('now'), datetime('now'), datetime('now'));

-- 2. 课程设置 (single_page id=20) - 包含注册表单
INSERT INTO single_page (id, column_id, title, subtitle, content_html, status, published_at, created_at, updated_at)
VALUES (20, 27, '课程设置', 'Chess Courses & Registration',
'<h2>课程体系</h2>
<p>博文国际象棋俱乐部提供系统化的国际象棋培训课程，根据学员的年龄和棋力水平分为不同班级。</p>

<h3>课程级别</h3>

<div class="card mb-3">
    <div class="card-body">
        <h4 class="card-title"><i class="fas fa-chess-pawn"></i> 启蒙班（5-7岁）</h4>
        <p><strong>课程目标：</strong>激发孩子对国际象棋的兴趣，学习基本规则和简单战术。</p>
        <p><strong>课程内容：</strong></p>
        <ul>
            <li>国际象棋棋盘和棋子介绍</li>
            <li>各类棋子的走法和吃子规则</li>
            <li>特殊走法：王车易位、吃过路兵、兵的升变</li>
            <li>将军、将死、和棋的概念</li>
            <li>基本战术：双重攻击、牵制、困子</li>
            <li>简单残局：单王对单后、单王对双车</li>
        </ul>
        <p><strong>课时安排：</strong>每周1次，每次1.5小时（90分钟）</p>
        <p><strong>学费：</strong>£180/学期（12周）</p>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body">
        <h4 class="card-title"><i class="fas fa-chess-knight"></i> 初级班（8-10岁）</h4>
        <p><strong>课程目标：</strong>掌握国际象棋基本战术，能够独立完成一局完整的对局。</p>
        <p><strong>课程内容：</strong></p>
        <ul>
            <li>开局原则：控制中心、快速出子、王的安全</li>
            <li>中局战术：双重攻击、牵制、闪击、困子、引离</li>
            <li>基本杀法：后翼杀王、王翼杀王</li>
            <li>兵的结构：孤兵、叠兵、通路兵</li>
            <li>简单残局：王兵残局、车兵残局</li>
            <li>实战对局分析</li>
        </ul>
        <p><strong>课时安排：</strong>每周1次，每次2小时</p>
        <p><strong>学费：</strong>£220/学期（12周）</p>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body">
        <h4 class="card-title"><i class="fas fa-chess-rook"></i> 中级班（11-13岁）</h4>
        <p><strong>课程目标：</strong>系统学习开局理论，提高中局战术和残局技巧，参加ECF等级赛。</p>
        <p><strong>课程内容：</strong></p>
        <ul>
            <li>常见开局体系：意大利开局、西班牙开局、西西里防御</li>
            <li>复杂战术组合：牺牲、腾挪、消除防御</li>
            <li>局面评估：子力、空间、王的安全、兵型</li>
            <li>计划与战略</li>
            <li>复杂残局：马兵残局、象兵残局</li>
            <li>赛前准备和心理调适</li>
            <li>ECF等级赛实战训练</li>
        </ul>
        <p><strong>课时安排：</strong>每周1次，每次2.5小时</p>
        <p><strong>学费：</strong>£260/学期（12周）</p>
    </div>
</div>

<div class="card mb-3">
    <div class="card-body">
        <h4 class="card-title"><i class="fas fa-chess-queen"></i> 高级班（14-16岁）</h4>
        <p><strong>课程目标：</strong>深入研究开局理论，掌握高级战术和战略，参加高水平比赛。</p>
        <p><strong>课程内容：</strong></p>
        <ul>
            <li>开局准备：变例研究、新手研究</li>
            <li>高级战术：复杂组合、长远计算</li>
            <li>战略思想：弱格、开放线、空间优势</li>
            <li>复杂残局：车马残局、后残局</li>
            <li>经典对局赏析</li>
            <li>个性化开局体系建立</li>
            <li>高水平比赛实战</li>
        </ul>
        <p><strong>课时安排：</strong>每周1-2次，每次3小时</p>
        <p><strong>学费：</strong>£300/学期（12周，每周1次）；£550/学期（每周2次）</p>
    </div>
</div>

<h3>一对一私教课程</h3>
<p>针对有特殊需求或希望快速提升的学员，俱乐部提供一对一私教服务。</p>
<ul>
    <li><strong>课时：</strong>60分钟/90分钟可选</li>
    <li><strong>学费：</strong>£40/小时（60分钟）；£55/90分钟</li>
    <li><strong>内容：</strong>根据学员水平和需求定制</li>
</ul>

<h3>在线课程</h3>
<p>为方便无法到场的学员，俱乐部提供在线直播课程，使用Zoom平台授课。</p>
<ul>
    <li><strong>课时：</strong>与线下课程相同</li>
    <li><strong>学费：</strong>比线下课程优惠10%</li>
    <li><strong>平台：</strong>Zoom + Lichess / Chess.com</li>
</ul>

<div class="alert alert-info mt-4">
    <h4><i class="fas fa-gift"></i> 优惠政策</h4>
    <ul class="mb-0">
        <li>兄弟姐妹同时报名享受9折优惠</li>
        <li>连续报名两个学期享受95折优惠</li>
        <li>推荐新学员成功报名，双方各获£20学费抵扣</li>
        <li>首次体验课免费</li>
    </ul>
</div>

<hr class="my-5">

<h2 id="registration-form">会员注册</h2>
<p>欢迎加入博文国际象棋俱乐部！请填写以下表单完成注册，我们会在24小时内与您联系。</p>

<form id="chessClubRegistrationForm" class="needs-validation" novalidate>
    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="studentName" class="form-label">学员姓名 <span class="text-danger">*</span></label>
            <input type="text" class="form-control" id="studentName" name="studentName" required>
            <div class="invalid-feedback">请输入学员姓名</div>
        </div>
        <div class="col-md-6 mb-3">
            <label for="studentAge" class="form-label">学员年龄 <span class="text-danger">*</span></label>
            <select class="form-control" id="studentAge" name="studentAge" required>
                <option value="">请选择年龄</option>
                <option value="5">5岁</option>
                <option value="6">6岁</option>
                <option value="7">7岁</option>
                <option value="8">8岁</option>
                <option value="9">9岁</option>
                <option value="10">10岁</option>
                <option value="11">11岁</option>
                <option value="12">12岁</option>
                <option value="13">13岁</option>
                <option value="14">14岁</option>
                <option value="15">15岁</option>
                <option value="16">16岁</option>
            </select>
            <div class="invalid-feedback">请选择学员年龄</div>
        </div>
    </div>

    <div class="row">
        <div class="col-md-6 mb-3">
            <label for="parentName" class="form-label">家长姓名 <span class="text-danger">*</span></label>
            <input type="text" class="form-control" id="parentName" name="parentName" required>
            <div class="invalid-feedback">请输入家长姓名</div>
        </div>
        <div class="col-md-6 mb-3">
            <label for="parentPhone" class="form-label">联系电话 <span class="text-danger">*</span></label>
            <input type="tel" class="form-control" id="parentPhone" name="parentPhone" required>
            <div class="invalid-feedback">请输入联系电话</div>
        </div>
    </div>

    <div class="mb-3">
        <label for="parentEmail" class="form-label">电子邮箱 <span class="text-danger">*</span></label>
        <input type="email" class="form-control" id="parentEmail" name="parentEmail" required>
        <div class="invalid-feedback">请输入有效的电子邮箱</div>
    </div>

    <div class="mb-3">
        <label for="chessLevel" class="form-label">当前国际象棋水平 <span class="text-danger">*</span></label>
        <select class="form-control" id="chessLevel" name="chessLevel" required>
            <option value="">请选择</option>
            <option value="beginner">零基础（从未接触过国际象棋）</option>
            <option value="basic">初学者（了解基本规则）</option>
            <option value="intermediate">初级（能下完整对局，了解基本战术）</option>
            <option value="advanced">中级（有比赛经验，ECF等级500-1000）</option>
            <option value="expert">高级（ECF等级1000+）</option>
        </select>
        <div class="invalid-feedback">请选择国际象棋水平</div>
    </div>

    <div class="mb-3">
        <label for="preferredCourse" class="form-label">意向课程 <span class="text-danger">*</span></label>
        <select class="form-control" id="preferredCourse" name="preferredCourse" required>
            <option value="">请选择</option>
            <option value="enlightenment">启蒙班（5-7岁）</option>
            <option value="beginner">初级班（8-10岁）</option>
            <option value="intermediate">中级班（11-13岁）</option>
            <option value="advanced">高级班（14-16岁）</option>
            <option value="private">一对一私教</option>
            <option value="online">在线课程</option>
        </select>
        <div class="invalid-feedback">请选择意向课程</div>
    </div>

    <div class="mb-3">
        <label for="preferredSchedule" class="form-label">首选上课时间</label>
        <select class="form-control" id="preferredSchedule" name="preferredSchedule">
            <option value="">请选择</option>
            <option value="sat_morning">周六上午（10:00-12:00）</option>
            <option value="sat_afternoon">周六下午（14:00-17:00）</option>
            <option value="sun_morning">周日上午（10:00-12:00）</option>
            <option value="sun_afternoon">周日下午（14:00-17:00）</option>
            <option value="weekday">平日（需协商）</option>
        </select>
    </div>

    <div class="mb-3">
        <label for="howHeard" class="form-label">如何得知我们的俱乐部</label>
        <select class="form-control" id="howHeard" name="howHeard">
            <option value="">请选择</option>
            <option value="friend">朋友推荐</option>
            <option value="social_media">社交媒体</option>
            <option value="website">网站搜索</option>
            <option value="school">学校宣传</option>
            <option value="event">参加活动</option>
            <option value="other">其他</option>
        </select>
    </div>

    <div class="mb-3">
        <label for="additionalInfo" class="form-label">其他信息或特殊需求</label>
        <textarea class="form-control" id="additionalInfo" name="additionalInfo" rows="3" placeholder="请告诉我们您的其他需求或想了解的信息"></textarea>
    </div>

    <div class="mb-3 form-check">
        <input type="checkbox" class="form-check-input" id="agreeTerms" name="agreeTerms" required>
        <label class="form-check-label" for="agreeTerms">
            我已阅读并同意 <a href="/terms" target="_blank">服务条款</a> 和 <a href="/privacy" target="_blank">隐私政策</a> <span class="text-danger">*</span>
        </label>
        <div class="invalid-feedback">请同意服务条款和隐私政策</div>
    </div>

    <div class="alert alert-warning">
        <small>
            <i class="fas fa-info-circle"></i>
            提交注册后，我们会在24小时内通过电话或邮件与您联系，确认课程详情并安排免费体验课。
        </small>
    </div>

    <button type="submit" class="btn btn-primary btn-lg">
        <i class="fas fa-paper-plane"></i> 提交注册
    </button>
</form>

<script>
// 表单验证
(function () {
    "use strict";
    const forms = document.querySelectorAll(".needs-validation");
    Array.from(forms).forEach(function (form) {
        form.addEventListener("submit", function (event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            } else {
                event.preventDefault();
                // 这里可以添加实际的表单提交逻辑
                alert("感谢您的注册！我们会尽快与您联系。");
                form.reset();
                form.classList.remove("was-validated");
                return false;
            }
            form.classList.add("was-validated");
        }, false);
    });
})();
</script>',
'published', datetime('now'), datetime('now'), datetime('now'));

COMMIT;

-- ================================================================
-- 继续：学习资源页面
-- ================================================================

-- 3. 学习资源 (single_page id=21)
INSERT INTO single_page (id, column_id, title, subtitle, content_html, status, published_at, created_at, updated_at)
VALUES (21, 28, '学习资源', 'Chess Learning Resources',
'<h2>国际象棋学习资源</h2>
<p>为了帮助学员更好地提升棋力，我们整理了一系列优质的国际象棋学习资源。以下资源均来自权威机构和专业网站，特别是英国本土的资源。</p>

<div class="alert alert-info">
    <i class="fas fa-lightbulb"></i>
    <strong>学习建议：</strong>建议学员结合课堂学习，利用这些在线资源进行课后练习。初学者可以从ECF的免费教材开始，有一定基础的学员可以使用战术训练网站每天练习。
</div>

<h3><i class="fas fa-landmark"></i> 官方组织与认证</h3>
<div class="resource-card">
    <h4><a href="https://www.englishchess.org.uk/" target="_blank" rel="noopener">English Chess Federation (ECF)</a></h4>
    <p><strong>简介：</strong>英格兰国际象棋联合会，英国国际象棋的官方管理机构。</p>
    <p><strong>主要资源：</strong></p>
    <ul>
        <li><a href="https://www.englishchess.org.uk/certificate-of-excellence/" target="_blank">Certificate of Excellence</a> - 官方认证课程，分为铜、银、金、钻石四个级别</li>
        <li><a href="https://www.englishchess.org.uk/new-to-chess/" target="_blank">New to Chess Guide</a> - 新手入门指南</li>
        <li>免费下载教材：Chess Booklet One 和 Chess Booklet Two（适合1200 Elo以下）</li>
        <li>ECF等级分查询和会员注册</li>
    </ul>
    <p><strong>适合人群：</strong>所有水平，特别是希望获得官方认证的学员</p>
</div>

<div class="resource-card">
    <h4><a href="https://www.chess-in-schools.co.uk/" target="_blank" rel="noopener">Chess in Schools and Communities (CSC)</a></h4>
    <p><strong>简介：</strong>英国最大的国际象棋教育慈善机构，在全英1600+所学校推广国际象棋教育。</p>
    <p><strong>主要资源：</strong></p>
    <ul>
        <li>免费的在线国际象棋课程</li>
        <li>教学资源和活动组织指南</li>
        <li>青少年比赛信息</li>
    </ul>
    <p><strong>适合人群：</strong>学校和青少年学习者</p>
</div>

<h3><i class="fas fa-graduation-cap"></i> 在线课程平台</h3>

<div class="resource-card">
    <h4><a href="https://learningchess.net/uk/courses" target="_blank" rel="noopener">LearningChess.net UK</a></h4>
    <p><strong>简介：</strong>专业的国际象棋在线学习平台，提供系统化的课程。</p>
    <p><strong>主要资源：</strong></p>
    <ul>
        <li>3门在线课程，包含108节课</li>
        <li>70节免费课程</li>
        <li>GM Jozsef Pinter提供50节基于实战的免费教学</li>
    </ul>
    <p><strong>适合人群：</strong>初学者到中级玩家</p>
</div>

<div class="resource-card">
    <h4><a href="https://chessacademy.uk/" target="_blank" rel="noopener">Chess Rising Stars (Chess Academy UK)</a></h4>
    <p><strong>简介：</strong>由WFM Maria Manelidou创办的在线国际象棋学院，社区超过500名成员。</p>
    <p><strong>主要特色：</strong></p>
    <ul>
        <li>经验丰富的教练团队</li>
        <li>互动式在线课程</li>
        <li>自2020年起专注在线教学</li>
        <li>定期组织线上比赛和活动</li>
    </ul>
    <p><strong>适合人群：</strong>所有水平，特别是希望在线学习的学员</p>
</div>

<div class="resource-card">
    <h4><a href="https://www.mindfulchess.org/" target="_blank" rel="noopener">Mindful Chess</a></h4>
    <p><strong>简介：</strong>成立于2015年的伦敦国际象棋教育机构，每周教授超过500名学生。</p>
    <p><strong>主要特色：</strong></p>
    <ul>
        <li>每周7天提供在线课程</li>
        <li>从初学者到国际比赛选手的全方位培训</li>
        <li>专业教练团队</li>
    </ul>
    <p><strong>适合人群：</strong>伦敦地区和在线学员</p>
</div>

<div class="resource-card">
    <h4><a href="https://www.chess-lessons.co.uk/" target="_blank" rel="noopener">Royal Chess Coaching Academy</a></h4>
    <p><strong>简介：</strong>伦敦地区的高水平专业国际象棋学校。</p>
    <p><strong>主要特色：</strong></p>
    <ul>
        <li>面向所有水平：从儿童初学者到成人专业选手</li>
        <li>在线一对一辅导</li>
        <li>收费：£30/小时起</li>
    </ul>
    <p><strong>适合人群：</strong>希望接受高水平个性化指导的学员</p>
</div>

<h3><i class="fas fa-puzzle-piece"></i> 在线练习与战术训练</h3>

<div class="resource-card">
    <h4><a href="https://lichess.org/" target="_blank" rel="noopener">Lichess.org</a></h4>
    <p><strong>简介：</strong>世界领先的免费开源国际象棋平台。</p>
    <p><strong>主要功能：</strong></p>
    <ul>
        <li><a href="https://lichess.org/training" target="_blank">战术训练</a> - 无限免费战术题，基于真实对局</li>
        <li><a href="https://lichess.org/study" target="_blank">学习模块</a> - 开局、中局、残局系统学习</li>
        <li>在线对弈 - 支持各种时间控制</li>
        <li>分析工具 - AI分析你的对局</li>
        <li>完全免费，无广告</li>
    </ul>
    <p><strong>适合人群：</strong>所有水平，强烈推荐</p>
</div>

<div class="resource-card">
    <h4><a href="https://www.chess.com/" target="_blank" rel="noopener">Chess.com</a></h4>
    <p><strong>简介：</strong>世界最大的国际象棋网站，提供全面的学习和对弈功能。</p>
    <p><strong>主要功能：</strong></p>
    <ul>
        <li><a href="https://www.chess.com/puzzles" target="_blank">战术训练</a> - 50万+战术题库</li>
        <li><a href="https://www.chess.com/lessons" target="_blank">视频课程</a> - 大师级教学视频</li>
        <li>Puzzle Rush - 快速战术训练</li>
        <li>在线比赛和锦标赛</li>
        <li>免费账号 + 付费高级功能</li>
    </ul>
    <p><strong>适合人群：</strong>所有水平</p>
</div>

<div class="resource-card">
    <h4><a href="https://www.chesstempo.com/" target="_blank" rel="noopener">ChessTempo</a></h4>
    <p><strong>简介：</strong>专注于战术训练的平台，题库质量高。</p>
    <p><strong>主要特色：</strong></p>
    <ul>
        <li>基于真实对局的战术题</li>
        <li>间隔重复学习系统</li>
        <li>详细的统计分析</li>
        <li>开局训练器</li>
    </ul>
    <p><strong>适合人群：</strong>中级以上学员</p>
</div>

<h3><i class="fas fa-book"></i> 推荐书籍</h3>
<div class="resource-card">
    <h4>经典教材推荐</h4>
    <ul>
        <li><strong>《My System》by Aron Nimzowitsch</strong> - 国际象棋战略思想经典</li>
        <li><strong>《Bobby Fischer Teaches Chess》</strong> - 世界冠军的教学书</li>
        <li><strong>《Logical Chess: Move by Move》by Irving Chernev</strong> - 每一步都有解释</li>
        <li><strong>《The Amateur Mind》by Jeremy Silman</strong> - 适合业余棋手的思维训练</li>
        <li><strong>《Chess Tactics for Champions》by Susan Polgar</strong> - 战术训练经典</li>
        <li><strong>《Dvoretsky Endgame Manual》</strong> - 残局圣经（高级）</li>
    </ul>
    <p><strong>购买渠道：</strong>Amazon UK, Waterstones, 或当地书店</p>
</div>

<h3><i class="fas fa-video"></i> YouTube 频道推荐</h3>
<div class="resource-card">
    <h4>英文教学频道</h4>
    <ul>
        <li><strong><a href="https://www.youtube.com/@GMHikaru" target="_blank">GMHikaru</a></strong> - 顶尖GM的实战和教学</li>
        <li><strong><a href="https://www.youtube.com/@GothamChess" target="_blank">GothamChess (Levy Rozman)</a></strong> - 生动有趣的教学风格</li>
        <li><strong><a href="https://www.youtube.com/@chessbrah" target="_blank">Chessbrah</a></strong> - 加拿大GM的教学频道</li>
        <li><strong><a href="https://www.youtube.com/@STLChessClub" target="_blank">Saint Louis Chess Club</a></strong> - 专业讲座和比赛</li>
        <li><strong><a href="https://www.youtube.com/@ChessNetwork" target="_blank">ChessNetwork</a></strong> - 清晰的战术讲解</li>
    </ul>
</div>

<h3><i class="fas fa-laptop"></i> 国际象棋软件</h3>
<div class="resource-card">
    <h4>推荐软件工具</h4>
    <ul>
        <li><strong>ChessBase</strong> - 专业数据库软件（付费）</li>
        <li><strong>Stockfish</strong> - 最强免费引擎</li>
        <li><strong>Lucas Chess</strong> - 免费训练软件，适合初学者</li>
        <li><strong>Arena Chess GUI</strong> - 免费的引擎界面</li>
    </ul>
</div>

<div class="alert alert-success mt-4">
    <h4><i class="fas fa-question-circle"></i> 需要帮助？</h4>
    <p>如果您在使用这些资源时遇到任何问题，或者需要更多学习建议，欢迎联系我们的教练团队：</p>
    <p><strong>邮箱：</strong>chess@boweneducation.org</p>
</div>

<style>
.resource-card {
    background: #f8f9fa;
    border-left: 4px solid #0066cc;
    padding: 15px;
    margin-bottom: 20px;
}
.resource-card h4 {
    color: #0066cc;
    margin-top: 0;
}
.resource-card h4 a {
    color: #0066cc;
    text-decoration: none;
}
.resource-card h4 a:hover {
    text-decoration: underline;
}
</style>',
'published', datetime('now'), datetime('now'), datetime('now'));


-- ================================================================
-- 第四步：为"新闻与精彩回顾"栏目创建文章
-- ================================================================

-- 文章 1: 俱乐部年度盛典回顾
INSERT INTO post (id, column_id, title, slug, summary, content_html, is_recommended, status, is_approved, published_at, created_at, updated_at)
VALUES (19, 29, '博文国际象棋俱乐部2024年度盛典圆满落幕', 'chess-annual-event-2024',
'博文国际象棋俱乐部2024年度盛典于12月举办，表彰优秀学员，展望2025年发展规划。',
'<h2>年度盛典精彩回顾</h2>
<p>2024年12月15日下午，博文国际象棋俱乐部在Sale Sports Centre成功举办了年度盛典活动。本次活动回顾了2024年俱乐部的发展成果，表彰了优秀学员和教练，并展望了2025年的发展规划。</p>

<h3>2024年成绩回顾</h3>
<p>2024年对博文国际象棋俱乐部来说是硕果累累的一年：</p>
<ul>
    <li><strong>会员增长：</strong>俱乐部注册会员从年初的60人增长到80人，增长33%</li>
    <li><strong>比赛成绩：</strong>学员在各级比赛中获得15个奖项，包括3个冠军</li>
    <li><strong>ECF认证：</strong>20名学员获得ECF官方等级分认证</li>
    <li><strong>教学创新：</strong>成功推出在线课程，服务更多学员</li>
</ul>

<h3>优秀学员表彰</h3>
<p>年度盛典上，俱乐部表彰了2024年度的优秀学员：</p>
<ul>
    <li><strong>年度最佳进步奖：</strong>李小明（从初学者成长为中级班优秀学员）</li>
    <li><strong>年度最佳新人奖：</strong>王晓芳（首年参赛即获得U12组第三名）</li>
    <li><strong>年度MVP：</strong>张锐（代表俱乐部参加多项比赛，获得优异成绩）</li>
    <li><strong>最佳团队精神奖：</strong>赵明、李强、陈晓丽（积极参与俱乐部活动，互帮互助）</li>
</ul>

<h3>教练团队表彰</h3>
<p>主教练李老师荣获"年度最佳教练"称号，表彰他在教学和比赛指导中的杰出贡献。助教王老师获得"最受欢迎教练"称号。</p>

<h3>精彩活动</h3>
<p>盛典期间举办了多项活动：</p>
<ul>
    <li><strong>车轮战表演：</strong>李教练一对十车轮战</li>
    <li><strong>蒙目棋表演：</strong>王教练蒙目同时对战三人</li>
    <li><strong>经典对局讲解：</strong>分享2024年世界冠军赛精彩对局</li>
    <li><strong>互动问答：</strong>学员与教练面对面交流</li>
</ul>

<h3>2025年展望</h3>
<p>俱乐部负责人在盛典上分享了2025年的发展规划：</p>
<ul>
    <li>计划举办更多内部比赛和训练营</li>
    <li>加强与ECF的合作，提供更多认证机会</li>
    <li>扩大在线课程规模，服务更多学员</li>
    <li>组织学员参观职业比赛，拓宽视野</li>
    <li>引进新的教学设备和软件</li>
</ul>

<p class="mt-4"><em>感谢所有学员、家长和教练团队的支持！让我们共同期待2025年更加精彩的表现！</em></p>',
1, 'published', 1, 1, datetime('now'), datetime('now'), datetime('now'));

-- 文章 2: 小棋手成长故事
INSERT INTO post (id, column_id, title, slug, summary, content_html, is_recommended, status, is_approved, published_at, created_at, updated_at)
VALUES (20, 29, '从零基础到冠军：张明的国际象棋成长之路', 'student-success-story-zhang-ming',
'记录张明同学从零基础开始学习国际象棋，到获得校际锦标赛冠军的成长历程。',
'<h2>一个小棋手的成长故事</h2>
<p>2022年9月，8岁的张明第一次来到博文国际象棋俱乐部时，还不知道国际象棋的棋子怎么走。两年多后的今天，他已经成为曼彻斯特地区U12组的佼佼者，在2024年秋季校际锦标赛中获得冠军。</p>

<h3>初识国际象棋</h3>
<p>"一开始只是觉得好玩，"张明的妈妈回忆道，"他在学校的国际象棋兴趣小组接触到这个游戏，回家后就一直缠着我们要学。"</p>

<p>在启蒙班的第一节课上，李教练发现张明对国际象棋有着超乎寻常的兴趣。"他总是第一个举手回答问题，课后也会缠着我多讲一会儿，"李教练说，"这种对学习的热情是非常难得的。"</p>

<h3>快速成长</h3>
<p>仅用了半年时间，张明就从启蒙班升到了初级班。他每天放学后都要在Lichess上练习战术题，周末的训练课从不缺席。</p>

<p>"张明很聪明，但更重要的是他的勤奋和专注，"李教练评价道，"很多孩子学棋只是三分钟热度，但张明坚持了下来，而且越学越有兴趣。"</p>

<h3>第一次比赛</h3>
<p>2023年3月，张明参加了他的第一场正式比赛——俱乐部内部快棋赛。虽然只获得了第五名，但这次经历让他意识到实战的重要性。</p>

<p>"比赛和平时练习完全不同，"张明说，"对手的每一步棋都让我紧张，时间压力也很大。但我很享受这种挑战的感觉。"</p>

<h3>突破瓶颈</h3>
<p>2023年下半年，张明进入了一个瓶颈期。连续几次内部比赛的成绩都不理想，一度让他有些气馁。</p>

<p>李教练发现了问题所在："他的战术能力很强，但缺乏整体的战略思维，经常在占优的情况下找不到继续进攻的方向。"</p>

<p>针对这个问题，李教练为张明制定了专门的训练计划，重点学习局面评估和制定计划。通过系统的学习和大量实战，张明逐渐掌握了中局的精髓。</p>

<h3>通往冠军之路</h3>
<p>2024年初，张明升入中级班，开始参加ECF等级赛。他的等级分稳步上升，从最初的800分提高到1200分。</p>

<p>11月的校际锦标赛是张明的高光时刻。在七轮瑞士制比赛中，他发挥出色，前六轮取得5胜1和的成绩，提前一轮锁定冠军。</p>

<p>"决赛那盘棋我记得很清楚，"张明兴奋地说，"对手是去年的冠军，实力很强。但我牢记李教练的教导，保持冷静，一步步下出了我的计划。当对手投子认输时，我简直不敢相信自己赢了！"</p>

<h3>未来规划</h3>
<p>获得冠军后，张明并没有满足。"这只是个开始，"他说，"我希望能继续提高，参加更高水平的比赛，也许将来能代表英国参加国际比赛。"</p>

<p>李教练对张明的未来充满信心："他有天赋，更有毅力。只要保持现在的学习态度，未来一定能取得更大的成就。"</p>

<div class="alert alert-success mt-4">
    <h4>教练寄语</h4>
    <p>"张明的故事告诉我们，天赋固然重要，但热情、勤奋和坚持更加关键。国际象棋不仅教会孩子们下棋的技巧，更重要的是培养他们面对挑战、解决问题的能力。每个孩子都有自己的成长节奏，只要坚持下去，都能收获属于自己的成功。" —— 李教练</p>
</div>

<p class="mt-4"><em>祝贺张明取得优异成绩！期待更多小棋手在博文国际象棋俱乐部实现自己的梦想！</em></p>',
1, 'published', 1, 1, datetime('now'), datetime('now'), datetime('now'));

-- 文章 3: 国际象棋知识分享
INSERT INTO post (id, column_id, title, slug, summary, content_html, is_recommended, status, is_approved, published_at, created_at, updated_at)
VALUES (21, 29, '国际象棋中的"战术主题"：双重攻击详解', 'chess-tactics-double-attack',
'深入讲解国际象棋中最重要的战术主题之一——双重攻击，帮助学员提升战术能力。',
'<h2>什么是双重攻击？</h2>
<p>双重攻击（Double Attack）是国际象棋中最基本也是最重要的战术主题之一。简单来说，就是一个棋子同时攻击对方的两个或多个目标，迫使对手无法同时防守所有被攻击的棋子。</p>

<div class="alert alert-info">
    <strong>核心思想：</strong>当你的一个棋子能同时威胁对手的两个弱点时，对手最多只能保护其中一个，你就能吃掉另一个。
</div>

<h3>双重攻击的类型</h3>

<h4>1. 马的双重攻击（Fork）</h4>
<p>马是实施双重攻击最常用的棋子，因为它的特殊走法可以同时攻击不在同一直线、斜线上的多个目标。</p>

<p><strong>经典案例：</strong>马叉王和车</p>
<ul>
    <li>马跳到一个位置，同时将军并攻击对方的车</li>
    <li>对手必须应将，无法保护车</li>
    <li>你在下一步可以安全地吃掉车</li>
</ul>

<p><strong>学习要点：</strong></p>
<ul>
    <li>时刻留意对手王和重子（后、车）的相对位置</li>
    <li>寻找能让马同时攻击它们的落点</li>
    <li>注意你的马跳到该位置时是否安全</li>
</ul>

<h4>2. 兵的双重攻击</h4>
<p>兵虽然是价值最低的棋子，但其斜向吃子的特性使它也能实施有效的双重攻击。</p>

<p><strong>特点：</strong></p>
<ul>
    <li>一个兵前进后，可以同时威胁两个斜向的棋子</li>
    <li>常用于攻击对手在同一横线相邻的两个棋子</li>
    <li>迫使对手移动其中一个，另一个被吃</li>
</ul>

<h4>3. 后的双重攻击</h4>
<p>后的移动方式结合了车和象，可以在直线、斜线上实施强大的双重攻击。</p>

<p><strong>常见形式：</strong></p>
<ul>
    <li>同时攻击王和其他重子</li>
    <li>攻击两个无防护的棋子</li>
    <li>利用对方棋子的"串"（在同一线上）</li>
</ul>

<h4>4. 其他棋子的双重攻击</h4>
<ul>
    <li><strong>象：</strong>在长对角线上同时威胁多个目标</li>
    <li><strong>车：</strong>在横线或竖线上的双重攻击</li>
    <li><strong>王：</strong>在残局中，王也能实施简单的双重攻击</li>
</ul>

<h3>如何发现双重攻击机会</h3>

<p><strong>步骤1：寻找目标</strong></p>
<ul>
    <li>找出对手防守薄弱的棋子</li>
    <li>特别关注对手的王和重子（后、车）</li>
    <li>留意价值不等的两个棋子</li>
</ul>

<p><strong>步骤2：寻找攻击者</strong></p>
<ul>
    <li>看看你的哪个棋子能同时攻击这两个目标</li>
    <li>马是最常用的，但不要忽略其他棋子</li>
    <li>有时需要先走一步准备，再实施双重攻击</li>
</ul>

<p><strong>步骤3：计算安全性</strong></p>
<ul>
    <li>确认攻击的棋子移动后是否安全</li>
    <li>检查对手是否有反击手段</li>
    <li>计算接下来的变化</li>
</ul>

<h3>防御双重攻击</h3>

<p>了解如何实施双重攻击的同时，也要学会防御：</p>

<ul>
    <li><strong>预判：</strong>时刻警惕对手可能的双重攻击</li>
    <li><strong>避免：</strong>不要让你的重要棋子处于容易被双重攻击的位置</li>
    <li><strong>反击：</strong>如果对手实施双重攻击，看能否通过反击迫使对手放弃</li>
    <li><strong>弃子：</strong>有时牺牲价值较小的棋子，保护更重要的目标</li>
</ul>

<h3>练习建议</h3>

<div class="alert alert-success">
    <h4>如何提高双重攻击能力</h4>
    <ol>
        <li><strong>做战术题：</strong>在Lichess或Chess.com上专门练习"Fork"（叉）主题的题目</li>
        <li><strong>实战应用：</strong>在对局中有意识地寻找双重攻击机会</li>
        <li><strong>复盘学习：</strong>看看你错过了哪些双重攻击机会</li>
        <li><strong>研究经典对局：</strong>学习大师如何运用双重攻击</li>
    </ol>
</div>

<h3>实战案例分析</h3>

<p><strong>案例：著名的"马叉车"</strong></p>
<p>在下面这个经典局面中，白方有一个绝妙的马叉车机会...</p>
<p><em>（这里可以插入棋局图）</em></p>

<div class="alert alert-warning mt-4">
    <h4>教练提示</h4>
    <p>双重攻击是战术训练的基础，掌握了这个概念后，很多其他战术（如牵制、困子等）也会更容易理解。建议学员每天至少做10道相关战术题，持之以恒就能大幅提高战术视野。</p>
</div>

<p class="mt-4"><em>下期我们将讲解另一个重要战术主题：牵制（Pin）。敬请期待！</em></p>',
0, 'published', 1, 1, datetime('now'), datetime('now'), datetime('now'));


-- ================================================================
-- 脚本完成
-- ================================================================
COMMIT;
