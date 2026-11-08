import unittest,re,sys,hashlib,subprocess,pathlib
W=pathlib.Path(__file__).resolve().parents[3];HERE=pathlib.Path(__file__).parent
OUT=W/'xhs/creators.html';SRC=HERE/'ai-creators-growth.src.html'
BASE=subprocess.run(['git','-C',str(W),'show','origin/main:xhs/creators.html'],capture_output=True,text=True).stdout
K=['lenny','shreyas','ali','swyx','levelsio','justinwelsh']
def strip(t):
    for k in K: t=re.sub(r'<h2 id="%s">.*?(?=<h2 id=")'%k,'',t,flags=re.S)
    t=t.replace('.tw{overflow-x:auto;max-width:100%}.tw table{min-width:40rem}\n','')
    return re.sub(r'<h2 id="sources">.*','',t,flags=re.S)
class T(unittest.TestCase):
    def setUp(s): s.t=OUT.read_text()
    def test_generated_from_copy(s):
        sys.path.insert(0,'/workspace/digests');import xhs_library as X
        X.CREATORS_SRC=SRC;X.CREATORS_OUT=pathlib.Path('/tmp/b4-regen.html');X.sync_creators()
        s.assertEqual(pathlib.Path('/tmp/b4-regen.html').read_text(),s.t)
    def test_ids_kept(s):
        for i in re.findall(r'id="([^"]+)"',BASE): s.assertIn(f'id="{i}"',s.t,i)
    def test_others_unchanged(s): s.assertEqual(strip(BASE),strip(s.t))
    def test_anchors(s):
        ids=set(re.findall(r'id="([^"]+)"',s.t))
        for h in re.findall(r'href="#([^"]+)"',s.t): s.assertIn(h,ids,h)
    def test_sections(s):
        for k in K:
            m=re.search(r'<h2 id="%s">(.*?)(?=<h2 id=")'%k,s.t,re.S).group(1)
            for need in [f'id="{k}-timeline"',f'id="{k}-inflect"',f'id="{k}-works"',f'id="{k}-audience"',f'id="{k}-success"','读者现在','内容指向','普通内容','语气与节奏','失败与边界','小红书未核',f'batch4/{k}-ledger.md']: s.assertIn(need,m,(k,need))
            for bad in ['爆款','已上线','CNBC Make It','growthinreverse','sidestack','passionfroot','2.834M','454.8k']: s.assertNotIn(bad,m.replace('CNBC、Growth In Reverse','').replace('Sidestack 目录',''),(k,bad))
    def test_x_ids_in_ledger(s):
        for k in K:
            m=re.search(r'<h2 id="%s">(.*?)(?=<h2 id=")'%k,s.t,re.S).group(1)
            led=(HERE/f'{k}-ledger.md').read_text()
            for i in re.findall(r'x\.com/\w+/status/(\d+)',m): s.assertIn(i,led,(k,i))
    def test_shared_source_untouched(s):
        s.assertEqual(hashlib.sha256(open('/workspace/money/ai-creators-growth.html','rb').read()).hexdigest()[:8],'9569e987')
if __name__=='__main__': unittest.main()
