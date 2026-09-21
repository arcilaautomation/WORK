"""Open_WOs_auto.xlsx: like Open_WOs_with_graph.xlsx, but the weekly table on Sheet1 reads the
dated blocks on the Totals page (A:B, D:E, G:H, ... every 3 columns) so the chart updates itself."""
import re, zipfile
from xml.sax.saxutils import escape
SRC, OUT = "Open_WOs_original.xlsm", "Open_WOs_tracker.xlsx"
NROWS = 26   # table rows pre-built (one per Totals block); more can be added with Tab in the last cell
zin = zipfile.ZipFile(SRC); parts = {n: zin.read(n) for n in zin.namelist()}; order = zin.namelist()
def get(n): return parts[n].decode('utf-8')
def put(n, t): parts[n] = t.encode('utf-8')
def sub1(t, pat, rep, flags=0):
    new, k = re.subn(pat, rep, t, count=1, flags=flags); assert k == 1, pat[:90]; return new
def drop(n): del parts[n]; order.remove(n)

for n in ('xl/worksheets/sheet3.xml','xl/worksheets/sheet4.xml','xl/worksheets/_rels/sheet3.xml.rels',
          'xl/worksheets/_rels/sheet4.xml.rels','xl/printerSettings/printerSettings3.bin','xl/printerSettings/printerSettings4.bin',
          'xl/calcChain.xml','xl/vbaProject.bin','xl/comments1.xml','xl/comments2.xml','xl/drawings/vmlDrawing1.vml','xl/drawings/vmlDrawing2.vml'):
    drop(n)
ct = get('[Content_Types].xml')
for part in ('/xl/worksheets/sheet3.xml','/xl/worksheets/sheet4.xml','/xl/comments1.xml','/xl/comments2.xml','/xl/calcChain.xml','/xl/vbaProject.bin'):
    ct = sub1(ct, rf'<Override PartName="{re.escape(part)}" ContentType="[^"]+"/>', '')
