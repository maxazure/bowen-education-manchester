/* 简版页面编辑器交互脚本：加载布局、新增分区、新增区块、发布与预览 */

function api(path, opts = {}) {
  return fetch(path, Object.assign({ headers: { 'Content-Type': 'application/json' } }, opts)).then(r => r.json());
}

function getScopeBase() {
  // 依据当前页面路径判断是首页管理还是栏目页面编辑
  const pathname = window.location.pathname;
  if (pathname.startsWith('/admin/home')) return '/admin/home';
  const m = pathname.match(/\/admin\/columns\/(\d+)\/builder/);
  if (m) return `/admin/columns/${m[1]}/builder`;
  return '/admin/home';
}

function renderTree(tree) {
  const sectionsEl = document.getElementById('sections');
  sectionsEl.innerHTML = '';
  const layoutId = tree && tree.layout && tree.layout.id ? tree.layout.id : document.getElementById('layout-root').dataset.layoutId;
  document.getElementById('layout-root').dataset.layoutId = layoutId;
  const sections = (tree && tree.sections) ? tree.sections : [];
  sections.forEach(section => {
    const card = document.createElement('div');
    card.className = 'card';
    card.innerHTML = `
      <div class="card-header d-flex justify-content-between align-items-center">
        <span>分区 #${section.id} ${section.title || ''}</span>
        <div>
          <button class="btn btn-sm btn-outline-secondary" onclick="addBlock(${section.id}, 'RichText')">+ RichText</button>
          <button class="btn btn-sm btn-outline-secondary" onclick="addBlock(${section.id}, 'HeroBanner')">+ HeroBanner</button>
        </div>
      </div>
      <div class="card-body" id="section-${section.id}"></div>
    `;
    sectionsEl.appendChild(card);
    const body = card.querySelector(`#section-${section.id}`);
    body.innerHTML = '';
    section.blocks.forEach(block => {
      const div = document.createElement('div');
      div.className = 'border rounded p-2 mb-2';
      div.dataset.blockId = block.id;
      const attrs = block.attributes_json || '{}';
      div.innerHTML = `<div class="d-flex justify-content-between"><strong>${block.block_type}</strong><div><button class="btn btn-sm btn-outline-secondary me-2" onclick="toggleAttrs(${block.id})">属性(JSON)</button><button class="btn btn-sm btn-outline-primary me-2" onclick="openForm(${block.id}, '${block.block_type}')">表单编辑</button><button class="btn btn-sm btn-outline-danger" onclick="deleteBlock(${block.id})">删除</button></div></div>
        <small class="text-muted">id=${block.id}</small>
        <div id="attrs-${block.id}" class="mt-2 d-none">
          <textarea class="form-control" rows="4">${attrs}</textarea>
          <div class="mt-2">
            <button class="btn btn-sm btn-primary" onclick="saveAttrs(${block.id})">保存</button>
          </div>
        </div>
        <div id="form-${block.id}" class="mt-2 d-none"></div>`;
      body.appendChild(div);
    });

    // 初始化区块拖拽排序
    if (window.Sortable) {
      Sortable.create(body, {
        animation: 150,
        onEnd: () => {
          const order = Array.from(body.children).map((el, idx) => ({ id: parseInt(el.dataset.blockId, 10), sort_order: idx }));
          const base = getScopeBase();
          const path = base === '/admin/home' ? '/admin/home/blocks/reorder' : `${base}/blocks/reorder`;
          api(path, { method: 'POST', body: JSON.stringify({ section_id: section.id, order }) });
        }
      });
    }
  });

  // 初始化分区拖拽排序
  if (window.Sortable) {
    Sortable.create(sectionsEl, {
      animation: 150,
      handle: '.card-header',
      onEnd: () => {
        const order = Array.from(sectionsEl.children).map((card, idx) => {
          const idText = card.querySelector('.card-header span').textContent;
          const id = parseInt(idText.replace(/[^0-9]/g, ''), 10);
          return { id, sort_order: idx };
        });
        const layoutId = document.getElementById('layout-root').dataset.layoutId;
        const base = getScopeBase();
        const path = base === '/admin/home' ? '/admin/home/sections/reorder' : `${base}/sections/reorder`;
        api(path, { method: 'POST', body: JSON.stringify({ layout_id: layoutId, order }) });
      }
    });
  }
}

function loadData() {
  const base = getScopeBase();
  const path = base === '/admin/home' ? '/admin/home/data' : `${base}/data`;
  api(path).then(tree => {
    window.__LAYOUT_TREE__ = tree;
    renderTree(tree);
  });
}

function addSection() {
  const layoutId = document.getElementById('layout-root').dataset.layoutId;
  const base = getScopeBase();
  const path = base === '/admin/home' ? '/admin/home/sections' : `${base}/sections`;
  api(path + `?layout_id=${layoutId}&title=分区&sort_order=0`, { method: 'POST' }).then(() => loadData());
}

