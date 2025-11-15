from typing import Any, Dict, List, Callable
from pydantic import BaseModel


class BlockDefinition(BaseModel):
    type: str
    name: str
    category: str
    schema: BaseModel
    render: Callable[[Dict[str, Any], Any], str]


class RichTextSchema(BaseModel):
    html: str = ""


class HeroBannerSchema(BaseModel):
    title: str = ""
    subtitle: str = ""
    background_url: str = ""
    cta_text: str = ""
    cta_link: str = ""


class PostListSchema(BaseModel):
    column_id: int | None = None
    category_id: int | None = None
    limit: int = 6
    status: str = "published"
    is_recommended: bool | None = None


class ProductGridSchema(BaseModel):
    column_id: int | None = None
    category_id: int | None = None
    limit: int = 6
    is_recommended: bool | None = None


class GalleryGridSchema(BaseModel):
    limit: int = 9


class ContactCTASchema(BaseModel):
    title: str = ""
    button_text: str = ""
    button_link: str = "#"

class HeroCarouselItem(BaseModel):
    title: str = ""
    subtitle: str = ""
    desc: str = ""
    background_url: str = ""
    badge_text: str = ""
    cta_text: str = ""
    cta_link: str = "#"

class HeroCarouselSchema(BaseModel):
    items: List[HeroCarouselItem] = []

class QuickEntryItem(BaseModel):
    title: str = ""
    subtitle: str = ""
    desc: str = ""
    href: str = "#"
    icon: str = ""
    tags: List[str] = []

class QuickEntryGridSchema(BaseModel):
    items: List[QuickEntryItem] = []
    heading_badge: str | None = None
    heading_title: str | None = None
    heading_subtitle: str | None = None

class ServiceBlockItem(BaseModel):
    title: str = ""
    subtitle: str = ""
    desc: str = ""
    href: str = "#"
    icon: str = ""
    background_url: str = ""
    badge_text: str | None = None

class ServiceBlocksGridSchema(BaseModel):
    items: List[ServiceBlockItem] = []
    heading_badge: str | None = None
    heading_title: str | None = None
    heading_subtitle: str | None = None

class PartnerLogosSchema(BaseModel):
    logos: List[str] = []
    heading_title: str | None = None
    heading_subtitle: str | None = None
    names: List[str] | None = None

class StatsSectionSchema(BaseModel):
    established_year_key: str = "established_year"
    student_count_key: str = "student_count"
    gcse_pass_rate_key: str = "gcse_pass_rate"
    teacher_count_key: str = "teacher_count"
    heading_title: str | None = None
    heading_subtitle: str | None = None

class ContactSectionSchema(BaseModel):
    enable_form: bool = True
    heading_badge: str | None = None
    heading_title: str | None = None
    heading_subtitle: str | None = None

class NewsGridSchema(BaseModel):
    column_id: int | None = None
    limit: int = 6
    heading_badge: str | None = None
    heading_title: str | None = None
    heading_subtitle: str | None = None
    view_all: bool | None = None
    view_all_href: str | None = None


def render_rich_text(attrs: Dict[str, Any], db) -> str:
    html = attrs.get("html") or ""
    return f"<section class=\"section rich-text\">{html}</section>"


def render_hero_banner(attrs: Dict[str, Any], db) -> str:
    title = attrs.get("title", "")
    subtitle = attrs.get("subtitle", "")
    bg = attrs.get("background_url", "")
    cta_text = attrs.get("cta_text", "")
    cta_link = attrs.get("cta_link", "#")
    style = f"style=\"background-image:url('{bg}')\"" if bg else ""
    btn = f"<a href=\"{cta_link}\" class=\"btn btn-primary\">{cta_text}</a>" if cta_text else ""
    return f"<section class=\"section hero-banner\" {style}><div class=\"container\"><h1>{title}</h1><p class=\"lead\">{subtitle}</p>{btn}</div></section>"


