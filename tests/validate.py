"""DRIVEBASE standalone consistency validator (stdlib only)."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(condition, message):
    if not condition:
        errors.append(message)

def read(name):
    with (ROOT / 'data' / name).open(encoding='utf-8') as stream:
        value = json.load(stream)
    check(isinstance(value, list), f'{name} must be a list')
    return value

brands = read('brands.json')
models = read('models.json')
variants = read('variants.json')

for label, items in [('brands', brands), ('models', models), ('variants', variants)]:
    ids = [x.get('id') for x in items]
    check(len(ids) == len(set(ids)), f'duplicate ids in {label}')
    for record in items:
        check(isinstance(record.get('id'), str) and bool(re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', record['id'])), f'{label} invalid id {record.get("id")}')

brand_ids = {x['id'] for x in brands}
model_ids = {x['id'] for x in models}

for model in models:
    mid = model['id']
    check(model.get('brand_id') in brand_ids, f'{mid}: unknown brand')
    for key in ('name', 'body_type', 'tagline', 'description', 'image_path', 'image_credit'):
        check(isinstance(model.get(key), str) and bool(model[key].strip()), f'{mid}: missing {key}')
    check(isinstance(model.get('featured'), bool), f'{mid}: invalid featured flag')
    path = (ROOT / model['image_path']).resolve()
    check(path.is_relative_to(ROOT) and path.is_file(), f'{mid}: missing or unsafe image path')

spec_keys = ('displacement_cc', 'power_kw', 'power_ps', 'torque_nm', 'torque_kgm',
             'length_mm', 'width_mm', 'height_mm', 'wheelbase_mm', 'weight_kg',
             'fuel_economy_km_l', 'fuel_cycle')
for variant in variants:
    vid = variant['id']
    check(variant.get('model_id') in model_ids, f'{vid}: unknown model')
    check(variant.get('status') in ('published', 'draft'), f'{vid}: invalid status')
    check(isinstance(variant.get('market'), str) and bool(variant['market']), f'{vid}: missing market')
    check(variant.get('year') is None or (isinstance(variant['year'], int) and 1900 <= variant['year'] <= 2100), f'{vid}: invalid year')
    check(isinstance(variant.get('trim'), str) and bool(variant['trim'].strip()), f'{vid}: missing trim')
    for key in ('transmission', 'drivetrain', 'fuel_type'):
        check(variant.get(key) is None or isinstance(variant[key], str), f'{vid}: invalid {key}')
    spec = variant.get('specs')
    check(isinstance(spec, dict), f'{vid}: no specs')
    if isinstance(spec, dict):
        for key in spec_keys:
            check(key in spec, f'{vid}: missing spec {key}')
            if key in spec:
                v = spec[key]
                check(v is None or (isinstance(v, str) if key == 'fuel_cycle' else isinstance(v, (float, int)) and not isinstance(v, bool) and v > 0), f'{vid}: invalid spec {key}')
    sources = variant.get('sources')
    check(isinstance(sources, list) and (bool(sources) if variant.get('status') == 'published' else True), f'{vid}: no sources')
    for item in sources if isinstance(sources, list) else []:
        url = item.get('url', '')
        host = urlparse(url)
        check(host.scheme == 'https' and bool(host.netloc), f'{vid}: invalid source URL')
        check(bool(item.get('name')), f'{vid}: missing source name')
        check(bool(re.fullmatch(r'\d{4}-\d{2}-\d{2}', item.get('accessed', ''))), f'{vid}: invalid accessed date')
    if spec and spec.get('fuel_economy_km_l') is not None:
        check(bool(spec.get('fuel_cycle')), f'{vid}: fuel-cycle required for consumption')

for name in ('index.html', 'explore.html', 'car.html', 'compare.html', 'about.html', 'css/style.css', 'js/app.js', 'AGENTS.md', 'README.md'):
    check((ROOT / name).is_file(), f'missing required file: {name}')

print(f'DRIVEBASE validation: {len(brands)} brands, {len(models)} models, {len(variants)} variants')
if errors:
    for message in errors:
        print('FAIL', message)
    sys.exit(1)
print('PASS: schema, unique IDs, references, source links and asset paths')
