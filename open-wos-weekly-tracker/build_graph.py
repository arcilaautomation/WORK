"""Build Open_WOs_with_graph.xlsx: Sheet1 = the weekly-history chart page (transplanted from the
original workbook's 'Weekly History' sheet), Totals = the user's page with the values they typed."""
import re, zipfile
from xml.sax.saxutils import escape

SRC, OUT = 'Open_WOs_original.xlsm', 'Open_WOs_with_graph.xlsx'
zin = zipfile.ZipFile(SRC)
parts = {n: zin.read(n) for n in zin.namelist()}
order = zin.namelist()
def get(n): return parts[n].decode('utf-8')
def put(n, t): parts[n] = t.encode('utf-8')
def sub1(t, pat, rep, flags=0):
    new, k = re.subn(pat, rep, t, count=1, flags=flags); assert k == 1, pat[:90]; return new
def drop(n):
    del parts[n]; order.remove(n)

# ---- remove what is not wanted: Calculation, Directions, VBA, comments, calcChain
for n in ('xl/worksheets/sheet3.xml', 'xl/worksheets/sheet4.xml', 'xl/worksheets/_rels/sheet3.xml.rels',
          'xl/worksheets/_rels/sheet4.xml.rels', 'xl/printerSettings/printerSettings3.bin',
          'xl/printerSettings/printerSettings4.bin', 'xl/calcChain.xml', 'xl/vbaProject.bin',
          'xl/comments1.xml', 'xl/comments2.xml', 'xl/drawings/vmlDrawing1.vml', 'xl/drawings/vmlDrawing2.vml'):
    drop(n)

ct = get('[Content_Types].xml')
for part in ('/xl/worksheets/sheet3.xml', '/xl/worksheets/sheet4.xml', '/xl/comments1.xml',
             '/xl/comments2.xml', '/xl/calcChain.xml', '/xl/vbaProject.bin'):
    ct = sub1(ct, rf'<Override PartName="{re.escape(part)}" ContentType="[^"]+"/>', '')
ct = sub1(ct, r'application/vnd.ms-excel.sheet.macroEnabled.main\+xml',
          'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml')
put('[Content_Types].xml', ct)

rels = get('xl/_rels/workbook.xml.rels')
for rid in ('rId3', 'rId4', 'rId9', 'rId11'):
    rels = sub1(rels, rf'<Relationship Id="{rid}" [^>]+/>', '')
put('xl/_rels/workbook.xml.rels', rels)

# ---- workbook.xml: Sheet1 (chart page) first, Totals second and active; names rescoped
wb = get('xl/workbook.xml')
wb = sub1(wb, r'<sheets>.*?</sheets>',
          '<sheets><sheet name="Sheet1" sheetId="17" r:id="rId2"/><sheet name="Totals" sheetId="2" r:id="rId1"/></sheets>', flags=re.S)
wb = sub1(wb, r'<definedName name="_xlnm._FilterDatabase"[^>]*>[^<]*</definedName>', '')
wb = sub1(wb, r'<definedName name="_xleta.SUM"[^>]*>[^<]*</definedName>', '')
wb = wb.replace('localSheetId="1"', 'localSheetId="0"'); assert wb.count('localSheetId="0"') == 7
wb = sub1(wb, r'<workbookView ', '<workbookView activeTab="1" ')
wb = sub1(wb, r'<workbookPr codeName="ThisWorkbook" ', '<workbookPr ')
wb = sub1(wb, r' codeName="\{[0-9A-F-]+\}"', '')
wb = sub1(wb, r'<mc:AlternateContent xmlns:mc="[^"]+"><mc:Choice Requires="x15"><x15ac:absPath[^>]+/></mc:Choice></mc:AlternateContent>', '')
wb = sub1(wb, r'<calcPr calcId="191029"/>', '<calcPr calcId="191029" fullCalcOnLoad="1"/>')
put('xl/workbook.xml', wb)

# ---- Totals (sheet1.xml): user's typed values, no comments, no broken formats
s1 = get('xl/worksheets/sheet1.xml')
s1 = sub1(s1, r'<sheetPr codeName="Sheet1"/>', '<sheetPr/>')
s1 = sub1(s1, r'<selection activeCell="H19" sqref="H19"/>', '<selection activeCell="A1" sqref="A1"/>')
s1 = sub1(s1, r'<c r="D3" s="42"/>', '<c r="D3" s="42" t="s"><v>1</v></c>')                # BURNSVILLE header
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