def render_post_list(attrs: Dict[str, Any], db) -> str:
    from app.services import post_service
    posts = post_service.get_posts(
        db,
        column_id=attrs.get("column_id"),
        category_id=attrs.get("category_id"),
        is_recommended=attrs.get("is_recommended"),
        status=attrs.get("status", "published"),
        limit=attrs.get("limit", 6),
    )
    items = "".join([
        f"<li><a href=\"/{p.column.slug}/{p.slug}\">{p.title}</a></li>" if getattr(p, "column", None) else f"<li>{p.title}</li>"
        for p in posts
    ])
    return f"<section class=\"section post-list\"><div class=\"container\"><ul class=\"list-unstyled\">{items}</ul></div></section>"


def render_product_grid(attrs: Dict[str, Any], db) -> str:
    from app.services import product_service
    products = product_service.get_products(
        db,
        column_id=attrs.get("column_id"),
        category_id=attrs.get("category_id"),
        is_recommended=attrs.get("is_recommended"),
        limit=attrs.get("limit", 6),
    )
    cards = "".join([
        f"<div class=\"col-md-4 mb-3\"><div class=\"card\"><div class=\"card-body\"><h5>{pr.name}</h5><p class=\"text-muted\">{pr.price_text or ''}</p></div></div></div>"
        for pr in products
    ])
    return f"<section class=\"section product-grid\"><div class=\"container\"><div class=\"row\">{cards}</div></div></section>"


def render_gallery_grid(attrs: Dict[str, Any], db) -> str:
    from app.services.gallery_service import GalleryService
    service = GalleryService(db)
    from app.models.gallery import Gallery
    galleries = db.query(Gallery).filter(Gallery.is_public == True).order_by(Gallery.sort_order).limit(attrs.get("limit", 9)).all()
    tiles = "".join([
        f"<div class=\"col-md-4 mb-3\"><a href=\"/{g.slug}\" class=\"d-block\"><div class=\"ratio ratio-16x9 bg-light\"></div><div class=\"mt-2\">{g.name}</div></a></div>"
        for g in galleries
    ])
    return f"<section class=\"section gallery-grid\"><div class=\"container\"><div class=\"row\">{tiles}</div></div></section>"


def render_contact_cta(attrs: Dict[str, Any], db) -> str:
    t = attrs.get("title", "")
    bt = attrs.get("button_text", "")
    bl = attrs.get("button_link", "#")
    btn = f"<a href=\"{bl}\" class=\"btn btn-primary\">{bt}</a>" if bt else ""
    return f"<section class=\"section contact-cta\"><div class=\"container\"><h3>{t}</h3>{btn}</div></section>"

def render_hero_carousel(attrs: Dict[str, Any], db) -> str:
    items = attrs.get("items", [])
    slides = []
    for it in items:
        badge = f"<div class=\"hero-badge\"><span>{it.get('badge_text','')}</span></div>" if it.get("badge_text") else ""
        btn = f"<a href=\"{it.get('cta_link','#')}\" class=\"btn btn-primary btn-lg\">{it.get('cta_text','')}</a>" if it.get("cta_text") else ""
        slides.append(
            f"<div class=\"swiper-slide\"><div class=\"hero-slide\" style=\"background-image: url('{it.get('background_url','')}');\">{badge}<div class=\"container\"><div class=\"hero-slide-content\"><h1 class=\"hero-slide-title\">{it.get('title','')}</h1><p class=\"hero-slide-subtitle\">{it.get('subtitle','')}</p><p class=\"hero-slide-desc\">{it.get('desc','')}</p><div class=\"mt-4\">{btn}</div></div></div></div></div>"
        )
    html = "".join(slides)
    return (
        "<section class=\"hero-carousel\"><div class=\"swiper heroSwiper\"><div class=\"swiper-wrapper\">"
        + html
        + "</div><div class=\"swiper-button-next\"></div><div class=\"swiper-button-prev\"></div><div class=\"swiper-pagination\"></div></div></section>"
    )

