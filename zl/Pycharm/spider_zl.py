import datetime
import json
import math
import os

import requests

'''
任务：爬取智联招聘XX城市XX岗位信息
最后实现：2019.10.28
'''

# 配置所有需要的参数
job_names = ['Java', '大数据', 'C++']
# job_names = ['大数据']
city_names = ['合肥', '北京', '上海']
# city_names = ['合肥']
output_path = 'zl_test'
# headers暂时没用到，可以正在爬取，放这备用
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Cookie': 'acw_tc=2760828f15705836401326114eea73d60307718b339cedfa4aee6ee9c1ccda; x-zp-client-id=e462c47c-62fe-42fc-fab9-b7a6a4b56a51; sts_deviceid=16db344bf1e3bc-03884c2f616058-36664c08-2073600-16db344bf1f4e9; adfbid2=0; sou_experiment=unexperiment; LastCity=%E5%90%88%E8%82%A5; LastCity%5Fid=664; campusOperateJobUserInfo=e6aa5d83-af6a-4d1f-9067-3fef626002b5; ZP_OLD_FLAG=false; POSSPORTLOGIN=7; CANCELALL=0; jobRiskWarning=true; sts_sg=1; sts_sid=16e0d812ac22da-09923605a7deef-36664c08-2073600-16e0d812ac45be; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fsou.zhaopin.com%2F%3Fp%3D2%26jl%3D664%26kw%3Djava%26kt%3D3%26sf%3D0%26st%3D0; dywea=95841923.2894189925394779000.1570670688.1572159523.1572184639.8; dywec=95841923; dywez=95841923.1572184639.8.8.dywecsr=sou.zhaopin.com|dyweccn=(referral)|dywecmd=referral|dywectr=undefined|dywecct=/; __utmc=269921210; adfbid=0; ZPCITIESCLICKED=|664; dyweb=95841923.4.10.1572184639; __utma=269921210.260536354.1570670688.1572184639.1572186078.10; __utmz=269921210.1572186078.10.9.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utmt=1; __utmb=269921210.1.10.1572186078; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216db344bf5b418-09a988bc62e4d-36664c08-2073600-16db344bf5c615%22%2C%22%24device_id%22%3A%2216db344bf5b418-09a988bc62e4d-36664c08-2073600-16db344bf5c615%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; Hm_lvt_38ba284938d5eddca645bb5e02a02006=1572146737,1572159471,1572184599,1572186079; urlfrom=121114584; urlfrom2=121114584; adfcid=www.google.com; adfcid2=www.google.com; sts_evtseq=37; Hm_lpvt_38ba284938d5eddca645bb5e02a02006=1572186123; ZL_REPORT_GLOBAL={%22sou%22:{%22actionid%22:%22c6956428-7868-40bc-8185-8e0faaa51a67-sou%22%2C%22funczone%22:%22smart_matching%22}%2C%22//www%22:{%22seid%22:%22%22%2C%22actionid%22:%2266df4d20-eefa-4b33-b9e5-a00e8fbae64d-cityPage%22}%2C%22jobs%22:{%22recommandActionidShare%22:%22cc809946-4877-4e12-8f19-630bbc5efe0a-job%22%2C%22funczoneShare%22:%22dtl_best_for_you%22}}'
}


# 获取总页数，用于设置遍历结束条件
def get_page_nums(city_name, job_name):
    url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(
        city_name, job_name)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            j = json.loads(response.text)
            count_nums = j.get('data')['count']
            page_nums = math.ceil(count_nums / 90)
            return page_nums
    except Exception as e:
        return None


def get_job_list(start, city_name, job_name):
    # 当请求第一页时，请求头中不包含start请求参数_20191027
    if (start == 0):
        url = 'https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(
            city_name, job_name)
    else:
        url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId={}&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'.format(
            start, city_name, job_name)
    # 创建一个空列表，用于存储job的所有信息
    job_list = []
    try:
        respone = requests.get(url)
        if respone.status_code == 200:
            j = json.loads(respone.text)
            results = j.get('data').get('results')
            for job in results:
                # 筛选职位类型为全职的job，这也是为什么最后爬取的数据比岗位总数少的原因
                if job.get('emplType') == '全职':
                    job_dict = {
                        'jobName': job.get('jobName'),
                        'company': job.get('company').get('name'),
                        'city': job.get('city').get('items')[0].get('name'),
                        'number': job.get('company').get('size').get('name'),
                        'salary': job.get('salary'),
                        # 此处极坑，个别JSON行没有workingExp
                        'workingExp': job.get('workingExp').get('name') if (job.get('workingExp') != None) else '未说明'
                    }
                    # 追加
                    job_list.append(job_dict)
        return job_list
    except Exception as e:
        return None


def main():
    # 把结果放在文件夹里面，不存在就创建
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    # 双层遍历城市和职位
    for city_name in city_names:
        for job_name in job_names:
            # 打印正在爬取city_name的job_name
            print('Searching: %s - %s' % (city_name, job_name))
            total_page = get_page_nums(city_name, job_name)
            # 打印总页数
            print('Total_page: %d' % total_page)
            json_file = output_path + '/{0}_{1}.json'.format(city_name, job_name)
            # 写JSON操作
            with open(json_file, 'w', encoding='utf-8') as f:
                for i in range(int(total_page)):
                    # 打印当前在第几页
                    print('For i: %d in %d' % (i + 1, total_page))
                    # 调用get_job_list函数，获取所有需要的job信息
                    job_list = get_job_list(i * 90, city_name, job_name)
                    for job in job_list:
                        print(job)
                        data = json.dumps(job, ensure_ascii=False)
                        f.write(data + '\n')


if __name__ == '__main__':
    start_time = datetime.datetime.now()
    main()
    end_time = datetime.datetime.now()
    print("Running time: %s" % (end_time - start_time))
