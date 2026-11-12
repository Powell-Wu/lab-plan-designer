"""将通用 furniture-import.json 注入设计器家具库，不写入任何布局坐标。"""
import argparse
import json
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--data', required=True, help='通用家具 JSON')
parser.add_argument('--source', required=True, help='已有设计器 HTML')
parser.add_argument('--output', required=True, help='输出 HTML')
args = parser.parse_args()

data_path = Path(args.data)
payload = json.loads(data_path.read_text(encoding='utf8'))
records = payload['records']
payload.setdefault('recordCount', len(records))
payload.setdefault('totalQuantity', sum(int(p.get('quantity', 1)) for p in records))
payload.setdefault('completeDimensions', sum(not p.get('estimatedDimensions') for p in records))
payload['layout'] = False

items = []
for p in records:
    if p.get('w') is None or p.get('d') is None or p.get('h') is None:
        raise ValueError(f"{p.get('id')} 缺少模型占位尺寸；请明确提供 w/d/h，并在 estimatedDimensions 中标记估算项")
    items.append(dict(
        key='product:' + p['id'], type=p['type'], name=p.get('libraryName') or p.get('shortName') or p['name'],
        w=p['w'], d=p['d'], h=p['h'], color=p.get('color', '#9A7B5C'),
        opt=dict(product=p),
    ))

bootstrap = '\nwindow.__FURNITURE_IMPORT__ = ' + json.dumps(payload, ensure_ascii=False) + ';\n'
bootstrap += 'window.__FURNITURE_LIBRARY_ITEMS__ = ' + json.dumps(items, ensure_ascii=False) + ';\n'
bootstrap += '''for (const item of window.__FURNITURE_LIBRARY_ITEMS__) {
  if (!zt[item.key]) {
    zt[item.key] = item;
    v1.push({group: '采购清单', items: [item]});
    zz.push(['采购清单', item.name, [item.key]]);
  }
}
window.__FURNITURE_LAYOUT__ = false;
'''

html = Path(args.source).read_text(encoding='utf8')
module_start = html.find('<script type="module" crossorigin>')
module_end = html.find('</script>', module_start)
if module_start < 0 or module_end < 0:
    raise RuntimeError('不是受支持的设计器 HTML：未找到模块脚本')
html = html[:module_end] + bootstrap + html[module_end:]
Path(args.output).write_text(html, encoding='utf8')
print(json.dumps(dict(output=args.output, records=len(records), layout=False), ensure_ascii=False))