def render_quick_entry_grid(attrs: Dict[str, Any], db) -> str:
    items = attrs.get("items", [])
    cards = []
    for it in items:
        tags_html = "".join([f"<span class=\"quick-entry-tag\">{t}</span>" for t in it.get("tags", [])])
        cards.append(
            f"<a href=\"{it.get('href','#')}\" class=\"quick-entry-card\"><div class=\"quick-entry-icon\"><div class=\"quick-entry-icon-bg\">{it.get('icon','')}</div></div><div class=\"quick-entry-content\"><h3 class=\"quick-entry-title\">{it.get('title','')}</h3><p class=\"quick-entry-subtitle\">{it.get('subtitle','')}</p><p class=\"quick-entry-desc\">{it.get('desc','')}</p><div class=\"quick-entry-features\">{tags_html}</div></div><div class=\"quick-entry-arrow\"><svg width=\"24\" height=\"24\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\"><path d=\"M5 12h14M12 5l7 7-7 7\"/></svg></div></a>"
        )
    head = ""
    if attrs.get("heading_badge") or attrs.get("heading_title") or attrs.get("heading_subtitle"):
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<span class=\"badge-custom mb-3\">{attrs.get('heading_badge')}</span>" if attrs.get("heading_badge") else "")
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + "</div>"
        )
    return (
        "<section class=\"section py-5\"><div class=\"container\">"
        + head
        + "<div class=\"quick-entry-grid\">"
        + "".join(cards)
        + "</div></div></section>"
    )

def render_service_blocks_grid(attrs: Dict[str, Any], db) -> str:
    items = attrs.get("items", [])
    blocks = []
    for it in items:
        badge = f"<div class=\"service-badge\">{it.get('badge_text','')}</div>" if it.get("badge_text") else ""
        blocks.append(
            f"<a href=\"{it.get('href','#')}\" class=\"text-decoration-none\"><div class=\"service-block\">{badge}<div class=\"service-block-bg\" style=\"background-image: url('{it.get('background_url','')}');\"></div><div class=\"service-block-content\"><div class=\"service-block-icon\">{it.get('icon','')}</div><h3 class=\"service-block-title\">{it.get('title','')}<br><span style=\"font-size: 1.25rem;\">{it.get('subtitle','')}</span></h3><p class=\"service-block-desc\">{it.get('desc','')}</p></div></div></a>"
        )
    head = ""
    if attrs.get("heading_badge") or attrs.get("heading_title") or attrs.get("heading_subtitle"):
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<span class=\"badge-custom mb-3\">{attrs.get('heading_badge')}</span>" if attrs.get("heading_badge") else "")
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + "</div>"
        )
    return (
        "<section class=\"section bg-light py-5\"><div class=\"container\">"
        + head
        + "<div class=\"service-blocks\">"
        + "".join(blocks)
        + "</div></div></section>"
    )

def render_news_grid(attrs: Dict[str, Any], db) -> str:
    from app.services import post_service
    posts = post_service.get_posts(db, status="published", limit=attrs.get("limit", 6), column_id=attrs.get("column_id"))
    cards = []
    for idx, p in enumerate(posts):
        img = getattr(p, "featured_image", "")
        column_name = getattr(getattr(p, "column", None), "name", "")
        date1 = p.published_at.strftime("%Y年%m月%d日") if getattr(p, "published_at", None) else ""
        date2 = p.published_at.strftime("%B %d, %Y") if getattr(p, "published_at", None) else ""
        excerpt = (p.summary or (p.content_html or "").strip())
        excerpt = excerpt[:100] + "..." if excerpt else ""
        cards.append(
            f"<article class=\"news-card\" data-aos-delay=\"{idx*100}\"><div class=\"news-card-image\" style=\"background-image: url('{img}');\"><span class=\"news-card-category\">{column_name}</span></div><div class=\"news-card-content\"><div class=\"news-card-date\">{date1} | {date2}</div><h3 class=\"news-card-title\">{p.title}</h3><p class=\"news-card-excerpt\">{excerpt}</p><a href=\"/{getattr(getattr(p,'column',None),'slug','news')}/{p.slug}/\" class=\"btn btn-sm btn-primary\">阅读更多 Read More →</a></div></article>"
        )
    head = ""
    if attrs.get("heading_badge") or attrs.get("heading_title") or attrs.get("heading_subtitle"):
        btn = (
            f"<div class=\"mt-3\"><a href=\"{attrs.get('view_all_href','/news/')}\" class=\"btn btn-outline-primary\">查看全部 View All →</a></div>"
            if attrs.get("view_all")
            else ""
        )
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<span class=\"badge-custom mb-3\">{attrs.get('heading_badge')}</span>" if attrs.get("heading_badge") else "")
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + btn
            + "</div>"
        )
    return "<section class=\"section py-5\"><div class=\"container\">" + head + "<div class=\"news-grid\">" + "".join(cards) + "</div></div></section>"

