# Paramotor Pilot Logbook

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/M4M03Q2JN)

<p align="center">
  <img src="https://github.com/dievus/Paramotor-Pilot-Logbook/blob/main/images/main.png" width="901" height="438" />
</p>

Every pilot needs a logbook to keep track of their flights, whether it be for personal interest, training, or keeping track of mechanical hours for upkeep and maintenance. Unfortunately, there aren't a lot of options outside of paper logbooks and some mobile applications. Using Python3, I've developed this basic application utilizing the Tkinter Graphical User Interface (GUI) to manage log entries and output them to a comma separated value (CSV) sheet.

## Usage

### Installation
Installing is as simple as clicking this [link](https://github.com/dievus/Paramotor-Pilot-Logbook/archive/refs/heads/main.zip) to download the "Paramotor-Pilot-Logbook-main.zip" file. Once downloaded, unzip the file, open the directory, and double-click the "Paramotor-Pilot-Logbook.exe" file to open. 

You may find that Windows SmartScreen suggests not opening the file. This is because the file does not have a valid certificate chain. These are typically cost-prohibitive, and in order to provide this for free, the application is signed using a "self-signed" certificate. Just click on the "More info" button and "Run anyway."

### Entering Data
Entering flight data is simple. All that is required is to enter the information as required, and click submit.

### Importing Logbook Data
Already have a logbook? See the "demo_logbook_file.csv" and add existing log data to the file as specified by the file headers.

### Exporting Logbook Data
Pilots can export their logbooks by clicking File -> Save Flight Log.

### Deleting an Entry
If you find that you made a mistake, you can click Edit -> Remove Latest Entry, or by selecting the record(s) in the table and clicking the "Delete Record" button.

## Coming Soon

- [x] Import existing logbook into Paramotor Pilot Logbook database
- [x] Add some scrollbars to the interface that allow for a larger number of flights to be viewable
- [x] Add check for deleting flight entries

## Security Considerations

Unfortunately, code-signing certificates can be cost-prohibitive for applications that are free and open-source like this. Worse, is that "Extended Validation" certificates that are approved by Defender SmartScreen are even more expensive. Paramotor Pilot Logbook uses a "self-signed" certificate, which is issued by the developer. 

The Paramotor Pilot Logbook.exe file has the following SHA-256 hash value:

- 5647ABFBFDDB9D06639142E20D7D59C5F4EE6A8A60C3BEAC3650254D1F5FC26E

You can confirm that the file is legitimate by opening PowerShell, and running ```Get-FileHash "Paramotor Pilot Logbook.exe"```. If the value matches, it means that the file is legitimate and has not been tampered with.
