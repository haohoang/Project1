import re

#mo file txt
file = open("enwiki/enwiki-20191101-3.txt", "r", errors='ignore')

with open('bodoc3.txt', 'w') as f: #file ket qua
    article_txt = file.read(80000) #doc file den khi het file
    while article_txt != '':
        # bo tab doc
        article_txt = re.sub(r"<doc.*>", "", article_txt)
        article_txt = re.sub(r"<\/doc>", "", article_txt)

        #bo cac dau cau
        article_txt = re.sub(
            r"\"|\#|\$|\%|\&amp;|\(|\)|\*|\+|\,|\-|\–|\/|\:|\;|\|\@|\[|\\|\]|\^|\_|\`|\{|\||\}|\~|\<|\>|\=", " ",
            article_txt)
        article_txt = re.sub(r"\n", " ", article_txt)
        article_txt = re.sub(r"\'\'", " ", article_txt)

        #bo cac chu so
        article_txt = re.sub(r"\d+", "", article_txt)

        #bo dau cach thua
        article_txt = re.sub(r"  ", " ", article_txt)

        f.write(article_txt) #ghi file
        article_txt = file.read(80000)
   