def render_partner_logos(attrs: Dict[str, Any], db) -> str:
    logos = attrs.get("logos", [])
    names = attrs.get("names") or []
    items = "".join([f"<div class=\"partner-logo\"><img src=\"{src}\" alt=\"logo\"/></div>" for src in logos])
    if not logos and names:
        items = "".join([f"<div class=\"partner-name\">{n}</div>" for n in names])
    head = ""
    if attrs.get("heading_title") or attrs.get("heading_subtitle"):
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + "</div>"
        )
    return "<section class=\"section bg-light py-5\"><div class=\"container\">" + head + "<div class=\"partner-logos justify-content-center\">" + items + "</div></div></section>"

def render_stats_section(attrs: Dict[str, Any], db) -> str:
    from app.services import site_service
    s = site_service.get_all_site_settings(db)
    est = s.get(attrs.get("established_year_key","established_year")) or "2018"
    stu = s.get(attrs.get("student_count_key","student_count")) or "500+"
    gcse = s.get(attrs.get("gcse_pass_rate_key","gcse_pass_rate")) or "100%"
    tch = s.get(attrs.get("teacher_count_key","teacher_count")) or "30+"
    head = ""
    if attrs.get("heading_title") or attrs.get("heading_subtitle"):
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + "</div>"
        )
    return (
        "<section class=\"stats-section\"><div class=\"container\">"
        + head
        + "<div class=\"stats-grid\">"
        + f"<div class=\"stat-item\"><div class=\"stat-icon\">📅</div><div class=\"stat-number\">{est}</div><div class=\"stat-label\">成立年份<br>Established</div></div>"
        + f"<div class=\"stat-item\"><div class=\"stat-icon\">👨‍🎓</div><div class=\"stat-number\">{stu}</div><div class=\"stat-label\">在读学生<br>Active Students</div></div>"
        + f"<div class=\"stat-item\"><div class=\"stat-icon\">🏆</div><div class=\"stat-number\">{gcse}</div><div class=\"stat-label\">GCSE通过率<br>Pass Rate</div></div>"
        + f"<div class=\"stat-item\"><div class=\"stat-icon\">👨‍🏫</div><div class=\"stat-number\">{tch}</div><div class=\"stat-label\">专业教师<br>Teachers</div></div>"
        + "</div></div></section>"
    )

