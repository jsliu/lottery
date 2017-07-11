import json, urllib, datetime, csv
from urllib.request import urlopen, Request
from pprint import pprint


class REQUEST:

    def __init__(self):
        self.appcode = '5b0299a3dac844bda64e013b3464c19c'
        self.host = 'http://jisucpkj.market.alicloudapi.com'

    def live_data(self, caipiaoid, issueno):
        path = '/caipiao/query'
        querys = 'caipiaoid={0}&issueno={1}'.format(caipiaoid, issueno)

        url = self.host + path + '?' + querys
        request = Request(url, method='GET')
        request.add_header('Authorization', 'APPCODE ' + self.appcode)
        try:
            content = urlopen(request).read()
            output = json.loads(content)
            print('Downloaded ' + issueno)
        except urllib.error.HTTPError:
            output = {}
            print('Unable to access to ' + issueno)

        return output

    def historical_data(self, caipiaoid, issueno):
        path = '/caipiao/history'
        querys = 'caipiaoid=' + caipiaoid + '&issueno=' + issueno + '&num=20'
        url = self.host + path + '?' + querys

        request = Request(url, method='GET')
        request.add_header('Authorization', 'APPCODE ' + self.appcode)
        content = urlopen(request).read()
        output = json.loads(content)

        return output

    def caipiao_class(self):
        path = '/caipiao/class'
        url = self.host + path

        request = Request(url, method='GET')
        request.add_header('Authorization', 'APPCODE ' + self.appcode)
        content = urlopen(request).read()
        output = json.loads(content)

        return output

    @staticmethod
    def print_data(file_name):
        with open(file_name, 'r') as fp:
            output = json.load(fp)
            pprint(output)


def download_data(file_name, max_number, formats='%Y%m%d', start = datetime.datetime.now().date()):
    end = datetime.datetime.now().date()
    dates = [start + datetime.timedelta(days=x) for x in range((end-start).days+1)]

    options = {'ahk3.json': 76,
               'gxk3.json': 78,
               'yik3.json': 87,
               'shk3.json': 105}

    data_request = REQUEST()
    with open(file_name, 'r') as fp:
        try:
            output = json.load(fp)
        except json.decoder.JSONDecodeError:
            output = []

    with open(file_name, 'w') as fp:
        caipiaoid = options[file_name]
        for i in range(len(dates)):
            for j in range(max_number):
                if j < 9:
                    issueno = dates[i].strftime(formats) + '00' + str(j+1)
                else:
                    issueno = dates[i].strftime(formats) + '0' + str(j+1)
                response = data_request.live_data(caipiaoid, issueno)
                if response:
                    output.append(response['result'])
        json.dump(output, fp)


'''
def download_live_data(file_name, number, formats='%Y%m%d'):
    with open(file_name, 'r') as fp:
        data = json.load(fp)

    options = {'ahk3.json': 76,
               'gxk3.json': 78,
               'shk3.json': 105}

    caipiaoid = options[file_name]
    date = datetime.datetime.today()
    for j in range(number):
        if j < 9:
            issueno = date.strftime(formats) + '00' + str(j + 1)
        else:
            issueno = date.strftime(formats) + '0' + str(j + 1)
        data_request = REQUEST()
        response = data_request.live_data(caipiaoid, issueno)
        if response:
            data.append(response['result'])

    with open(file_name,'w') as fp:
        json.dump(data, fp)
'''


def convert2csv(json_file, csv_file):
    with open(json_file) as fp:
        data = json.load(fp)

    with open(csv_file, 'w') as fp:
        cf = csv.writer(fp)
        cf.writerow(["IssueNo", "number"])
        for item in data:
            cf.writerow([item['issueno'], item['number'][0], item['number'][2], item['number'][4]])


def main():
    '''
    caipiaoid = '78'
    issueno = '20170704078'
    data_request = REQUEST()
    #output = data_request.caipiao_class()
    output = data_request.live_data(caipiaoid, issueno)
    #REQUEST.save_data(output['result'], 'anhui_kuai3.json')
    if output:
        pprint(output)
    '''
    download_data('gxk3.json', 78)
    download_data('yik3.json', 73, '%y%m%d')


if __name__ == '__main__':
    main()