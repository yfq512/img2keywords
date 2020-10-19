import requests
from urllib import parse
import json
from keywords_fit import nsword_fit as nsw_fit
import base64
import os, time, shutil, fcntl, random

def clean_str(text):
    pass_sign = [' ','`','~','!','@','#','$','%','^','&','*','(',')','-','_','+','=','{','}','[',']','|',':',';','"','?','/','<','>',',','.','：','；','“','‘','《','》','，','。','？']
    x = ''
    for n in text:
        if not n in pass_sign:
            x = x + n
    if len(x) == 0:
        return None
    return x

def load_keywords(keywords_path):
    keywords_list = []
    keywords_path_list = os.listdir(keywords_path)
    for m in keywords_path_list:
        keywords_file_path = os.path.join(keywords_path, m)
        print('loading: ', keywords_file_path)
        for n in open(keywords_file_path):
            if not (n == '' or n == '\n'): # delete unlaw words
                keywords_list.append(n[:-1])
    keywords_list = list(set(keywords_list))
    return keywords_list

def updata_keywords(updatawordsroot, keywords_path):
    newkeywords_list = []
    addkeyword_file_list = os.listdir(updatawordsroot)
    for n in addkeyword_file_list:
        addwordpath = os.path.join(updatawordsroot, n)
        for m in open(addwordpath):
            newkeywords_list.append(m[:-1])
        copy_path = os.path.join(keywords_path, n)
        shutil.copyfile(addwordpath, copy_path)
        os.remove(addwordpath)
    return newkeywords_list

def find_keywords(imgpath, updatawordsroot, keywords_list,  keywords_path, delkeywordspath):
    delkeywordspath_list = os.listdir(delkeywordspath)
    if not len(delkeywordspath_list) == 0: # if exists signfle, reload keywords 
        keywords_list = load_keywords(keywords_path)
        os.remove(os.path.join(delkeywordspath, 'sign.txt'))
        print('reload keywords for del some keywords')
    new_keywords_list = updata_keywords(updatawordsroot, keywords_path)
    print(new_keywords_list)
    for n in new_keywords_list:
        keywords_list.append(n)
    keywords_list = list(set(keywords_list))
    print(keywords_list)
    nsw_out = None
    sign = -1
    if os.path.exists(imgpath):
        time.sleep(0.5)
        imgbase64 = None
        with open(imgpath,'rb') as f:
            imgbase64 = base64.b64encode(f.read())
        # imgString2 = imgbase64.decode('utf-8')
        # imgString = 'base64,' + imgString2
        data = {"imgbase64":imgbase64}
        # header = {'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}
        postUrl = 'http://192.168.132.151:8090/tyocr'
        # data = json.dumps(data)
        t11 = time.time()
        r2 = requests.post(postUrl, data=data).text
        print('>>>>>>>>>>>', r2)
        r2 = json.loads(r2)
        print(r2['text'])
        r = [r2['text']]
        print('time cost', time.time()-t11)
        # 增加异常捕捉，存在某些时候识别异常
        sign = 0
  #      try:
        #r = json.loads(r)
        #list_ = r['data']
        list_ = r
        if len(list_) == 0:
            nsw_out = ''
        else:
            sign = 1
            text_out = ''
            # 文字按行输出
            for n in list_:
                text_out = text_out + n
            sign = 0 # -1, 0,1,2 means: error, no words, not find keywords, find keywords
            text_out = clean_str(text_out)
            if text_out == None:
                return {'sign':sign, 'text':None}
            print('clean',text_out)

            cnt = 0
            wf_words = []
            for n in keywords_list:
                cnt = 0
                #if text_out is None:
                #    return text_out
                if n in text_out:
                    cnt2 = text_out.count(n)
                    wf_words.append({n:cnt2})
            nsw_out = wf_words

            if nsw_out is None:
                str1 = str(sign) + ':' + str([])
                return {'sign':sign, 'text':None}
            else:
                sign = 1
                if len(nsw_out) == 0:
                    return {'sign':sign, 'text':None}
                else:
                    sign = 2
                    return {'sign':sign, 'text':nsw_out}

def delkeywords(keywordspath, delkeywordspath, delkeyword):
    # 整理敏感词，建立文件让findwords重载keywords
    temp_keywords_list = []
    sign = -1
    keywordspath_list = os.listdir(keywordspath)
    for  n in keywordspath_list:
        keyword_file_path = os.path.join(keywordspath, n)
        for m in open(keyword_file_path):
            if m[:-1] == delkeyword:
                sign = 0
                continue
            else:
                temp_keywords_list.append(m[:-1])
        os.remove(keyword_file_path)
    txtkeywordspath = os.path.join(keywordspath, 'keywords.txt')
    with open(txtkeywordspath, 'w') as f:
        for k in temp_keywords_list:
            f.write(k)
            f.write('\n')
        f.close()
    txtsignpath = os.path.join(delkeywordspath, 'sign.txt')
    with open(txtsignpath, 'w') as f:
        f.write('sign')
        f.close()
    return sign, temp_keywords_list

keywords_path = './keywords/'
keywords_list = load_keywords(keywords_path)


import requests
from flask import Flask,render_template,request
import base64

def getRandomSet(bits):
    num_set = [chr(i) for i in range(48,58)]
    char_set = [chr(i) for i in range(97,123)]
    total_set = num_set + char_set
    value_set = "".join(random.sample(total_set, bits))
    return value_set

app = Flask(__name__)
imgroot = 'images'
updata_word_path = './updatawords'
updatawordsroot = 'updatawords'
delkeywordspath ='delkeywords'

@app.route("/findkeywords",methods = ['GET', 'POST'])
def findwords():
    if request.method == "POST":
        # base64data encode to iamge and save
        imgbase64 = request.form.get('imgbase64')
        imgdata = base64.b64decode(imgbase64)
        randname = getRandomSet(15)
        imgrandpath = os.path.join(imgroot, randname + '.jpg')
        file = open(imgrandpath,'wb')
        file.write(imgdata)
        file.close()
        print(imgrandpath)
        res = find_keywords(imgrandpath, updatawordsroot, keywords_list, keywords_path, delkeywordspath)
        return res
    else:
        return "<h1>Find faces, please use post!</h1>"

@app.route("/upkeywords",methods = ['GET', 'POST'])
def upkeyword():
    if request.method == "POST":
        try:
            keyword = request.form.get('keyword')
            randname = getRandomSet(15)
            txtrandname = randname + '.txt'
            txtrandpath = os.path.join(updatawordsroot, txtrandname)
            with open(txtrandpath,'w') as f:
                f.write(keyword)
                f.write('\n')
                f.close()
            return {'sign':1} # write keyword scuessful
        except:
            print('>>>upkeywords error')
            return {'sign':-1}
    else:
        return "<h1>Updata keywords, please use post!</h1>"

@app.route("/delkeywords",methods = ['GET', 'POST'])
def del_keyword():
    if request.method == "POST":
        try:
            delkeyword = request.form.get('delkeyword')
            sign, _list = delkeywords(keywords_path, delkeywordspath, delkeyword)
            if sign == 0:
                return {'sign':sign, 'text':None} # delete sucuessful
            else:
                return {'sign':sign, 'text':_list} # delword is not in org keywords
        except:
            return {'sign':-2, 'text':None} # code error
    else:
        return "<h1>Delete keywords, please use post!</h1>"


if __name__ == '__main__':
    host = '0.0.0.0'
    port = '8082'
    app.run(debug=True, host=host, port=port)