def render_contact_section(attrs: Dict[str, Any], db) -> str:
    form = "" if not attrs.get("enable_form", True) else (
        "<form id=\"contactForm\" class=\"needs-validation\" novalidate>"
        + "<div class=\"mb-3\"><label class=\"form-label\">姓名 Name *</label><input type=\"text\" class=\"form-control\" name=\"name\" required></div>"
        + "<div class=\"mb-3\"><label class=\"form-label\">邮箱 Email *</label><input type=\"email\" class=\"form-control\" name=\"email\" required></div>"
        + "<div class=\"mb-3\"><label class=\"form-label\">电话 Phone</label><input type=\"tel\" class=\"form-control\" name=\"phone\"></div>"
        + "<div class=\"mb-3\"><label class=\"form-label\">感兴趣 Interested In *</label><select class=\"form-select\" name=\"interest\" required><option value=\"\">Please select</option><option value=\"chinese-school\">Chinese School</option><option value=\"chess-club\">Chess Club</option><option value=\"badminton-club\">Badminton Club</option><option value=\"haf-programme\">HAF Government Programmes</option><option value=\"tutoring\">Academic Tutoring</option><option value=\"other\">Other</option></select></div>"
        + "<div class=\"mb-3\"><label class=\"form-label\">留言 Message *</label><textarea class=\"form-control\" name=\"message\" rows=\"4\" required></textarea></div>"
        + "<button type=\"submit\" class=\"btn btn-primary btn-lg w-100\">发送消息 Send Message</button>"
        + "</form>"
    )
    info = (
        "<div class=\"bg-light p-4 rounded mb-3\"><h4 class=\"h5 fw-bold mb-3\">Contact Information</h4>"
        + "<p class=\"mb-2\"><strong>📍 Address:</strong><br>Manchester, UK</p>"
        + "<p class=\"mb-2\"><strong>📞 Phone:</strong><br><span class=\"text-muted\">0161 xxx xxxx</span></p>"
        + "<p class=\"mb-2\"><strong>📧 Email:</strong><br><span class=\"text-muted\">info@boweneducation.org</span></p>"
        + "<p class=\"mb-0\"><strong>🕐 Opening Hours:</strong><br>Saturday: 9:00 - 17:00<br>Sunday: 9:00 - 17:00</p>"
        + "</div>"
    )
    head = ""
    if attrs.get("heading_badge") or attrs.get("heading_title") or attrs.get("heading_subtitle"):
        head = (
            "<div class=\"text-center mb-5\">"
            + (f"<span class=\"badge-custom mb-3\">{attrs.get('heading_badge')}</span>" if attrs.get("heading_badge") else "")
            + (f"<h2 class=\"display-5 fw-bold mb-3\">{attrs.get('heading_title')}</h2>" if attrs.get("heading_title") else "")
            + (f"<p class=\"lead text-muted\">{attrs.get('heading_subtitle')}</p>" if attrs.get("heading_subtitle") else "")
            + "</div>"
        )
    return "<section class=\"section py-5\"><div class=\"container\">" + head + "<div class=\"contact-map-section\"><div>" + form + "</div><div>" + info + "</div></div></div></section>"


REGISTRY: Dict[str, BlockDefinition] = {
    "RichText": BlockDefinition(type="RichText", name="富文本", category="content", schema=RichTextSchema(), render=render_rich_text),
    "HeroBanner": BlockDefinition(type="HeroBanner", name="横幅", category="layout", schema=HeroBannerSchema(), render=render_hero_banner),
    "PostList": BlockDefinition(type="PostList", name="文章列表", category="content", schema=PostListSchema(), render=render_post_list),
    "ProductGrid": BlockDefinition(type="ProductGrid", name="产品网格", category="content", schema=ProductGridSchema(), render=render_product_grid),
    "GalleryGrid": BlockDefinition(type="GalleryGrid", name="相册网格", category="media", schema=GalleryGridSchema(), render=render_gallery_grid),
    "ContactCTA": BlockDefinition(type="ContactCTA", name="联系CTA", category="content", schema=ContactCTASchema(), render=render_contact_cta),
    "HeroCarousel": BlockDefinition(type="HeroCarousel", name="横幅轮播", category="layout", schema=HeroCarouselSchema(), render=render_hero_carousel),
    "QuickEntryGrid": BlockDefinition(type="QuickEntryGrid", name="快捷入口", category="content", schema=QuickEntryGridSchema(), render=render_quick_entry_grid),
    "ServiceBlocksGrid": BlockDefinition(type="ServiceBlocksGrid", name="服务模块", category="content", schema=ServiceBlocksGridSchema(), render=render_service_blocks_grid),
    "NewsGrid": BlockDefinition(type="NewsGrid", name="新闻栅格", category="content", schema=NewsGridSchema(), render=render_news_grid),
    "PartnerLogos": BlockDefinition(type="PartnerLogos", name="合作伙伴", category="media", schema=PartnerLogosSchema(), render=render_partner_logos),
    "StatsSection": BlockDefinition(type="StatsSection", name="统计数据", category="content", schema=StatsSectionSchema(), render=render_stats_section),
    "ContactSection": BlockDefinition(type="ContactSection", name="联系板块", category="content", schema=ContactSectionSchema(), render=render_contact_section),
}


def get_block_types() -> List[Dict[str, Any]]:
    return [{"type": b.type, "name": b.name, "category": b.category} for b in REGISTRY.values()]


def render_block(block_type: str, attributes: Dict[str, Any], db) -> str:
    block_def = REGISTRY.get(block_type)
    if not block_def:
        return ""
    model = block_def.schema.__class__(**(attributes or {}))
    return block_def.render(model.model_dump(), db)