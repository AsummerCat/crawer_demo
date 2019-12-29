import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"
}
# 1.代码登录
login_url = 'https://mm006.xyz/api/register.php'
login_form_data = {
    'ip': '127.0.0.2'
}

# 2.登录成功之后带着有效的cookie访问请求数据
# login_response = requests.post(login_url, data=login_form_data)
# 这个session跟服务器的session不是一回事,这个session可以自动保存cookie,
# 可以理解为cookiejar
session = requests.session()
login_response = session.post(login_url, data=login_form_data, headers=headers)
# 个人中心页面
member_url = "https://www.yaozh.com/member/"
# 登录成功  则 访问个人中心页面  session中携带了cookies
data = session.get(member_url, headers=headers).content.decode('utf-8')
with open('05-cookie2.html', 'w', encoding='utf-8') as f:
    f.write(data)


