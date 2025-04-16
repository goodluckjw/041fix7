import requests

def fetch_law_list(keyword):
    url = f"http://www.law.go.kr/DRF/lawSearch.do?OC=chetera&target=law&type=XML&display=100&search=2&knd=A0002&query={keyword}"
    res = requests.get(url)
    res.encoding = "utf-8"
    from xml.etree import ElementTree as ET
    law_dict = {}
    try:
        root = ET.fromstring(res.content)
        for law in root.findall("law"):
            name = law.findtext("법령명한글")
            link = law.findtext("법령상세링크")
            if name and link:
                law_dict[name] = link
    except:
        pass
    return law_dict

def fetch_law_detail(law_url):
    try:
        law_id = law_url.split("lawId=")[-1].split("&")[0]
        response = requests.get(f"http://www.law.go.kr/DRF/lawService.do?OC=chetera&target=law&type=XML&lawId={law_id}")
        response.encoding = "utf-8"
        return response.text
    except:
        return ""