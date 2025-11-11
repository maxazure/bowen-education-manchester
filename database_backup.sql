PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE alembic_version (
	version_num VARCHAR(32) NOT NULL, 
	CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);
INSERT INTO alembic_version VALUES('21fd3e69434b');
CREATE TABLE booking_service (
	name VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	duration_minutes INTEGER NOT NULL, 
	price FLOAT, 
	buffer_time_minutes INTEGER NOT NULL, 
	max_capacity INTEGER NOT NULL, 
	allow_waitlist BOOLEAN NOT NULL, 
	min_advance_hours INTEGER NOT NULL, 
	max_advance_days INTEGER NOT NULL, 
	allow_cancel_hours INTEGER NOT NULL, 
	working_days VARCHAR(100), 
	working_start_time TIME, 
	working_end_time TIME, 
	is_active BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO booking_service VALUES('Free Trial Class (Chinese School)','trial-class-chinese','Book a free 45-minute trial class for your child to experience our Chinese School programme',45,0.0,15,8,1,24,30,24,NULL,NULL,NULL,1,1,NULL,1,'2025-11-04 21:58:23.631751','2025-11-04 21:58:23.631756');
INSERT INTO booking_service VALUES('Parent Consultation','parent-consultation','One-on-one consultation with our education team to discuss your child''s learning needs',30,0.0,10,1,0,48,14,48,NULL,NULL,NULL,1,2,NULL,2,'2025-11-04 21:58:23.631757','2025-11-04 21:58:23.631758');
CREATE TABLE faq (
	category VARCHAR(100), 
	question VARCHAR(500) NOT NULL, 
	answer TEXT NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	is_pinned BOOLEAN NOT NULL, 
	view_count INTEGER NOT NULL, 
	helpful_count INTEGER NOT NULL, 
	unhelpful_count INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO faq VALUES('Enrolment','How do I enroll my child in Chinese School?','<p>You can enroll your child by filling out our online registration form or visiting our centre in person. We offer a free trial class so your child can experience our teaching approach before committing to a term.</p>',1,1,1,0,0,0,1,'2025-11-04 21:58:23.546012','2025-11-04 21:58:23.546016');
INSERT INTO faq VALUES('Courses','What is the difference between HSK and YCT examinations?','<p>HSK (Hanyu Shuiping Kaoshi) is the standardized Chinese proficiency test for adults, while YCT (Youth Chinese Test) is designed specifically for young learners aged 15 and under. YCT has a more age-appropriate vocabulary and testing format.</p>',2,1,0,0,0,0,2,'2025-11-04 21:58:23.546018','2025-11-04 21:58:23.546019');
INSERT INTO faq VALUES('Fees & Payment','What are your fees and payment terms?','<p>Our fees are charged per term (12 weeks). Payment is due at the start of each term. We accept bank transfer, card payments, and cash. Sibling discounts of 10% are available for families enrolling multiple children.</p>',3,1,0,0,0,0,3,'2025-11-04 21:58:23.546021','2025-11-04 21:58:23.546022');
CREATE TABLE faq_category (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	description TEXT, 
	icon VARCHAR(50), 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (slug)
);
INSERT INTO faq_category VALUES('Enrolment','enrolment',NULL,NULL,1,1,1,'2025-11-04 21:58:23.525812','2025-11-04 21:58:23.525816');
INSERT INTO faq_category VALUES('Courses','courses',NULL,NULL,2,1,2,'2025-11-04 21:58:23.525818','2025-11-04 21:58:23.525818');
INSERT INTO faq_category VALUES('Fees & Payment','fees-payment',NULL,NULL,3,1,3,'2025-11-04 21:58:23.525819','2025-11-04 21:58:23.525820');
INSERT INTO faq_category VALUES('Facilities','facilities',NULL,NULL,4,1,4,'2025-11-04 21:58:23.525820','2025-11-04 21:58:23.525821');
CREATE TABLE file_category (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	description TEXT, 
	parent_id INTEGER, 
	icon_class VARCHAR(50), 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES file_category (id)
);
INSERT INTO file_category VALUES('Enrolment Forms','enrolment',NULL,NULL,NULL,1,1,1,'2025-11-04 21:58:23.608652','2025-11-04 21:58:23.608657');
INSERT INTO file_category VALUES('Course Materials','course-materials',NULL,NULL,NULL,2,1,2,'2025-11-04 21:58:23.608659','2025-11-04 21:58:23.608660');
INSERT INTO file_category VALUES('Policies','policies',NULL,NULL,NULL,3,1,3,'2025-11-04 21:58:23.608661','2025-11-04 21:58:23.608661');
CREATE TABLE media_file (
	filename_original VARCHAR(255) NOT NULL, 
	mime_type VARCHAR(100) NOT NULL, 
	size_bytes INTEGER NOT NULL, 
	width INTEGER, 
	height INTEGER, 
	path_original VARCHAR(500) NOT NULL, 
	path_medium VARCHAR(500), 
	path_thumb VARCHAR(500), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
INSERT INTO media_file VALUES('course-a-level-chinese.jpg','image/jpeg',114733,NULL,NULL,'/static/images/course-a-level-chinese.jpg','/static/images/course-a-level-chinese.jpg','/static/images/course-a-level-chinese.jpg',1,'2025-11-04 22:53:59.654814','2025-11-04 22:53:59.654818');
INSERT INTO media_file VALUES('course-cantonese.jpg','image/jpeg',125491,NULL,NULL,'/static/images/course-cantonese.jpg','/static/images/course-cantonese.jpg','/static/images/course-cantonese.jpg',2,'2025-11-04 22:53:59.654818','2025-11-04 22:53:59.654819');
INSERT INTO media_file VALUES('course-foundation-mandarin.jpg','image/jpeg',129900,NULL,NULL,'/static/images/course-foundation-mandarin.jpg','/static/images/course-foundation-mandarin.jpg','/static/images/course-foundation-mandarin.jpg',3,'2025-11-04 22:53:59.654819','2025-11-04 22:53:59.654821');
INSERT INTO media_file VALUES('course-gcse-chinese.jpg','image/jpeg',115996,NULL,NULL,'/static/images/course-gcse-chinese.jpg','/static/images/course-gcse-chinese.jpg','/static/images/course-gcse-chinese.jpg',4,'2025-11-04 22:53:59.654822','2025-11-04 22:53:59.654823');
INSERT INTO media_file VALUES('course-hsk-level-3.jpg','image/jpeg',112926,NULL,NULL,'/static/images/course-hsk-level-3.jpg','/static/images/course-hsk-level-3.jpg','/static/images/course-hsk-level-3.jpg',5,'2025-11-04 22:53:59.654823','2025-11-04 22:53:59.654824');
INSERT INTO media_file VALUES('hero-chess-club.jpg','image/jpeg',121566,NULL,NULL,'/static/images/hero-chess-club.jpg','/static/images/hero-chess-club.jpg','/static/images/hero-chess-club.jpg',6,'2025-11-04 22:53:59.654824','2025-11-04 22:53:59.654824');
INSERT INTO media_file VALUES('hero-chinese-new-year.jpg','image/jpeg',206766,NULL,NULL,'/static/images/hero-chinese-new-year.jpg','/static/images/hero-chinese-new-year.jpg','/static/images/hero-chinese-new-year.jpg',7,'2025-11-04 22:53:59.654825','2025-11-04 22:53:59.654825');
INSERT INTO media_file VALUES('hero-chinese-school.jpg','image/jpeg',110187,NULL,NULL,'/static/images/hero-chinese-school.jpg','/static/images/hero-chinese-school.jpg','/static/images/hero-chinese-school.jpg',8,'2025-11-04 22:53:59.654825','2025-11-04 22:53:59.654826');
INSERT INTO media_file VALUES('hero-haf-programme.jpg','image/jpeg',119878,NULL,NULL,'/static/images/hero-haf-programme.jpg','/static/images/hero-haf-programme.jpg','/static/images/hero-haf-programme.jpg',9,'2025-11-04 22:53:59.654826','2025-11-04 22:53:59.654826');
INSERT INTO media_file VALUES('hero-henan-university.jpg','image/jpeg',107905,NULL,NULL,'/static/images/hero-henan-university.jpg','/static/images/hero-henan-university.jpg','/static/images/hero-henan-university.jpg',10,'2025-11-04 22:53:59.654827','2025-11-04 22:53:59.654827');
INSERT INTO media_file VALUES('henan-university-partnership.jpg','image/jpeg',84714,NULL,NULL,'/static/images/news/henan-university-partnership.jpg','/static/images/news/henan-university-partnership.jpg','/static/images/news/henan-university-partnership.jpg',11,'2025-11-05 10:38:18','2025-11-05 10:38:18');
INSERT INTO media_file VALUES('2024-autumn-term-enrollment.jpg','image/jpeg',119053,NULL,NULL,'/static/images/news/2024-autumn-term-enrollment.jpg','/static/images/news/2024-autumn-term-enrollment.jpg','/static/images/news/2024-autumn-term-enrollment.jpg',12,'2025-11-05 10:38:18','2025-11-05 10:38:18');
INSERT INTO media_file VALUES('haf-programme-success-2024.jpg','image/jpeg',103873,NULL,NULL,'/static/images/news/haf-programme-success-2024.jpg','/static/images/news/haf-programme-success-2024.jpg','/static/images/news/haf-programme-success-2024.jpg',13,'2025-11-05 10:38:18','2025-11-05 10:38:18');
INSERT INTO media_file VALUES('chess-club-tournament-achievements.jpg','image/jpeg',135090,NULL,NULL,'/static/images/news/chess-club-tournament-achievements.jpg','/static/images/news/chess-club-tournament-achievements.jpg','/static/images/news/chess-club-tournament-achievements.jpg',14,'2025-11-05 10:38:18','2025-11-05 10:38:18');
INSERT INTO media_file VALUES('news-hero-background.jpg','image/jpeg',85797,NULL,NULL,'/static/images/news/news-hero-background.jpg','/static/images/news/news-hero-background.jpg','/static/images/news/news-hero-background.jpg',15,'2025-11-05 10:38:18','2025-11-05 10:38:18');
INSERT INTO media_file VALUES('course-foundation-mandarin.jpg','image/jpeg',106169,1024,1024,'/static/images/courses/course-foundation-mandarin.jpg','/static/images/courses/course-foundation-mandarin.jpg','/static/images/courses/course-foundation-mandarin.jpg',16,'2025-11-08 00:19:29.404795','2025-11-08 00:19:29.404795');
INSERT INTO media_file VALUES('course-gcse-chinese.jpg','image/jpeg',109682,1024,1024,'/static/images/courses/course-gcse-chinese.jpg','/static/images/courses/course-gcse-chinese.jpg','/static/images/courses/course-gcse-chinese.jpg',17,'2025-11-08 00:19:29.410866','2025-11-08 00:19:29.410866');
INSERT INTO media_file VALUES('course-a-level-chinese.jpg','image/jpeg',155121,1024,1024,'/static/images/courses/course-a-level-chinese.jpg','/static/images/courses/course-a-level-chinese.jpg','/static/images/courses/course-a-level-chinese.jpg',18,'2025-11-08 00:19:29.410898','2025-11-08 00:19:29.410898');
INSERT INTO media_file VALUES('course-hsk-level-3.jpg','image/jpeg',138453,1024,1024,'/static/images/courses/course-hsk-level-3.jpg','/static/images/courses/course-hsk-level-3.jpg','/static/images/courses/course-hsk-level-3.jpg',19,'2025-11-08 00:19:29.411082','2025-11-08 00:19:29.411082');
INSERT INTO media_file VALUES('course-cantonese-language.jpg','image/jpeg',109504,1024,1024,'/static/images/courses/course-cantonese-language.jpg','/static/images/courses/course-cantonese-language.jpg','/static/images/courses/course-cantonese-language.jpg',20,'2025-11-08 00:19:29.411104','2025-11-08 00:19:29.411104');
INSERT INTO media_file VALUES('course-gcse-mathematics.jpg','image/jpeg',97524,1024,1024,'/static/images/courses/course-gcse-mathematics.jpg','/static/images/courses/course-gcse-mathematics.jpg','/static/images/courses/course-gcse-mathematics.jpg',21,'2025-11-08 00:19:29.411123','2025-11-08 00:19:29.411123');
INSERT INTO media_file VALUES('course-a-level-physics.jpg','image/jpeg',98084,1024,1024,'/static/images/courses/course-a-level-physics.jpg','/static/images/courses/course-a-level-physics.jpg','/static/images/courses/course-a-level-physics.jpg',22,'2025-11-08 00:19:29.411141','2025-11-08 00:19:29.411141');
INSERT INTO media_file VALUES('post-foundation-mandarin.jpg','image/jpeg',121788,1024,1024,'/static/images/courses/post-foundation-mandarin.jpg','/static/images/courses/post-foundation-mandarin.jpg','/static/images/courses/post-foundation-mandarin.jpg',23,'2025-11-08 09:15:01.430206','2025-11-08 09:15:01.430206');
INSERT INTO media_file VALUES('post-primary-mandarin.jpg','image/jpeg',102315,1024,1024,'/static/images/courses/post-primary-mandarin.jpg','/static/images/courses/post-primary-mandarin.jpg','/static/images/courses/post-primary-mandarin.jpg',24,'2025-11-08 09:15:01.434021','2025-11-08 09:15:01.434021');
INSERT INTO media_file VALUES('post-gcse-chinese.jpg','image/jpeg',102480,1024,1024,'/static/images/courses/post-gcse-chinese.jpg','/static/images/courses/post-gcse-chinese.jpg','/static/images/courses/post-gcse-chinese.jpg',25,'2025-11-08 09:15:01.434195','2025-11-08 09:15:01.434195');
INSERT INTO media_file VALUES('post-a-level-chinese.jpg','image/jpeg',97658,1024,1024,'/static/images/courses/post-a-level-chinese.jpg','/static/images/courses/post-a-level-chinese.jpg','/static/images/courses/post-a-level-chinese.jpg',26,'2025-11-08 09:15:01.434231','2025-11-08 09:15:01.434231');
INSERT INTO media_file VALUES('post-hsk-preparation.jpg','image/jpeg',96794,1024,1024,'/static/images/courses/post-hsk-preparation.jpg','/static/images/courses/post-hsk-preparation.jpg','/static/images/courses/post-hsk-preparation.jpg',27,'2025-11-08 09:15:01.434264','2025-11-08 09:15:01.434264');
INSERT INTO media_file VALUES('post-beginner-cantonese.jpg','image/jpeg',106780,1024,1024,'/static/images/courses/post-beginner-cantonese.jpg','/static/images/courses/post-beginner-cantonese.jpg','/static/images/courses/post-beginner-cantonese.jpg',28,'2025-11-08 09:15:01.434438','2025-11-08 09:15:01.434438');
INSERT INTO media_file VALUES('post-gcse-cantonese.jpg','image/jpeg',88137,1024,1024,'/static/images/courses/post-gcse-cantonese.jpg','/static/images/courses/post-gcse-cantonese.jpg','/static/images/courses/post-gcse-cantonese.jpg',29,'2025-11-08 09:15:01.434467','2025-11-08 09:15:01.434467');
CREATE TABLE newsletter_campaign (
	name VARCHAR(200) NOT NULL, 
	subject VARCHAR(200) NOT NULL, 
	preview_text VARCHAR(255), 
	content_html TEXT NOT NULL, 
	content_text TEXT, 
	status VARCHAR(9) NOT NULL, 
	scheduled_at DATETIME, 
	sent_at DATETIME, 
	target_groups VARCHAR(255), 
	target_all BOOLEAN NOT NULL, 
	total_recipients INTEGER NOT NULL, 
	total_sent INTEGER NOT NULL, 
	total_failed INTEGER NOT NULL, 
	total_opened INTEGER NOT NULL, 
	total_clicked INTEGER NOT NULL, 
	total_unsubscribed INTEGER NOT NULL, 
	total_bounced INTEGER NOT NULL, 
	from_name VARCHAR(100), 
	from_email VARCHAR(100), 
	reply_to_email VARCHAR(100), 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id)
);
CREATE TABLE newsletter_subscriber (
	email VARCHAR(100) NOT NULL, 
	first_name VARCHAR(50), 
	last_name VARCHAR(50), 
	status VARCHAR(12) NOT NULL, 
	is_verified BOOLEAN NOT NULL, 
	subscription_source VARCHAR(100), 
	subscription_ip VARCHAR(50), 
	subscribed_at DATETIME, 
	unsubscribed_at DATETIME, 
	unsubscribe_reason TEXT, 
	group_tags VARCHAR(255), 
	total_emails_sent INTEGER NOT NULL, 
	total_emails_opened INTEGER NOT NULL, 
	total_links_clicked INTEGER NOT NULL, 
	last_email_sent_at DATETIME, 
	last_email_opened_at DATETIME, 
	preferred_language VARCHAR(10), 
	email_frequency VARCHAR(7) NOT NULL, 
	notes TEXT, 
	bounce_count INTEGER NOT NULL, 
	complaint_count INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email)
);
CREATE TABLE portfolio_category (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	description TEXT, 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (slug)
);
CREATE TABLE site_column (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	column_type VARCHAR(11) NOT NULL, 
	parent_id INTEGER, 
	icon VARCHAR(50), 
	sort_order INTEGER NOT NULL, 
	show_in_nav BOOLEAN NOT NULL, 
	is_enabled BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, menu_location VARCHAR(20) NOT NULL DEFAULT 'header', 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES site_column (id), 
	UNIQUE (slug)
);
INSERT INTO site_column VALUES('首页','home','CUSTOM',NULL,NULL,1,1,1,1,'2025-11-04 21:58:23.384980','2025-11-05 02:27:06.860060','HEADER');
INSERT INTO site_column VALUES('关于博文','about','SINGLE_PAGE',NULL,NULL,2,1,1,2,'2025-11-04 21:58:23.384983','2025-11-04 21:58:23.384983','HEADER');
INSERT INTO site_column VALUES('中文学校','school','CUSTOM',NULL,NULL,4,1,1,3,'2025-11-04 21:58:23.384984','2025-11-05 06:02:28.491805','HEADER');
INSERT INTO site_column VALUES('补习中心','tuition','PRODUCT',NULL,NULL,5,1,1,4,'2025-11-04 21:58:23.384984','2025-11-05 02:27:32.968280','HEADER');
INSERT INTO site_column VALUES('国际象棋俱乐部','chess','CUSTOM',NULL,NULL,6,1,1,5,'2025-11-04 21:58:23.384985','2025-11-05 02:27:32.968280','HEADER');
INSERT INTO site_column VALUES('政府项目','programmes','CUSTOM',NULL,NULL,8,1,1,6,'2025-11-04 21:58:23.384985','2025-11-05 02:27:32.968281','HEADER');
INSERT INTO site_column VALUES('博文活动','events','CUSTOM',NULL,NULL,9,1,1,7,'2025-11-04 21:58:23.384986','2025-11-05 02:27:32.968283','HEADER');
INSERT INTO site_column VALUES('博文新闻','news','POST',2,NULL,3,1,1,8,'2025-11-04 21:58:23.384986','2025-11-05 02:27:32.968284','HEADER');
INSERT INTO site_column VALUES('图库','gallery','CUSTOM',NULL,NULL,9,0,1,9,'2025-11-04 21:58:23.384987','2025-11-07 08:11:45.437356','FOOTER');
INSERT INTO site_column VALUES('常见问题','faq','SINGLE_PAGE',NULL,NULL,10,0,1,10,'2025-11-04 21:58:23.384987','2025-11-07 06:48:05.038682','FOOTER');
INSERT INTO site_column VALUES('联系我们','contact','SINGLE_PAGE',NULL,NULL,10,1,1,11,'2025-11-04 21:58:23.384988','2025-11-05 01:09:49.165359','HEADER');
INSERT INTO site_column VALUES('羽毛球俱乐部','badminton','CUSTOM',NULL,NULL,7,1,1,12,'2025-11-05 01:09:49.166605','2025-11-05 02:27:32.968284','HEADER');
INSERT INTO site_column VALUES('课程设置','school-curriculum','POST',3,NULL,1,0,1,13,'2025-11-05 06:02:28.512109','2025-11-05 06:02:28.512112','HEADER');
INSERT INTO site_column VALUES('学期日期','school-term-dates','SINGLE_PAGE',3,NULL,2,0,1,14,'2025-11-05 06:02:28.513188','2025-11-05 06:02:28.513190','HEADER');
INSERT INTO site_column VALUES('PTA家长教师协会','school-pta','SINGLE_PAGE',3,NULL,3,0,1,15,'2025-11-05 06:02:28.513956','2025-11-05 06:02:28.513957','HEADER');
INSERT INTO site_column VALUES('我们的比赛','chess-competitions','POST',5,NULL,1,0,1,16,'2025-11-05 06:02:28.514732','2025-11-05 06:02:28.514733','HEADER');
INSERT INTO site_column VALUES('棋手信息','chess-players','SINGLE_PAGE',5,NULL,2,0,1,17,'2025-11-05 06:02:28.515467','2025-11-05 06:02:28.515468','HEADER');
INSERT INTO site_column VALUES('相册','chess-gallery','CUSTOM',5,NULL,3,0,1,18,'2025-11-05 06:02:28.516193','2025-11-07 19:57:00.645766','HEADER');
INSERT INTO site_column VALUES('赛事活动','badminton-events','POST',12,NULL,1,0,1,19,'2025-11-05 06:02:28.516923','2025-11-05 06:02:28.516924','HEADER');
INSERT INTO site_column VALUES('训练时间表','badminton-schedule','SINGLE_PAGE',12,NULL,2,0,1,20,'2025-11-05 06:02:28.517638','2025-11-05 06:02:28.517639','HEADER');
INSERT INTO site_column VALUES('精彩瞬间','badminton-gallery','CUSTOM',12,NULL,3,0,1,21,'2025-11-05 06:02:28.518324','2025-11-07 19:57:00.647038','HEADER');
INSERT INTO site_column VALUES('HAF项目','programmes-haf','SINGLE_PAGE',6,NULL,1,0,1,22,'2025-11-05 06:02:28.519031','2025-11-05 06:02:28.519033','HEADER');
INSERT INTO site_column VALUES('公园活动','programmes-parks','POST',6,NULL,2,0,1,23,'2025-11-05 06:02:28.519708','2025-11-05 06:02:28.519709','HEADER');
INSERT INTO site_column VALUES('河南大学合作','events-henan','SINGLE_PAGE',7,NULL,1,0,1,24,'2025-11-05 06:02:28.520273','2025-11-05 06:02:28.520274','HEADER');
INSERT INTO site_column VALUES('博文集团','about-company','SINGLE_PAGE',2,NULL,1,1,1,25,'2025-11-07 02:35:49','2025-11-07 02:35:49','HEADER');
CREATE TABLE site_setting (
	setting_key VARCHAR(100) NOT NULL, 
	value_text TEXT NOT NULL, 
	value_type VARCHAR(6) NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (setting_key)
);
INSERT INTO site_setting VALUES('site_name','Bowen Education Group','string',1,'2025-11-04 21:58:23.365500','2025-11-04 21:58:23.365503');
INSERT INTO site_setting VALUES('site_name_chinese','博文集团','string',2,'2025-11-04 21:58:23.365504','2025-11-04 21:58:23.365504');
INSERT INTO site_setting VALUES('tagline','Bridging East and West Through Education','string',3,'2025-11-04 21:58:23.365505','2025-11-04 21:58:23.365507');
INSERT INTO site_setting VALUES('tagline_chinese','中西融汇，博学致远','string',4,'2025-11-04 21:58:23.365508','2025-11-04 21:58:23.365508');
INSERT INTO site_setting VALUES('company_phone','+44 (0)161 6672668','string',5,'2025-11-04 21:58:23.365509','2025-11-04 21:58:23.365509');
INSERT INTO site_setting VALUES('company_email','info@boweneducation.org','string',6,'2025-11-04 21:58:23.365509','2025-11-04 21:58:23.365510');
INSERT INTO site_setting VALUES('company_address','1/F, 2A Curzon Road, Sale, Manchester, M33 7DR, UK','string',7,'2025-11-04 21:58:23.365510','2025-11-04 21:58:23.365510');
INSERT INTO site_setting VALUES('company_wechat','bowenedu_uk','string',8,'2025-11-04 21:58:23.365511','2025-11-04 21:58:23.365511');
INSERT INTO site_setting VALUES('founded_year','2018','string',9,'2025-11-04 21:58:23.365511','2025-11-04 21:58:23.365511');
INSERT INTO site_setting VALUES('business_hours','Monday - Friday: 9:00 - 17:00, Saturday - Sunday: 10:00 - 16:00','string',10,'2025-11-04 21:58:23.365512','2025-11-04 21:58:23.365512');
INSERT INTO site_setting VALUES('mission','To provide high-quality Chinese language education and cultural enrichment programmes that bridge Eastern and Western educational traditions, empowering students to succeed in a globalised world.','string',11,'2025-11-04 21:58:23.365512','2025-11-04 21:58:23.365513');
INSERT INTO site_setting VALUES('vision','To be the leading Chinese education provider in Greater Manchester, recognised for academic excellence, cultural authenticity, and community impact.','string',12,'2025-11-04 21:58:23.365513','2025-11-04 21:58:23.365513');
INSERT INTO site_setting VALUES('about_description','Bowen Education Group is a registered educational institution in Manchester, UK, offering comprehensive Chinese language programmes from Foundation to A-Level, academic tutoring, chess club, badminton club, and government-funded community programmes.','string',13,'2025-11-04 21:58:23.365513','2025-11-04 21:58:23.365514');
CREATE TABLE user (
	username VARCHAR(100) NOT NULL, 
	email VARCHAR(100) NOT NULL, 
	phone VARCHAR(50), 
	password_hash VARCHAR(255) NOT NULL, 
	first_name VARCHAR(50), 
	last_name VARCHAR(50), 
	display_name VARCHAR(100), 
	bio TEXT, 
	avatar_url VARCHAR(255), 
	date_of_birth DATETIME, 
	gender VARCHAR(17), 
	address_line1 VARCHAR(255), 
	address_line2 VARCHAR(255), 
	city VARCHAR(100), 
	state VARCHAR(100), 
	postal_code VARCHAR(20), 
	country VARCHAR(100), 
	role VARCHAR(6) NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	is_verified BOOLEAN NOT NULL, 
	is_staff BOOLEAN NOT NULL, 
	membership_level VARCHAR(8) NOT NULL, 
	membership_expires_at DATETIME, 
	points INTEGER NOT NULL, 
	total_earned_points INTEGER NOT NULL, 
	last_login_at DATETIME, 
	last_login_ip VARCHAR(50), 
	login_count INTEGER NOT NULL, 
	failed_login_attempts INTEGER NOT NULL, 
	locked_until DATETIME, 
	email_notifications BOOLEAN NOT NULL, 
	sms_notifications BOOLEAN NOT NULL, 
	marketing_emails BOOLEAN NOT NULL, 
	facebook_id VARCHAR(100), 
	google_id VARCHAR(100), 
	linkedin_id VARCHAR(100), 
	notes TEXT, 
	email_verified_at DATETIME, 
	phone_verified_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	UNIQUE (email), 
	UNIQUE (username)
);
CREATE TABLE video_category (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	description TEXT, 
	parent_id INTEGER, 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES video_category (id)
);
INSERT INTO video_category VALUES('Student Performances','performances','',NULL,1,1,1,'2025-11-04 21:58:23.566413','2025-11-04 21:58:23.566418');
INSERT INTO video_category VALUES('Cultural Events','cultural-events','',NULL,2,1,2,'2025-11-04 21:58:23.566420','2025-11-04 21:58:23.566421');
INSERT INTO video_category VALUES('Teaching Resources','teaching-resources','',NULL,3,1,3,'2025-11-04 21:58:23.566421','2025-11-04 21:58:23.566422');
CREATE TABLE comment (
	commentable_type VARCHAR(50) NOT NULL, 
	commentable_id INTEGER NOT NULL, 
	author_name VARCHAR(100) NOT NULL, 
	author_email VARCHAR(100) NOT NULL, 
	author_website VARCHAR(255), 
	user_id INTEGER, 
	content TEXT NOT NULL, 
	rating INTEGER, 
	parent_id INTEGER, 
	status VARCHAR(8) NOT NULL, 
	is_featured BOOLEAN NOT NULL, 
	admin_reply TEXT, 
	replied_at DATETIME, 
	helpful_count INTEGER NOT NULL, 
	report_count INTEGER NOT NULL, 
	ip_address VARCHAR(45), 
	user_agent VARCHAR(500), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parent_id) REFERENCES comment (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE custom_field_def (
	module_type VARCHAR(7) NOT NULL, 
	column_id INTEGER, 
	field_key VARCHAR(100) NOT NULL, 
	label VARCHAR(100) NOT NULL, 
	input_type VARCHAR(11) NOT NULL, 
	required BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	min_value FLOAT, 
	max_value FLOAT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id)
);
CREATE TABLE event (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT NOT NULL, 
	summary TEXT, 
	event_type VARCHAR(10) NOT NULL, 
	start_datetime DATETIME NOT NULL, 
	end_datetime DATETIME NOT NULL, 
	timezone VARCHAR(50), 
	registration_deadline DATETIME, 
	location_type VARCHAR(8) NOT NULL, 
	venue_name VARCHAR(200), 
	venue_address VARCHAR(500), 
	venue_city VARCHAR(100), 
	venue_postal_code VARCHAR(20), 
	online_meeting_url VARCHAR(500), 
	online_meeting_password VARCHAR(100), 
	max_attendees INTEGER, 
	current_attendees INTEGER NOT NULL, 
	allow_waitlist BOOLEAN NOT NULL, 
	waitlist_count INTEGER NOT NULL, 
	is_free BOOLEAN NOT NULL, 
	ticket_price FLOAT, 
	early_bird_price FLOAT, 
	early_bird_deadline DATETIME, 
	cover_media_id INTEGER, 
	status VARCHAR(9) NOT NULL, 
	is_featured BOOLEAN NOT NULL, 
	is_public BOOLEAN NOT NULL, 
	organizer_name VARCHAR(200), 
	organizer_email VARCHAR(100), 
	organizer_phone VARCHAR(50), 
	contact_person VARCHAR(100), 
	agenda TEXT, 
	speakers TEXT, 
	materials_url VARCHAR(500), 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	tags VARCHAR(255), 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id)
);
INSERT INTO event VALUES('Chinese New Year Celebration 2025','chinese-new-year-2025','Join us for our annual Chinese New Year celebration featuring traditional performances, calligraphy workshops, dumpling making, and lion dance!','Annual Chinese New Year celebration with performances and cultural activities','social','2025-12-15 10:00:00','2025-02-10 17:00:00.000000','Pacific/Auckland',NULL,'physical','Manchester Community Centre','123 Main Street','Manchester','M1 1AA',NULL,NULL,200,0,1,0,0,5.0,NULL,NULL,NULL,'published',1,1,'Bowen Education Group','info@boweneducation.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,1,'2025-11-04 21:58:23.507544','2025-11-04 21:58:23.507548');
INSERT INTO event VALUES('HSK Level 3 Mock Examination','hsk-3-mock-exam','Full mock examination for HSK Level 3 students including listening, reading, and writing sections. Get familiarized with exam format and timing.','Practice HSK Level 3 exam under real conditions','training','2025-03-15 10:00:00.000000','2025-03-15 12:00:00.000000','Pacific/Auckland',NULL,'physical','Bowen Education Centre','1/F, 2A Curzon Road, Sale','Manchester','M33 7DR',NULL,NULL,40,0,0,0,1,NULL,NULL,NULL,NULL,'published',0,0,'Bowen Education Group','info@boweneducation.org',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,2,'2025-11-04 21:58:23.507550','2025-11-04 21:58:23.507550');
INSERT INTO event VALUES('2025春节联欢晚会','2025-spring-festival-gala',replace('\n<h3>🧧 2025年博文春节联欢晚会</h3>\n\n<div class="event-details">\n    <div class="event-header">\n        <h4>活动简介</h4>\n        <p>博文教育集团诚邀您参加2025年春节联欢晚会！这是一场充满中华文化韵味的盛大庆典，我们将与社区朋友们一起庆祝中国新年，分享传统文化，品尝美食，欣赏精彩的文艺表演。</p>\n    </div>\n\n    <div class="event-content">\n        <div class="event-section">\n            <h4><i class="fas fa-star"></i> 活动亮点</h4>\n            <ul>\n                <li>传统舞龙舞狮表演</li>\n                <li>学生文艺汇演（歌舞、器乐、朗诵）</li>\n                <li>传统美食品尝</li>\n                <li>书法展示体验</li>\n                <li>互动游戏和抽奖环节</li>\n                <li>新年祝福交换</li>\n            </ul>\n        </div>\n\n        <div class="event-section">\n            <h4><i class="fas fa-users"></i> 参与对象</h4>\n            <p>博文教育全体学生、家长、教师以及社区朋友</p>\n            <div class="audience">\n                <span class="audience-tag">👨‍👩‍👧‍👦 家庭亲子</span>\n                <span class="audience-tag">👫 社区居民</span>\n                <span class="audience-tag">🎓 教职员工</span>\n            </div>\n        </div>\n\n        <div class="event-section">\n            <h4><i class="fas fa-utensils"></i> 美食安排</h4>\n            <p>我们将提供丰富的传统中式美食：</p>\n            <div class="food-grid">\n                <div class="food-item">🥟 饺子</div>\n                <div class="food-item">🍜 汤圆</div>\n                <div class="food-item">🥢 春卷</div>\n                <div class="food-item">🍗 年糕</div>\n                <div class="food-item">🍊 橘子</div>\n                <div class="food-item">🧈 茶点</div>\n            </div>\n        </div>\n\n        <div class="event-section">\n            <h4><i class="fas fa-ticket-alt"></i> 参与方式</h4>\n            <p>本次活动<strong>完全免费</strong>，但需要提前报名以便我们准备足够的食物和礼品。</p>\n            <div class="registration-info">\n                <p><strong>报名截止日期：</strong>2025年2月5日</p>\n                <p><strong>报名方式：</strong>请联系学校办公室或通过微信家长群报名</p>\n                <p><strong>咨询电话：</strong>0161 969 3071</p>\n            </div>\n        </div>\n\n        <div class="event-section">\n            <h4><i class="fas fa-calendar-check"></i> 温馨提示</h4>\n            <ul>\n                <li>请穿着节庆服装，可选择红色元素</li>\n                <li>可携带小礼物参与新年祝福交换</li>\n                <li>现场将提供停车位</li>\n                <li>请准时到场，活动将在14:00准时开始</li>\n            </ul>\n        </div>\n    </div>\n</div>\n\n<style>\n.event-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.event-header {\n    background: linear-gradient(135deg, #dc2626 0%, #f97316 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.event-header p {\n    font-size: 1.1rem;\n    line-height: 1.6;\n    margin: 0;\n}\n\n.event-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.event-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #dc2626;\n}\n\n.event-section h4 {\n    color: #dc2626;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.event-section ul {\n    list-style: none;\n    padding: 0;\n}\n\n.event-section li {\n    padding: 0.5rem 0;\n    padding-left: 1.5rem;\n    position: relative;\n    color: #6c757d;\n}\n\n.event-section li::before {\n    content: "•";\n    color: #dc2626;\n    position: absolute;\n    left: 0;\n    font-weight: bold;\n}\n\n.audience {\n    display: flex;\n    gap: 1rem;\n    margin-top: 1rem;\n    flex-wrap: wrap;\n}\n\n.audience-tag {\n    background: white;\n    padding: 0.5rem 1rem;\n    border-radius: 20px;\n    border: 2px solid #dc2626;\n    color: #dc2626;\n    font-weight: 500;\n}\n\n.food-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.food-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    text-align: center;\n    font-weight: 500;\n    color: #6c757d;\n}\n\n.registration-info {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    margin-top: 1rem;\n}\n\n.registration-info p {\n    margin-bottom: 0.5rem;\n    color: #6c757d;\n}\n</style>\n            ','\n',char(10)),'2025年春节联欢晚会 - 传统舞龙舞狮、学生文艺汇演、传统美食品尝','social','2025-12-15 10:00:00','2025-02-10 17:00:00',NULL,NULL,'physical','博文教育曼彻斯特校区','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,200,0,1,0,1,NULL,NULL,NULL,NULL,'published',1,1,'博文教育集团','info@boweneducation.org','0161 969 3071','前台接待',NULL,NULL,NULL,'2025年春节联欢晚会 | 博文教育集团','博文教育2025年春节联欢晚会，传统舞龙舞狮、学生文艺汇演、美食品尝等丰富活动','春节,联欢会,文化,家庭',NULL,3,'2025-11-07T17:07:33.363867','2025-11-07T17:07:33.363867');
INSERT INTO event VALUES('国际象棋夏季训练营','chess-summer-camp-2025',replace('\n<h3>♟️ 2025年国际象棋夏季训练营</h3>\n\n<div class="camp-details">\n    <div class="camp-header">\n        <h4>训练营简介</h4>\n        <p>博文国际象棋俱乐部举办的专业夏季训练营，由IM（国际大师）和FIDE认证教练执教，为学生提供系统的国际象棋训练和实战经验。</p>\n    </div>\n\n    <div class="camp-content">\n        <div class="camp-section">\n            <h4><i class="fas fa-calendar-alt"></i> 训练安排</h4>\n            <div class="schedule">\n                <div class="schedule-item">\n                    <div class="date">7月28日-8月1日（第一周）</div>\n                    <div class="level">初级班</div>\n                    <div class="focus">基础战术、开局原理</div>\n                </div>\n                <div class="schedule-item">\n                    <div class="date">8月4日-8月8日（第二周）</div>\n                    <div class="level">中级班</div>\n                    <div class="focus">中局技巧、残局练习</div>\n                </div>\n                <div class="schedule-item">\n                    <div class="date">8月11日-8月15日（第三周）</div>\n                    <div class="level">高级班</div>\n                    <div class="focus">比赛策略、心理训练</div>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-trophy"></i> 训练内容</h4>\n            <div class="training-grid">\n                <div class="training-item">\n                    <div class="icon">📚</div>\n                    <h5>理论学习</h5>\n                    <ul>\n                        <li>开局系统学习</li>\n                        <li>战术组合识别</li>\n                        <li>残局技巧掌握</li>\n                    </ul>\n                </div>\n                <div class="training-item">\n                    <div class="icon">🎮</div>\n                    <h5>实战训练</h5>\n                    <ul>\n                        <li>友谊对局</li>\n                        <li>闪电战比赛</li>\n                        <li>团队竞赛</li>\n                    </ul>\n                </div>\n                <div class="training-item">\n                    <div class="icon">🧠</div>\n                    <h5>心理训练</h5>\n                    <ul>\n                        <li>比赛心理准备</li>\n                        <li>时间管理技巧</li>\n                        <li>压力应对策略</li>\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-user-graduate"></i> 教练团队</h4>\n            <div class="coaches">\n                <div class="coach">\n                    <h5>主教练 - IM李明</h5>\n                    <p>国际大师，15年教学经验，培养多名地区冠军</p>\n                </div>\n                <div class="coach">\n                    <h5>助理教练 - FIDE教练王华</h5>\n                    <p>FIDE认证教练，专攻青少年培训</p>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-gift"></i> 训练营福利</h4>\n            <div class="benefits">\n                <ul>\n                    <li>专业训练教材</li>\n                    <li>训练证书</li>\n                    <li>结业比赛奖品</li>\n                    <li>每日营养午餐</li>\n                    <li>训练T恤</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n.camp-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.camp-header {\n    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.camp-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.camp-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #6366f1;\n}\n\n.camp-section h4 {\n    color: #6366f1;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.schedule {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.schedule-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    display: grid;\n    grid-template-columns: 1fr auto 2fr;\n    gap: 1rem;\n    align-items: center;\n}\n\n.date {\n    font-weight: 600;\n    color: #1f2937;\n}\n\n.level {\n    background: #6366f1;\n    color: white;\n    padding: 0.25rem 0.75rem;\n    border-radius: 20px;\n    font-size: 0.9rem;\n}\n\n.training-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.training-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    text-align: center;\n}\n\n.training-item .icon {\n    font-size: 2rem;\n    margin-bottom: 0.5rem;\n}\n\n.training-item h5 {\n    color: #6366f1;\n    margin-bottom: 0.5rem;\n}\n\n.coaches {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.coach {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n}\n\n.coach h5 {\n    color: #6366f1;\n    margin-bottom: 0.5rem;\n}\n\n.benefits ul {\n    list-style: none;\n    padding: 0;\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 0.5rem;\n}\n\n.benefits li {\n    padding: 0.5rem;\n    background: white;\n    border-radius: 4px;\n    text-align: center;\n    color: #6c757d;\n}\n</style>\n            ','\n',char(10)),'国际象棋夏季训练营 - IM执教，分级训练，理论实战结合','training','2025-12-20 14:00:00','2025-08-15 17:00:00',NULL,NULL,'physical','博文教育曼彻斯特校区','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,30,0,1,0,0,279.99999999999999999,250.0,'2025-07-01 23:59:59',NULL,'published',1,1,'博文国际象棋俱乐部','chess@boweneducation.org','0161 969 3071','李教练','每日安排：9:00-10:30 理论课，10:45-12:00 实战训练，12:00-13:00 午餐，13:00-15:00 比赛，15:00-17:00 分析总结',NULL,NULL,'2025年国际象棋夏季训练营 | 博文教育','专业国际象棋夏季训练营，IM执教，系统训练，适合各级水平棋手','国际象棋,训练营,夏天,比赛',NULL,4,'2025-11-07T17:07:33.364207','2025-11-07T17:07:33.364207');
INSERT INTO event VALUES('HSK汉语水平考试模拟测试','hsk-mock-test-2025',replace('\n<h3>📝 HSK汉语水平考试模拟测试</h3>\n\n<div class="exam-details">\n    <div class="exam-header">\n        <h4>考试介绍</h4>\n        <p>博文中文学校定期举办HSK汉语水平考试模拟测试，帮助学生熟悉考试流程，检测学习成果，为正式考试做好充分准备。</p>\n    </div>\n\n    <div class="exam-content">\n        <div class="exam-section">\n            <h4><i class="fas fa-clipboard-list"></i> 考试安排</h4>\n            <div class="exam-schedule">\n                <div class="exam-item">\n                    <div class="exam-level">HSK 3级</div>\n                    <div class="exam-datetime">2025年3月15日 10:00-12:00</div>\n                    <div class="exam-fee">免费（在校学生）</div>\n                </div>\n                <div class="exam-item">\n                    <div class="exam-level">HSK 4级</div>\n                    <div class="exam-datetime">2025年4月19日 14:00-16:30</div>\n                    <div class="exam-fee">£10</div>\n                </div>\n                <div class="exam-item">\n                    <div class="exam-level">HSK 5级</div>\n                    <div class="exam-datetime">2025年5月17日 10:00-13:00</div>\n                    <div class="exam-fee">£15</div>\n                </div>\n            </div>\n        </div>\n\n        <div class="exam-section">\n            <h4><i class="fas fa-tasks"></i> 考试内容</h4>\n            <div class="exam-content-grid">\n                <div class="content-item">\n                    <h5>听力理解</h5>\n                    <p>模拟真实考试环境，训练听力理解能力</p>\n                </div>\n                <div class="content-item">\n                    <h5>阅读理解</h5>\n                    <p>各种文体的阅读练习，提升阅读速度</p>\n                </div>\n                <div class="content-item">\n                    <h5>书写表达</h5>\n                    <p>写作练习和语法应用训练</p>\n                </div>\n            </div>\n        </div>\n\n        <div class="exam-section">\n            <h4><i class="fas fa-chart-line"></i> 考后反馈</h4>\n            <div class="feedback">\n                <ul>\n                    <li>详细的成绩分析和评估报告</li>\n                    <li>个人学习建议和改进方案</li>\n                    <li>错题分析和知识点讲解</li>\n                    <li>一对一学习计划制定</li>\n                </ul>\n            </div>\n        </div>\n\n        <div class="exam-section">\n            <h4><i class="fas fa-user-check"></i> 报名须知</h4>\n            <div class="registration">\n                <p><strong>报名截止时间：</strong>考试前一周</p>\n                <p><strong>报名方式：</strong>通过学校办公室或微信联系</p>\n                <p><strong>注意事项：</strong></p>\n                <ul>\n                    <li>请提前15分钟到场</li>\n                    <li>携带身份证或学生证</li>\n                    <li>自备铅笔和橡皮</li>\n                    <li>手机需调至静音状态</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n.exam-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.exam-header {\n    background: linear-gradient(135deg, #059669 0%, #10b981 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.exam-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.exam-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #059669;\n}\n\n.exam-section h4 {\n    color: #059669;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.exam-schedule {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.exam-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    display: grid;\n    grid-template-columns: auto 2fr auto;\n    gap: 1rem;\n    align-items: center;\n}\n\n.exam-level {\n    background: #059669;\n    color: white;\n    padding: 0.5rem 1rem;\n    border-radius: 8px;\n    font-weight: 600;\n}\n\n.exam-content-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.content-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    text-align: center;\n}\n\n.content-item h5 {\n    color: #059669;\n    margin-bottom: 0.5rem;\n}\n\n.feedback ul {\n    list-style: none;\n    padding: 0;\n}\n\n.feedback li {\n    padding: 0.5rem 0;\n    padding-left: 1.5rem;\n    position: relative;\n    color: #6c757d;\n}\n\n.feedback li::before {\n    content: "✓";\n    color: #059669;\n    position: absolute;\n    left: 0;\n    font-weight: bold;\n}\n\n.registration ul {\n    list-style: none;\n    padding: 0;\n}\n\n.registration li {\n    padding: 0.25rem 0;\n    color: #6c757d;\n    position: relative;\n    padding-left: 1rem;\n}\n\n.registration li::before {\n    content: "•";\n    color: #059669;\n    position: absolute;\n    left: 0;\n}\n</style>\n            ','\n',char(10)),'HSK汉语水平考试模拟测试 - 真实考试环境模拟，详细成绩分析','training','2025-03-15 10:00:00','2025-03-15 12:00:00',NULL,NULL,'physical','博文中文学校','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,50,0,1,0,1,NULL,NULL,NULL,NULL,'published',0,1,'博文中文学校','info@boweneducation.org','0161 969 3071','王老师',NULL,NULL,NULL,'HSK汉语水平考试模拟测试 | 博文中文学校','HSK汉语水平考试模拟测试，真实考试环境模拟，详细成绩分析和学习建议','HSK,汉语考试,模拟测试,中文学习',NULL,5,'2025-11-07T17:07:33.364239','2025-11-07T17:07:33.364239');
INSERT INTO event VALUES('羽毛球友谊邀请赛','badminton-tournament-2025',replace('\n<h3>🏸 2025年羽毛球友谊邀请赛</h3>\n\n<div class="tournament-details">\n    <div class="tournament-header">\n        <h4>比赛介绍</h4>\n        <p>博文羽毛球俱乐部举办年度友谊邀请赛，邀请周边地区羽毛球俱乐部参与，增进友谊，切磋球技，享受羽毛球运动的乐趣。</p>\n    </div>\n\n    <div class="tournament-content">\n        <div class="tournament-section">\n            <h4><i class="fas fa-calendar-alt"></i> 比赛时间</h4>\n            <div class="time-info">\n                <p><strong>比赛日期：</strong>2025年6月21-22日（周六日）</p>\n                <p><strong>比赛时间：</strong>9:00-18:00</p>\n                <p><strong>报名截止：</strong>2025年6月15日</p>\n            </div>\n        </div>\n\n        <div class="tournament-section">\n            <h4><i class="fas fa-trophy"></i> 比赛项目</h4>\n            <div class="events-grid">\n                <div class="event-card">\n                    <h5>男子单打</h5>\n                    <p>A组：16岁以下 | B组：17岁以上</p>\n                </div>\n                <div class="event-card">\n                    <h5>女子单打</h5>\n                    <p>A组：16岁以下 | B组：17岁以上</p>\n                </div>\n                <div class="event-card">\n                    <h5>男子双打</h5>\n                    <p>无年龄限制</p>\n                </div>\n                <div class="event-card">\n                    <h5>女子双打</h5>\n                    <p>无年龄限制</p>\n                </div>\n                <div class="event-card">\n                    <h5>混合双打</h5>\n                    <p>无年龄限制</p>\n                </div>\n                <div class="event-card">\n                    <h5>家庭双打</h5>\n                    <p>家长+子女组合</p>\n                </div>\n            </div>\n        </div>\n\n        <div class="tournament-section">\n            <h4><i class="fas fa-medal"></i> 奖励设置</h4>\n            <div class="prizes">\n                <div class="prize-group">\n                    <h5>个人项目奖励</h5>\n                    <ul>\n                        <li>🥇 冠军：奖杯 + £100代金券</li>\n                        <li>🥈 亚军：奖牌 + £50代金券</li>\n                        <li>🥉 季军：奖牌 + £25代金券</li>\n                    </ul>\n                </div>\n                <div class="prize-group">\n                    <h5>特别奖励</h5>\n                    <ul>\n                        <li>🏆 最佳体育精神奖</li>\n                        <li>⭐ 最佳新人奖</li>\n                        <li>👨‍👩‍👧‍👦 最佳家庭组合奖</li>\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class="tournament-section">\n            <h4><i class="fas fa-ticket-alt"></i> 参赛费用</h4>\n            <div class="fees">\n                <div class="fee-item">\n                    <div class="category">单打项目</div>\n                    <div class="amount">£15/人</div>\n                </div>\n                <div class="fee-item">\n                    <div class="category">双打项目</div>\n                    <div class="amount">£20/对</div>\n                </div>\n                <div class="fee-item">\n                    <div class="category">家庭双打</div>\n                    <div class="amount">£10/家庭</div>\n                </div>\n            </div>\n            <p class="fee-note">*费用包含场地费、裁判费、饮用水</p>\n        </div>\n\n        <div class="tournament-section">\n            <h4><i class="fas fa-info-circle"></i> 参赛须知</h4>\n            <div class="rules">\n                <ul>\n                    <li>参赛者需自备羽毛球拍和运动装备</li>\n                    <li>比赛采用国际羽联21分制</li>\n                    <li>提供比赛用球</li>\n                    <li>现场提供免费停车</li>\n                    <li>提供休息区和更衣室</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n.tournament-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.tournament-header {\n    background: linear-gradient(135deg, #ea580c 0%, #f97316 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.tournament-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.tournament-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #ea580c;\n}\n\n.tournament-section h4 {\n    color: #ea580c;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.time-info p {\n    margin-bottom: 0.5rem;\n    color: #6c757d;\n}\n\n.events-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.event-card {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    text-align: center;\n}\n\n.event-card h5 {\n    color: #ea580c;\n    margin-bottom: 0.5rem;\n}\n\n.prizes {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.prize-group {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n}\n\n.prize-group h5 {\n    color: #ea580c;\n    margin-bottom: 0.5rem;\n}\n\n.prize-group ul {\n    list-style: none;\n    padding: 0;\n}\n\n.prize-group li {\n    padding: 0.25rem 0;\n    color: #6c757d;\n}\n\n.fees {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.fee-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n}\n\n.fee-item .category {\n    font-weight: 600;\n    color: #1f2937;\n}\n\n.fee-item .amount {\n    color: #ea580c;\n    font-weight: 700;\n    font-size: 1.2rem;\n}\n\n.fee-note {\n    margin-top: 1rem;\n    color: #6c757d;\n    font-style: italic;\n}\n\n.rules ul {\n    list-style: none;\n    padding: 0;\n}\n\n.rules li {\n    padding: 0.5rem 0;\n    padding-left: 1.5rem;\n    position: relative;\n    color: #6c757d;\n}\n\n.rules li::before {\n    content: "•";\n    color: #ea580c;\n    position: absolute;\n    left: 0;\n    font-weight: bold;\n}\n</style>\n            ','\n',char(10)),'羽毛球友谊邀请赛 - 多项目比赛，丰富奖励，促进羽毛球交流','seminar','2025-06-21 09:00:00','2025-06-22 18:00:00',NULL,NULL,'physical','博文体育中心','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,100,0,1,0,0,15.0,NULL,NULL,NULL,'published',1,1,'博文羽毛球俱乐部','badminton@boweneducation.org','0161 969 3071','李教练',NULL,NULL,NULL,'羽毛球友谊邀请赛 2025 | 博文羽毛球俱乐部','2025年羽毛球友谊邀请赛，多项目比赛，丰富奖励，欢迎各水平选手参与','羽毛球,比赛,邀请赛,体育',NULL,6,'2025-11-07T17:07:33.364258','2025-11-07T17:07:33.364258');
INSERT INTO event VALUES('家长教育讲座：如何帮助孩子学好中文','parent-education-seminar-2025',replace('\n<h3>👨‍👩‍👧‍👦 家长教育讲座</h3>\n\n<div class="seminar-details">\n    <div class="seminar-header">\n        <h4>讲座主题：如何帮助孩子学好中文</h4>\n        <p>专为海外华人家长设计的教育讲座，分享实用的中文学习方法和家庭教育策略，帮助家长更好地支持孩子的中文学习。</p>\n    </div>\n\n    <div class="seminar-content">\n        <div class="seminar-section">\n            <h4><i class="fas fa-user-clock"></i> 时间安排</h4>\n            <div class="schedule">\n                <div class="time-item">\n                    <span class="time">14:00-14:30</span>\n                    <span class="activity">签到交流</span>\n                </div>\n                <div class="time-item">\n                    <span class="time">14:30-15:30</span>\n                    <span class="activity">主题讲座</span>\n                </div>\n                <div class="time-item">\n                    <span class="time">15:30-16:00</span>\n                    <span class="activity">互动问答</span>\n                </div>\n                <div class="time-item">\n                    <span class="time">16:00-16:30</span>\n                    <span class="activity">茶歇交流</span>\n                </div>\n            </div>\n        </div>\n\n        <div class="seminar-section">\n            <h4><i class="fas fa-book-open"></i> 讲座内容</h4>\n            <div class="topics-grid">\n                <div class="topic-card">\n                    <div class="topic-icon">🏠</div>\n                    <h5>家庭语言环境营造</h5>\n                    <ul>\n                        <li>日常中文对话技巧</li>\n                        <li>家庭中文角设置</li>\n                        <li>中文读物选择</li>\n                    </ul>\n                </div>\n                <div class="topic-card">\n                    <div class="topic-icon">🎯</div>\n                    <h5>学习方法指导</h5>\n                    <ul>\n                        <li>听说读写全面发展</li>\n                        <li>游戏化学习策略</li>\n                        <li>多媒体资源利用</li>\n                    </ul>\n                </div>\n                <div class="topic-card">\n                    <div class="topic-icon">📚</div>\n                    <h5>教材选择与使用</h5>\n                    <ul>\n                        <li>适龄教材推荐</li>\n                        <li>学习计划制定</li>\n                        <li>作业辅导方法</li>\n                    </ul>\n                </div>\n                <div class="topic-card">\n                    <div class="topic-icon">🌟</div>\n                    <h5>文化传承培养</h5>\n                    <ul>\n                        <li>节日传统体验</li>\n                        <li>文化故事讲述</li>\n                        <li>价值观教育</li>\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class="seminar-section">\n            <h4><i class="fas fa-chalkboard-teacher"></i> 主讲嘉宾</h4>\n            <div class="speakers">\n                <div class="speaker">\n                    <h5>王校长 - 博文中文学校校长</h5>\n                    <p>20年海外中文教育经验，儿童语言教育专家</p>\n                </div>\n                <div class="speaker">\n                    <h5>李老师 - 资深中文教师</h5>\n                    <p>HSK考试专家，青少年中文教学专家</p>\n                </div>\n            </div>\n        </div>\n\n        <div class="seminar-section">\n            <h4><i class="fas fa-gift"></i> 参会福利</h4>\n            <div class="benefits">\n                <ul>\n                    <li>免费中文学习资料包</li>\n                    <li>推荐书单和学习计划模板</li>\n                    <li>一对一咨询机会</li>\n                    <li>家长交流群邀请</li>\n                    <li>精美茶点和饮品</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n.seminar-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.seminar-header {\n    background: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.seminar-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.seminar-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #7c3aed;\n}\n\n.seminar-section h4 {\n    color: #7c3aed;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.schedule {\n    display: flex;\n    flex-direction: column;\n    gap: 0.75rem;\n}\n\n.time-item {\n    display: grid;\n    grid-template-columns: auto 2fr;\n    gap: 1rem;\n    background: white;\n    padding: 0.75rem 1rem;\n    border-radius: 6px;\n    align-items: center;\n}\n\n.time {\n    background: #7c3aed;\n    color: white;\n    padding: 0.25rem 0.75rem;\n    border-radius: 20px;\n    font-weight: 600;\n    font-size: 0.9rem;\n}\n\n.topics-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1rem;\n    margin-top: 1rem;\n}\n\n.topic-card {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n    text-align: center;\n}\n\n.topic-icon {\n    font-size: 2rem;\n    margin-bottom: 0.5rem;\n}\n\n.topic-card h5 {\n    color: #7c3aed;\n    margin-bottom: 0.75rem;\n}\n\n.topic-card ul {\n    list-style: none;\n    padding: 0;\n    text-align: left;\n}\n\n.topic-card li {\n    padding: 0.25rem 0;\n    color: #6c757d;\n    font-size: 0.9rem;\n}\n\n.speakers {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.speaker {\n    background: white;\n    padding: 1rem;\n    border-radius: 8px;\n}\n\n.speaker h5 {\n    color: #7c3aed;\n    margin-bottom: 0.5rem;\n}\n\n.benefits ul {\n    list-style: none;\n    padding: 0;\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 0.5rem;\n}\n\n.benefits li {\n    padding: 0.5rem;\n    background: white;\n    border-radius: 4px;\n    text-align: center;\n    color: #6c757d;\n}\n</style>\n            ','\n',char(10)),'家长教育讲座 - 帮助家长支持孩子中文学习的专业指导','seminar','2026-01-10 09:00:00','2025-05-10 16:30:00',NULL,NULL,'physical','博文中文学校','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,60,0,1,0,1,NULL,NULL,NULL,NULL,'published',0,1,'博文中文学校','info@boweneducation.org','0161 969 3071','王校长',NULL,NULL,NULL,'家长教育讲座：如何帮助孩子学好中文 | 博文中文学校','专为海外华人家长设计的中文教育讲座，分享实用的家庭教育方法和学习策略','家长教育,中文学习,讲座,家庭教育',NULL,7,'2025-11-07T17:07:33.364278','2025-11-07T17:07:33.364278');
INSERT INTO event VALUES('暑期中文文化体验营','summer-chinese-culture-camp-2025',replace('\n<h3>🏮 暑期中文文化体验营</h3>\n\n<div class="camp-details">\n    <div class="camp-header">\n        <h4>探索中华文化，感受东方魅力</h4>\n        <p>博文中文学校暑期特别推出中文文化体验营，让孩子们在轻松愉快的氛围中学习中文，体验传统文化，培养跨文化视野。</p>\n    </div>\n\n    <div class="camp-content">\n        <div class="camp-section">\n            <h4><i class="fas fa-calendar-week"></i> 营期安排</h4>\n            <div class="camp-schedule">\n                <div class="camp-week">\n                    <div class="week-header">\n                        <h5>第一期：文化探索</h5>\n                        <span class="week-dates">7月21日-7月25日</span>\n                    </div>\n                    <div class="week-themes">\n                        <span class="theme">🏛️ 传统文化</span>\n                        <span class="theme">🎭 民间艺术</span>\n                        <span class="theme">🍜 中华美食</span>\n                    </div>\n                </div>\n                <div class="camp-week">\n                    <div class="week-header">\n                        <h5>第二期：技艺体验</h5>\n                        <span class="week-dates">8月4日-8月8日</span>\n                    </div>\n                    <div class="week-themes">\n                        <span class="theme">🖌️ 书法绘画</span>\n                        <span class="theme">🧶 手工制作</span>\n                        <span class="theme">🎵 民乐欣赏</span>\n                    </div>\n                </div>\n                <div class="camp-week">\n                    <div class="week-header">\n                        <h5>第三期：现代中国</h5>\n                        <span class="week-dates">8月18日-8月22日</span>\n                    </div>\n                    <div class="week-themes">\n                        <span class="theme">🏙️ 城市发展</span>\n                        <span class="theme">🎮 科技创新</span>\n                        <span class="theme">🎬 影视文化</span>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-star"></i> 每日活动</h4>\n            <div class="daily-activities">\n                <div class="activity-time">\n                    <span class="time-block">9:00-10:00</span>\n                    <div class="activity-details">\n                        <h5>晨读时间</h5>\n                        <p>古诗词朗诵、汉字认读</p>\n                    </div>\n                </div>\n                <div class="activity-time">\n                    <span class="time-block">10:00-11:30</span>\n                    <div class="activity-details">\n                        <h5>文化课程</h5>\n                        <p>传统文化讲解、历史故事</p>\n                    </div>\n                </div>\n                <div class="activity-time">\n                    <span class="time-block">11:30-12:00</span>\n                    <div class="activity-details">\n                        <h5>互动游戏</h5>\n                        <p>中文游戏、文化问答</p>\n                    </div>\n                </div>\n                <div class="activity-time">\n                    <span class="time-block">12:00-13:00</span>\n                    <div class="activity-details">\n                        <h5>午餐时间</h5>\n                        <p>中式营养午餐</p>\n                    </div>\n                </div>\n                <div class="activity-time">\n                    <span class="time-block">13:00-14:30</span>\n                    <div class="activity-details">\n                        <h5>手工实践</h5>\n                        <p>书法、绘画、手工制作</p>\n                    </div>\n                </div>\n                <div class="activity-time">\n                    <span class="time-block">14:30-15:30</span>\n                    <div class="activity-details">\n                        <h5>才艺展示</h5>\n                        <p>表演练习、成果分享</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-users"></i> 招生信息</h4>\n            <div class="enrollment-info">\n                <div class="info-grid">\n                    <div class="info-item">\n                        <strong>招生对象：</strong>\n                        <p>6-14岁儿童，中文基础不限</p>\n                    </div>\n                    <div class="info-item">\n                        <strong>班级规模：</strong>\n                        <p>每班15人，小班教学</p>\n                    </div>\n                    <div class="info-item">\n                        <strong>费用标准：</strong>\n                        <p>£150/周，三周连报£400</p>\n                    </div>\n                    <div class="info-item">\n                        <strong>包含项目：</strong>\n                        <p>课程材料、午餐、保险、结业证书</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="camp-section">\n            <h4><i class="fas fa-certificate"></i> 结业成果</h4>\n            <div class="achievements">\n                <ul>\n                    <li>个人中文文化学习档案</li>\n                    <li>手工作品展示集</li>\n                    <li>传统文化体验证书</li>\n                    <li>结营汇报演出</li>\n                    <li>家长参观开放日</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n.camp-details {\n    max-width: 1000px;\n    margin: 0 auto;\n}\n\n.camp-header {\n    background: linear-gradient(135deg, #dc2626 0%, #f97316 100%);\n    color: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 2rem;\n    text-align: center;\n}\n\n.camp-content {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n}\n\n.camp-section {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #dc2626;\n}\n\n.camp-section h4 {\n    color: #dc2626;\n    margin-bottom: 1rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.camp-schedule {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.camp-week {\n    background: white;\n    padding: 1.5rem;\n    border-radius: 8px;\n}\n\n.week-header {\n    display: flex;\n    justify-content: space-between;\n    align-items: center;\n    margin-bottom: 1rem;\n}\n\n.week-header h5 {\n    color: #dc2626;\n    margin: 0;\n}\n\n.week-dates {\n    color: #6c757d;\n    font-size: 0.9rem;\n}\n\n.week-themes {\n    display: flex;\n    gap: 0.5rem;\n    flex-wrap: wrap;\n}\n\n.theme {\n    background: #fef3c7;\n    color: #92400e;\n    padding: 0.25rem 0.75rem;\n    border-radius: 20px;\n    font-size: 0.85rem;\n}\n\n.daily-activities {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.activity-time {\n    display: grid;\n    grid-template-columns: 100px 1fr;\n    gap: 1rem;\n    background: white;\n    padding: 1rem;\n    border-radius: 6px;\n    align-items: center;\n}\n\n.time-block {\n    background: #dc2626;\n    color: white;\n    padding: 0.5rem;\n    border-radius: 6px;\n    font-weight: 600;\n    text-align: center;\n    font-size: 0.9rem;\n}\n\n.activity-details h5 {\n    color: #1f2937;\n    margin-bottom: 0.25rem;\n    font-size: 1rem;\n}\n\n.activity-details p {\n    color: #6c757d;\n    margin: 0;\n    font-size: 0.9rem;\n}\n\n.info-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1rem;\n}\n\n.info-item {\n    background: white;\n    padding: 1rem;\n    border-radius: 6px;\n}\n\n.info-item strong {\n    color: #dc2626;\n    display: block;\n    margin-bottom: 0.5rem;\n}\n\n.info-item p {\n    color: #6c757d;\n    margin: 0;\n}\n\n.achievements ul {\n    list-style: none;\n    padding: 0;\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 0.5rem;\n}\n\n.achievements li {\n    padding: 0.5rem;\n    background: white;\n    border-radius: 4px;\n    text-align: center;\n    color: #6c757d;\n}\n</style>\n            ','\n',char(10)),'暑期中文文化体验营 - 传统文化、手工实践、语言学习综合体验','seminar','2025-12-25 10:00:00','2025-08-22 15:30:00',NULL,NULL,'physical','博文中文学校','Anchor House, Daisy Street, Manchester, M8 5AW','Manchester','M8 5AW',NULL,NULL,45,0,1,0,0,150.0,129.99999999999999999,'2025-07-01 23:59:59',NULL,'published',1,1,'博文中文学校','info@boweneducation.org','0161 969 3071','王老师','每日安排：9:00-10:00 晨读时间，10:00-11:30 文化课程，11:30-12:00 互动游戏，12:00-13:00 午餐，13:00-14:30 手工实践，14:30-15:30 才艺展示',NULL,NULL,'暑期中文文化体验营 2025 | 博文中文学校','2025年暑期中文文化体验营，传统文化、手工实践、语言学习，适合6-14岁儿童','暑假,中文学习,文化体验,夏令营',NULL,8,'2025-11-07T17:07:33.364296','2025-11-07T17:07:33.364296');
CREATE TABLE file_download (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	category_id INTEGER, 
	file_media_id INTEGER NOT NULL, 
	file_name VARCHAR(255) NOT NULL, 
	file_extension VARCHAR(20), 
	file_size_kb INTEGER, 
	file_type VARCHAR(5) NOT NULL, 
	version VARCHAR(50), 
	is_latest BOOLEAN NOT NULL, 
	previous_version_id INTEGER, 
	thumbnail_media_id INTEGER, 
	access_level VARCHAR(12) NOT NULL, 
	requires_login BOOLEAN NOT NULL, 
	allowed_roles VARCHAR(255), 
	download_limit_per_user INTEGER, 
	link_expiry_days INTEGER, 
	is_featured BOOLEAN NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	tags VARCHAR(255), 
	download_count INTEGER NOT NULL, 
	view_count INTEGER NOT NULL, 
	last_downloaded_at DATETIME, 
	usage_instructions TEXT, 
	system_requirements TEXT, 
	release_notes TEXT, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	author VARCHAR(100), 
	published_date DATETIME, 
	last_updated_date DATETIME, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES file_category (id), 
	FOREIGN KEY(file_media_id) REFERENCES media_file (id), 
	FOREIGN KEY(previous_version_id) REFERENCES file_download (id), 
	FOREIGN KEY(thumbnail_media_id) REFERENCES media_file (id)
);
CREATE TABLE gallery (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	category VARCHAR(100), 
	tags VARCHAR(255), 
	cover_media_id INTEGER, 
	display_mode VARCHAR(50), 
	is_featured BOOLEAN NOT NULL, 
	is_public BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	allow_download BOOLEAN NOT NULL, 
	watermark_enabled BOOLEAN NOT NULL, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	view_count INTEGER NOT NULL, 
	image_count INTEGER NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id)
);
INSERT INTO gallery VALUES('国际象棋俱乐部相册','chess-gallery','记录国际象棋俱乐部的精彩瞬间，包括比赛、训练和团队活动。','国际象棋',NULL,NULL,'grid',1,1,0,0,0,'相册 - 国际象棋俱乐部 | Bowen Education Manchester','博文国际象棋俱乐部相册，记录比赛精彩瞬间、训练场景、颁奖典礼和团队活动。',12,6,NULL,1,'2025-11-07 06:57:00.649290','2025-11-07 23:35:01.972961');
INSERT INTO gallery VALUES('羽毛球俱乐部精彩瞬间','badminton-gallery','记录羽毛球俱乐部成员在训练、比赛和活动中的精彩表现。','羽毛球',NULL,NULL,'grid',1,1,0,0,0,'精彩瞬间 - 羽毛球俱乐部 | Bowen Education Manchester','博文羽毛球俱乐部精彩瞬间，记录训练、比赛、团队活动和青少年培养的照片集锦。',13,6,NULL,2,'2025-11-07 06:57:00.650995','2025-11-07 23:35:46.022676');
CREATE TABLE menu_category (
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	description TEXT, 
	sort_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	available_times VARCHAR(255), 
	image_media_id INTEGER, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(image_media_id) REFERENCES media_file (id)
);
CREATE TABLE IF NOT EXISTS "order" (
	order_number VARCHAR(50) NOT NULL, 
	user_id INTEGER, 
	status VARCHAR(10) NOT NULL, 
	payment_status VARCHAR(8) NOT NULL, 
	customer_email VARCHAR(100) NOT NULL, 
	customer_phone VARCHAR(50), 
	customer_name VARCHAR(100) NOT NULL, 
	shipping_address_line1 VARCHAR(255) NOT NULL, 
	shipping_address_line2 VARCHAR(255), 
	shipping_city VARCHAR(100) NOT NULL, 
	shipping_state VARCHAR(100), 
	shipping_postal_code VARCHAR(20) NOT NULL, 
	shipping_country VARCHAR(100) NOT NULL, 
	billing_address_line1 VARCHAR(255), 
	billing_address_line2 VARCHAR(255), 
	billing_city VARCHAR(100), 
	billing_state VARCHAR(100), 
	billing_postal_code VARCHAR(20), 
	billing_country VARCHAR(100), 
	billing_same_as_shipping BOOLEAN NOT NULL, 
	subtotal FLOAT NOT NULL, 
	shipping_fee FLOAT NOT NULL, 
	tax_amount FLOAT NOT NULL, 
	discount_amount FLOAT NOT NULL, 
	total_amount FLOAT NOT NULL, 
	paid_amount FLOAT NOT NULL, 
	coupon_code VARCHAR(50), 
	coupon_discount FLOAT NOT NULL, 
	shipping_method VARCHAR(8) NOT NULL, 
	shipping_carrier VARCHAR(100), 
	tracking_number VARCHAR(100), 
	tracking_url VARCHAR(255), 
	payment_method VARCHAR(13), 
	payment_transaction_id VARCHAR(100), 
	paid_at DATETIME, 
	confirmed_at DATETIME, 
	shipped_at DATETIME, 
	delivered_at DATETIME, 
	cancelled_at DATETIME, 
	customer_notes TEXT, 
	admin_notes TEXT, 
	cancel_reason TEXT, 
	refund_reason TEXT, 
	ip_address VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	UNIQUE (order_number)
);
CREATE TABLE portfolio (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	subtitle VARCHAR(300), 
	cover_media_id INTEGER, 
	summary TEXT, 
	background TEXT, 
	challenge TEXT, 
	solution TEXT, 
	result TEXT, 
	content_html TEXT, 
	client_name VARCHAR(200), 
	client_logo_media_id INTEGER, 
	is_client_anonymous BOOLEAN NOT NULL, 
	project_date DATE, 
	project_duration VARCHAR(100), 
	project_url VARCHAR(500), 
	tags VARCHAR(500), 
	is_featured BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(client_logo_media_id) REFERENCES media_file (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id), 
	UNIQUE (slug)
);
CREATE TABLE post (
	column_id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	summary TEXT, 
	cover_media_id INTEGER, 
	content_html TEXT NOT NULL, 
	is_recommended BOOLEAN NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	published_at DATETIME, 
	is_approved INTEGER NOT NULL, 
	admin_reply TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id)
);
INSERT INTO post VALUES(8,'博文集团与河南大学建立战略合作伙伴关系','henan-university-partnership','博文教育集团正式与中国河南大学签署战略合作协议，共同推进中英教育文化交流项目，为曼彻斯特华裔青少年提供寻根之旅机会。',11,'<h2>合作背景</h2><p>2024年3月，博文教育集团与河南大学在郑州正式签署战略合作协议。此次合作标志着博文集团在推动中英教育文化交流方面迈出了重要一步。河南大学作为中国百年名校，在汉语国际教育和文化传播领域具有深厚的学术积淀和丰富的教学资源。</p><h2>合作内容</h2><p>本次战略合作涵盖多个领域：</p><ul><li><strong>师资交流项目</strong>：河南大学将定期派遣优秀汉语教师来曼彻斯特进行短期教学交流。</li><li><strong>学生交流计划</strong>：每年组织博文学校学生赴河南大学参加短期文化体验营。</li><li><strong>课程资源共享</strong>：河南大学将向博文集团提供优质的教学资源。</li><li><strong>学术研究合作</strong>：双方将在海外华文教育研究领域开展合作。</li></ul><h2>寻根之旅</h2><p>作为合作的重要组成部分，博文集团每年将组织"寻根之旅"活动。</p><h2>报名咨询</h2><p>邮箱：china-trip@boweneducation.org<br>电话：0161 xxx xxxx</p>',0,'published','博文集团与河南大学建立战略合作伙伴关系','博文教育集团正式与中国河南大学签署战略合作协议。','2024-03-15 10:00:00',1,NULL,1,'2025-11-05 10:23:43','2025-11-05 10:23:43');
INSERT INTO post VALUES(8,'2024年秋季学期招生现已开放','2024-autumn-term-enrollment','博文中文学校2024年秋季学期招生全面启动，提供从基础班到A-Level的全方位中文课程，GCSE通过率保持100%。',12,'<h2>招生公告</h2><p>博文中文学校2024年秋季学期招生现已全面启动！</p><h2>课程设置</h2><h3>1. 基础中文班（5-7岁）</h3><ul><li>上课时间：每周六 10:00-11:00</li><li>学费：£180/学期（12周）</li></ul><h3>2. GCSE中文班（14-16岁）</h3><ul><li>课程特色：历年通过率100%</li></ul><h2>新生优惠</h2><p>首月学费九折优惠。</p>',1,'published','2024年秋季学期招生现已开放','博文中文学校2024年秋季学期招生全面启动。','2024-02-20 09:00:00',1,NULL,2,'2025-11-05 10:23:43','2025-11-05 10:23:43');
INSERT INTO post VALUES(8,'2024年HAF项目圆满结束，惠及200余名儿童','haf-programme-success-2024','博文集团作为Trafford Council官方合作伙伴，成功举办2024年暑期HAF项目，为200多名儿童提供免费活动和健康餐食。',13,'<h2>项目概况</h2><p>2024年暑期，博文教育集团成功举办了为期四周的假期活动，惠及200余名儿童。</p><h2>项目亮点</h2><ul><li>中华文化体验活动</li><li>体育运动项目</li></ul><h2>项目成果</h2><ul><li>参与儿童：206名</li><li>家长满意度：98%</li></ul>',0,'published','2024年HAF项目圆满结束','博文集团成功举办2024年暑期HAF项目。','2024-08-25 14:30:00',1,NULL,3,'2025-11-05 10:23:43','2025-11-05 10:23:43');
INSERT INTO post VALUES(8,'博文国际象棋俱乐部在曼彻斯特地区赛事中斩获佳绩','chess-club-tournament-achievements','博文国际象棋俱乐部学员在2024年春季曼彻斯特青少年锦标赛中表现出色，3名学员分别获得各组别冠军。',14,'<h2>赛事背景</h2><p>2024年3月16-17日，曼彻斯特青少年国际象棋锦标赛举行。</p><h2>博文俱乐部战绩</h2><ul><li><strong>U10组冠军</strong>：王思远</li><li><strong>U12组冠军</strong>：李明轩</li><li><strong>U14组冠军</strong>：张雨涵</li></ul><h2>ECF等级分提升</h2><ul><li>5名学员首次获得ECF等级分</li><li>12名学员等级分提升100分以上</li></ul>',0,'published','博文国际象棋俱乐部斩获佳绩','3名学员获得冠军。','2024-03-20 16:00:00',1,NULL,4,'2025-11-05 10:23:43','2025-11-05 10:23:43');
INSERT INTO post VALUES(13,'Foundation Mandarin / 基础中文启蒙班','foundation-mandarin','Ages 5-7 years. Playful introduction to Mandarin through songs, games, and stories.',23,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">🎵</div>\n                <h3>歌曲教学</h3>\n                <p>通过中文儿歌学习基础词汇和发音</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🎮</div>\n                <h3>互动游戏</h3>\n                <p>趣味游戏巩固学习内容，提高学习兴趣</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">📚</div>\n                <h3>故事时间</h3>\n                <p>经典中文故事，培养语言感知能力</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">✏️</div>\n                <h3>基础书写</h3>\n                <p>认识基本笔画，学习简单汉字书写</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">年龄范围 Age Range:</span>\n                <span class="value">5-7岁 (Years 5-7)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周六 10:00-11:00 | Saturday 10:00-11:00</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">12周 (12 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">8-12人 (8-12 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£180/学期 (£180 per term)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课地点 Location:</span>\n                <span class="value">Sale Sports Centre, Sale, Manchester</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握基础汉语拼音 Master basic Pinyin</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>认识50-100个基本汉字 Recognize 50-100 basic characters</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>学会日常简单对话 Learn daily simple conversations</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>培养中文学习兴趣 Develop interest in Chinese learning</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>欢迎预约试听课，名额有限，请提前联系。Free trial lesson available, limited spaces, please contact us in advance.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),1,'published','Foundation Mandarin / 基础中文启蒙班 | Bowen Education Group','Ages 5-7 years. Playful introduction to Mandarin through songs, games, and stories. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,5,'2025-11-07 02:09:29.547197+00:00','2025-11-08 09:15:01.430206');
INSERT INTO post VALUES(13,'Primary Mandarin / 小学中文进阶班','primary-mandarin','Ages 8-10 years. Systematic Mandarin learning with reading, writing, and conversation practice.',24,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">📖</div>\n                <h3>系统教学</h3>\n                <p>遵循英国国家课程标准，系统学习中文</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">💬</div>\n                <h3>口语练习</h3>\n                <p>强化日常对话，提高口语表达能力</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">✍️</div>\n                <h3>写作训练</h3>\n                <p>学习汉字书写规则，练习短文写作</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🌟</div>\n                <h3>文化体验</h3>\n                <p>了解中华文化，参与传统节日活动</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">年龄范围 Age Range:</span>\n                <span class="value">8-10岁 (Years 8-10)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周六 11:00-13:00 | Saturday 11:00-13:00</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">12周 (12 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">10-15人 (10-15 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£220/学期 (£220 per term)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">教材 Textbooks:</span>\n                <span class="value">《轻松学中文》教材配套练习册</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握300-500个常用汉字 Master 300-500 common characters</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>流利进行日常对话 Fluent daily conversation</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>阅读简单中文文章 Read simple Chinese texts</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>书写100-200字短文 Write 100-200 character compositions</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>需要具备基础中文基础，可安排入学测试。Basic Chinese foundation required, placement test available.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),1,'published','Primary Mandarin / 小学中文进阶班 | Bowen Education Group','Ages 8-10 years. Systematic Mandarin learning with reading, writing, and conversation practice. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,6,'2025-11-07 02:09:29.548549+00:00','2025-11-08 09:15:01.434021');
INSERT INTO post VALUES(13,'GCSE Chinese / GCSE中文考试班','gcse-chinese','Ages 14-16 years. Comprehensive GCSE Chinese exam preparation with listening, speaking, reading, and writing.',25,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">🎯</div>\n                <h3>考试导向</h3>\n                <p>针对GCSE考试大纲，全方位备考训练</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">👂</div>\n                <h3>听力训练</h3>\n                <p>强化听力理解，提高听力应试技巧</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🗣️</div>\n                <h3>口语突破</h3>\n                <p>一对一口语练习，提升流利度和准确性</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">📝</div>\n                <h3>写作技巧</h3>\n                <p>掌握各类文体写作，提高作文分数</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">年龄范围 Age Range:</span>\n                <span class="value">14-16岁 (Years 14-16)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">考试局 Exam Board:</span>\n                <span class="value">Edexcel / AQA (根据学校选择)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周六 14:00-16:30 | Saturday 14:00-16:30</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">15周 (15 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">6-10人 (6-10 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£320/学期 (£320 per term)</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="exam-preparation">\n        <h3>考试准备 Exam Preparation</h3>\n        <div class="exam-grid">\n            <div class="exam-item">\n                <h4>听力 Listening (25%)</h4>\n                <ul>\n                    <li>模拟试题练习 Mock exam practice</li>\n                    <li>真题解析 Past paper analysis</li>\n                    <li>速记技巧训练 Note-taking skills</li>\n                </ul>\n            </div>\n            <div class="exam-item">\n                <h4>口语 Speaking (25%)</h4>\n                <ul>\n                    <li>角色扮演练习 Role-play practice</li>\n                    <li>话题演讲准备 Topic presentation</li>\n                    <li>发音纠正 Pronunciation correction</li>\n                </ul>\n            </div>\n            <div class="exam-item">\n                <h4>阅读 Reading (25%)</h4>\n                <ul>\n                    <li>阅读理解训练 Reading comprehension</li>\n                    <li>词汇扩充 Vocabulary expansion</li>\n                    <li>快速阅读技巧 Speed reading techniques</li>\n                </ul>\n            </div>\n            <div class="exam-item">\n                <h4>写作 Writing (25%)</h4>\n                <ul>\n                    <li>各类文体写作 Different writing styles</li>\n                    <li>语法结构强化 Grammar structure</li>\n                    <li>作文模板指导 Writing templates</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握800-1000个考试词汇 Master 800-1000 exam vocabulary</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>达到GCSE 7-9分水平 Achieve GCSE grades 7-9</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>流利进行各类话题讨论 Discuss various topics fluently</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>熟练掌握应试技巧 Master exam techniques</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>提供免费入学评估，制定个性化学习计划。Free assessment available with personalized learning plan.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),1,'published','GCSE Chinese / GCSE中文考试班 | Bowen Education Group','Ages 14-16 years. Comprehensive GCSE Chinese exam preparation with listening, speaking, reading, and writing. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,7,'2025-11-07 02:09:29.548570+00:00','2025-11-08 09:15:01.434195');
INSERT INTO post VALUES(13,'A-Level Chinese / A-Level中文课程','a-level-chinese','Ages 16-18 years. Advanced Chinese language and literature study for A-Level qualification.',26,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">📚</div>\n                <h3>文学分析</h3>\n                <p>深入学习中文文学作品，培养文学鉴赏能力</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🎭</div>\n                <h3>文化研究</h3>\n                <p>探索中华文化历史，理解现代社会</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">📰</div>\n                <h3>媒体分析</h3>\n                <p>分析中文媒体，了解当代中国发展</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🗨️</div>\n                <h3>高级翻译</h3>\n                <p>中英文互译训练，提升翻译技巧</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">年龄范围 Age Range:</span>\n                <span class="value">16-18岁 (Years 16-18)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">考试局 Exam Board:</span>\n                <span class="value">Edexcel / AQA / Cambridge</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周六 14:00-17:00 | Saturday 14:00-17:00</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">18周 (18 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">4-8人 (4-8 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£380/学期 (£380 per term)</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="a-level-modules">\n        <h3>A-Level课程模块 A-Level Modules</h3>\n        <div class="modules-grid">\n            <div class="module-item">\n                <h4>Paper 1: 阅读、写作和翻译</h4>\n                <ul>\n                    <li>阅读理解 Reading comprehension</li>\n                    <li>文章写作 Essay writing</li>\n                    <li>中英翻译 Translation Chinese-English</li>\n                </ul>\n            </div>\n            <div class="module-item">\n                <h4>Paper 2: 写作和文学</h4>\n                <ul>\n                    <li>创意写作 Creative writing</li>\n                    <li>文学分析 Literary analysis</li>\n                    <li>作品研究 Text study</li>\n                </ul>\n            </div>\n            <div class="module-item">\n                <h4>Paper 3: 口语</h4>\n                <ul>\n                    <li>独立研究项目 Individual research project</li>\n                    <li>话题讨论 Discussion</li>\n                    <li>表达能力 Communication skills</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握1500+个高级词汇 Master 1500+ advanced vocabulary</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>达到A-Level A*-A水平 Achieve A-Level A*-A grades</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>独立完成研究项目 Complete independent research project</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>深入理解中华文化 Deep understanding of Chinese culture</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>要求GCSE中文7分以上或同等水平。Requires GCSE Chinese grade 7+ or equivalent level.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),0,'published','A-Level Chinese / A-Level中文课程 | Bowen Education Group','Ages 16-18 years. Advanced Chinese language and literature study for A-Level qualification. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,8,'2025-11-07 02:09:29.548586+00:00','2025-11-08 09:15:01.434231');
INSERT INTO post VALUES(13,'HSK Preparation / HSK汉语水平考试','hsk-preparation','All ages. Professional HSK exam preparation for all levels (HSK 1-6).',27,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">📊</div>\n                <h3>分级教学</h3>\n                <p>根据HSK 1-6级不同要求，针对性教学</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🎯</div>\n                <h3>真题训练</h3>\n                <p>大量历年真题练习，熟悉考试题型</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">⏱️</div>\n                <h3>时间管理</h3>\n                <p>培养考试时间管理技巧，提高答题效率</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">📈</div>\n                <h3>进度跟踪</h3>\n                <p>定期模拟考试，跟踪学习进度</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">适合年龄 Age Range:</span>\n                <span class="value">全年龄段 (All ages)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">考试等级 Levels:</span>\n                <span class="value">HSK 1-6级 (HSK Levels 1-6)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">根据等级安排 | Scheduled by level</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">12-20周 (12-20 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">6-12人 (6-12 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£200-350/学期 (根据等级)</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="hsk-levels">\n        <h3>HSK等级说明 HSK Level Information</h3>\n        <div class="levels-grid">\n            <div class="level-item">\n                <h4>HSK 1-2级 (初级)</h4>\n                <ul>\n                    <li>基础日常交流 Basic daily communication</li>\n                    <li>300个词汇 300 vocabulary words</li>\n                    <li>简单语法结构 Simple grammar structures</li>\n                    <li>学费: £200/学期 Tuition: £200/term</li>\n                </ul>\n            </div>\n            <div class="level-item">\n                <h4>HSK 3-4级 (中级)</h4>\n                <ul>\n                    <li>生活话题讨论 Life topic discussions</li>\n                    <li>1200个词汇 1200 vocabulary words</li>\n                    <li>复杂语法表达 Complex grammar expressions</li>\n                    <li>学费: £280/学期 Tuition: £280/term</li>\n                </ul>\n            </div>\n            <div class="level-item">\n                <h4>HSK 5-6级 (高级)</h4>\n                <ul>\n                    <li>学术专业语言 Academic language</li>\n                    <li>5000+个词汇 5000+ vocabulary words</li>\n                    <li>深度文化交流 Deep cultural communication</li>\n                    <li>学费: £350/学期 Tuition: £350/term</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class="exam-structure">\n        <h3>考试结构 Exam Structure</h3>\n        <div class="exam-grid">\n            <div class="exam-item">\n                <h4>听力 Listening</h4>\n                <p>理解不同语境下的对话和短文 Understand dialogues and passages in various contexts</p>\n            </div>\n            <div class="exam-item">\n                <h4>阅读 Reading</h4>\n                <p>阅读理解不同题材文章 Read articles of various topics and styles</p>\n            </div>\n            <div class="exam-item">\n                <h4>写作 Writing</h4>\n                <p>完成不同类型的写作任务 Complete various writing tasks</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>提供免费水平测试，确定最适合的HSK等级。Free level test available to determine appropriate HSK level.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),0,'published','HSK Preparation / HSK汉语水平考试 | Bowen Education Group','All ages. Professional HSK exam preparation for all levels (HSK 1-6). Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,9,'2025-11-07 02:09:29.548603+00:00','2025-11-08 09:15:01.434264');
INSERT INTO post VALUES(13,'Beginner Cantonese / 粤语初级班','beginner-cantonese','All ages. Learn Cantonese from basics with focus on speaking and listening skills.',28,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">🗣️</div>\n                <h3>口语优先</h3>\n                <p>重点培养口语交流能力，快速掌握日常对话</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">👂</div>\n                <h3>听力强化</h3>\n                <p>大量听力练习，提高粤语听力理解能力</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">😊</div>\n                <h3>实用表达</h3>\n                <p>学习地道粤语表达，了解本地文化</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🎵</div>\n                <h3>粤语歌曲</h3>\n                <p>通过粤语歌曲学习，增加学习趣味性</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">适合年龄 Age Range:</span>\n                <span class="value">全年龄段 (All ages)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">课程水平 Level:</span>\n                <span class="value">初级零基础 Beginner level</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周日 14:00-16:00 | Sunday 14:00-16:00</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">12周 (12 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">8-12人 (8-12 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£200/学期 (£200 per term)</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-content">\n        <h3>学习内容 Learning Content</h3>\n        <div class="content-grid">\n            <div class="content-item">\n                <h4>基础发音 Basic Pronunciation</h4>\n                <ul>\n                    <li>粤拼系统学习 Jyutping system</li>\n                    <li>声调练习 Tone practice</li>\n                    <li>常用字发音 Common character pronunciation</li>\n                </ul>\n            </div>\n            <div class="content-item">\n                <h4>日常对话 Daily Conversations</h4>\n                <ul>\n                    <li>问候与自我介绍 Greetings & self-introduction</li>\n                    <li>购物问价 Shopping & prices</li>\n                    <li>餐饮点餐 Food ordering</li>\n                    <li>交通出行 Transportation</li>\n                </ul>\n            </div>\n            <div class="content-item">\n                <h4>文化体验 Cultural Experience</h4>\n                <ul>\n                    <li>粤语流行文化 Cantonese pop culture</li>\n                    <li>传统节日习俗 Traditional festivals</li>\n                    <li>地道俚语表达 Local slang expressions</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握基础粤拼发音 Master basic Jyutping pronunciation</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>进行日常简单对话 Basic daily conversation</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>理解简单粤语对话 Understand simple Cantonese dialogues</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>了解粤语文化特色 Understand Cantonese culture</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>无需任何粤语基础，欢迎对粤语文化感兴趣的朋友。No prior Cantonese knowledge required.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),0,'published','Beginner Cantonese / 粤语初级班 | Bowen Education Group','All ages. Learn Cantonese from basics with focus on speaking and listening skills. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,10,'2025-11-07 02:09:29.548619+00:00','2025-11-08 09:15:01.434438');
INSERT INTO post VALUES(13,'GCSE Cantonese / GCSE粤语考试班','gcse-cantonese','Ages 14-16 years. Complete GCSE Cantonese exam preparation for all four language skills.',29,replace('\n<div class="course-detail">\n    <div class="course-info">\n        <h2>课程特色 Course Features</h2>\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="icon">🎯</div>\n                <h3>考试导向</h3>\n                <p>针对GCSE粤语考试要求，系统化备考</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">💬</div>\n                <h3>口语强化</h3>\n                <p>一对一口语训练，提高表达流利度</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">📖</div>\n                <h3>阅读写作</h3>\n                <p>强化阅读理解，掌握各类文体写作</p>\n            </div>\n            <div class="feature-item">\n                <div class="icon">🎧</div>\n                <h3>听力训练</h3>\n                <p>模拟考试听力环境，提升应试技巧</p>\n            </div>\n        </div>\n    </div>\n\n    <div class="course-details">\n        <h3>课程信息 Course Information</h3>\n        <div class="details-table">\n            <div class="detail-row">\n                <span class="label">年龄范围 Age Range:</span>\n                <span class="value">14-16岁 (Years 14-16)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">考试局 Exam Board:</span>\n                <span class="value">Edexcel GCSE Cantonese</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">上课时间 Class Time:</span>\n                <span class="value">每周日 10:00-13:00 | Sunday 10:00-13:00</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学期长度 Term Length:</span>\n                <span class="value">15周 (15 weeks)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">班级人数 Class Size:</span>\n                <span class="value">6-10人 (6-10 students)</span>\n            </div>\n            <div class="detail-row">\n                <span class="label">学费 Tuition:</span>\n                <span class="value">£300/学期 (£300 per term)</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="exam-modules">\n        <h3>考试模块 Exam Modules</h3>\n        <div class="modules-grid">\n            <div class="module-item">\n                <h4>单元1: 听力理解 Unit 1: Listening</h4>\n                <ul>\n                    <li>理解不同语境对话 Understand various context dialogues</li>\n                    <li>获取关键信息 Extract key information</li>\n                    <li>时间、地点、人物信息识别 Identify time, place, person details</li>\n                    <li>占考试总分25% Weight: 25% of total marks</li>\n                </ul>\n            </div>\n            <div class="module-item">\n                <h4>单元2: 阅读理解 Unit 2: Reading</h4>\n                <ul>\n                    <li>不同题材文章阅读 Read various topic texts</li>\n                    <li>词汇和语法理解 Vocabulary & grammar comprehension</li>\n                    <li>信息提取和推理 Information extraction & inference</li>\n                    <li>占考试总分25% Weight: 25% of total marks</li>\n                </ul>\n            </div>\n            <div class="module-item">\n                <h4>单元3: 口语表达 Unit 3: Speaking</h4>\n                <ul>\n                    <li>角色扮演 Role-play scenarios</li>\n                    <li>话题讨论 Topic discussions</li>\n                    <li>个人介绍和观点表达 Personal introduction & opinion</li>\n                    <li>占考试总分25% Weight: 25% of total marks</li>\n                </ul>\n            </div>\n            <div class="module-item">\n                <h4>单元4: 写作表达 Unit 4: Writing</h4>\n                <ul>\n                    <li>短文写作 Short composition writing</li>\n                    <li>不同文体练习 Various writing styles</li>\n                    <li>语法结构运用 Grammar structure application</li>\n                    <li>占考试总分25% Weight: 25% of total marks</li>\n                </ul>\n            </div>\n        </div>\n    </div>\n\n    <div class="learning-outcomes">\n        <h3>学习目标 Learning Outcomes</h3>\n        <div class="outcomes-grid">\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握800+粤语词汇 Master 800+ Cantonese vocabulary</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>达到GCSE 7-9分水平 Achieve GCSE grades 7-9</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>流利进行粤语交流 Fluent Cantonese communication</span>\n            </div>\n            <div class="outcome-item">\n                <span class="check">✓</span>\n                <span>掌握粤语读写技能 Master Cantonese reading & writing</span>\n            </div>\n        </div>\n    </div>\n\n    <div class="enrollment">\n        <h3>报名咨询 Enrollment Information</h3>\n        <p>要求具备基础粤语听说能力，可安排入学测试。Basic Cantonese listening/speaking skills required.</p>\n        <div class="contact-info">\n            <p>📞 电话 Phone: 0161 xxx xxxx</p>\n            <p>📧 邮箱 Email: info@boweneducation.org</p>\n            <p>🌐 网站 Website: www.boweneducation.org</p>\n        </div>\n    </div>\n</div>\n            ','\n',char(10)),0,'published','GCSE Cantonese / GCSE粤语考试班 | Bowen Education Group','Ages 14-16 years. Complete GCSE Cantonese exam preparation for all four language skills. Learn more about this course at Bowen Education Chinese School.','2025-11-07 10:00:00+00:00',1,NULL,11,'2025-11-07 02:09:29.548635+00:00','2025-11-08 09:15:01.434467');
INSERT INTO post VALUES(23,'2025年博文假期营 - 戏剧运动活动','holiday-camp-2025','2025年8月4-29日，博文教育为5-11岁儿童举办的假期营活动，包括戏剧表演、运动游戏、艺术手工等丰富内容。',NULL,replace('\n<div class="holiday-camp-content">\n    <!-- Hero Section -->\n    <div class="holiday-camp-hero">\n        <div class="hero-image">\n            <img src="/static/images/holiday-camp/holiday-camp-2025.jpg" alt="2025年假期营活动">\n        </div>\n        <div class="hero-content">\n            <h1 class="hero-title">2025年博文假期营</h1>\n            <p class="hero-subtitle">戏剧、运动、手工艺 - 全面发展孩子的潜能</p>\n            <div class="hero-dates">\n                <i class="fas fa-calendar"></i>\n                <span>2025年8月4-29日</span>\n            </div>\n        </div>\n    </div>\n\n    <!-- Main Content -->\n    <div class="holiday-camp-info">\n        <div class="info-section">\n            <h2><i class="fas fa-clock"></i> 活动时间</h2>\n            <div class="time-details">\n                <p class="main-dates"><strong>2025年8月4-29日</strong>（周一至周五）</p>\n                <p class="daily-time"><strong>每日时间：</strong>上午10:00 - 下午2:00</p>\n                <div class="excluded-dates">\n                    <p><strong>休息日：</strong></p>\n                    <ul>\n                        <li>8月5日（周二）</li>\n                        <li>8月25日（周一）</li>\n                    </ul>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-child"></i> 参与年龄</h2>\n            <p class="age-range"><strong>5-11岁儿童</strong></p>\n            <div class="age-groups">\n                <div class="age-group">\n                    <span class="age-label">幼儿组：</span>\n                    <span class="age-details">5-8岁（戏剧与艺术活动）</span>\n                </div>\n                <div class="age-group">\n                    <span class="age-label">少儿组：</span>\n                    <span class="age-details">8-11岁（运动与团队活动）</span>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-star"></i> 活动内容</h2>\n            <div class="activities-grid">\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-theater-masks"></i>\n                    </div>\n                    <h3>戏剧表演</h3>\n                    <p>培养孩子的表达能力和自信心，通过角色扮演和表演技巧训练，每周五有小型表演展示。</p>\n                </div>\n\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-football-ball"></i>\n                    </div>\n                    <h3>运动游戏</h3>\n                    <p>多种体育运动和团队游戏，提高孩子的身体素质和团队协作能力。</p>\n                </div>\n\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-palette"></i>\n                    </div>\n                    <h3>艺术手工</h3>\n                    <p>创意手工制作，绘画、剪纸、手工制作等，培养孩子的创造力和动手能力。</p>\n                </div>\n\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-chess"></i>\n                    </div>\n                    <h3>国际象棋</h3>\n                    <p>基础国际象棋教学，培养逻辑思维和战略思考能力。</p>\n                </div>\n\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-music"></i>\n                    </div>\n                    <h3>自由游戏</h3>\n                    <p>自由活动时间，让孩子在安全的环境中自主选择游戏，发展社交技能。</p>\n                </div>\n\n                <div class="activity-card">\n                    <div class="activity-icon">\n                        <i class="fas fa-book"></i>\n                    </div>\n                    <h3>主题学习</h3>\n                    <p>每周围绕不同主题展开活动：分享、家庭、社区、友谊等。</p>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-calendar-week"></i> 每日安排</h2>\n            <div class="daily-schedule">\n                <div class="schedule-item">\n                    <div class="time-block">\n                        <span class="time">10:00-10:30</span>\n                    </div>\n                    <div class="activity-block">\n                        <h4>早晨集合</h4>\n                        <p>欢迎活动，今日主题介绍</p>\n                    </div>\n                </div>\n\n                <div class="schedule-item">\n                    <div class="time-block">\n                        <span class="time">10:30-12:00</span>\n                    </div>\n                    <div class="activity-block">\n                        <h4>上午活动</h4>\n                        <p>5-8岁：戏剧表演 | 8-11岁：运动游戏</p>\n                    </div>\n                </div>\n\n                <div class="schedule-item">\n                    <div class="time-block">\n                        <span class="time">12:00-12:30</span>\n                    </div>\n                    <div class="activity-block">\n                        <h4>午餐时间</h4>\n                        <p>提供营养午餐和水果</p>\n                    </div>\n                </div>\n\n                <div class="schedule-item">\n                    <div class="time-block">\n                        <span class="time">12:30-13:30</span>\n                    </div>\n                    <div class="activity-block">\n                        <h4>下午活动</h4>\n                        <p>5-8岁：运动游戏 | 8-11岁：戏剧表演</p>\n                    </div>\n                </div>\n\n                <div class="schedule-item">\n                    <div class="time-block">\n                        <span class="time">13:30-14:00</span>\n                    </div>\n                    <div class="activity-block">\n                        <h4>艺术手工/国际象棋</h4>\n                        <p>创意活动时间</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-coins"></i> 活动费用</h2>\n            <div class="pricing-cards">\n                <div class="price-card free">\n                    <div class="price-header">\n                        <h3>免费参与</h3>\n                        <div class="price">£0 <span>/天</span></div>\n                    </div>\n                    <div class="price-content">\n                        <p>适用于符合免费校餐资格的儿童</p>\n                        <ul>\n                            <li>包含所有活动费用</li>\n                            <li>提供免费午餐</li>\n                            <li>提供水果和饮料</li>\n                            <li>所有材料和用品</li>\n                        </ul>\n                    </div>\n                </div>\n\n                <div class="price-card paid">\n                    <div class="price-header">\n                        <h3>标准收费</h3>\n                        <div class="price">£12 <span>/天</span></div>\n                    </div>\n                    <div class="price-content">\n                        <p>不符合免费资格的儿童</p>\n                        <ul>\n                            <li>包含所有活动费用</li>\n                            <li>提供营养午餐</li>\n                            <li>提供水果和饮料</li>\n                            <li>所有手工材料</li>\n                        </ul>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-map-marker-alt"></i> 活动地点</h2>\n            <div class="venue-info">\n                <div class="venue-details">\n                    <h3>Woodhouse Park Lifestyle Centre</h3>\n                    <p><i class="fas fa-location-dot"></i> 206 Portway, Wythenshawe, Manchester M22 1QW</p>\n                    <div class="venue-features">\n                        <div class="feature">\n                            <i class="fas fa-shield-alt"></i>\n                            <span>安全宽敞的活动场地</span>\n                        </div>\n                        <div class="feature">\n                            <i class="fas fa-parking"></i>\n                            <span>免费停车场</span>\n                        </div>\n                        <div class="feature">\n                            <i class="fas fa-utensils"></i>\n                            <span>现代化厨房设施</span>\n                        </div>\n                        <div class="feature">\n                            <i class="fas fa-wheelchair"></i>\n                            <span>无障碍设施</span>\n                        </div>\n                    </div>\n                </div>\n                <div class="venue-map">\n                    <img src="/static/images/holiday-camp/venue-map.jpg" alt="活动地点地图">\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-user-plus"></i> 报名方式</h2>\n            <div class="registration-steps">\n                <div class="step">\n                    <div class="step-number">1</div>\n                    <div class="step-content">\n                        <h3>注册MCR Active Go</h3>\n                        <p>访问 <a href="http://www.mcractive.com" target="_blank">www.mcractive.com</a> 网站并注册成为MCR Active Go会员</p>\n                    </div>\n                </div>\n\n                <div class="step">\n                    <div class="step-number">2</div>\n                    <div class="step-content">\n                        <h3>添加家庭成员</h3>\n                        <p>在您的账户中添加孩子的信息到家庭账户</p>\n                    </div>\n                </div>\n\n                <div class="step">\n                    <div class="step-number">3</div>\n                    <div class="step-content">\n                        <h3>预订活动</h3>\n                        <p>在活动页面找到"博文假期营"并选择参加的日期进行预订</p>\n                    </div>\n                </div>\n            </div>\n\n            <div class="registration-cta">\n                <a href="http://www.mcractive.com" target="_blank" class="btn btn-primary btn-large">\n                    <i class="fas fa-external-link-alt"></i>\n                    立即前往MCR Active报名\n                </a>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-phone"></i> 联系方式</h2>\n            <div class="contact-info">\n                <div class="contact-item">\n                    <div class="contact-icon">\n                        <i class="fas fa-phone"></i>\n                    </div>\n                    <div class="contact-details">\n                        <h4>联系电话</h4>\n                        <p><a href="tel:01616672668">0161 667 2668</a></p>\n                    </div>\n                </div>\n\n                <div class="contact-item">\n                    <div class="contact-icon">\n                        <i class="fas fa-envelope"></i>\n                    </div>\n                    <div class="contact-details">\n                        <h4>邮箱地址</h4>\n                        <p><a href="mailto:Camp@bowenuk.org">Camp@bowenuk.org</a></p>\n                    </div>\n                </div>\n\n                <div class="contact-item">\n                    <div class="contact-icon">\n                        <i class="fas fa-clock"></i>\n                    </div>\n                    <div class="contact-details">\n                        <h4>咨询时间</h4>\n                        <p>周一至周五 9:00-17:00</p>\n                    </div>\n                </div>\n            </div>\n        </div>\n\n        <div class="info-section">\n            <h2><i class="fas fa-question-circle"></i> 常见问题</h2>\n            <div class="faq-section">\n                <div class="faq-item">\n                    <h4>我的孩子需要带什么？</h4>\n                    <p>我们提供所有材料和用品。请孩子穿舒适的适合运动的衣服，并带上一件外套以防天气变化。</p>\n                </div>\n\n                <div class="faq-item">\n                    <h4>食物是如何安排的？</h4>\n                    <p>我们为每个孩子提供营养均衡的午餐，以及新鲜水果和饮料。如果您孩子有特殊的饮食要求，请在报名时告知我们。</p>\n                </div>\n\n                <div class="faq-item">\n                    <h4>工作人员的资质如何？</h4>\n                    <p>我们的所有工作人员都经过DBS背景调查，具有丰富的儿童看护经验，并接受过急救培训。</p>\n                </div>\n\n                <div class="faq-item">\n                    <h4>如何确认我的免费校餐资格？</h4>\n                    <p>在注册过程中，系统会自动验证您孩子的免费校餐资格。如果您不确定，请联系您孩子所在的学校确认。</p>\n                </div>\n            </div>\n        </div>\n    </div>\n</div>\n\n<style>\n/* Holiday Camp Styles */\n.holiday-camp-content {\n    max-width: 1200px;\n    margin: 0 auto;\n}\n\n/* Hero Section */\n.holiday-camp-hero {\n    position: relative;\n    border-radius: 16px;\n    overflow: hidden;\n    margin-bottom: 3rem;\n    height: 400px;\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n    display: flex;\n    align-items: center;\n}\n\n.hero-image {\n    position: absolute;\n    top: 0;\n    left: 0;\n    width: 100%;\n    height: 100%;\n    opacity: 0.3;\n}\n\n.hero-image img {\n    width: 100%;\n    height: 100%;\n    object-fit: cover;\n}\n\n.hero-content {\n    position: relative;\n    z-index: 2;\n    text-align: center;\n    color: white;\n    padding: 2rem;\n}\n\n.hero-title {\n    font-size: 3rem;\n    font-weight: 700;\n    margin-bottom: 1rem;\n}\n\n.hero-subtitle {\n    font-size: 1.2rem;\n    margin-bottom: 2rem;\n    opacity: 0.9;\n}\n\n.hero-dates {\n    display: inline-flex;\n    align-items: center;\n    gap: 0.5rem;\n    background: rgba(255, 255, 255, 0.2);\n    padding: 0.75rem 1.5rem;\n    border-radius: 30px;\n    backdrop-filter: blur(10px);\n    font-weight: 600;\n}\n\n/* Info Sections */\n.info-section {\n    background: white;\n    border-radius: 12px;\n    padding: 2.5rem;\n    margin-bottom: 2rem;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n}\n\n.info-section h2 {\n    color: #1e3a8a;\n    font-size: 1.8rem;\n    margin-bottom: 1.5rem;\n    display: flex;\n    align-items: center;\n    gap: 0.75rem;\n}\n\n.info-section h2 i {\n    font-size: 1.5rem;\n}\n\n/* Time Details */\n.main-dates {\n    font-size: 1.3rem;\n    color: #1e3a8a;\n    margin-bottom: 1rem;\n}\n\n.daily-time {\n    font-size: 1.1rem;\n    margin-bottom: 1rem;\n}\n\n.excluded-dates ul {\n    list-style: none;\n    padding: 0;\n}\n\n.excluded-dates li {\n    padding: 0.25rem 0;\n    color: #dc2626;\n    font-weight: 500;\n}\n\n/* Age Groups */\n.age-range {\n    font-size: 1.3rem;\n    color: #1e3a8a;\n    margin-bottom: 1.5rem;\n}\n\n.age-groups {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    gap: 1rem;\n}\n\n.age-group {\n    background: #f8f9fa;\n    padding: 1rem;\n    border-radius: 8px;\n    border-left: 4px solid #1e3a8a;\n}\n\n.age-label {\n    font-weight: 600;\n    color: #1e3a8a;\n    display: block;\n    margin-bottom: 0.25rem;\n}\n\n/* Activities Grid */\n.activities-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n    gap: 1.5rem;\n}\n\n.activity-card {\n    background: #f8f9fa;\n    padding: 2rem;\n    border-radius: 12px;\n    text-align: center;\n    transition: all 0.3s;\n    border: 2px solid transparent;\n}\n\n.activity-card:hover {\n    transform: translateY(-5px);\n    border-color: #1e3a8a;\n    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);\n}\n\n.activity-icon {\n    background: #1e3a8a;\n    color: white;\n    width: 60px;\n    height: 60px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    margin: 0 auto 1rem;\n    font-size: 1.5rem;\n}\n\n.activity-card h3 {\n    color: #1e3a8a;\n    margin-bottom: 1rem;\n    font-size: 1.2rem;\n}\n\n.activity-card p {\n    color: #6c757d;\n    line-height: 1.6;\n}\n\n/* Daily Schedule */\n.daily-schedule {\n    display: flex;\n    flex-direction: column;\n    gap: 1rem;\n}\n\n.schedule-item {\n    display: grid;\n    grid-template-columns: 120px 1fr;\n    gap: 1rem;\n    padding: 1rem;\n    background: #f8f9fa;\n    border-radius: 8px;\n    align-items: center;\n}\n\n.time-block {\n    text-align: center;\n}\n\n.time {\n    background: #1e3a8a;\n    color: white;\n    padding: 0.5rem;\n    border-radius: 6px;\n    font-weight: 600;\n    display: inline-block;\n}\n\n.activity-block h4 {\n    color: #1e3a8a;\n    margin-bottom: 0.25rem;\n}\n\n.activity-block p {\n    color: #6c757d;\n    margin: 0;\n}\n\n/* Pricing Cards */\n.pricing-cards {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    gap: 2rem;\n}\n\n.price-card {\n    border-radius: 12px;\n    overflow: hidden;\n    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);\n    transition: all 0.3s;\n}\n\n.price-card:hover {\n    transform: translateY(-5px);\n}\n\n.price-card.free {\n    border: 3px solid #10b981;\n}\n\n.price-card.paid {\n    border: 3px solid #1e3a8a;\n}\n\n.price-header {\n    text-align: center;\n    padding: 2rem;\n    color: white;\n}\n\n.price-card.free .price-header {\n    background: linear-gradient(135deg, #10b981 0%, #059669 100%);\n}\n\n.price-card.paid .price-header {\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n}\n\n.price-header h3 {\n    margin-bottom: 1rem;\n    font-size: 1.5rem;\n}\n\n.price {\n    font-size: 3rem;\n    font-weight: 700;\n}\n\n.price span {\n    font-size: 1.2rem;\n    opacity: 0.8;\n}\n\n.price-content {\n    padding: 2rem;\n}\n\n.price-content p {\n    margin-bottom: 1.5rem;\n    color: #6c757d;\n    font-weight: 500;\n}\n\n.price-content ul {\n    list-style: none;\n    padding: 0;\n}\n\n.price-content li {\n    padding: 0.5rem 0;\n    padding-left: 1.5rem;\n    position: relative;\n    color: #6c757d;\n}\n\n.price-content li::before {\n    content: "✓";\n    position: absolute;\n    left: 0;\n    color: #10b981;\n    font-weight: bold;\n}\n\n/* Venue Info */\n.venue-info {\n    display: grid;\n    grid-template-columns: 2fr 1fr;\n    gap: 2rem;\n    align-items: start;\n}\n\n.venue-details h3 {\n    color: #1e3a8a;\n    font-size: 1.5rem;\n    margin-bottom: 1rem;\n}\n\n.venue-details p {\n    color: #6c757d;\n    margin-bottom: 1.5rem;\n    display: flex;\n    align-items: center;\n    gap: 0.5rem;\n}\n\n.venue-features {\n    display: grid;\n    grid-template-columns: repeat(2, 1fr);\n    gap: 1rem;\n}\n\n.feature {\n    display: flex;\n    align-items: center;\n    gap: 0.75rem;\n    padding: 0.75rem;\n    background: #f8f9fa;\n    border-radius: 8px;\n}\n\n.feature i {\n    color: #1e3a8a;\n    width: 20px;\n}\n\n.venue-map {\n    border-radius: 8px;\n    overflow: hidden;\n}\n\n.venue-map img {\n    width: 100%;\n    height: auto;\n    border-radius: 8px;\n}\n\n/* Registration Steps */\n.registration-steps {\n    display: flex;\n    flex-direction: column;\n    gap: 1.5rem;\n    margin-bottom: 2rem;\n}\n\n.step {\n    display: flex;\n    gap: 1.5rem;\n    align-items: flex-start;\n}\n\n.step-number {\n    background: #1e3a8a;\n    color: white;\n    width: 40px;\n    height: 40px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    font-size: 1.2rem;\n    font-weight: 700;\n    flex-shrink: 0;\n}\n\n.step-content h3 {\n    color: #1e3a8a;\n    margin-bottom: 0.5rem;\n    font-size: 1.2rem;\n}\n\n.step-content p {\n    color: #6c757d;\n    line-height: 1.6;\n}\n\n.step-content a {\n    color: #1e3a8a;\n    text-decoration: none;\n    font-weight: 500;\n}\n\n.step-content a:hover {\n    text-decoration: underline;\n}\n\n.registration-cta {\n    text-align: center;\n}\n\n.btn-primary {\n    background: #1e3a8a;\n    color: white;\n    text-decoration: none;\n    padding: 1rem 2rem;\n    border-radius: 8px;\n    font-weight: 600;\n    display: inline-flex;\n    align-items: center;\n    gap: 0.5rem;\n    transition: all 0.3s;\n}\n\n.btn-primary:hover {\n    background: #1e40af;\n    transform: translateY(-2px);\n}\n\n.btn-large {\n    font-size: 1.1rem;\n    padding: 1.2rem 2.5rem;\n}\n\n/* Contact Info */\n.contact-info {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 1.5rem;\n}\n\n.contact-item {\n    display: flex;\n    gap: 1rem;\n    align-items: flex-start;\n}\n\n.contact-icon {\n    background: #1e3a8a;\n    color: white;\n    width: 50px;\n    height: 50px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    flex-shrink: 0;\n}\n\n.contact-details h4 {\n    color: #1e3a8a;\n    margin-bottom: 0.5rem;\n    font-size: 1.1rem;\n}\n\n.contact-details a {\n    color: #1e3a8a;\n    text-decoration: none;\n    font-weight: 500;\n}\n\n.contact-details a:hover {\n    text-decoration: underline;\n}\n\n/* FAQ Section */\n.faq-section {\n    display: flex;\n    flex-direction: column;\n    gap: 1.5rem;\n}\n\n.faq-item {\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #1e3a8a;\n}\n\n.faq-item h4 {\n    color: #1e3a8a;\n    margin-bottom: 1rem;\n    font-size: 1.1rem;\n}\n\n.faq-item p {\n    color: #6c757d;\n    line-height: 1.6;\n    margin: 0;\n}\n\n/* Responsive */\n@media (max-width: 768px) {\n    .hero-title {\n        font-size: 2rem;\n    }\n\n    .activities-grid {\n        grid-template-columns: 1fr;\n    }\n\n    .age-groups {\n        grid-template-columns: 1fr;\n    }\n\n    .pricing-cards {\n        grid-template-columns: 1fr;\n    }\n\n    .venue-info {\n        grid-template-columns: 1fr;\n    }\n\n    .schedule-item {\n        grid-template-columns: 1fr;\n        text-align: center;\n    }\n\n    .time-block {\n        margin-bottom: 0.5rem;\n    }\n\n    .venue-features {\n        grid-template-columns: 1fr;\n    }\n\n    .registration-cta .btn-large {\n        width: 100%;\n        max-width: none;\n    }\n}\n</style>\n','\n',char(10)),1,'published','2025年博文假期营 - Bowen Education Group','2025年8月假期营活动，为5-11岁儿童提供戏剧、运动、手工艺等全面发展的假期体验。','2025-01-01T00:00:00',1,NULL,12,'2025-11-07T17:01:00.392126','2025-11-07T17:01:00.392126');
CREATE TABLE post_category (
	column_id INTEGER NOT NULL, 
	parent_id INTEGER, 
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id), 
	FOREIGN KEY(parent_id) REFERENCES post_category (id)
);
INSERT INTO post_category VALUES(8,NULL,'School News','school-news',1,1,1,'2025-11-04 21:58:23.467552','2025-11-04 21:58:23.467557');
INSERT INTO post_category VALUES(8,NULL,'Events','events',2,1,2,'2025-11-04 21:58:23.467558','2025-11-04 21:58:23.467559');
INSERT INTO post_category VALUES(8,NULL,'Student Success','student-success',3,1,3,'2025-11-04 21:58:23.467560','2025-11-04 21:58:23.467560');
CREATE TABLE product (
	column_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	summary TEXT, 
	description_html TEXT NOT NULL, 
	cover_media_id INTEGER, 
	price_text VARCHAR(100), 
	availability_status VARCHAR(12) NOT NULL, 
	is_recommended BOOLEAN NOT NULL, 
	status VARCHAR(7) NOT NULL, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	published_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id)
);
INSERT INTO product VALUES(3,'Foundation Mandarin (Ages 5-7)','foundation-mandarin','Playful introduction to Mandarin for young learners through songs, games, and stories','<p>Our Foundation Mandarin programme is designed for children aged 5-7 who are just beginning their Chinese language journey...</p>',16,'£180 per term','in_stock',1,'online',NULL,NULL,'2025-11-04 21:58:23.426108',1,'2025-11-04 21:58:23.428883','2025-11-08 00:19:29.404795');
INSERT INTO product VALUES(3,'GCSE Chinese (Ages 14-16)','gcse-chinese','Comprehensive GCSE Chinese preparation aligned with AQA/Edexcel specifications','<p>Our GCSE Chinese programme provides comprehensive preparation for the AQA or Edexcel GCSE Chinese examinations...</p>',17,'£240 per term','in_stock',1,'online',NULL,NULL,'2025-11-04 21:58:23.426114',2,'2025-11-04 21:58:23.428885','2025-11-08 00:19:29.410866');
INSERT INTO product VALUES(3,'A-Level Chinese (Ages 16-18)','a-level-chinese','Advanced Chinese language and literature course for university-bound students','<p>Our A-Level Chinese programme offers advanced study of Chinese language and literature...</p>',18,'£280 per term','in_stock',1,'online',NULL,NULL,'2025-11-04 21:58:23.426116',3,'2025-11-04 21:58:23.428886','2025-11-08 00:19:29.410898');
INSERT INTO product VALUES(3,'HSK Level 3 Preparation','hsk-level-3','Targeted preparation for the HSK Level 3 examination with mock tests','<p>Our HSK Level 3 preparation course is designed to help students pass the HSK Level 3 examination...</p>',19,'£200 per term','in_stock',0,'online',NULL,NULL,'2025-11-04 21:58:23.426118',4,'2025-11-04 21:58:23.428887','2025-11-08 00:19:29.411082');
INSERT INTO product VALUES(3,'Cantonese Language Course','cantonese-language','Preserve your Cantonese heritage with our authentic language programme','<p>Our Cantonese language course helps students maintain and develop their Cantonese language skills...</p>',20,'£180 per term','in_stock',0,'online',NULL,NULL,'2025-11-04 21:58:23.426120',5,'2025-11-04 21:58:23.428887','2025-11-08 00:19:29.411104');
INSERT INTO product VALUES(4,'GCSE Mathematics Tutoring','gcse-mathematics','Expert GCSE Maths tutoring with focus on problem-solving and exam technique','<p>Our GCSE Mathematics tutoring provides comprehensive support for students preparing for their GCSE exams...</p>',21,'£30 per hour','in_stock',1,'online',NULL,NULL,'2025-11-04 21:58:23.426715',6,'2025-11-04 21:58:23.428888','2025-11-08 00:19:29.411123');
INSERT INTO product VALUES(4,'A-Level Physics Tutoring','a-level-physics','One-to-one A-Level Physics tutoring from experienced educators','<p>Our A-Level Physics tutoring provides personalized support for students studying A-Level Physics...</p>',22,'£35 per hour','in_stock',0,'online',NULL,NULL,'2025-11-04 21:58:23.426720',7,'2025-11-04 21:58:23.428889','2025-11-08 00:19:29.411141');
CREATE TABLE product_category (
	column_id INTEGER NOT NULL, 
	parent_id INTEGER, 
	name VARCHAR(100) NOT NULL, 
	slug VARCHAR(100) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id), 
	FOREIGN KEY(parent_id) REFERENCES product_category (id)
);
INSERT INTO product_category VALUES(3,NULL,'Chinese Language Courses','chinese-language',1,1,1,'2025-11-04 21:58:23.406291','2025-11-04 21:58:23.406293');
INSERT INTO product_category VALUES(4,NULL,'Academic Tutoring','academic-tutoring',2,1,2,'2025-11-04 21:58:23.406294','2025-11-04 21:58:23.406294');
INSERT INTO product_category VALUES(3,NULL,'Exam Preparation','exam-preparation',3,1,3,'2025-11-04 21:58:23.406294','2025-11-04 21:58:23.406295');
INSERT INTO product_category VALUES(3,NULL,'Adult Classes','adult-classes',4,1,4,'2025-11-04 21:58:23.406295','2025-11-04 21:58:23.406295');
CREATE TABLE restaurant_order (
	order_number VARCHAR(50) NOT NULL, 
	user_id INTEGER, 
	order_type VARCHAR(8) NOT NULL, 
	status VARCHAR(10) NOT NULL, 
	payment_status VARCHAR(8) NOT NULL, 
	customer_name VARCHAR(100) NOT NULL, 
	customer_phone VARCHAR(50) NOT NULL, 
	customer_email VARCHAR(100), 
	table_number VARCHAR(20), 
	number_of_guests INTEGER, 
	delivery_address VARCHAR(500), 
	delivery_city VARCHAR(100), 
	delivery_postal_code VARCHAR(20), 
	delivery_instructions TEXT, 
	pickup_time DATETIME, 
	scheduled_time DATETIME, 
	subtotal FLOAT NOT NULL, 
	delivery_fee FLOAT NOT NULL, 
	service_fee FLOAT NOT NULL, 
	tax_amount FLOAT NOT NULL, 
	discount_amount FLOAT NOT NULL, 
	tip_amount FLOAT NOT NULL, 
	total_amount FLOAT NOT NULL, 
	coupon_code VARCHAR(50), 
	payment_method VARCHAR(6), 
	paid_at DATETIME, 
	confirmed_at DATETIME, 
	preparing_at DATETIME, 
	ready_at DATETIME, 
	delivered_at DATETIME, 
	completed_at DATETIME, 
	cancelled_at DATETIME, 
	customer_notes TEXT, 
	kitchen_notes TEXT, 
	cancel_reason TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	UNIQUE (order_number)
);
CREATE TABLE single_page (
	column_id INTEGER NOT NULL, 
	title VARCHAR(200) NOT NULL, 
	subtitle VARCHAR(300), 
	content_html TEXT NOT NULL, 
	hero_media_id INTEGER, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	status VARCHAR(9) NOT NULL, 
	published_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(column_id) REFERENCES site_column (id), 
	FOREIGN KEY(hero_media_id) REFERENCES media_file (id), 
	UNIQUE (column_id)
);
INSERT INTO single_page VALUES(2,'About Us','Learn about Bowen Education Group','<p>Welcome to Bowen Education Group - Manchester''s premier Chinese language school.</p>',NULL,NULL,NULL,'published','2025-11-04 22:59:06.623365',1,'2025-11-04 22:59:06.625733','2025-11-04 22:59:06.625736');
INSERT INTO single_page VALUES(11,'Contact Us','Get in touch with us','<p>We''re here to help! Contact us for more information about our courses.</p>',NULL,NULL,NULL,'published','2025-11-04 22:59:06.623533',2,'2025-11-04 22:59:06.625736','2025-11-04 22:59:06.625737');
INSERT INTO single_page VALUES(3,'中文学校','Manchester Chinese School','<div class="container"><h2>中文学校</h2><p>博文中文学校为不同年龄段的学生提供优质的中文教育服务。</p><p>课程内容正在建设中，敬请期待。</p></div>',NULL,'中文学校 - 博文集团','博文中文学校提供启蒙班、中级班、精英班、GCSE普通话等课程','published','2025-11-05 02:22:26.641503',3,'2025-11-05 02:22:26.647020','2025-11-05 02:22:26.647022');
INSERT INTO single_page VALUES(4,'补习中心','Tuition Centre','<div class="container"><h2>补习中心</h2><p>博文补习中心提供GCSE和A-Level各科目的专业辅导。</p><p>课程内容正在建设中，敬请期待。</p></div>',NULL,'补习中心 - 博文集团','提供GCSE数学、物理、化学、英语和A-Level课程辅导','published','2025-11-05 02:22:26.642242',4,'2025-11-05 02:22:26.647023','2025-11-05 02:22:26.647023');
INSERT INTO single_page VALUES(5,'国际象棋俱乐部','Chess Club','<div class="container"><h2>国际象棋俱乐部</h2><p>博文国际象棋俱乐部为学生提供专业的国际象棋培训和比赛机会。</p><p>详细内容正在建设中，敬请期待。</p></div>',NULL,'国际象棋俱乐部 - 博文集团','专业的国际象棋培训和比赛','published','2025-11-05 02:22:26.642839',5,'2025-11-05 02:22:26.647023','2025-11-05 02:22:26.647026');
INSERT INTO single_page VALUES(6,'政府项目','Government Programmes','<div class="container"><h2>政府项目</h2><p>博文集团参与多项政府合作项目，包括HAF项目和公园活动等。</p><p>详细内容正在建设中，敬请期待。</p></div>',NULL,'政府项目 - 博文集团','HAF项目、公园活动等政府合作项目','published','2025-11-05 02:22:26.643443',6,'2025-11-05 02:22:26.647026','2025-11-05 02:22:26.647027');
INSERT INTO single_page VALUES(7,'博文活动','Events','<div class="container"><h2>博文活动</h2><p>博文集团定期举办各类文化活动，包括中国新年庆典、文化进校园、寻根之旅等。</p><p>详细内容正在建设中，敬请期待。</p></div>',NULL,'博文活动 - 博文集团','中国新年庆典、文化进校园、寻根之旅等文化活动','published','2025-11-05 02:22:26.643996',7,'2025-11-05 02:22:26.647028','2025-11-05 02:22:26.647028');
INSERT INTO single_page VALUES(8,'博文新闻','News','<div class="container"><h2>博文新闻</h2><p>了解博文集团的最新动态、活动报道和合作消息。</p><p>详细内容正在建设中，敬请期待。</p></div>',NULL,'博文新闻 - 博文集团','博文集团最新动态、活动报道和合作消息','published','2025-11-05 02:22:26.644552',8,'2025-11-05 02:22:26.647028','2025-11-05 02:22:26.647029');
INSERT INTO single_page VALUES(12,'羽毛球俱乐部','Badminton Club','<div class="container"><h2>羽毛球俱乐部</h2><p>博文羽毛球俱乐部为学生提供专业的羽毛球训练和比赛机会。</p><p>详细内容正在建设中，敬请期待。</p></div>',NULL,'羽毛球俱乐部 - 博文集团','专业的羽毛球训练和比赛','published','2025-11-05 02:22:26.645107',9,'2025-11-05 02:22:26.647029','2025-11-05 02:22:26.647029');
INSERT INTO single_page VALUES(14,'学期日期','Term Dates',replace('\n                <h2>2024-2025学年学期安排</h2>\n\n                <h3>秋季学期 Autumn Term</h3>\n                <ul>\n                    <li><strong>开学日期：</strong>2024年9月7日</li>\n                    <li><strong>期中假期：</strong>2024年10月26日 - 11月3日</li>\n                    <li><strong>学期结束：</strong>2024年12月21日</li>\n                </ul>\n\n                <h3>春季学期 Spring Term</h3>\n                <ul>\n                    <li><strong>开学日期：</strong>2025年1月6日</li>\n                    <li><strong>期中假期：</strong>2025年2月15日 - 2月23日</li>\n                    <li><strong>学期结束：</strong>2025年4月4日</li>\n                </ul>\n\n                <h3>夏季学期 Summer Term</h3>\n                <ul>\n                    <li><strong>开学日期：</strong>2025年4月21日</li>\n                    <li><strong>期中假期：</strong>2025年5月24日 - 6月1日</li>\n                    <li><strong>学期结束：</strong>2025年7月18日</li>\n                </ul>\n\n                <div class="alert alert-info mt-4">\n                    <p><strong>注意事项：</strong></p>\n                    <ul>\n                        <li>所有课程均在周六上午进行</li>\n                        <li>法定假日不上课</li>\n                        <li>如遇特殊情况需要调整，学校将提前通知</li>\n                    </ul>\n                </div>\n            ','\n',char(10)),NULL,'学期日期 - 博文中文学校','查看博文中文学校2024-2025学年的完整学期安排和重要日期','published','2025-11-05 06:06:15.023817',10,'2025-11-05 06:06:15.026300','2025-11-05 06:06:15.026303');
INSERT INTO single_page VALUES(15,'PTA家长教师协会','Parent-Teacher Association',replace('\n                <h2>关于我们的PTA</h2>\n                <p>博文中文学校家长教师协会（PTA）是一个由家长和教师组成的志愿组织，致力于促进家校合作，为学生创造更好的学习环境。</p>\n\n                <h3>我们的使命</h3>\n                <ul>\n                    <li>促进家长与学校之间的沟通与合作</li>\n                    <li>组织各类文化活动和社交活动</li>\n                    <li>为学校筹集资金，改善教学设施</li>\n                    <li>支持学校的教育项目和倡议</li>\n                </ul>\n\n                <h3>如何参与</h3>\n                <p>我们欢迎所有家长和教师加入PTA。您可以通过以下方式参与：</p>\n                <ul>\n                    <li>参加每学期的PTA会议</li>\n                    <li>协助组织学校活动</li>\n                    <li>担任PTA委员会成员</li>\n                    <li>提供您的专业技能和建议</li>\n                </ul>\n\n                <h3>联系我们</h3>\n                <p>如有任何问题或建议，请通过学校邮箱 <a href="mailto:info@boweneducation.org">info@boweneducation.org</a> 联系我们，或在家长微信群中与我们互动。</p>\n            ','\n',char(10)),NULL,'PTA家长教师协会 - 博文中文学校','加入博文中文学校PTA，与学校携手共同促进孩子的成长和发展','published','2025-11-05 06:06:15.027576',11,'2025-11-05 06:06:15.027993','2025-11-05 06:06:15.027995');
INSERT INTO single_page VALUES(17,'棋手信息','Information for Players',replace('\n                <h2>棋手注册与认证</h2>\n                <p>博文国际象棋俱乐部与英格兰国际象棋联合会（English Chess Federation, ECF）合作，为棋手提供正规的等级认证服务。</p>\n\n                <h3>ECF会员注册</h3>\n                <ul>\n                    <li>所有希望参加正式比赛的棋手需要注册ECF会员</li>\n                    <li>会员可以获得官方等级分（ECF Rating）</li>\n                    <li>青少年会员享有优惠价格</li>\n                </ul>\n\n                <h3>等级分体系</h3>\n                <p>ECF采用国际通用的等级分系统，根据比赛表现动态调整。等级分分为：</p>\n                <ul>\n                    <li><strong>初级：</strong>0-1000</li>\n                    <li><strong>中级：</strong>1000-1600</li>\n                    <li><strong>高级：</strong>1600-2000</li>\n                    <li><strong>专家：</strong>2000+</li>\n                </ul>\n\n                <h3>相关链接</h3>\n                <ul>\n                    <li><a href="https://www.englishchess.org.uk/" target="_blank">English Chess Federation 官网</a></li>\n                    <li><a href="https://www.englishchess.org.uk/ecf-membership/" target="_blank">ECF会员注册</a></li>\n                    <li><a href="https://www.englishchess.org.uk/rating-lists/" target="_blank">查询等级分</a></li>\n                </ul>\n\n                <p class="mt-4"><strong>如需协助注册或有任何疑问，请联系俱乐部教练。</strong></p>\n            ','\n',char(10)),NULL,'棋手信息 - 博文国际象棋俱乐部','了解ECF会员注册、等级分体系和相关信息','published','2025-11-05 06:06:15.028710',12,'2025-11-05 06:06:15.029066','2025-11-05 06:06:15.029068');
INSERT INTO single_page VALUES(20,'训练时间表','Training Schedule',replace('\n                <h2>训练时间安排</h2>\n\n                <h3>常规训练</h3>\n                <div class="table-responsive">\n                    <table class="table">\n                        <thead>\n                            <tr>\n                                <th>日期</th>\n                                <th>时间</th>\n                                <th>级别</th>\n                                <th>地点</th>\n                            </tr>\n                        </thead>\n                        <tbody>\n                            <tr>\n                                <td>每周六</td>\n                                <td>10:00 - 12:00</td>\n                                <td>初级班</td>\n                                <td>Sale Sports Centre</td>\n                            </tr>\n                            <tr>\n                                <td>每周六</td>\n                                <td>14:00 - 16:00</td>\n                                <td>中级班</td>\n                                <td>Sale Sports Centre</td>\n                            </tr>\n                            <tr>\n                                <td>每周日</td>\n                                <td>10:00 - 12:00</td>\n                                <td>高级班</td>\n                                <td>Sale Sports Centre</td>\n                            </tr>\n                            <tr>\n                                <td>每周日</td>\n                                <td>14:00 - 17:00</td>\n                                <td>竞技训练</td>\n                                <td>Sale Sports Centre</td>\n                            </tr>\n                        </tbody>\n                    </table>\n                </div>\n\n                <h3>训练内容</h3>\n                <ul>\n                    <li><strong>初级班：</strong>基础技术教学，包括握拍、步法、基本击球</li>\n                    <li><strong>中级班：</strong>技术提升，战术训练，双打配合</li>\n                    <li><strong>高级班：</strong>高级技战术，体能训练，心理素质培养</li>\n                    <li><strong>竞技训练：</strong>针对比赛的专项训练和实战演练</li>\n                </ul>\n\n                <h3>训练地点</h3>\n                <p>\n                    <strong>Sale Sports Centre</strong><br>\n                    Sale Road, Sale, Manchester M33 3SL<br>\n                    <a href="https://goo.gl/maps/example" target="_blank">查看地图</a>\n                </p>\n\n                <div class="alert alert-info mt-4">\n                    <p><strong>注意事项：</strong></p>\n                    <ul>\n                        <li>请提前10分钟到场热身</li>\n                        <li>自备球拍和运动装备</li>\n                        <li>如遇场馆维护或特殊情况，将提前通知</li>\n                    </ul>\n                </div>\n            ','\n',char(10)),NULL,'训练时间表 - 博文羽毛球俱乐部','查看博文羽毛球俱乐部的完整训练时间表和地点信息','published','2025-11-05 06:06:15.029792',13,'2025-11-05 06:06:15.030153','2025-11-05 06:06:15.030155');
INSERT INTO single_page VALUES(22,'HAF项目','Holiday Activities and Food Programme',replace('\n<!-- Hero Section -->\n<section class="haf-hero">\n    <div class="hero-content">\n        <div class="hero-badge">政府资助项目</div>\n        <h1 class="hero-title">Holiday Activities & Food (HAF)</h1>\n        <p class="hero-subtitle">为符合条件的儿童提供免费假期活动和营养餐食</p>\n        <div class="hero-buttons">\n            <a href="#eligibility" class="btn btn-primary">查看资格条件</a>\n            <a href="#enroll" class="btn btn-outline-primary">立即报名</a>\n        </div>\n    </div>\n</section>\n\n<!-- Key Features Section -->\n<section class="key-features">\n    <div class="container">\n        <div class="features-grid">\n            <div class="feature-item">\n                <div class="feature-icon">\n                    <i class="fas fa-utensils"></i>\n                </div>\n                <h3>营养餐食</h3>\n                <p>每日提供健康营养的午餐和小食</p>\n            </div>\n            <div class="feature-item">\n                <div class="feature-icon">\n                    <i class="fas fa-palette"></i>\n                </div>\n                <h3>丰富活动</h3>\n                <p>文化、体育、艺术等各类活动</p>\n            </div>\n            <div class="feature-item">\n                <div class="feature-icon">\n                    <i class="fas fa-shield-alt"></i>\n                </div>\n                <h3>安全环境</h3>\n                <p>专业工作人员和安全设施</p>\n            </div>\n            <div class="feature-item">\n                <div class="feature-icon">\n                    <i class="fas fa-gift"></i>\n                </div>\n                <h3>完全免费</h3>\n                <p>所有活动和餐食完全免费</p>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- About Section -->\n<section class="about-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>关于HAF项目</h2>\n            <p>英国政府资助的重要社区项目</p>\n        </div>\n        <div class="about-content">\n            <div class="about-text">\n                <p>Holiday Activities and Food (HAF) 项目是英国政府资助的一项重要社区项目，旨在在学校假期期间为符合条件的儿童提供健康食品和有趣的活动。博文集团积极参与该项目，为当地社区的孩子们提供丰富多彩的假期活动。</p>\n                <div class="stats-grid">\n                    <div class="stat-item">\n                        <div class="stat-number">1000+</div>\n                        <div class="stat-label">受益儿童</div>\n                    </div>\n                    <div class="stat-item">\n                        <div class="stat-number">50+</div>\n                        <div class="stat-label">活动类型</div>\n                    </div>\n                    <div class="stat-item">\n                        <div class="stat-number">8</div>\n                        <div class="stat-label">合作学校</div>\n                    </div>\n                </div>\n            </div>\n            <div class="about-image">\n                <img src="/static/images/haf/haf-activities.jpg" alt="HAF活动照片">\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- Project Goals Section -->\n<section class="goals-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>项目目标</h2>\n            <p>通过假期活动促进儿童全面发展</p>\n        </div>\n        <div class="goals-grid">\n            <div class="goal-card">\n                <div class="goal-icon">\n                    <i class="fas fa-heart"></i>\n                </div>\n                <h3>健康餐食保障</h3>\n                <p>为符合条件的儿童提供免费的健康餐食，确保假期能获得充足营养</p>\n            </div>\n            <div class="goal-card">\n                <div class="goal-icon">\n                    <i class="fas fa-running"></i>\n                </div>\n                <h3>身心健康发展</h3>\n                <p>通过多样化的体育和文化活动，促进儿童身心健康发展</p>\n            </div>\n            <div class="goal-card">\n                <div class="goal-icon">\n                    <i class="fas fa-users"></i>\n                </div>\n                <h3>家庭支持</h3>\n                <p>为工作家庭提供假期照看支持，减轻家庭负担</p>\n            </div>\n            <div class="goal-card">\n                <div class="goal-icon">\n                    <i class="fas fa-graduation-cap"></i>\n                </div>\n                <h3>教育娱乐</h3>\n                <p>组织各类教育和娱乐活动，让孩子在假期中继续学习和成长</p>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- Activities Section -->\n<section class="activities-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>活动内容</h2>\n            <p>丰富多彩的假期活动体验</p>\n        </div>\n        <div class="activities-categories">\n            <div class="category-card">\n                <div class="category-header">\n                    <div class="category-icon">\n                        <i class="fas fa-torii-gate"></i>\n                    </div>\n                    <h3>中华文化体验</h3>\n                </div>\n                <div class="category-activities">\n                    <ul>\n                        <li>书法练习</li>\n                        <li>传统剪纸</li>\n                        <li>中国结制作</li>\n                        <li>古诗词朗诵</li>\n                        <li>传统节日文化</li>\n                    </ul>\n                </div>\n            </div>\n\n            <div class="category-card">\n                <div class="category-header">\n                    <div class="category-icon">\n                        <i class="fas fa-football-ball"></i>\n                    </div>\n                    <h3>体育运动</h3>\n                </div>\n                <div class="category-activities">\n                    <ul>\n                        <li>羽毛球训练</li>\n                        <li>国际象棋课程</li>\n                        <li>团队运动游戏</li>\n                        <li>户外活动</li>\n                        <li>体能训练</li>\n                    </ul>\n                </div>\n            </div>\n\n            <div class="category-card">\n                <div class="category-header">\n                    <div class="category-icon">\n                        <i class="fas fa-paint-brush"></i>\n                    </div>\n                    <h3>艺术创作</h3>\n                </div>\n                <div class="category-activities">\n                    <ul>\n                        <li>绘画创作</li>\n                        <li>手工制作</li>\n                        <li>音乐欣赏</li>\n                        <li>戏剧表演</li>\n                        <li>创意设计</li>\n                    </ul>\n                </div>\n            </div>\n\n            <div class="category-card">\n                <div class="category-header">\n                    <div class="category-icon">\n                        <i class="fas fa-brain"></i>\n                    </div>\n                    <h3>教育游戏</h3>\n                </div>\n                <div class="category-activities">\n                    <ul>\n                        <li>益智游戏</li>\n                        <li>科学实验</li>\n                        <li>阅读时光</li>\n                        <li>数学游戏</li>\n                        <li>英语角活动</li>\n                    </ul>\n                </div>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- Eligibility Section -->\n<section id="eligibility" class="eligibility-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>参与资格</h2>\n            <p>查看您是否符合参与条件</p>\n        </div>\n        <div class="eligibility-content">\n            <div class="eligibility-criteria">\n                <div class="criteria-card primary">\n                    <div class="criteria-icon">\n                        <i class="fas fa-user-check"></i>\n                    </div>\n                    <h3>年龄要求</h3>\n                    <p>5-16岁儿童和青少年</p>\n                </div>\n                <div class="criteria-card primary">\n                    <div class="criteria-icon">\n                        <i class="fas fa-utensils"></i>\n                    </div>\n                    <h3>资格条件</h3>\n                    <p>有资格享受免费校餐（Free School Meals）</p>\n                </div>\n                <div class="criteria-card secondary">\n                    <div class="criteria-icon">\n                        <i class="fas fa-map-marker-alt"></i>\n                    </div>\n                    <h3>地区要求</h3>\n                    <p>居住在Trafford及周边地区</p>\n                </div>\n            </div>\n            <div class="eligibility-cta">\n                <p>不确定是否符合条件？</p>\n                <a href="/contact" class="btn btn-outline-primary">联系我们咨询</a>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- Schedule Section -->\n<section class="schedule-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>活动时间</h2>\n            <p>HAF项目假期安排</p>\n        </div>\n        <div class="schedule-timeline">\n            <div class="timeline-item">\n                <div class="timeline-date">\n                    <div class="date-icon">🌸</div>\n                    <div class="date-info">\n                        <h3>复活节假期</h3>\n                        <p>通常2周</p>\n                    </div>\n                </div>\n                <div class="timeline-activities">\n                    <p>春季主题活动、户外探索、手工制作</p>\n                </div>\n            </div>\n\n            <div class="timeline-item">\n                <div class="timeline-date">\n                    <div class="date-icon">☀️</div>\n                    <div class="date-info">\n                        <h3>暑假</h3>\n                        <p>通常4周</p>\n                    </div>\n                </div>\n                <div class="timeline-activities">\n                    <p>夏令营、体育竞技、文化体验、艺术创作</p>\n                </div>\n            </div>\n\n            <div class="timeline-item">\n                <div class="timeline-date">\n                    <div class="date-icon">🎄</div>\n                    <div class="date-info">\n                        <h3>圣诞假期</h3>\n                        <p>通常1周</p>\n                    </div>\n                </div>\n                <div class="timeline-activities">\n                    <p>节日庆祝、手工制作、表演活动</p>\n                </div>\n            </div>\n        </div>\n        <div class="schedule-note">\n            <p><strong>注意：</strong>具体活动日期将根据当地学校假期日历确定，报名信息将通过学校和家长群发布。</p>\n        </div>\n    </div>\n</section>\n\n<!-- Enrollment Section -->\n<section id="enroll" class="enrollment-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>如何报名</h2>\n            <p>简单几步即可参与HAF项目</p>\n        </div>\n        <div class="enrollment-steps">\n            <div class="step-item">\n                <div class="step-number">1</div>\n                <div class="step-content">\n                    <h3>确认资格</h3>\n                    <p>确认孩子符合HAF项目参与条件</p>\n                </div>\n            </div>\n            <div class="step-item">\n                <div class="step-number">2</div>\n                <div class="step-content">\n                    <h3>关注通知</h3>\n                    <p>通过学校、家长群等渠道了解报名信息</p>\n                </div>\n            </div>\n            <div class="step-item">\n                <div class="step-number">3</div>\n                <div class="step-content">\n                    <h3>在线报名</h3>\n                    <p>通过官方指定平台填写报名表格</p>\n                </div>\n            </div>\n            <div class="step-item">\n                <div class="step-number">4</div>\n                <div class="step-content">\n                    <h3>参加活动</h3>\n                    <p>按时参加假期活动，享受快乐时光</p>\n                </div>\n            </div>\n        </div>\n        <div class="enrollment-cta">\n            <div class="cta-buttons">\n                <a href="/contact" class="btn btn-primary btn-large">\n                    <i class="fas fa-phone"></i> 咨询报名详情\n                </a>\n                <a href="/programmes-parks" class="btn btn-outline-primary btn-large">\n                    <i class="fas fa-calendar"></i> 查看近期活动\n                </a>\n            </div>\n            <div class="contact-info">\n                <p><strong>咨询电话：</strong>0161 969 3071</p>\n                <p><strong>邮箱：</strong>info@boweneducation.org</p>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- Benefits Section -->\n<section class="benefits-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>项目优势</h2>\n            <p>选择博文HAF项目的理由</p>\n        </div>\n        <div class="benefits-grid">\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-check-circle"></i>\n                </div>\n                <h3>完全免费</h3>\n                <p>所有活动和餐食完全免费，无任何隐藏费用</p>\n            </div>\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-user-tie"></i>\n                </div>\n                <h3>专业团队</h3>\n                <p>经验丰富的教练和专业工作人员指导</p>\n            </div>\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-home"></i>\n                </div>\n                <h3>安全环境</h3>\n                <p>安全友好的活动环境，让家长放心</p>\n            </div>\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-user-friends"></i>\n                </div>\n                <h3>结识朋友</h3>\n                <p>与同龄人建立友谊，培养社交能力</p>\n            </div>\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-lightbulb"></i>\n                </div>\n                <h3>学习新技能</h3>\n                <p>在娱乐中学习，培养兴趣爱好</p>\n            </div>\n            <div class="benefit-card">\n                <div class="benefit-icon">\n                    <i class="fas fa-apple-alt"></i>\n                </div>\n                <h3>营养均衡</h3>\n                <p>每日提供营养均衡的餐食和零食</p>\n            </div>\n        </div>\n    </div>\n</section>\n\n<!-- FAQ Section -->\n<section class="faq-section">\n    <div class="container">\n        <div class="section-header">\n            <h2>常见问题</h2>\n            <p>解答家长关心的问题</p>\n        </div>\n        <div class="faq-list">\n            <div class="faq-item">\n                <h4>如何确认我的孩子是否有免费校餐资格？</h4>\n                <p>请联系您孩子所在的学校，学校能够确认您的孩子是否符合免费校餐条件。您也可以通过当地政府网站查询相关资格标准。</p>\n            </div>\n            <div class="faq-item">\n                <h4>HAF活动是全天制的吗？</h4>\n                <p>大多数HAF活动是全日制或半日制，具体时间安排会在每次活动通知中详细说明。通常包括午餐时间。</p>\n            </div>\n            <div class="faq-item">\n                <h4>需要为孩子准备什么物品？</h4>\n                <p>我们提供所有活动材料和餐食。您只需为孩子准备适合运动的服装，如有特殊医疗需求请提前告知我们。</p>\n            </div>\n            <div class="faq-item">\n                <h4>如何了解下一次HAF活动的具体时间？</h4>\n                <p>我们会通过学校、家长微信群、邮件等渠道发布活动通知。您也可以关注我们的网站或直接联系我们咨询。</p>\n            </div>\n        </div>\n    </div>\n</section>\n\n<style>\n/* HAF Page Styles */\n\n/* Hero Section */\n.haf-hero {\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n    color: white;\n    padding: 5rem 0;\n    text-align: center;\n    position: relative;\n    overflow: hidden;\n}\n\n.haf-hero::before {\n    content: '''';\n    position: absolute;\n    top: 0;\n    left: 0;\n    right: 0;\n    bottom: 0;\n    background: url(''/static/images/haf/haf-hero-bg.jpg'') center/cover;\n    opacity: 0.1;\n}\n\n.hero-content {\n    position: relative;\n    z-index: 2;\n    max-width: 800px;\n    margin: 0 auto;\n    padding: 0 2rem;\n}\n\n.hero-badge {\n    display: inline-block;\n    background: rgba(255, 255, 255, 0.2);\n    padding: 0.5rem 1rem;\n    border-radius: 30px;\n    font-size: 0.9rem;\n    margin-bottom: 1.5rem;\n    backdrop-filter: blur(10px);\n}\n\n.hero-title {\n    font-size: 3rem;\n    font-weight: 700;\n    margin-bottom: 1.5rem;\n    line-height: 1.2;\n}\n\n.hero-subtitle {\n    font-size: 1.2rem;\n    margin-bottom: 2.5rem;\n    opacity: 0.9;\n    line-height: 1.6;\n}\n\n.hero-buttons {\n    display: flex;\n    gap: 1rem;\n    justify-content: center;\n    flex-wrap: wrap;\n}\n\n/* Key Features Section */\n.key-features {\n    padding: 4rem 0;\n    background: #f8f9fa;\n}\n\n.features-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 2rem;\n}\n\n.feature-item {\n    text-align: center;\n    background: white;\n    padding: 2rem;\n    border-radius: 12px;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    transition: all 0.3s;\n}\n\n.feature-item:hover {\n    transform: translateY(-5px);\n    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);\n}\n\n.feature-icon {\n    background: #1e3a8a;\n    color: white;\n    width: 70px;\n    height: 70px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    margin: 0 auto 1.5rem;\n    font-size: 1.8rem;\n}\n\n.feature-item h3 {\n    color: #1e3a8a;\n    font-size: 1.2rem;\n    margin-bottom: 1rem;\n}\n\n.feature-item p {\n    color: #6c757d;\n    line-height: 1.6;\n}\n\n/* About Section */\n.about-section {\n    padding: 5rem 0;\n}\n\n.section-header {\n    text-align: center;\n    margin-bottom: 3rem;\n}\n\n.section-header h2 {\n    font-size: 2.5rem;\n    color: #1e3a8a;\n    margin-bottom: 1rem;\n}\n\n.section-header p {\n    font-size: 1.1rem;\n    color: #6c757d;\n}\n\n.about-content {\n    display: grid;\n    grid-template-columns: 1fr 1fr;\n    gap: 4rem;\n    align-items: center;\n}\n\n.about-text p {\n    color: #6c757d;\n    font-size: 1.1rem;\n    line-height: 1.8;\n    margin-bottom: 2rem;\n}\n\n.stats-grid {\n    display: grid;\n    grid-template-columns: repeat(3, 1fr);\n    gap: 1rem;\n}\n\n.stat-item {\n    text-align: center;\n    padding: 1rem;\n    background: #f8f9fa;\n    border-radius: 8px;\n}\n\n.stat-number {\n    font-size: 2rem;\n    font-weight: 700;\n    color: #1e3a8a;\n    margin-bottom: 0.5rem;\n}\n\n.stat-label {\n    color: #6c757d;\n    font-size: 0.9rem;\n}\n\n.about-image {\n    border-radius: 12px;\n    overflow: hidden;\n    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);\n}\n\n.about-image img {\n    width: 100%;\n    height: auto;\n    display: block;\n}\n\n/* Goals Section */\n.goals-section {\n    padding: 5rem 0;\n    background: #f8f9fa;\n}\n\n.goals-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));\n    gap: 2rem;\n}\n\n.goal-card {\n    background: white;\n    padding: 2.5rem;\n    border-radius: 16px;\n    text-align: center;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    transition: all 0.3s;\n    border: 2px solid transparent;\n}\n\n.goal-card:hover {\n    transform: translateY(-8px);\n    border-color: #1e3a8a;\n    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);\n}\n\n.goal-icon {\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n    color: white;\n    width: 80px;\n    height: 80px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    margin: 0 auto 1.5rem;\n    font-size: 2rem;\n}\n\n.goal-card h3 {\n    color: #1e3a8a;\n    font-size: 1.3rem;\n    margin-bottom: 1rem;\n}\n\n.goal-card p {\n    color: #6c757d;\n    line-height: 1.6;\n}\n\n/* Activities Section */\n.activities-section {\n    padding: 5rem 0;\n}\n\n.activities-categories {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n    gap: 2rem;\n}\n\n.category-card {\n    background: white;\n    border-radius: 12px;\n    overflow: hidden;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    transition: all 0.3s;\n}\n\n.category-card:hover {\n    transform: translateY(-5px);\n    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);\n}\n\n.category-header {\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n    color: white;\n    padding: 2rem;\n    text-align: center;\n}\n\n.category-icon {\n    width: 60px;\n    height: 60px;\n    border-radius: 50%;\n    background: rgba(255, 255, 255, 0.2);\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    margin: 0 auto 1rem;\n    font-size: 1.5rem;\n}\n\n.category-header h3 {\n    margin: 0;\n    font-size: 1.3rem;\n}\n\n.category-activities {\n    padding: 2rem;\n}\n\n.category-activities ul {\n    list-style: none;\n    padding: 0;\n    margin: 0;\n}\n\n.category-activities li {\n    padding: 0.5rem 0;\n    padding-left: 1.5rem;\n    position: relative;\n    color: #6c757d;\n}\n\n.category-activities li::before {\n    content: "•";\n    color: #1e3a8a;\n    position: absolute;\n    left: 0;\n    font-weight: bold;\n}\n\n/* Eligibility Section */\n.eligibility-section {\n    padding: 5rem 0;\n    background: #f8f9fa;\n}\n\n.eligibility-content {\n    max-width: 800px;\n    margin: 0 auto;\n}\n\n.eligibility-criteria {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 1.5rem;\n    margin-bottom: 3rem;\n}\n\n.criteria-card {\n    background: white;\n    padding: 2rem;\n    border-radius: 12px;\n    text-align: center;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    transition: all 0.3s;\n}\n\n.criteria-card.primary {\n    border: 3px solid #1e3a8a;\n}\n\n.criteria-card.secondary {\n    border: 3px solid #3b82f6;\n}\n\n.criteria-card:hover {\n    transform: translateY(-5px);\n}\n\n.criteria-icon {\n    background: #1e3a8a;\n    color: white;\n    width: 60px;\n    height: 60px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    margin: 0 auto 1rem;\n    font-size: 1.5rem;\n}\n\n.criteria-card h3 {\n    color: #1e3a8a;\n    font-size: 1.2rem;\n    margin-bottom: 0.5rem;\n}\n\n.eligibility-cta {\n    text-align: center;\n    padding: 2rem;\n    background: white;\n    border-radius: 12px;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n}\n\n.eligibility-cta p {\n    color: #6c757d;\n    margin-bottom: 1.5rem;\n    font-size: 1.1rem;\n}\n\n/* Schedule Section */\n.schedule-section {\n    padding: 5rem 0;\n}\n\n.schedule-timeline {\n    display: flex;\n    flex-direction: column;\n    gap: 2rem;\n    margin-bottom: 3rem;\n}\n\n.timeline-item {\n    display: grid;\n    grid-template-columns: 200px 1fr;\n    gap: 2rem;\n    align-items: center;\n    background: white;\n    padding: 2rem;\n    border-radius: 12px;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n}\n\n.timeline-date {\n    display: flex;\n    align-items: center;\n    gap: 1rem;\n}\n\n.date-icon {\n    font-size: 2.5rem;\n}\n\n.date-info h3 {\n    color: #1e3a8a;\n    margin-bottom: 0.25rem;\n}\n\n.date-info p {\n    color: #6c757d;\n    margin: 0;\n}\n\n.timeline-activities p {\n    color: #6c757d;\n    margin: 0;\n    font-size: 1.1rem;\n}\n\n.schedule-note {\n    text-align: center;\n    background: #f8f9fa;\n    padding: 1.5rem;\n    border-radius: 8px;\n    border-left: 4px solid #1e3a8a;\n}\n\n/* Enrollment Section */\n.enrollment-section {\n    padding: 5rem 0;\n    background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);\n    color: white;\n}\n\n.enrollment-section .section-header h2,\n.enrollment-section .section-header p {\n    color: white;\n}\n\n.enrollment-steps {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));\n    gap: 2rem;\n    margin-bottom: 3rem;\n}\n\n.step-item {\n    text-align: center;\n}\n\n.step-number {\n    background: white;\n    color: #1e3a8a;\n    width: 60px;\n    height: 60px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    font-size: 1.5rem;\n    font-weight: 700;\n    margin: 0 auto 1rem;\n}\n\n.step-content h3 {\n    margin-bottom: 0.5rem;\n    font-size: 1.2rem;\n}\n\n.step-content p {\n    color: rgba(255, 255, 255, 0.9);\n}\n\n.enrollment-cta {\n    text-align: center;\n}\n\n.cta-buttons {\n    display: flex;\n    gap: 1rem;\n    justify-content: center;\n    margin-bottom: 2rem;\n    flex-wrap: wrap;\n}\n\n.btn {\n    padding: 1rem 2rem;\n    border-radius: 8px;\n    text-decoration: none;\n    font-weight: 600;\n    display: inline-flex;\n    align-items: center;\n    gap: 0.5rem;\n    transition: all 0.3s;\n}\n\n.btn-primary {\n    background: white;\n    color: #1e3a8a;\n}\n\n.btn-primary:hover {\n    background: #f8f9fa;\n    transform: translateY(-2px);\n}\n\n.btn-outline-primary {\n    background: transparent;\n    color: white;\n    border: 2px solid white;\n}\n\n.btn-outline-primary:hover {\n    background: white;\n    color: #1e3a8a;\n}\n\n.btn-large {\n    font-size: 1.1rem;\n    padding: 1.2rem 2.5rem;\n}\n\n.contact-info p {\n    color: rgba(255, 255, 255, 0.9);\n    margin-bottom: 0.5rem;\n}\n\n/* Benefits Section */\n.benefits-section {\n    padding: 5rem 0;\n    background: #f8f9fa;\n}\n\n.benefits-grid {\n    display: grid;\n    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));\n    gap: 2rem;\n}\n\n.benefit-card {\n    background: white;\n    padding: 2rem;\n    border-radius: 12px;\n    display: flex;\n    gap: 1.5rem;\n    align-items: flex-start;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    transition: all 0.3s;\n}\n\n.benefit-card:hover {\n    transform: translateY(-5px);\n    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);\n}\n\n.benefit-icon {\n    background: #1e3a8a;\n    color: white;\n    width: 50px;\n    height: 50px;\n    border-radius: 50%;\n    display: flex;\n    align-items: center;\n    justify-content: center;\n    flex-shrink: 0;\n}\n\n.benefit-card h3 {\n    color: #1e3a8a;\n    font-size: 1.1rem;\n    margin-bottom: 0.5rem;\n}\n\n.benefit-card p {\n    color: #6c757d;\n    line-height: 1.6;\n    margin: 0;\n}\n\n/* FAQ Section */\n.faq-section {\n    padding: 5rem 0;\n}\n\n.faq-list {\n    max-width: 800px;\n    margin: 0 auto;\n}\n\n.faq-item {\n    background: white;\n    padding: 2rem;\n    border-radius: 12px;\n    margin-bottom: 1.5rem;\n    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);\n    border-left: 4px solid #1e3a8a;\n}\n\n.faq-item h4 {\n    color: #1e3a8a;\n    font-size: 1.2rem;\n    margin-bottom: 1rem;\n}\n\n.faq-item p {\n    color: #6c757d;\n    line-height: 1.6;\n    margin: 0;\n}\n\n/* Responsive */\n@media (max-width: 768px) {\n    .hero-title {\n        font-size: 2rem;\n    }\n\n    .about-content {\n        grid-template-columns: 1fr;\n        gap: 2rem;\n    }\n\n    .stats-grid {\n        grid-template-columns: 1fr;\n        gap: 0.5rem;\n    }\n\n    .timeline-item {\n        grid-template-columns: 1fr;\n        text-align: center;\n        gap: 1rem;\n    }\n\n    .enrollment-steps {\n        grid-template-columns: 1fr;\n    }\n\n    .cta-buttons {\n        flex-direction: column;\n        align-items: center;\n    }\n\n    .benefits-grid {\n        grid-template-columns: 1fr;\n    }\n}\n</style>\n','\n',char(10)),NULL,'HAF项目 - 博文集团政府项目','了解博文集团参与的HAF假期活动和食品项目，为儿童提供免费健康餐食和丰富活动','published','2025-11-05 06:06:15.030825',14,'2025-11-05 06:06:15.031153','2025-11-07T17:02:42.020018');
INSERT INTO single_page VALUES(24,'河南大学合作','Cooperation with Henan University',replace('\n                <h2>河南大学合作项目</h2>\n                <p>博文集团与中国河南大学建立了长期战略合作伙伴关系，共同推动中英教育文化交流。</p>\n\n                <h3>合作内容</h3>\n                <ul>\n                    <li><strong>师资交流：</strong>河南大学定期派遣优秀教师到英国进行文化交流和教学支持</li>\n                    <li><strong>学生交流：</strong>组织学生互访活动，促进两国青少年的友谊和了解</li>\n                    <li><strong>文化活动：</strong>联合举办各类中华文化推广活动和学术研讨</li>\n                    <li><strong>资源共享：</strong>共享教学资源和研究成果</li>\n                </ul>\n\n                <h3>寻根之旅</h3>\n                <p>作为合作项目的重要组成部分，我们每年组织"寻根之旅"活动，带领在英国长大的华裔青少年回到中国，深入了解中华文化：</p>\n                <ul>\n                    <li>参观河南大学校园，体验中国大学生活</li>\n                    <li>游览历史文化名城，了解中国历史</li>\n                    <li>与中国学生交流，建立国际友谊</li>\n                    <li>参加文化体验活动（茶道、武术、传统工艺等）</li>\n                </ul>\n\n                <h3>Easter访华计划</h3>\n                <p>每年复活节期间，我们组织为期两周的访华活动：</p>\n                <ul>\n                    <li><strong>日期：</strong>每年复活节假期</li>\n                    <li><strong>对象：</strong>12-18岁学生</li>\n                    <li><strong>行程：</strong>河南（开封、郑州、洛阳）+ 北京</li>\n                    <li><strong>住宿：</strong>大学宿舍和精选酒店</li>\n                    <li><strong>陪同：</strong>专业领队和河南大学志愿者</li>\n                </ul>\n\n                <div class="alert alert-info mt-4">\n                    <p><strong>报名咨询：</strong></p>\n                    <p>如对河南大学合作项目或访华活动感兴趣，请联系我们获取详细信息和报名方式。</p>\n                    <p>邮箱：<a href="mailto:info@boweneducation.org">info@boweneducation.org</a></p>\n                </div>\n            ','\n',char(10)),NULL,'河南大学合作 - 博文集团','了解博文集团与河南大学的合作项目，包括寻根之旅和Easter访华计划','published','2025-11-05 06:06:15.031772',15,'2025-11-05 06:06:15.031992','2025-11-05 06:06:15.031993');
INSERT INTO single_page VALUES(25,'博文集团','融中西文化，育国际英才',replace('<div class="company-intro">\n    <h2>学校简介</h2>\n    <p>博文学校位于英国第二大繁华城市—曼彻斯特。建校于2020年。学校秉承"融中西文化，育国际英才"的办学理念。中文教学是学校的核心，健全科学的管理制度是学校规范管理、标准化管理的重要体现。</p>\n    <p>在中文教学中，学校注重培养学生的听、说、读、写、译五项能力，协助孩子在GCSE、A-level、A+等应试中取得优异成绩。学校还设有法语、西班牙语、日语等语言课程，以及GCSE、A-Level、HSK考试补习，牛津剑桥大学面试培训。</p>\n    \n    <h2>办学目的</h2>\n    <p>打造"精英教育"品牌是博文中文学校的办学目标，提高学生的语言表达能力、逻辑思维能力、受挫能力、增强自信心、建立过硬的心理素质。</p>\n    <p>在创建高质量中文教学体系的同时，该校更注重弘扬和培育中华民族精神，希望孩子们坚守民族身份与族群认知，吸收西方文化之长，融合中西文化精华。</p>\n    \n    <h2>我们的团队</h2>\n    <p>博文教师由英国主流学校专业从事中文教育多年的老师组成教研组，负责审核教师资质和管控教学质量。全校老师一起为优质教学而努力，每位老师都具备高素质好品德，注重培养孩子的个人修养、社会责任感以及同情、感恩等品格。</p>\n</div>','\n',char(10)),NULL,'博文集团 - Bowen Education Group | 曼彻斯特中文教育专家','博文教育集团位于英国曼彻斯特，提供专业的中文教育服务，致力于培养学生成为具有国际视野的人才。','published','2025-11-07 02:54:22',16,'2025-11-07 02:54:22','2025-11-07 02:54:22');
INSERT INTO single_page VALUES(9,'博文图库','记录精彩瞬间，分享美好时光',replace('\n                <div class="container py-5">\n                    <div class="row">\n                        <div class="col-lg-12">\n                            <h2 class="section-title mb-4">欢迎来到博文图库</h2>\n                            <p class="lead">这里汇集了博文教育集团的精彩瞬间，记录着学生们的成长历程和活动精彩。</p>\n                        </div>\n                    </div>\n\n                    <div class="row mt-5">\n                        <div class="col-md-4 mb-4">\n                            <div class="card">\n                                <div class="card-body">\n                                    <h4>中文学校活动</h4>\n                                    <p>记录学生们在中文课堂上的学习场景，以及各类文化活动的精彩瞬间。</p>\n                                </div>\n                            </div>\n                        </div>\n\n                        <div class="col-md-4 mb-4">\n                            <div class="card">\n                                <div class="card-body">\n                                    <h4>俱乐部活动</h4>\n                                    <p>国际象棋俱乐部和羽毛球俱乐部的比赛、训练和活动照片集锦。</p>\n                                </div>\n                            </div>\n                        </div>\n\n                        <div class="col-md-4 mb-4">\n                            <div class="card">\n                                <div class="card-body">\n                                    <h4>社区项目</h4>\n                                    <p>HAF项目、公园活动等社区服务项目的精彩记录。</p>\n                                </div>\n                            </div>\n                        </div>\n                    </div>\n\n                    <div class="row mt-4">\n                        <div class="col-lg-12">\n                            <div class="alert alert-info">\n                                <h5>更多精彩照片即将上线</h5>\n                                <p class="mb-0">我们正在整理更多精彩照片，敬请期待！如果您有活动照片想要分享，请联系我们。</p>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n                ','\n',char(10)),NULL,'图库 - 博文教育集团 | Bowen Education Manchester','博文教育集团图库，记录学生成长瞬间，分享活动精彩照片。包括中文学校、国际象棋俱乐部、羽毛球俱乐部和社区项目的照片集锦。','published','2025-11-07 06:48:05.037223',17,'2025-11-07 06:48:05.038007','2025-11-07 06:48:05.038008');
INSERT INTO single_page VALUES(10,'常见问题解答','您关心的问题，我们都有答案',replace('\n                <div class="container py-5">\n                    <div class="row">\n                        <div class="col-lg-10 mx-auto">\n                            <h2 class="section-title mb-5">常见问题解答</h2>\n\n                            <div class="accordion" id="faqAccordion">\n                                <!-- 关于课程 -->\n                                <div class="mb-4">\n                                    <h3 class="h4 mb-3">关于课程</h3>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    如何报名课程？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>您可以通过以下方式报名：</p>\n                                            <ul>\n                                                <li>访问我们的联系页面填写报名表</li>\n                                                <li>致电我们的办公室</li>\n                                                <li>发送邮件至我们的官方邮箱</li>\n                                                <li>亲临我们的办公地点现场咨询</li>\n                                            </ul>\n                                        </div>\n                                    </div>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    课程费用是多少？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>不同课程的费用有所不同。请访问"补习中心"页面查看具体课程的收费标准，或联系我们获取详细报价。</p>\n                                        </div>\n                                    </div>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    可以试听课程吗？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>是的，我们提供免费试听服务。请提前预约，我们会为您安排合适的试听时间。</p>\n                                        </div>\n                                    </div>\n                                </div>\n\n                                <!-- 关于学校 -->\n                                <div class="mb-4">\n                                    <h3 class="h4 mb-3">关于中文学校</h3>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    上课时间是什么时候？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>中文学校的课程通常安排在周末。具体上课时间请查看"学期日期"页面或联系我们咨询。</p>\n                                        </div>\n                                    </div>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    有哪些年龄段的课程？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>我们提供从基础启蒙班到A-Level的完整课程体系，适合4岁以上的所有年龄段学生。详情请查看"课程设置"页面。</p>\n                                        </div>\n                                    </div>\n                                </div>\n\n                                <!-- 关于俱乐部 -->\n                                <div class="mb-4">\n                                    <h3 class="h4 mb-3">关于俱乐部</h3>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    如何加入国际象棋俱乐部？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>请访问"国际象棋俱乐部"页面了解详情，或直接联系我们报名。我们欢迎所有水平的棋手加入。</p>\n                                        </div>\n                                    </div>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    羽毛球俱乐部需要自备装备吗？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>建议自备球拍和运动鞋。如果暂时没有装备，我们可以提供租借服务。</p>\n                                        </div>\n                                    </div>\n                                </div>\n\n                                <!-- 其他问题 -->\n                                <div class="mb-4">\n                                    <h3 class="h4 mb-3">其他问题</h3>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    学校地址在哪里？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>请访问"联系我们"页面查看详细地址和交通信息。</p>\n                                        </div>\n                                    </div>\n\n                                    <div class="card mb-3">\n                                        <div class="card-header">\n                                            <h5 class="mb-0">\n                                                <button class="btn btn-link text-start w-100" type="button">\n                                                    有停车位吗？\n                                                </button>\n                                            </h5>\n                                        </div>\n                                        <div class="card-body">\n                                            <p>是的，我们提供免费停车位。具体停车信息请在到访前联系我们确认。</p>\n                                        </div>\n                                    </div>\n                                </div>\n                            </div>\n\n                            <div class="alert alert-primary mt-5">\n                                <h5>没有找到您的问题？</h5>\n                                <p class="mb-0">请访问<a href="/contact" class="alert-link">联系我们</a>页面，我们很乐意为您解答任何疑问。</p>\n                            </div>\n                        </div>\n                    </div>\n                </div>\n                ','\n',char(10)),NULL,'常见问题 - 博文教育集团 | Bowen Education Manchester','博文教育集团常见问题解答。了解课程报名、费用、上课时间、俱乐部活动等相关信息。','published','2025-11-07 06:48:05.039022',18,'2025-11-07 06:48:05.039183','2025-11-07 06:48:05.039185');
CREATE TABLE team_member (
	name VARCHAR(100) NOT NULL, 
	title VARCHAR(100), 
	department VARCHAR(100), 
	photo_media_id INTEGER, 
	bio TEXT, 
	qualifications TEXT, 
	specialties VARCHAR(500), 
	email VARCHAR(100), 
	phone VARCHAR(50), 
	linkedin VARCHAR(255), 
	twitter VARCHAR(255), 
	sort_order INTEGER NOT NULL, 
	is_featured BOOLEAN NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(photo_media_id) REFERENCES media_file (id)
);
INSERT INTO team_member VALUES('Dr. Bowen Zhang','Founder & Director','Leadership',NULL,'Dr. Bowen Zhang founded Bowen Education Group in 2018 with a vision to bridge Eastern and Western educational traditions. With a PhD in Education from the University of Manchester and over 15 years of teaching experience, Dr. Zhang has developed innovative Chinese language curricula that have helped hundreds of students achieve fluency and cultural competence.','PhD in Education (University of Manchester), MA in Chinese Linguistics (Peking University), QTS (UK)','Chinese Language Education, Curriculum Development, Educational Leadership','bowen.zhang@boweneducation.org',NULL,NULL,NULL,1,1,1,1,'2025-11-04 21:58:23.446958','2025-11-04 21:58:23.446961');
INSERT INTO team_member VALUES('Miss Emily Chen','Head of Chinese School','Chinese School',NULL,'Miss Emily Chen leads our Chinese School with passion and expertise. A native Mandarin speaker with over 10 years of teaching experience, Emily holds a Master''s degree in Teaching Chinese as a Foreign Language and is certified by Hanban (Confucius Institute Headquarters).','MA in TCFL (Beijing Language and Culture University), Hanban Certified Chinese Teacher','Mandarin Teaching, YCT/HSK Preparation, Children''s Language Development','emily.chen@boweneducation.org',NULL,NULL,NULL,2,1,1,2,'2025-11-04 21:58:23.446962','2025-11-04 21:58:23.446963');
INSERT INTO team_member VALUES('Mr. James Wilson','Head of Tuition Centre','Tuition Centre',NULL,'Mr. James Wilson brings extensive experience in British secondary education to his role as Head of Tuition Centre. With 12 years of teaching experience in Manchester schools and a track record of helping students achieve top grades, James specializes in GCSE and A-Level exam preparation.','BSc Mathematics (University of Cambridge), PGCE Secondary Mathematics, QTS','GCSE/A-Level Mathematics, Physics, Exam Technique','james.wilson@boweneducation.org',NULL,NULL,NULL,3,1,1,3,'2025-11-04 21:58:23.446963','2025-11-04 21:58:23.446964');
CREATE TABLE video (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	category_id INTEGER, 
	video_source VARCHAR(8) NOT NULL, 
	video_media_id INTEGER, 
	youtube_id VARCHAR(100), 
	vimeo_id VARCHAR(100), 
	external_url VARCHAR(500), 
	thumbnail_media_id INTEGER, 
	duration_seconds INTEGER, 
	resolution VARCHAR(20), 
	file_size_mb INTEGER, 
	autoplay BOOLEAN NOT NULL, 
	loop BOOLEAN NOT NULL, 
	muted BOOLEAN NOT NULL, 
	controls BOOLEAN NOT NULL, 
	has_subtitles BOOLEAN NOT NULL, 
	subtitle_url VARCHAR(500), 
	is_featured BOOLEAN NOT NULL, 
	is_public BOOLEAN NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	tags VARCHAR(255), 
	view_count INTEGER NOT NULL, 
	like_count INTEGER NOT NULL, 
	share_count INTEGER NOT NULL, 
	seo_title VARCHAR(200), 
	seo_description TEXT, 
	embed_code TEXT, 
	allow_embed BOOLEAN NOT NULL, 
	requires_login BOOLEAN NOT NULL, 
	allowed_roles VARCHAR(255), 
	notes TEXT, 
	published_at VARCHAR(200), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES video_category (id), 
	FOREIGN KEY(thumbnail_media_id) REFERENCES media_file (id), 
	FOREIGN KEY(video_media_id) REFERENCES media_file (id)
);
INSERT INTO video VALUES('Chinese New Year 2024 Highlights','cny-2024-highlights','Highlights from our spectacular Chinese New Year 2024 celebration featuring student performances and cultural activities.',1,'youtube',NULL,'example1',NULL,NULL,NULL,180,NULL,NULL,0,0,0,1,0,NULL,1,1,'published',1,NULL,0,0,0,NULL,NULL,NULL,1,0,NULL,NULL,NULL,1,'2025-11-04 21:58:23.591021','2025-11-04 21:58:23.591024');
INSERT INTO video VALUES('Student Dragon Dance Performance','dragon-dance-performance','Our talented students perform a traditional Chinese dragon dance at the Manchester Chinese Cultural Festival.',1,'youtube',NULL,'example2',NULL,NULL,NULL,240,NULL,NULL,0,0,0,1,0,NULL,0,1,'published',2,NULL,0,0,0,NULL,NULL,NULL,1,0,NULL,NULL,NULL,2,'2025-11-04 21:58:23.591025','2025-11-04 21:58:23.591025');
CREATE TABLE video_playlist (
	title VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	cover_media_id INTEGER, 
	is_featured BOOLEAN NOT NULL, 
	is_public BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	video_count INTEGER NOT NULL, 
	total_duration_seconds INTEGER NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cover_media_id) REFERENCES media_file (id)
);
CREATE TABLE booking (
	user_id INTEGER, 
	service_id INTEGER NOT NULL, 
	staff_id INTEGER, 
	booking_number VARCHAR(50) NOT NULL, 
	booking_date DATETIME NOT NULL, 
	duration_minutes INTEGER NOT NULL, 
	end_datetime DATETIME, 
	customer_name VARCHAR(100) NOT NULL, 
	customer_email VARCHAR(100) NOT NULL, 
	customer_phone VARCHAR(50) NOT NULL, 
	status VARCHAR(9) NOT NULL, 
	confirmation_method VARCHAR(6) NOT NULL, 
	price FLOAT, 
	payment_status VARCHAR(8) NOT NULL, 
	payment_method VARCHAR(50), 
	paid_at DATETIME, 
	confirmed_at DATETIME, 
	cancelled_at DATETIME, 
	completed_at DATETIME, 
	reminder_sent_at DATETIME, 
	reminder_count INTEGER NOT NULL, 
	customer_notes TEXT, 
	admin_notes TEXT, 
	cancel_reason TEXT, 
	source VARCHAR(50), 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(service_id) REFERENCES booking_service (id), 
	FOREIGN KEY(staff_id) REFERENCES team_member (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	UNIQUE (booking_number)
);
CREATE TABLE booking_time_slot (
	service_id INTEGER NOT NULL, 
	staff_id INTEGER, 
	date DATETIME NOT NULL, 
	start_time TIME NOT NULL, 
	end_time TIME NOT NULL, 
	is_available BOOLEAN NOT NULL, 
	available_slots INTEGER NOT NULL, 
	booked_slots INTEGER NOT NULL, 
	is_special BOOLEAN NOT NULL, 
	special_price FLOAT, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(service_id) REFERENCES booking_service (id), 
	FOREIGN KEY(staff_id) REFERENCES team_member (id)
);
CREATE TABLE cart (
	user_id INTEGER, 
	session_id VARCHAR(100), 
	is_active INTEGER NOT NULL, 
	converted_to_order_id INTEGER, 
	subtotal FLOAT NOT NULL, 
	estimated_tax FLOAT NOT NULL, 
	estimated_shipping FLOAT NOT NULL, 
	estimated_total FLOAT NOT NULL, 
	coupon_code VARCHAR(50), 
	discount_amount FLOAT NOT NULL, 
	last_activity_at DATETIME, 
	expires_at DATETIME, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(converted_to_order_id) REFERENCES "order" (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE contact_message (
	name VARCHAR(100) NOT NULL, 
	contact_info VARCHAR(200) NOT NULL, 
	message_text TEXT NOT NULL, 
	product_id INTEGER, 
	source_page_url VARCHAR(500), 
	status VARCHAR(7) NOT NULL, 
	handled_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE custom_field_option (
	field_id INTEGER NOT NULL, 
	value VARCHAR(100) NOT NULL, 
	label VARCHAR(100) NOT NULL, 
	sort_order INTEGER NOT NULL, 
	is_active BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(field_id) REFERENCES custom_field_def (id)
);
CREATE TABLE event_registration (
	event_id INTEGER NOT NULL, 
	user_id INTEGER, 
	registration_number VARCHAR(50) NOT NULL, 
	attendee_name VARCHAR(100) NOT NULL, 
	attendee_email VARCHAR(100) NOT NULL, 
	attendee_phone VARCHAR(50), 
	company VARCHAR(200), 
	job_title VARCHAR(100), 
	status VARCHAR(9) NOT NULL, 
	ticket_type VARCHAR(10) NOT NULL, 
	ticket_price FLOAT NOT NULL, 
	payment_status VARCHAR(8) NOT NULL, 
	payment_method VARCHAR(50), 
	payment_transaction_id VARCHAR(100), 
	paid_at DATETIME, 
	registered_at DATETIME, 
	confirmed_at DATETIME, 
	checked_in_at DATETIME, 
	cancelled_at DATETIME, 
	check_in_code VARCHAR(100), 
	is_checked_in BOOLEAN NOT NULL, 
	check_in_method VARCHAR(50), 
	dietary_requirements TEXT, 
	special_needs TEXT, 
	how_heard VARCHAR(100), 
	custom_fields TEXT, 
	notes TEXT, 
	admin_notes TEXT, 
	cancel_reason TEXT, 
	confirmation_email_sent BOOLEAN NOT NULL, 
	reminder_email_sent BOOLEAN NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(event_id) REFERENCES event (id), 
	FOREIGN KEY(user_id) REFERENCES user (id), 
	UNIQUE (registration_number)
);
CREATE TABLE event_ticket_type (
	event_id INTEGER NOT NULL, 
	name VARCHAR(100) NOT NULL, 
	description TEXT, 
	price FLOAT NOT NULL, 
	quantity INTEGER, 
	sold_count INTEGER NOT NULL, 
	sale_start_time DATETIME, 
	sale_end_time DATETIME, 
	is_active BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(event_id) REFERENCES event (id)
);
CREATE TABLE file_download_log (
	file_id INTEGER NOT NULL, 
	user_id INTEGER, 
	ip_address VARCHAR(50), 
	user_agent VARCHAR(500), 
	referrer VARCHAR(500), 
	download_status VARCHAR(9) NOT NULL, 
	error_message TEXT, 
	downloaded_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES file_download (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE gallery_image (
	gallery_id INTEGER NOT NULL, 
	media_id INTEGER NOT NULL, 
	title VARCHAR(200), 
	caption TEXT, 
	alt_text VARCHAR(255), 
	tags VARCHAR(255), 
	sort_order INTEGER NOT NULL, 
	is_visible BOOLEAN NOT NULL, 
	is_featured BOOLEAN NOT NULL, 
	link_url VARCHAR(500), 
	link_target VARCHAR(20), 
	view_count INTEGER NOT NULL, 
	download_count INTEGER NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(gallery_id) REFERENCES gallery (id), 
	FOREIGN KEY(media_id) REFERENCES media_file (id)
);
INSERT INTO gallery_image VALUES(1,1,'2024年曼彻斯特地区青少年锦标赛','我们的小棋手在激烈的比赛中展现出色的棋艺和良好的竞技精神。','2024年曼彻斯特地区青少年锦标赛',NULL,1,1,0,NULL,'_self',0,0,NULL,1,'2025-11-07 06:57:00.650332','2025-11-07 06:57:00.650334');
INSERT INTO gallery_image VALUES(1,1,'每周训练课','专业教练指导学员进行系统化训练，提升棋艺水平。','每周训练课',NULL,2,1,0,NULL,'_self',0,0,NULL,2,'2025-11-07 06:57:00.650335','2025-11-07 06:57:00.650336');
INSERT INTO gallery_image VALUES(1,1,'优胜者颁奖典礼','记录获奖者的荣耀时刻，见证努力付出后的收获。','优胜者颁奖典礼',NULL,3,1,0,NULL,'_self',0,0,NULL,3,'2025-11-07 06:57:00.650337','2025-11-07 06:57:00.650337');
INSERT INTO gallery_image VALUES(1,1,'友谊赛合影','与其他俱乐部进行友谊赛，增进交流与友谊。','友谊赛合影',NULL,4,1,0,NULL,'_self',0,0,NULL,4,'2025-11-07 06:57:00.650338','2025-11-07 06:57:00.650339');
INSERT INTO gallery_image VALUES(1,1,'一对一专项指导','教练为学员提供个性化指导，针对性提升棋艺。','一对一专项指导',NULL,5,1,0,NULL,'_self',0,0,NULL,5,'2025-11-07 06:57:00.650340','2025-11-07 06:57:00.650340');
INSERT INTO gallery_image VALUES(1,1,'团队活动日','除了下棋，我们还组织各类团队活动，增进成员友谊。','团队活动日',NULL,6,1,0,NULL,'_self',0,0,NULL,6,'2025-11-07 06:57:00.650341','2025-11-07 06:57:00.650342');
INSERT INTO gallery_image VALUES(2,1,'专业训练课','在专业教练的指导下进行系统化训练，不断提升技术水平。','专业训练课',NULL,1,1,0,NULL,'_self',0,0,NULL,7,'2025-11-07 06:57:00.651295','2025-11-07 06:57:00.651297');
INSERT INTO gallery_image VALUES(2,1,'俱乐部内部联赛','定期举办内部联赛，为成员提供实战机会。','俱乐部内部联赛',NULL,2,1,0,NULL,'_self',0,0,NULL,8,'2025-11-07 06:57:00.651298','2025-11-07 06:57:00.651298');
INSERT INTO gallery_image VALUES(2,1,'青少年培训','俱乐部特别注重青少年运动员的培养，提供系统的训练计划。','青少年培训',NULL,3,1,0,NULL,'_self',0,0,NULL,9,'2025-11-07 06:57:00.651299','2025-11-07 06:57:00.651300');
INSERT INTO gallery_image VALUES(2,1,'友谊交流赛','与其他俱乐部进行友谊交流，切磋技艺。','友谊交流赛',NULL,4,1,0,NULL,'_self',0,0,NULL,10,'2025-11-07 06:57:00.651301','2025-11-07 06:57:00.651301');
INSERT INTO gallery_image VALUES(2,1,'体能训练','专业的体能训练帮助运动员提升身体素质。','体能训练',NULL,5,1,0,NULL,'_self',0,0,NULL,11,'2025-11-07 06:57:00.651302','2025-11-07 06:57:00.651303');
INSERT INTO gallery_image VALUES(2,1,'团队建设活动','通过各类团队活动，增强成员之间的凝聚力。','团队建设活动',NULL,6,1,0,NULL,'_self',0,0,NULL,12,'2025-11-07 06:57:00.651304','2025-11-07 06:57:00.651304');
CREATE TABLE menu_item (
	category_id INTEGER NOT NULL, 
	name VARCHAR(200) NOT NULL, 
	slug VARCHAR(200) NOT NULL, 
	description TEXT, 
	price FLOAT NOT NULL, 
	original_price FLOAT, 
	image_media_id INTEGER, 
	sizes VARCHAR(255), 
	spice_levels VARCHAR(255), 
	customizations TEXT, 
	calories INTEGER, 
	allergens VARCHAR(255), 
	dietary_tags VARCHAR(255), 
	is_available BOOLEAN NOT NULL, 
	stock_quantity INTEGER, 
	daily_limit INTEGER, 
	today_sold INTEGER NOT NULL, 
	is_recommended BOOLEAN NOT NULL, 
	is_popular BOOLEAN NOT NULL, 
	is_new BOOLEAN NOT NULL, 
	is_seasonal BOOLEAN NOT NULL, 
	sort_order INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(category_id) REFERENCES menu_category (id), 
	FOREIGN KEY(image_media_id) REFERENCES media_file (id)
);
CREATE TABLE order_item (
	order_id INTEGER NOT NULL, 
	product_id INTEGER, 
	product_name VARCHAR(200) NOT NULL, 
	product_sku VARCHAR(100), 
	product_variant VARCHAR(255), 
	quantity INTEGER NOT NULL, 
	unit_price FLOAT NOT NULL, 
	subtotal FLOAT NOT NULL, 
	discount_amount FLOAT NOT NULL, 
	total_price FLOAT NOT NULL, 
	notes TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES "order" (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE portfolio_category_link (
	portfolio_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (portfolio_id, category_id), 
	FOREIGN KEY(category_id) REFERENCES portfolio_category (id), 
	FOREIGN KEY(portfolio_id) REFERENCES portfolio (id)
);
CREATE TABLE portfolio_image (
	portfolio_id INTEGER NOT NULL, 
	media_id INTEGER NOT NULL, 
	caption VARCHAR(500), 
	sort_order INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(media_id) REFERENCES media_file (id), 
	FOREIGN KEY(portfolio_id) REFERENCES portfolio (id)
);
CREATE TABLE post_category_link (
	post_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (post_id, category_id), 
	FOREIGN KEY(category_id) REFERENCES post_category (id), 
	FOREIGN KEY(post_id) REFERENCES post (id)
);
CREATE TABLE product_category_link (
	product_id INTEGER NOT NULL, 
	category_id INTEGER NOT NULL, 
	PRIMARY KEY (product_id, category_id), 
	FOREIGN KEY(category_id) REFERENCES product_category (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE product_custom_field_value (
	product_id INTEGER NOT NULL, 
	field_id INTEGER NOT NULL, 
	value_text TEXT NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(field_id) REFERENCES custom_field_def (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE review (
	reviewable_type VARCHAR(50) NOT NULL, 
	reviewable_id INTEGER NOT NULL, 
	reviewer_name VARCHAR(100) NOT NULL, 
	reviewer_email VARCHAR(100) NOT NULL, 
	reviewer_photo VARCHAR(500), 
	user_id INTEGER, 
	title VARCHAR(200), 
	content TEXT NOT NULL, 
	overall_rating INTEGER NOT NULL, 
	quality_rating INTEGER, 
	service_rating INTEGER, 
	value_rating INTEGER, 
	is_verified_purchase BOOLEAN NOT NULL, 
	order_id INTEGER, 
	status VARCHAR(8) NOT NULL, 
	is_featured BOOLEAN NOT NULL, 
	helpful_count INTEGER NOT NULL, 
	unhelpful_count INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(order_id) REFERENCES "order" (id), 
	FOREIGN KEY(user_id) REFERENCES user (id)
);
CREATE TABLE video_playlist_link (
	playlist_id INTEGER NOT NULL, 
	video_id INTEGER NOT NULL, 
	sort_order INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(playlist_id) REFERENCES video_playlist (id), 
	FOREIGN KEY(video_id) REFERENCES video (id)
);
CREATE TABLE cart_item (
	cart_id INTEGER NOT NULL, 
	product_id INTEGER NOT NULL, 
	product_variant VARCHAR(255), 
	product_sku VARCHAR(100), 
	quantity INTEGER NOT NULL, 
	unit_price FLOAT NOT NULL, 
	subtotal FLOAT NOT NULL, 
	discount_amount FLOAT NOT NULL, 
	total_price FLOAT NOT NULL, 
	notes TEXT, 
	added_at DATETIME, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(cart_id) REFERENCES cart (id), 
	FOREIGN KEY(product_id) REFERENCES product (id)
);
CREATE TABLE restaurant_order_item (
	order_id INTEGER NOT NULL, 
	menu_item_id INTEGER, 
	item_name VARCHAR(200) NOT NULL, 
	item_description TEXT, 
	quantity INTEGER NOT NULL, 
	unit_price FLOAT NOT NULL, 
	subtotal FLOAT NOT NULL, 
	size_option VARCHAR(50), 
	spice_level VARCHAR(50), 
	customizations TEXT, 
	special_instructions TEXT, 
	id INTEGER NOT NULL, 
	created_at DATETIME NOT NULL, 
	updated_at DATETIME NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(menu_item_id) REFERENCES menu_item (id), 
	FOREIGN KEY(order_id) REFERENCES restaurant_order (id)
);
CREATE INDEX idx_site_column_menu_location ON site_column(menu_location);
COMMIT;
