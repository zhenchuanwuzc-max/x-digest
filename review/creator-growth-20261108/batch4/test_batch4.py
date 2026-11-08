"""batch4 内容核对（2026-11-08 起六人已拆为 xhs/{id}.html；结构/兼容/生成一致性见 xhs/growth/src/test_growth.py）。"""
import unittest, re, pathlib
W = pathlib.Path(__file__).resolve().parents[3]; HERE = pathlib.Path(__file__).parent
K = ['lenny', 'shreyas', 'ali', 'swyx', 'levelsio', 'justinwelsh']
def sec(k):
    t = (W/f'xhs/{k}.html').read_text()
    return re.search(r'<h2 id="%s">(.*?)(?=<p class="foot">)' % k, t, re.S).group(1)
class T(unittest.TestCase):
    def test_sections(s):
        for k in K:
            m = sec(k)
            for need in [f'id="{k}-timeline"', f'id="{k}-inflect"', f'id="{k}-works"', f'id="{k}-audience"', f'id="{k}-success"', '读者现在', '内容指向', '普通内容', '语气与节奏', '失败与边界', '小红书未核', f'batch4/{k}-ledger.md']: s.assertIn(need, m, (k, need))
            for bad in ['爆款', '已上线', 'CNBC Make It', 'growthinreverse', 'sidestack', 'passionfroot', '2.834M', '454.8k']: s.assertNotIn(bad, m.replace('CNBC、Growth In Reverse', '').replace('Sidestack 目录', ''), (k, bad))
    def test_x_ids_in_ledger(s):
        for k in K:
            led = (HERE/f'{k}-ledger.md').read_text()
            for i in re.findall(r'x\.com/\w+/status/(\d+)', sec(k)): s.assertIn(i, led, (k, i))
if __name__ == '__main__': unittest.main()
