#Read settings in array
with open('settings.txt','r') as f:
    settings = f.readlines()
f.close()
firstSetting = settings[0].rstrip()

print(firstSetting)
