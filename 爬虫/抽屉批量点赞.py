from  bs4 import BeautifulSoup
import requests


headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.4882.400 QQBrowser/9.7.13059.400',
    }


resoponse_1 = requests.get(url='https://dig.chouti.com/',
                           headers=headers
                           )
cookie_dict = resoponse_1.cookies.get_dict()

resoponse_2 = requests.post(
    url='https://dig.chouti.com/login',
    data={
        'phone':'8615733239039',
        'password':'xxxxxx',
        'oneMonth':'1',
    },
    headers=headers,
    cookies=cookie_dict
)
for page in range(1,3):
    html = requests.get(url='https://dig.chouti.com/all/hot/recent/{}'.format(page),headers=headers)
    soup = BeautifulSoup(html.text,'html.parser')
    divs = soup.find(name='div',id='content-list')
    items = divs.find_all(attrs={'class':'item'})
    for i in items:
        click_id = i.find('img').get('lang')
        if click_id:

            click_hand = requests.post(url='https://dig.chouti.com/link/vote?linksId={}'.format(click_id),
                                       headers=headers,
                                       cookies=cookie_dict,
                                       )

            print(click_id)






