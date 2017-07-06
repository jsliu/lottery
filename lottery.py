import json, urllib, datetime, csv
from urllib.request import urlopen, Request
from pprint import pprint


class REQUEST:

    def __init__(self):
        self.appcode = '5b0299a3dac844bda64e013b3464c19c'
        self.host = 'http://jisucpkj.market.alicloudapi.com'

    def live_data(self, caipiaoid, issueno):
        path = '/caipiao/query'
        querys = 'caipiaoid=' + caipiaoid + '&issueno=' + issueno

        url = self.host + path + '?' + querys
        request = Request(url, method='GET')
        request.add_header('Authorization', 'APPCODE ' + self.appcode)
        try:
            content = urlopen(request).read()
            output = json.loads(content)
            print(issueno + ' readed.')
        except urllib.error.HTTPError:
            print('Unable to access to ' + issueno)
            output = {}

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
    def save_data(data, fp):
        if data:
            fp.writerow([data['issueno'], data['number']])

    @staticmethod
    def print_data(file_name):
        with open(file_name, 'r') as fp:
            output = json.load(fp)
            pprint(output)


def download_gx_kuai3():
    start = datetime.datetime(2017,4,19)
    end = datetime.datetime.today()
    dates = [start + datetime.timedelta(days=x) for x in range((end-start).days)]
    caipiaoid = '78'

    data_request = REQUEST()
    with open('gx_kuai3.csv', 'w') as file:
        fp = csv.writer(file)
        fp.writerow(['IssueNo', 'Number'])

        for i in range(len(dates)):
            for j in range(1,79):
                if j < 10:
                    issueno = dates[i].strftime('%Y%m%d') + '00' + str(j)
                else:
                    issueno = dates[i].strftime('%Y%m%d') + '0' + str(j)


                output = data_request.live_data(caipiaoid, issueno)
                if output:
                    REQUEST.save_data(output, fp)


def download_yi_kuai3():
    start = datetime.datetime(2017, 4, 18)
    end = datetime.datetime.today()
    dates = [start + datetime.timedelta(days=x) for x in range((end - start).days)]
    caipiaoid = '87'

    data_request = REQUEST()
    with open('yi_kuai3.csv', 'w') as file:
        fp = csv.writer(file)
        fp.writerow(['IssueNo', 'Number'])

        for i in range(len(dates)):
            for j in range(73):
                if j < 9:
                    issueno = dates[i].strftime('%y%m%d') + '00' + str(j+1)
                else:
                    issueno = dates[i].strftime('%y%m%d') + '0' + str(j+1)

                output = data_request.live_data(caipiaoid, issueno)
                if output:
                    REQUEST.save_data(output['result'], fp)


def main():

    caipiaoid = '78'
    issueno = '20170704001'
    data_request = REQUEST()
    #output = data_request.caipiao_class()
    output = data_request.live_data(caipiaoid, issueno)
    #REQUEST.save_data(output['result'], 'anhui_kuai3.json')
    if output:
        pprint(output)


def convert2csv(json_file, csv_file):
    with open(json_file) as fp:
        data = json.load(fp)

    with open(csv_file, 'w') as fp:
        cf = csv.writer(fp)
        cf.writerow(["IssueNo", "number"])
        for item in data:
            cf.writerow([item['issueno'], item['number'][0], item['number'][2], item['number'][4]])


if __name__ == '__main__':
    main()
