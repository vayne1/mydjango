import requests
from bs4 import BeautifulSoup
import json,os


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
all_name = []
basedir = os.path.dirname(os.path.abspath(__file__))
res_file = os.path.join(basedir,'aa.txt')
for i in range(1,51):
    html = requests.get(url='http://hz.ziroom.com/z/nl/z2.html?p={}'.format(i),
                        headers=headers
                        )
    soup = BeautifulSoup(html.text,'html.parser')
    ul = soup.find(name='ul',id='houseList')
    all_houses = ul.find_all(attrs={'class':'clearfix'})

    for house in all_houses:
        house_url = house.find(name='a',attrs={'class':'t1'})
        if house_url:
            house_url = 'http:'+house_url.get('href')
            house_html = requests.get(url=house_url,headers=headers)
            house_soup = BeautifulSoup(house_html.text,'html.parser')
            resblock_id = house_soup.find(name='input',id='resblock_id').get('value')
            room_id = house_soup.find(name='input',id='room_id').get('value')
            house_id = house_soup.find(name='input',id='house_id').get('value')
            ly_name = house_soup.find(name='input',id='ly_name').get('value')
            ly_phone = house_soup.find(name='input',id='ly_phone').get('value')
            name = requests.get(url='http://hz.ziroom.com/detail/steward',
                                params={'resblock_id':resblock_id,'room_id':room_id,'house_id':house_id,'ly_name':ly_name,'ly_phone':ly_phone},
                                headers=headers
                                )
            name_dict = json.loads(name.text)
            # print(name_dict)
            if (name_dict['data']):
                print(name_dict['data']['keeperName'])
                all_name.append(name_dict['data']['keeperName'])
                with open(res_file,'a+') as f:
                    f.write(str(name_dict['data']['keeperName'])+'\t')
                    f.write(str(name_dict['data']['headCorn'])+'\t')
                    f.write(str(name_dict['data']['keeperPhone'])+'\t')
                    f.write(house_url+'\n')
print(set(all_name))
