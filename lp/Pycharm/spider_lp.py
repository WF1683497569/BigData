import json
import re

import requests
from requests import RequestException


# 获取页面
def get_one_page(url):
    try:
        headers = {
            'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'cookie': 'x-zp-client-id=e462c47c-62fe-42fc-fab9-b7a6a4b56a51; sts_deviceid=16db344bf1e3bc-03884c2f616058-36664c08-2073600-16db344bf1f4e9; sajssdk_2015_cross_new_user=1; urlfrom2=121114583; adfcid2=www.baidu.com; adfbid2=0; sou_experiment=unexperiment; LastCity=%E5%90%88%E8%82%A5; LastCity%5Fid=664; ZP_OLD_FLAG=false; POSSPORTLOGIN=0; CANCELALL=0; urlfrom=121114583; adfcid=www.baidu.com; adfbid=0; dywea=95841923.2894189925394779000.1570670688.1570670688.1570693614.2; dywec=95841923; dywez=95841923.1570693614.2.2.dywecsr=baidu|dyweccn=(organic)|dywecmd=organic|dywectr=%25E6%2599%25BA%25E8%2581%2594; __utma=269921210.260536354.1570670688.1570670688.1570693614.2; __utmc=269921210; __utmz=269921210.1570693614.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic|utmctr=%E6%99%BA%E8%81%94; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1570670688,1570693614; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1570693614; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fwww.baidu.com%2Fs%3Fwd%3D%25E6%2599%25BA%25E8%2581%2594%26ie%3DUTF-8; jobRiskWarning=true; acw_tc=2760820415706936195338279efc21f3280857b5cdc321c4c6de168584a722; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216db344bf5b418-09a988bc62e4d-36664c08-2073600-16db344bf5c615%22%2C%22%24device_id%22%3A%2216db344bf5b418-09a988bc62e4d-36664c08-2073600-16db344bf5c615%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


# 解析页面
def parse_one_page(res):
    patten = re.compile(
        '.*?<h3 title="招聘(.*?)">.*?href="(.*?)".*?title="(.*?)_(.*?)_(.*?)_.*?公司(.*?)"',
        re.S)
    items = re.findall(patten, res)
    for item in items:
        yield {
            '职位': item[0],
            '公司': item[5],
            '薪资': item[2],
            '地点': item[3],
            '学历': item[4],
            'uri': item[1]
        }


# 写入文件
def write_to_file(content):
    with open('spider_lp.json', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


# 主函数
def main(page):
    url = 'https://www.liepin.com/zhaopin/?isAnalysis=&dqs=&pubTime=&salary=&subIndustry=&industryType=&compscale=&key=java&init=-1&searchType=1&headckid=9aa072bcb5fa43b6&compkind=&fromSearchBtn=2&sortFlag=15&ckid=9aa072bcb5fa43b6&degradeFlag=0&jobKind=&industries=&clean_condition=&siTag=k_cloHQj_hyIn0SLM9IfRg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_prime&d_ckId=9e632cfb4945a9be32b3336295db599f&d_curPage=1&d_pageSize=40&d_headId=9e632cfb4945a9be32b3336295db599f&curPage={}'.format(
        page)
    res = get_one_page(url)
    for item in parse_one_page(res):
        print(item)
        write_to_file(item)


# 程序入口
if __name__ == '__main__':
    for i in range(0, 99):
        main(page=i)
