from requests_toolbelt import MultipartEncoder
import requests, os

UPLOAD_API_HOST=os.environ['ALIST_HOST'] if os.environ.__contains__('ALIST_HOST') else '18.188.239.112'


def upload_to_server(source_file_path: str, target_folder='/local/rss'):
    if os.path.exists(source_file_path) is True:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Referer": "http://{}/alist{}".format(UPLOAD_API_HOST, target_folder),
            "Origin": "http://{}/alist".format(UPLOAD_API_HOST),
            "Host": UPLOAD_API_HOST,
            "As-Task": "false",
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Authorization": "",
            "Connection": "keep-alive",
            "Content-Length": "{}".format(os.path.getsize(source_file_path)),
            "Content-Type": "video/mp4",
            "File-Path": "/alist/{}/{}".format(target_folder, source_file_path.split('/')[-1])
        }
        upload_url = "http://{}/alist/api/fs/put".format(UPLOAD_API_HOST)
        with open(source_file_path, 'rb') as vf:
            res = requests.put(upload_url, headers=headers, data=vf)
            if res.status_code == 200:
                return True
            print(res.text)
    return False


if __name__ == '__main__':
    print(upload_to_server('../rss/xhdtsgs.rss'))