function addBlock(sectionId, type) {
  const base = getScopeBase();
  const path = base === '/admin/home' ? '/admin/home/blocks' : `${base}/blocks`;
  const attrs = type === 'RichText' ? { html: '<p>示例文本</p>' } : { title: '欢迎', subtitle: '副标题', background_url: '', cta_text: '', cta_link: '#' };
  api(path, { method: 'POST', body: JSON.stringify({ section_id: sectionId, block_type: type, attributes_json: JSON.stringify(attrs) }) }).then(() => loadData());
}

function deleteBlock(blockId) {
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path, { method: 'DELETE' }).then(() => loadData());
}

function publishLayout() {
  const base = getScopeBase();
  const path = base === '/admin/home' ? '/admin/home/publish' : `${base}/publish`;
  api(path, { method: 'POST' }).then(() => alert('发布成功'));
}

function previewLayout(e) {
  e && e.preventDefault();
  const base = getScopeBase();
  const path = base === '/admin/home' ? '/admin/home/preview' : `${base}/preview`;
  window.location.href = path;
}

function addRichText() { alert('请选择分区中的 + RichText 按钮'); }
function addHeroBanner() { alert('请选择分区中的 + HeroBanner 按钮'); }

document.addEventListener('DOMContentLoaded', loadData);
function toggleAttrs(blockId) {
  const el = document.getElementById(`attrs-${blockId}`);
  if (!el) return;
  el.classList.toggle('d-none');
}

function saveAttrs(blockId) {
  const base = getScopeBase();
  const box = document.querySelector(`#attrs-${blockId} textarea`);
  if (!box) return;
  const val = box.value;
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(val)}`, { method: 'PUT' }).then(() => loadData());
}

function paletteAdd(type) {
  const sectionsEl = document.getElementById('sections');
  const firstSection = sectionsEl.querySelector('.card');
  if (!firstSection) { addSection(); setTimeout(() => paletteAdd(type), 300); return; }
  const idText = firstSection.querySelector('.card-header span').textContent;
  const sectionId = parseInt(idText.replace(/[^0-9]/g, ''), 10);
  addBlock(sectionId, type);
}
function setFormHtml(el, html){ el.innerHTML = html; el.classList.remove('d-none'); }

function openForm(blockId, blockType){
  const formBox = document.getElementById(`form-${blockId}`);
  if(!formBox) return;
  const raw = document.querySelector(`#attrs-${blockId} textarea`);
  let attrs = {};
  try{ attrs = raw ? JSON.parse(raw.value) : {}; } catch(e){ attrs = {}; }
  if(blockType === 'HeroBanner'){
    const h = `
      <div class="row g-2">
        <div class="col-md-6"><input class="form-control" id="f-title-${blockId}" placeholder="标题" value="${attrs.title||''}"></div>
        <div class="col-md-6"><input class="form-control" id="f-subtitle-${blockId}" placeholder="副标题" value="${attrs.subtitle||''}"></div>
        <div class="col-md-8"><input class="form-control" id="f-bg-${blockId}" placeholder="背景URL" value="${attrs.background_url||''}"></div>
        <div class="col-md-2"><input class="form-control" id="f-cta-text-${blockId}" placeholder="按钮文本" value="${attrs.cta_text||''}"></div>
        <div class="col-md-2"><input class="form-control" id="f-cta-link-${blockId}" placeholder="按钮链接" value="${attrs.cta_link||''}"></div>
      </div>
      <div class="mt-2"><button class="btn btn-sm btn-primary" onclick="saveFormHero(${blockId})">保存</button></div>
    `;
    setFormHtml(formBox, h);
  } else if(blockType === 'ContactSection'){
    const h = `
      <div class="form-check">
        <input class="form-check-input" type="checkbox" id="f-enable-${blockId}" ${attrs.enable_form? 'checked':''}>
        <label class="form-check-label" for="f-enable-${blockId}">启用表单</label>
      </div>
      <div class="mt-2"><button class="btn btn-sm btn-primary" onclick="saveFormContact(${blockId})">保存</button></div>
    `;
    setFormHtml(formBox, h);
  } else if(blockType === 'QuickEntryGrid' || blockType === 'ServiceBlocksGrid'){
    const items = Array.isArray(attrs.items) ? attrs.items : [];
    const isService = blockType === 'ServiceBlocksGrid';
    const cols = isService ? ['title','subtitle','desc','href','icon','background_url','badge_text'] : ['title','subtitle','desc','href','icon','tags'];
    let rows = '';
    items.forEach((it, idx) => {
      rows += '<tr>' + cols.map(c => {
        const v = it[c] || '';
        return `<td><input class="form-control" id="f-${c}-${blockId}-${idx}" value="${Array.isArray(v)? v.join(',') : v}"></td>`;
      }).join('') + `<td><div class="d-flex gap-2"><button class="btn btn-sm btn-primary" onclick="saveGridItem(${blockId}, ${idx}, '${blockType}')">保存</button><button class="btn btn-sm btn-outline-danger" onclick="deleteGridItem(${blockId}, ${idx}, '${blockType}')">删除</button></div></td></tr>`;
    });
    const h = `
      <div class="table-responsive">
        <table class="table table-sm">
          <thead><tr>${cols.map(c=>`<th>${c}</th>`).join('')}<th>操作</th></tr></thead>
          <tbody id="grid-${blockId}-tbody">${rows}</tbody>
        </table>
      </div>
      <div class="d-flex gap-2">
        <button class="btn btn-sm btn-outline-secondary" onclick="addGridItem(${blockId}, '${blockType}')">新增项</button>
        <button class="btn btn-sm btn-primary" onclick="saveGridAll(${blockId}, '${blockType}')">保存全部</button>
      </div>
    `;
    setFormHtml(formBox, h);
  } else {
    formBox.classList.add('d-none');
    alert('该区块暂未提供表单编辑，请使用属性(JSON)编辑');
  }
}

