# Define the path to the directory containing chromedriver.exe
$chromeDriverPath = "C:\Program Files\Google\Chrome\Application"

# Get the current PATH variable
$currentPath = [System.Environment]::GetEnvironmentVariable("PATH", [System.EnvironmentVariableTarget]::Machine)

# Check if the directory is already in the PATH
if ($currentPath -notlike "*$chromeDriverPath*") {
    # Add the directory to the PATH variable
    $newPath = $currentPath + ";" + $chromeDriverPath
    [System.Environment]::SetEnvironmentVariable("PATH", $newPath, [System.EnvironmentVariableTarget]::Machine)
    
    # Notify the user about the update
    Write-Host "Added '$chromeDriverPath' to the PATH variable."
} else {
    # Directory is already in the PATH
    Write-Host "'$chromeDriverPath' is already in the PATH variable."
}

# Refresh the environment to apply changes (log out and log back in or restart the computer)
Write-Host "Please log out and log back in or restart your computer to apply the changes."
