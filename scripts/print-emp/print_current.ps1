
param(
    [string]$empID
)

chrome.exe -remote-debugging-port=9014 --kiosk-printing  --user-data-dir="C:\Documents\Selenium\Test_Chrome\"
# chrome.exe -remote-debugging-port=9014 --profile-directory=ERISA --user-data-dir="C:\Documents\Selenium\Test_Chrome\"

# python .\scripts\print_current.py $empID 
python  .\scripts\print_current.py $empID 