function saveFormHero(blockId){
  const attrs = {
    title: document.getElementById(`f-title-${blockId}`).value.trim(),
    subtitle: document.getElementById(`f-subtitle-${blockId}`).value.trim(),
    background_url: document.getElementById(`f-bg-${blockId}`).value.trim(),
    cta_text: document.getElementById(`f-cta-text-${blockId}`).value.trim(),
    cta_link: document.getElementById(`f-cta-link-${blockId}`).value.trim(),
  };
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(JSON.stringify(attrs))}`, { method: 'PUT' }).then(() => loadData());
}

function saveFormContact(blockId){
  const attrs = { enable_form: document.getElementById(`f-enable-${blockId}`).checked };
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(JSON.stringify(attrs))}`, { method: 'PUT' }).then(() => loadData());
}

function readGridAttrs(blockId, blockType){
  const raw = document.querySelector(`#attrs-${blockId} textarea`);
  let attrs = {};
  try{ attrs = raw ? JSON.parse(raw.value) : {}; } catch(e){ attrs = {}; }
  if(!Array.isArray(attrs.items)) attrs.items = [];
  return attrs;
}

function addGridItem(blockId, blockType){
  const tbody = document.getElementById(`grid-${blockId}-tbody`);
  const idx = tbody ? tbody.children.length : 0;
  const isService = blockType === 'ServiceBlocksGrid';
  const cols = isService ? ['title','subtitle','desc','href','icon','background_url','badge_text'] : ['title','subtitle','desc','href','icon','tags'];
  const row = document.createElement('tr');
  row.innerHTML = cols.map(c=>`<td><input class="form-control" id="f-${c}-${blockId}-${idx}" value=""></td>`).join('') + `<td><div class="d-flex gap-2"><button class="btn btn-sm btn-primary" onclick="saveGridItem(${blockId}, ${idx}, '${blockType}')">保存</button><button class="btn btn-sm btn-outline-danger" onclick="deleteGridItem(${blockId}, ${idx}, '${blockType}')">删除</button></div></td>`;
  if(tbody) tbody.appendChild(row);
}

function saveGridItem(blockId, idx, blockType){
  const isService = blockType === 'ServiceBlocksGrid';
  const cols = isService ? ['title','subtitle','desc','href','icon','background_url','badge_text'] : ['title','subtitle','desc','href','icon','tags'];
  const attrs = readGridAttrs(blockId, blockType);
  while(attrs.items.length <= idx) attrs.items.push({});
  const item = {};
  cols.forEach(c=>{
    const el = document.getElementById(`f-${c}-${blockId}-${idx}`);
    const val = el ? el.value.trim() : '';
    item[c] = c==='tags' ? (val? val.split(',').map(s=>s.trim()).filter(Boolean) : []) : val;
  });
  attrs.items[idx] = item;
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(JSON.stringify(attrs))}`, { method: 'PUT' }).then(() => loadData());
}

function deleteGridItem(blockId, idx, blockType){
  const attrs = readGridAttrs(blockId, blockType);
  attrs.items = attrs.items.filter((_, i)=> i !== idx);
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(JSON.stringify(attrs))}`, { method: 'PUT' }).then(() => loadData());
}

function saveGridAll(blockId, blockType){
  const isService = blockType === 'ServiceBlocksGrid';
  const cols = isService ? ['title','subtitle','desc','href','icon','background_url','badge_text'] : ['title','subtitle','desc','href','icon','tags'];
  const tbody = document.getElementById(`grid-${blockId}-tbody`);
  const attrs = { items: [] };
  if(tbody){
    Array.from(tbody.children).forEach((tr, idx)=>{
      const item = {};
      cols.forEach(c=>{
        const el = document.getElementById(`f-${c}-${blockId}-${idx}`);
        const val = el ? el.value.trim() : '';
        item[c] = c==='tags' ? (val? val.split(',').map(s=>s.trim()).filter(Boolean) : []) : val;
      });
      attrs.items.push(item);
    });
  }
  const base = getScopeBase();
  const path = base === '/admin/home' ? `/admin/home/blocks/${blockId}` : `${base}/blocks/${blockId}`;
  fetch(path + `?attributes_json=${encodeURIComponent(JSON.stringify(attrs))}`, { method: 'PUT' }).then(() => loadData());
}