#!/usr/bin/env python3
"""Explicit, bounded opt-in internet refresh of research metadata; not a VOID runtime process.
No automatic polling, no source code modifications. JSON observations remain outside core.
Use --fixture to test offline; --network requires explicit command from operator.
"""
import argparse,csv,json,urllib.request,urllib.parse,urllib.error,time,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
SEED=ROOT/'01_SOURCE_CATALOG/sources_seed.tsv'
OUT=ROOT/'01_SOURCE_CATALOG/network_snapshots'
MAX_RESPONSE=128*1024

def normalized_metadata(record):
    msg=record.get('message',{})
    return {'DOI':str(msg.get('DOI','')).strip().lower(), 'title':(msg.get('title') or [''])[0],
            'published':msg.get('published',{}).get('date-parts',[]),
            'publisher':msg.get('publisher',''), 'container_title':(msg.get('container-title') or [''])[0],
            'reference_count':msg.get('reference-count',None)}

def online_request(doi):
    url='https://api.crossref.org/works/'+urllib.parse.quote(doi,safe='/')
    req=urllib.request.Request(url,headers={'User-Agent':'VOID-Research-Catalog/0.1 (manual review); accept application/json','Accept':'application/json'})
    with urllib.request.urlopen(req,timeout=12) as resp:
        assert resp.status==200
        raw=resp.read(MAX_RESPONSE+1)
        if len(raw)>MAX_RESPONSE: raise ValueError('response too large')
        return json.loads(raw.decode('utf-8'))

def refresh(use_network=False,fixture=None):
    if not use_network and fixture is None:
        raise ValueError('Refusing connection without --network; use --fixture to test offline')
    with SEED.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f,delimiter='\t'))
    OUT.mkdir(exist_ok=True)
    output=[]
    fixtures=json.loads(pathlib.Path(fixture).read_text()) if fixture else {}
    for row in rows:
        doi=row['doi']
        if not doi: continue
        if use_network:
            try: r=online_request(doi); status='fetched'
            except (urllib.error.URLError,TimeoutError,ValueError,json.JSONDecodeError) as exc:
                output.append({'id':row['id'],'doi':doi,'status':'failed','reason':str(exc)[:120]})
                continue
        else:
            if doi not in fixtures: continue
            r=fixtures[doi];status='fixture'
        data=normalized_metadata(r)
        if data['DOI']!=doi.lower():
            output.append({'id':row['id'],'doi':doi,'status':'mismatch'});continue
        output.append({'id':row['id'],'doi':doi,'status':status,'metadata':data})
    payload={'source':'Crossref public metadata API' if use_network else 'LOCAL TEST FIXTURE',
             'mode':'manual isolated scholarly metadata refresh; does not change primary citations',
             'items':output}
    content=json.dumps(payload,sort_keys=True,ensure_ascii=False,indent=2)+'\n'
    digest=hashlib.sha256(content.encode()).hexdigest()[:16]
    out=OUT/f'crossref_{digest}.json'
    out.write_text(content,encoding='utf-8')
    print(json.dumps({'snapshot':str(out),'items':len(output),'network_used':use_network}))
if __name__=='__main__':
    p=argparse.ArgumentParser(); group=p.add_mutually_exclusive_group(required=True)
    group.add_argument('--network',action='store_true',help='Operator explicitly authorizes public Crossref HTTP requests')
    group.add_argument('--fixture',help='Offline fixture JSON path')
    a=p.parse_args();refresh(use_network=a.network, fixture=a.fixture)
