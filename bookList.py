import os

scanPath = "/Users/denny/Library/Mobile Documents/iCloud~QReader~MarginStudy/Documents/"

for category in os.listdir(scanPath):
    if os.path.isdir(scanPath+ category) and category[0:1] != ".":
        print("分类:"+ category)
        for bookName in os.listdir(scanPath+ category):
            print("   《"+ bookName.rsplit(".",1)[0]+"》")