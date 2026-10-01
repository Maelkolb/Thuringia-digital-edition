"""Layout/data audit of the raw Gemini extraction (no re-extraction)."""
import json, glob, re, collections, statistics, os
pages = {}
for f in glob.glob('source/json_batch1/*.json') + glob.glob('source/json_batch2/*.json'):
    d = json.load(open(f, encoding='utf-8'))
    st = d['structure']
    if 'content_blocks' not in st:
        bl = [{'block_type': 'paragraph', 'content': x} for x in st.pop('body_paragraphs', [])]
        bl += [{'block_type': 'table', 'content': t} for t in st.pop('tables', [])]
        st['content_blocks'] = bl
    pages[d['page_number']] = d
P = sorted(pages)
issues = collections.defaultdict(list)
hdr_counter = collections.Counter(p['structure']['header'] for p in pages.values() if p['structure']['header'])
def txt(b):
    c = b['content']
    if isinstance(c, str): return c
    if isinstance(c, list): return '\n'.join(map(str, c))
    return '\n'.join(' | '.join(map(str, r)) for r in c.get('cells', []))
for pn in P:
    s = pages[pn]['structure']; blocks = s['content_blocks']
    if not blocks: issues['empty_page'].append(pn); continue
    total = sum(len(txt(b)) for b in blocks)
    if total < 400: issues['short_page(<400ch)'].append((pn, total))
    b0 = blocks[0]
    # running header leaked into first block
    if b0['block_type'] == 'heading' and isinstance(b0['content'], str) and hdr_counter.get(b0['content'].strip(), 0) >= 3:
        issues['first_heading_equals_a_running_header'].append((pn, b0['content'][:50]))
    if s['header'] and isinstance(b0['content'], str) and b0['content'].strip() == s['header'].strip():
        issues['header_duplicated_in_blocks'].append(pn)
    if isinstance(b0['content'], str) and re.match(r'^\d{1,3}\s', b0['content']) and b0['block_type'] == 'paragraph':
        issues['paragraph_starts_with_number(page no?)'].append((pn, b0['content'][:40]))
    for b in blocks:
        t = txt(b)
        if b['block_type'] == 'heading' and len(t) > 160: issues['overlong_heading'].append((pn, t[:60]))
        if b['block_type'] == 'paragraph' and len(t) < 70 and re.match(r'^([IVX]+\.|\d+\)|\d+\.|[a-z]\))\s+\S', t) and t.rstrip().endswith('.'):
            issues['short_numbered_paragraph(heading?)'].append((pn, t[:70]))
        if b['block_type'] in ('paragraph',):
            if re.search(r'\b(\w\s){4,}\w\b', t): issues['letterspaced_word'].append((pn, re.search(r'\b(\w\s){4,}\w\b', t).group(0)))
            for m in re.finditer(r'(\w{2,})[-¬] (\w+)', t):
                if m.group(2)[0].islower() and m.group(2) not in ('und', 'oder', 'bis', 'u.', 'resp.', 'wie', 'sowie'):
                    issues['inline_linebreak_hyphen'].append((pn, m.group(0))); break
            # repetition loops
            sents = re.split(r'(?<=[.;!?])\s+', t)
            cnt = collections.Counter(x for x in sents if len(x) > 40)
            if cnt and cnt.most_common(1)[0][1] >= 3: issues['repetition_loop'].append((pn, cnt.most_common(1)[0][0][:60]))
        if b['block_type'] == 'table':
            c = b['content']; cells = c.get('cells', [])
            if not cells: issues['empty_table'].append(pn); continue
            lens = [len(r) for r in cells]
            if len(set(lens)) > 1: issues['ragged_table'].append((pn, collections.Counter(lens).most_common(3)))
            if c.get('rows') != len(cells) or c.get('cols') != max(lens): issues['table_dims_mismatch'].append((pn, c.get('rows'), len(cells), c.get('cols'), max(lens)))
            if max(lens) == 1: issues['single_column_table'].append(pn)
            emptycols = [j for j in range(max(lens)) if all((j >= len(r) or not str(r[j]).strip()) for r in cells)]
            if emptycols: issues['table_empty_columns'].append((pn, emptycols))
            row0 = cells[0]; num0 = sum(bool(re.search(r'\d', str(x))) for x in row0)
            if num0 >= max(1, len(row0) // 2): issues['table_first_row_is_data(rendered as th)'].append(pn)
            if c.get('caption'): issues['table_has_caption'].append(pn)
    # continuation
    last = blocks[-1]
    if last['block_type'] == 'paragraph' and isinstance(last['content'], str):
        if last['content'].rstrip().endswith(('-', '¬')): issues['page_ends_with_hyphen'].append(pn)
        elif not re.search(r'[.!?:;)"“]$', last['content'].rstrip()): issues['page_ends_midsentence'].append(pn)
    if b0['block_type'] == 'paragraph' and isinstance(b0['content'], str) and b0['content'][:1].islower():
        issues['page_starts_lowercase(continuation)'].append(pn)
    # footnotes
    fns = s.get('footnotes', [])
    body = ' '.join(txt(b) for b in blocks)
    for fn in fns:
        mk = (fn.get('marker') or '').strip()
        if mk and mk not in body: issues['footnote_marker_not_in_body'].append((pn, mk))
    for mk in set(re.findall(r'\*{1,3}\)|\d\)', body)):
        pass
    if re.search(r'\*\)', body) and not fns: issues['marker_in_body_but_no_footnotes'].append(pn)
    if s['page_number_printed'] and str(s['page_number_printed']).strip() != str(pn): issues['printed_no_mismatch'].append((pn, s['page_number_printed']))
    if not s['header']: issues['no_running_header'].append(pn)
print('pages', len(P), 'running headers distinct', len(hdr_counter))
for k, v in sorted(issues.items(), key=lambda kv: -len(kv[1])):
    print(f'{k:45s} {len(v):5d}  e.g. {v[:6]}')
json.dump({k: v for k, v in issues.items()}, open('audit/data_issues.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
