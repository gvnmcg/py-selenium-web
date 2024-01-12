
param(
    [string]$idListFilePath
)

chrome.exe -remote-debugging-port=9014 --kiosk-printing --user-data-dir="C:\Documents\Selenium\Test_Chrome\"
# chrome.exe -remote-debugging-port=9014 --profile-directory=ERISA

# python .\scripts\print_current.py $empID 

# Read the numbers from the text file into an array
$empIDs = Get-Content $idListFilePath

# Iterate through each number and execute the Python script
foreach ($empID  in $empIDs) {
    # Invoke the Python script with the current number as an argument
    # python .\scripts\print_current.py $empID 
    Start-Process python.exe -ArgumentList ".\scripts\print_current.py $empID" -Wait
    if ($?) {
        Write-Host "Printing for $empID was completed successfully."
    } else {
        Write-Host "Printing for $empID failed."
        
    }
}
