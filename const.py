login_url = 'http://p.nju.edu.cn/portal_io/login'
logout_url = 'http://p.nju.edu.cn/portal_io/logout'

volume_url = 'http://p.nju.edu.cn/portal_io/selfservice/volume/getlist'
getinfo_url = 'http://p.nju.edu.cn/portal_io/getinfo'

# generate fixed headers
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "DNT": "1",
    "Origin": "http://p.nju.edu.cn",
    "Referer": "http://p.nju.edu.cn/portal/index.html?v=201806151414",
    "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
}
