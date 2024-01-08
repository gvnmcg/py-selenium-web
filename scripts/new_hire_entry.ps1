
param(
    [int]$arg1
)

chrome.exe -remote-debugging-port=9014 --profile-directory="ERISA" --user-data-dir="C:\Documents\Selenium\Test_Chrome\"
# chrome.exe -remote-debugging-port=9014 --profile-directory=ERISA

# python .\test\test_chrome_getdata.py
python .\scripts\share_to_ibac_v2.py $arg1