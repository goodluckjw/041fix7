import xml.etree.ElementTree as ET
import re

def parse_law_xml(xml_data, keyword):
    tree = ET.ElementTree(ET.fromstring(xml_data))
    root = tree.getroot()

    def highlight(text):
        return text.replace(keyword, f'<span style="color:red;font-weight:bold;">{keyword}</span>')

    results = []
    for article in root.findall(".//조문단위"):
        article_number = article.findtext("조문번호", "")
        article_title = article.findtext("조문제목", "")
        full_title = f"제{article_number}조({article_title})" if article_title else f"제{article_number}조"

        if keyword in article.findtext("조문내용", ""):
            body = article.findtext("조문내용", "")
            results.append(f"<b>{highlight(full_title)}</b> {highlight(body)}")
            continue

        for clause in article.findall("항"):
            clause_text = clause.findtext("항내용", "")
            if keyword in clause_text:
                formatted = f"<b>{highlight(full_title)}</b> {highlight(clause_text)}"
                results.append(formatted)
            for sub in clause.findall("호"):
                sub_text = sub.findtext("호내용", "")
                if keyword in sub_text:
                    formatted = f"<b>{highlight(full_title)}</b><br>&nbsp;&nbsp;{highlight(sub_text)}"
                    results.append(formatted)
            for sub in clause.findall("목"):
                sub_text = sub.findtext("목내용", "")
                if keyword in sub_text:
                    formatted = f"<b>{highlight(full_title)}</b><br>&nbsp;&nbsp;&nbsp;&nbsp;- {highlight(sub_text)}"
                    results.append(formatted)
    return results