ct = sub1(ct, r'application/vnd.ms-excel.sheet.macroEnabled.main\+xml', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml')
put('[Content_Types].xml', ct)
rels = get('xl/_rels/workbook.xml.rels')
for rid in ('rId3','rId4','rId9','rId11'): rels = sub1(rels, rf'<Relationship Id="{rid}" [^>]+/>', '')
put('xl/_rels/workbook.xml.rels', rels)

# ---- formulas -------------------------------------------------------------------------
COLS = 'Totals!$A$1:$ZZ$1'
R = '(ROW()-ROW(WeeklyLog[[#Headers],[Week Of]]))'
BLK = f'_xlfn.AGGREGATE(15,6,COLUMN({COLS})/((MOD(COLUMN({COLS})-2,3)=0)*ISNUMBER({COLS})),{R})'
F = {
 'week': f'IFERROR(INDEX(Totals!$1:$1,{BLK}),"")',
 'bvrt': f'IFERROR(INDEX(Totals!$4:$4,{BLK}-1),"")',
 'bvpm': f'IFERROR(INDEX(Totals!$5:$5,{BLK}-1),"")',
 'bvt':  'IF(WeeklyLog[[#This Row],[Week Of]]="","",WeeklyLog[[#This Row],[Burnsville Repair Tickets]]+WeeklyLog[[#This Row],[Burnsville PMs]])',
 'lvrt': f'IFERROR(INDEX(Totals!$9:$9,{BLK}-1),"")',
 'lvpm': f'IFERROR(INDEX(Totals!$10:$10,{BLK}-1),"")',
 'lvt':  'IF(WeeklyLog[[#This Row],[Week Of]]="","",WeeklyLog[[#This Row],[Lakeville Repair Tickets]]+WeeklyLog[[#This Row],[Lakeville PMs]])',
 'co':   'IF(WeeklyLog[[#This Row],[Week Of]]="","",WeeklyLog[[#This Row],[Burnsville Total]]+WeeklyLog[[#This Row],[Lakeville Total]])',
 'chg':  'IFERROR(WeeklyLog[[#This Row],[Combined Total]]-OFFSET(WeeklyLog[[#This Row],[Combined Total]],-1,0),"")',
}
N = 'MAX(1,COUNT(WeeklyLog[Week Of]))'
NAMES = {
 'chart_Week': f'INDEX(WeeklyLog[Week Of],1):INDEX(WeeklyLog[Week Of],{N})',
 'chart_BV':   f'INDEX(WeeklyLog[Burnsville Total],1):INDEX(WeeklyLog[Burnsville Total],{N})',
 'chart_LV':   f'INDEX(WeeklyLog[Lakeville Total],1):INDEX(WeeklyLog[Lakeville Total],{N})',
 'chart_CO':   f'INDEX(WeeklyLog[Combined Total],1):INDEX(WeeklyLog[Combined Total],{N})',
 'last_BV':    'IF(Sheet1!chart_Week=MAX(Sheet1!chart_Week),Sheet1!chart_BV,NA())',
 'last_LV':    'IF(Sheet1!chart_Week=MAX(Sheet1!chart_Week),Sheet1!chart_LV,NA())',
 'last_CO':    'IF(Sheet1!chart_Week=MAX(Sheet1!chart_Week),Sheet1!chart_CO,NA())',
}

# ---- workbook.xml ---------------------------------------------------------------------
wb = get('xl/workbook.xml')
wb = sub1(wb, r'<sheets>.*?</sheets>', '<sheets><sheet name="Sheet1" sheetId="17" r:id="rId2"/><sheet name="Totals" sheetId="2" r:id="rId1"/></sheets>', flags=re.S)
dn = ''.join(f'<definedName name="{k}" localSheetId="0">{escape(v)}</definedName>' for k, v in NAMES.items())
wb = sub1(wb, r'<definedNames>.*?</definedNames>', f'<definedNames>{dn}</definedNames>', flags=re.S)
wb = sub1(wb, r'<workbookView ', '<workbookView activeTab="1" ')
wb = sub1(wb, r'<workbookPr codeName="ThisWorkbook" ', '<workbookPr ')
wb = sub1(wb, r' codeName="\{[0-9A-F-]+\}"', '')
wb = sub1(wb, r'<mc:AlternateContent xmlns:mc="[^"]+"><mc:Choice Requires="x15"><x15ac:absPath[^>]+/></mc:Choice></mc:AlternateContent>', '')
wb = sub1(wb, r'<calcPr calcId="191029"/>', '<calcPr calcId="191029" fullCalcOnLoad="1"/>')
put('xl/workbook.xml', wb)

# ---- Totals: the user's values (as in the file they uploaded on 2026-09-21) ------------
s1 = get('xl/worksheets/sheet1.xml')
s1 = sub1(s1, r'<sheetPr codeName="Sheet1"/>', '<sheetPr/>')
s1 = sub1(s1, r'<selection activeCell="H19" sqref="H19"/>', '<selection activeCell="A1" sqref="A1"/>')
s1 = sub1(s1, r'<c r="D3" s="42"/>', '<c r="D3" s="42" t="s"><v>1</v></c>')
s1 = sub1(s1, r'<c r="D4" s="5"><v>6</v></c>', '<c r="D4" s="5"><v>7</v></c>')
s1 = sub1(s1, r'<c r="D10" s="5"><v>240</v></c>', '<c r="D10" s="5"><v>241</v></c>')
s1 = sub1(s1, r'<c r="D6" s="5"><f>SUM\(D4\+D5\)</f><v>12</v></c>', '<c r="D6" s="5"><f>SUM(D4+D5)</f><v>13</v></c>')
s1 = sub1(s1, r'<c r="A11" s="5"><v>205</v></c>', '<c r="A11" s="5"><f>SUM(A9+A10)</f><v>205</v></c>')
s1 = sub1(s1, r'<c r="D11" s="5"><f>SUM\(D9\+D10\)</f><v>278</v></c>', '<c r="D11" s="5"><f>SUM(D9+D10)</f><v>279</v></c>')
s1 = sub1(s1, r'<c r="D14" s="5"><f>SUM\(D6\+D11\)</f><v>290</v></c>', '<c r="D14" s="5"><f>SUM(D6+D11)</f><v>292</v></c>')
s1 = sub1(s1, r'<conditionalFormatting sqref="A16">.*?<conditionalFormatting sqref="M16">.*?</conditionalFormatting>', '', flags=re.S)
s1 = sub1(s1, r'<legacyDrawing r:id="rId2"/>', '')
put('xl/worksheets/sheet1.xml', s1)
r1 = get('xl/worksheets/_rels/sheet1.xml.rels')
r1 = sub1(r1, r'<Relationship Id="rId3" [^>]+/>', ''); r1 = sub1(r1, r'<Relationship Id="rId2" [^>]+/>', '')
put('xl/worksheets/_rels/sheet1.xml.rels', r1)

# ---- Sheet1 (chart page): table rows are formulas over the Totals blocks ---------------
known = {1: (46280, 11, 3, 14, 32, 173, 205, 219, ''), 2: (46286, 7, 6, 13, 38, 241, 279, 292, 73)}
def cell(ref, s, f, v, ca=False):
    fa = ' ca="1"' if ca else ''
    if v == '': return f'<c r="{ref}" s="{s}" t="str"><f{fa}>{escape(f)}</f><v></v></c>'
    return f'<c r="{ref}" s="{s}"><f{fa}>{escape(f)}</f><v>{v}</v></c>'
rows = []
for i in range(1, NROWS + 1):
    r = 21 + i
    v = known.get(i, ('',)*9)
    rows.append('<row r="%d">' % r +
        cell(f'A{r}', 39, F['week'], v[0]) + cell(f'B{r}', 38, F['bvrt'], v[1]) + cell(f'C{r}', 38, F['bvpm'], v[2]) +
        cell(f'D{r}', 40, F['bvt'], v[3]) + cell(f'E{r}', 38, F['lvrt'], v[4]) + cell(f'F{r}', 38, F['lvpm'], v[5]) +
        cell(f'G{r}', 40, F['lvt'], v[6]) + cell(f'H{r}', 40, F['co'], v[7]) + cell(f'I{r}', 41, F['chg'], v[8], ca=True) + '</row>')
last = 21 + NROWS
s2 = get('xl/worksheets/sheet2.xml')
s2 = sub1(s2, r'<dimension ref="A1:I22"/>', f'<dimension ref="A1:I{last}"/>')
s2 = sub1(s2, r'<row r="2" spans="1:1" x14ac:dyDescent="0.25"><c r="A2" s="33"/></row>',
          '<row r="2" spans="1:1" x14ac:dyDescent="0.25"><c r="A2" s="33" t="inlineStr"><is><t>Updates by itself from the Totals page: each dated block there (every 3 columns: A, D, G, J, M ...) is one week.</t></is></c></row>')
s2 = sub1(s2, r'<row r="22" .*?</row></sheetData>', ''.join(rows) + '</sheetData>', flags=re.S)
s2 = sub1(s2, r'<conditionalFormatting sqref="I22">', '<conditionalFormatting sqref="I22:I1000">')
s2 = sub1(s2, r'<legacyDrawing r:id="rId3"/>', '')
put('xl/worksheets/sheet2.xml', s2)
r2 = get('xl/worksheets/_rels/sheet2.xml.rels')
r2 = sub1(r2, r'<Relationship Id="rId3" [^>]+/>', ''); r2 = sub1(r2, r'<Relationship Id="rId5" [^>]+/>', '')
put('xl/worksheets/_rels/sheet2.xml.rels', r2)

t1 = get('xl/tables/table1.xml').replace('ref="A21:I22"', f'ref="A21:I{last}"'); assert t1.count(f'ref="A21:I{last}"') == 2
colf = [('Week Of','week'),('Burnsville Repair Tickets','bvrt'),('Burnsville PMs','bvpm'),('Burnsville Total','bvt'),
        ('Lakeville Repair Tickets','lvrt'),('Lakeville PMs','lvpm'),('Lakeville Total','lvt'),('Combined Total','co'),('Change vs Last Week','chg')]
for name, key in colf:
    t1 = sub1(t1, rf'(<tableColumn id="\d+" xr3:uid="[^"]+" name="{re.escape(name)}" dataDxfId="\d+")(?:/>|>.*?</tableColumn>)',
              lambda m: m.group(1) + '><calculatedColumnFormula>' + escape(F[key]) + '</calculatedColumnFormula></tableColumn>', flags=re.S)
put('xl/tables/table1.xml', t1)

# ---- chart: refs to the renamed sheet, caches with both weeks --------------------------
ch = get('xl/charts/chart1.xml').replace("'Weekly History'!", 'Sheet1!'); assert ch.count('Sheet1!') == 12
sers = ch.split('<c:ser>'); vals = [13, 279, 292, 13, 279, 292]
for i in range(1, 7):
    s = sub1(sers[i], r'<c:ptCount val="1"/><c:pt idx="0"><c:v>46280</c:v></c:pt>',
             '<c:ptCount val="2"/><c:pt idx="0"><c:v>46280</c:v></c:pt><c:pt idx="1"><c:v>46286</c:v></c:pt>')
    if i <= 3: s = sub1(s, r'(<c:formatCode>#,##0</c:formatCode>)<c:ptCount val="1"/>(<c:pt idx="0"><c:v>\d+</c:v></c:pt>)', r'\1<c:ptCount val="2"/>\2' + f'<c:pt idx="1"><c:v>{vals[i-1]}</c:v></c:pt>')
    else:      s = sub1(s, r'(<c:formatCode>#,##0</c:formatCode>)<c:ptCount val="1"/><c:pt idx="0"><c:v>\d+</c:v></c:pt>', r'\1<c:ptCount val="2"/>' + f'<c:pt idx="1"><c:v>{vals[i-1]}</c:v></c:pt>')
    sers[i] = s
put('xl/charts/chart1.xml', '<c:ser>'.join(sers))

app = get('docProps/app.xml')
app = sub1(app, r'<HeadingPairs>.*?</TitlesOfParts>',
  '<HeadingPairs><vt:vector size="4" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>2</vt:i4></vt:variant>'
  '<vt:variant><vt:lpstr>Named Ranges</vt:lpstr></vt:variant><vt:variant><vt:i4>4</vt:i4></vt:variant></vt:vector></HeadingPairs>'
  '<TitlesOfParts><vt:vector size="6" baseType="lpstr"><vt:lpstr>Sheet1</vt:lpstr><vt:lpstr>Totals</vt:lpstr>'
  '<vt:lpstr>Sheet1!chart_BV</vt:lpstr><vt:lpstr>Sheet1!chart_CO</vt:lpstr><vt:lpstr>Sheet1!chart_LV</vt:lpstr><vt:lpstr>Sheet1!chart_Week</vt:lpstr></vt:vector></TitlesOfParts>', flags=re.S)
put('docProps/app.xml', app)


# ---- Totals: third block in G:H, yellow-when-empty input cells, weekly note, no stray M:N block ----
s1 = get('xl/worksheets/sheet1.xml')
s1 = re.sub(r'<c r="[MN]\d+"[^>]*/>', '', s1)                       # drop the header-only block in M:N
s1 = re.sub(r'<c r="[MN]\d+"[^>]*>.*?</c>', '', s1, flags=re.S)
s1 = re.sub(r' spans="[^"]+"', '', s1)
def add(row, cells):
    global s1
    s1 = sub1(s1, rf'(<row r="{row}"[^>]*>.*?)(</row>)', lambda m: m.group(1) + cells + m.group(2), flags=re.S)
add(1,  '<c r="G1" s="7" t="s"><v>0</v></c><c r="H1" s="8"/>')
add(2,  '<c r="G2" s="16"/><c r="H2" s="17"/>')
add(3,  '<c r="G3" s="42" t="s"><v>1</v></c><c r="H3" s="42"/>')
add(4,  '<c r="G4" s="5"/><c r="H4" s="6" t="s"><v>2</v></c>')
add(5,  '<c r="G5" s="5"/><c r="H5" s="6" t="s"><v>3</v></c>')
add(6,  '<c r="G6" s="5"><f>SUM(G4+G5)</f><v>0</v></c><c r="H6" s="6" t="s"><v>4</v></c>')
add(8,  '<c r="G8" s="43" t="s"><v>5</v></c><c r="H8" s="43"/>')
add(9,  '<c r="G9" s="5"/><c r="H9" s="6" t="s"><v>2</v></c>')
add(10, '<c r="G10" s="5"/><c r="H10" s="6" t="s"><v>3</v></c>')
add(11, '<c r="G11" s="5"><f>SUM(G9+G10)</f><v>0</v></c><c r="H11" s="6" t="s"><v>4</v></c>')
add(13, '<c r="G13" s="44" t="s"><v>6</v></c><c r="H13" s="44"/>')
add(14, '<c r="G14" s="5"><f>SUM(G6+G11)</f><v>0</v></c><c r="H14" s="6" t="s"><v>7</v></c>')
note1 = "Yellow cells = type this week's numbers here, from Aptean EAM > Open Work Orders: the date, then repair tickets and PMs for each plant."
note2 = "Next week: copy the newest block (for example G1:H14), paste it 3 columns to the right (J1), and fill in the yellow cells. The chart on Sheet1 updates by itself."
s1 = sub1(s1, r'<row r="16"[^>]*>.*?</row>', f'<row r="16"><c r="A16" s="31" t="inlineStr"><is><t>{escape(note1)}</t></is></c></row>', flags=re.S)
s1 = sub1(s1, r'<row r="17"[^>]*>.*?</row>', f'<row r="17"><c r="A17" s="31" t="inlineStr"><is><t>{escape(note2)}</t></is></c></row>', flags=re.S)
s1 = re.sub(r'<row r="(1[89]|2[01])"[^>]*>.*?</row>', '', s1, flags=re.S)
s1 = sub1(s1, r'<dimension ref="A1:N21"/>', '<dimension ref="A1:H17"/>')
cols = ['<col min="1" max="1" width="10.7109375" style="3" customWidth="1"/>', '<col min="2" max="2" width="35.140625" style="4" customWidth="1"/>']
for c in range(3, 91):   # label column of every block (E, H, K, ...) gets the same width as E
    w = '27' if c % 3 == 2 else '9.140625'
    cols.append(f'<col min="{c}" max="{c}" width="{w}" style="4" customWidth="1"/>')
cols.append('<col min="91" max="16384" width="9.140625" style="4"/>')
s1 = sub1(s1, r'<cols>.*?</cols>', '<cols>' + ''.join(cols) + '</cols>', flags=re.S)
s1 = sub1(s1, r'<mergeCells count="9">.*?</mergeCells>',
    '<mergeCells count="9">' + ''.join(f'<mergeCell ref="{m}"/>' for m in ('A3:B3','A8:B8','A13:B13','D3:E3','D8:E8','D13:E13','G3:H3','G8:H8','G13:H13')) + '</mergeCells>', flags=re.S)
cf = ('<conditionalFormatting sqref="A1:ZZ1"><cfRule type="expression" dxfId="18" priority="1"><formula>AND(ISBLANK(A1),MOD(COLUMN(A1)-2,3)=0,INDEX($3:$3,1,COLUMN(A1)-1)&lt;&gt;"")</formula></cfRule></conditionalFormatting>'
      '<conditionalFormatting sqref="A4:ZZ5"><cfRule type="expression" dxfId="18" priority="2"><formula>AND(ISBLANK(A4),MOD(COLUMN(A4)-1,3)=0,INDEX($3:$3,1,COLUMN(A4))&lt;&gt;"")</formula></cfRule></conditionalFormatting>'
      '<conditionalFormatting sqref="A9:ZZ10"><cfRule type="expression" dxfId="18" priority="3"><formula>AND(ISBLANK(A9),MOD(COLUMN(A9)-1,3)=0,INDEX($3:$3,1,COLUMN(A9))&lt;&gt;"")</formula></cfRule></conditionalFormatting>')
s1 = sub1(s1, r'</mergeCells>', '</mergeCells>' + cf)
put('xl/worksheets/sheet1.xml', s1)
st = get('xl/styles.xml')
st = sub1(st, r'<dxfs count="18">', '<dxfs count="19">')
st = sub1(st, r'</dxfs>', '<dxf><fill><patternFill><bgColor rgb="FFFFFF00"/></patternFill></fill></dxf></dxfs>')
put('xl/styles.xml', st)

# ---- prune unused shared strings, write -------------------------------------------------
ss = get('xl/sharedStrings.xml'); head, body = ss.split('<sst', 1); body = '<sst' + body
items = re.findall(r'<si>.*?</si>', body, flags=re.S)
pat = re.compile(r'(<c r="[A-Z]+\d+"(?: s="\d+")? t="s"><v>)(\d+)(</v></c>)')
sheets = ['xl/worksheets/sheet1.xml', 'xl/worksheets/sheet2.xml']
used = sorted({int(m.group(2)) for sh in sheets for m in pat.finditer(get(sh))}); remap = {o: n for n, o in enumerate(used)}
for sh in sheets: put(sh, pat.sub(lambda m: m.group(1) + str(remap[int(m.group(2))]) + m.group(3), get(sh)))
sst_open = re.match(r'<sst[^>]*>', body).group(0)
sst_open = re.sub(r'count="\d+"', f'count="{len(used)}"', sst_open); sst_open = re.sub(r'uniqueCount="\d+"', f'uniqueCount="{len(used)}"', sst_open)
put('xl/sharedStrings.xml', head + sst_open + ''.join(items[i] for i in used) + '</sst>')
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in ['[Content_Types].xml'] + [n for n in order if n != '[Content_Types].xml']: z.writestr(n, parts[n])
print('wrote', OUT)