# ---- Sheet1 (former Weekly History, sheet2.xml): add the 9/21 row with the user's numbers
row23 = ('<row r="23"><c r="A23" s="39"><v>46286</v></c><c r="B23" s="38"><v>7</v></c><c r="C23" s="38"><v>6</v></c>'
 '<c r="D23" s="40"><f>WeeklyLog[[#This Row],[Burnsville Repair Tickets]]+WeeklyLog[[#This Row],[Burnsville PMs]]</f><v>13</v></c>'
 '<c r="E23" s="38"><v>38</v></c><c r="F23" s="38"><v>241</v></c>'
 '<c r="G23" s="40"><f>WeeklyLog[[#This Row],[Lakeville Repair Tickets]]+WeeklyLog[[#This Row],[Lakeville PMs]]</f><v>279</v></c>'
 '<c r="H23" s="40"><f>WeeklyLog[[#This Row],[Burnsville Total]]+WeeklyLog[[#This Row],[Lakeville Total]]</f><v>292</v></c>'
 '<c r="I23" s="41"><f ca="1">IFERROR(WeeklyLog[[#This Row],[Combined Total]]-OFFSET(WeeklyLog[[#This Row],[Combined Total]],-1,0),"")</f><v>73</v></c></row>')
s2 = get('xl/worksheets/sheet2.xml')
s2 = sub1(s2, r'<dimension ref="A1:I22"/>', '<dimension ref="A1:I23"/>')
s2 = sub1(s2, r'</row></sheetData>', '</row>' + row23 + '</sheetData>')
s2 = sub1(s2, r'<conditionalFormatting sqref="I22">', '<conditionalFormatting sqref="I22:I1000">')
s2 = sub1(s2, r'<legacyDrawing r:id="rId3"/>', '')
put('xl/worksheets/sheet2.xml', s2)
r2 = get('xl/worksheets/_rels/sheet2.xml.rels')
r2 = sub1(r2, r'<Relationship Id="rId3" [^>]+/>', ''); r2 = sub1(r2, r'<Relationship Id="rId5" [^>]+/>', '')
put('xl/worksheets/_rels/sheet2.xml.rels', r2)
t1 = get('xl/tables/table1.xml').replace('ref="A21:I22"', 'ref="A21:I23"'); assert t1.count('ref="A21:I23"') == 2
put('xl/tables/table1.xml', t1)

# ---- chart: point at the renamed sheet, refresh the cached points
ch = get('xl/charts/chart1.xml').replace("'Weekly History'!", 'Sheet1!'); assert ch.count('Sheet1!') == 12
sers = ch.split('<c:ser>'); assert len(sers) == 7
vals = [13, 279, 292, 13, 279, 292]
for i in range(1, 7):
    s = sub1(sers[i], r'<c:ptCount val="1"/><c:pt idx="0"><c:v>46280</c:v></c:pt>',
             '<c:ptCount val="2"/><c:pt idx="0"><c:v>46280</c:v></c:pt><c:pt idx="1"><c:v>46286</c:v></c:pt>')
    if i <= 3:
        s = sub1(s, r'(<c:formatCode>#,##0</c:formatCode>)<c:ptCount val="1"/>(<c:pt idx="0"><c:v>\d+</c:v></c:pt>)',
                 r'\1<c:ptCount val="2"/>\2' + f'<c:pt idx="1"><c:v>{vals[i-1]}</c:v></c:pt>')
    else:
        s = sub1(s, r'(<c:formatCode>#,##0</c:formatCode>)<c:ptCount val="1"/><c:pt idx="0"><c:v>\d+</c:v></c:pt>',
                 r'\1<c:ptCount val="2"/>' + f'<c:pt idx="1"><c:v>{vals[i-1]}</c:v></c:pt>')
    sers[i] = s
put('xl/charts/chart1.xml', '<c:ser>'.join(sers))

# ---- docProps/app.xml
app = get('docProps/app.xml')
app = sub1(app, r'<HeadingPairs>.*?</TitlesOfParts>',
  '<HeadingPairs><vt:vector size="4" baseType="variant"><vt:variant><vt:lpstr>Worksheets</vt:lpstr></vt:variant><vt:variant><vt:i4>2</vt:i4></vt:variant>'
  '<vt:variant><vt:lpstr>Named Ranges</vt:lpstr></vt:variant><vt:variant><vt:i4>4</vt:i4></vt:variant></vt:vector></HeadingPairs>'
  '<TitlesOfParts><vt:vector size="6" baseType="lpstr"><vt:lpstr>Sheet1</vt:lpstr><vt:lpstr>Totals</vt:lpstr>'
  "<vt:lpstr>Sheet1!chart_BV</vt:lpstr><vt:lpstr>Sheet1!chart_CO</vt:lpstr><vt:lpstr>Sheet1!chart_LV</vt:lpstr><vt:lpstr>Sheet1!chart_Week</vt:lpstr></vt:vector></TitlesOfParts>", flags=re.S)
put('docProps/app.xml', app)

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for n in ['[Content_Types].xml'] + [n for n in order if n != '[Content_Types].xml']:
        z.writestr(n, parts[n])
print('wrote', OUT, len(order), 'parts')
