import requests # to request sites
from bs4 import BeautifulSoup # to manipulate data 
from codeforces_api import CodeforcesApi




url = input('Group Link : ')
key = input('your API key : ')
secret = input('your API secret : ')

# requests page
group = requests.get(url)

def main(group):

    src = group.content
    soup = BeautifulSoup(src,"lxml")
    contest_IDs= [] 

    contests = soup.find_all("tr",{"class":"highlighted-row"})
    

    for each_contest in range(len(contests)):

        contest_title = contests[each_contest].contents[1].text.strip().split("\n")[0].strip()
        
        link = contests[each_contest].find('td',{'class':'state'}).find('a').attrs['href'].split('/')
        contest_IDs.append([link[4],contest_title])
        print(contest_title,'was included in filtering..')

    else:
        print('- - - - - - - - - - - - - - - - - - - - - - - - -')
        
    
    def get_contest_data(id):

        sheet_data = {}
        try:
            api = CodeforcesApi(key, secret)
            result = api.contest_status(id[0])
        except:
            print('Something wrong with key or secret , check it again')
            return 
        

        for submit in result:
            if submit.verdict == "OK":
                user = submit.author.members[0].handle
                problem = submit.problem.index + '-' + str(id[0])
                try:
                    sheet_data[user].update({problem : True})
                except:
                    sheet_data[user]={problem : True}
        
        print(id[1],"\n")
        print_dict(sheet_data)
        print('+++++++++++++++++++++++++++++++++++++++++++++++++')
       
                        
    def print_dict(dic):
        for x, y in dic.items():
            print(x,' : ',len(y))
        print(">>>>>>>>> ",len(dic),'member')


    for ID in contest_IDs: 
        get_contest_data(ID)

main(group)
