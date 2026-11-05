"""Rebuild A's two datasets: python3 scripts/clean_a.py (pyproj, shapely)."""
from pathlib import Path
import csv, hashlib, html, json, math, re
from collections import Counter
from pyproj import Geod
from shapely.geometry import shape, Point

ROOT = Path(__file__).resolve().parents[1]
CORE = ['facility_type', 'facility_name', 'address', 'latitude', 'longitude']
GEOD = Geod(ellps='WGS84')

def text(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', ' ', s or ''))).strip()

def write(path, rows, fields):
    with (ROOT/path).open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
        w.writeheader(); w.writerows(rows)

def main():
    manifest = json.loads((ROOT/'data/source_manifest.json').read_text())
    polygons = [(f['properties']['district_name'], shape(f['geometry'])) for f in json.loads((ROOT/'data/source/districts_D.geojson').read_text())['features']]
    assert len(polygons) == 18 and all(p.is_valid for _,p in polygons)
    rows, issues, rejected, summary = [], [], [], []
    for src in manifest['sources']:
        short = src['short_code']; path = ROOT/'data/source'/f'{short}.csv'
        assert hashlib.sha256(path.read_bytes()).hexdigest() == src['english_sha256']
        with path.open(encoding='utf-8-sig') as f: raw = list(csv.DictReader(f))
        accepted = []; seen = set(); duplicates = invalid = 0
        for i,r in enumerate(raw,1):
            sid = f'{short}:{i}'
            name = text(r.get('NAME_EN')); address = text(r.get('ADDRESS_EN'))
            try:
                lon,lat = float(r['GeometryLongitude']),float(r['GeometryLatitude'])
                if not name or not all(map(math.isfinite,[lon,lat])) or not (113.8<=lon<=114.5 and 22.13<=lat<=22.57):
                    raise ValueError('Missing name or invalid/out-of-envelope coordinates')
            except (ValueError,KeyError) as e:
                invalid+=1; rejected.append({'source_id':sid,'reason':str(e),'source_row_json':json.dumps(r,ensure_ascii=False)}); continue
            # Remove only identical full source rows; near-duplicates remain reviewable.
            key = tuple(sorted(r.items()))
            if key in seen:
                duplicates+=1; rejected.append({'source_id':sid,'reason':'Identical full source row','source_row_json':json.dumps(r,ensure_ascii=False)}); continue
            seen.add(key)
            district = text(r.get('SEARCH01_EN')).upper().replace('CENTRAL AND WESTERN','CENTRAL & WESTERN')
            matches = sorted(n for n,p in polygons if p.covers(Point(lon,lat)))
            if len(matches)!=1 or district not in matches:
                issues.append({'source_id':sid,'issue':'DISTRICT_REVIEW','detail':f'Provider={district}; D polygons={matches}; retained, no guessed correction'})
            delta = ''
            try:
                delta = GEOD.inv(lon,lat,float(r['LONGITUDE']),float(r['LATITUDE']))[2]
                if not math.isfinite(delta): raise ValueError('Non-finite coordinate difference')
                if delta>5: issues.append({'source_id':sid,'issue':'COORDINATE_REVIEW','detail':f'Geometry vs attributes: {delta:.3f} m; source geometry retained'})
            except (ValueError,KeyError):
                issues.append({'source_id':sid,'issue':'ATTRIBUTE_COORDINATES_INVALID','detail':'Source geometry retained'})
            out = dict(facility_type={'badminton':'Badminton Court','basketball':'Basketball Court'}[short],facility_name=name,address=address,latitude=lat,longitude=lon,source_id=sid,source_district=district,spatial_district='; '.join(matches),coordinate_difference_m=delta,source_last_update=r.get('LASTUPDATE',''),source_dataset=src['dataset_id'])
            accepted.append(out)
        rows.extend(accepted)
        write(f'data/{short}_cleaned.csv',accepted,CORE+['source_id','source_district','spatial_district','coordinate_difference_m','source_last_update','source_dataset'])
        summary.append(dict(dataset=short,input_rows=len(raw),accepted_rows=len(accepted),duplicates_removed=duplicates,rejected_rows=invalid))
        assert len(raw)==len(accepted)+duplicates+invalid
    for key,count in Counter((r['facility_type'],r['facility_name'].casefold(),r['longitude'],r['latitude']) for r in rows).items():
        if count>1: issues.append({'source_id':'','issue':'POSSIBLE_DUPLICATE','detail':f'{key}: {count} records retained for review'})
    write('data/Facilities_A_handoff.csv',rows,CORE)
    write('results/cleaning_summary.csv',summary,list(summary[0]))
    write('results/quality_issues.csv',issues,['source_id','issue','detail'])
    write('results/rejected_rows.csv',rejected,['source_id','reason','source_row_json'])
    checks = {'input_hashes_verified':True,'row_accounting_verified':True,'source_ids_unique':len({r['source_id'] for r in rows})==len(rows),'accepted_records':len(rows),'issue_counts':dict(Counter(i['issue'] for i in issues)),'spatial_check_boundary':'D snapshot only; final C/B database validation pending'}
    assert checks['source_ids_unique']
    (ROOT/'results/validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps({'summary':summary,'validation':checks},indent=2))

if __name__ == '__main__': main()
