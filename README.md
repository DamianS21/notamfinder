# Init
This software is made to improve work of everyone who use NOTAMs on daily basis.

**This software is NOT certified for any operational use.**
# Functions:
## NOTAM download
This software downloads NOTAM from ICAO API. It's nessesery to put API Key, which you can get from [ICAO API Data Service](https://www.icao.int/safety/iStars/Pages/API-Data-Service.aspx).
API Key should be inserted in File->Settings->ICAO API key and saved with 'Save settings' button.
When NOTAMs would be downloaded correctly the File/Notams downloaded from ICAO checkbox is turned on. It makes boxes read-only and change the way of collecting NOTAM list.

## NOTAM filter
NOTAMs can be filter by date by selecting 'From' and 'To' date next to "NOTAM download" button in main window.
UFN - makes 'To' date as 2999/01/01
By default PERM and EST NOTAMS are appended to filtered NOTAM list. You can change those settings in File->Always PERM or Always EST.

If 'Notams downloaded from ICAO' settings is disabled NOTAMs should be pasted from Fusion list or another similar format.

## NOTAM tags highlight
You can choose tags you want to highlight in both lists. Default tags are:
> ILS RWY DME VOR

Tags should be separated by whitespace ' '.
Default tags can be changed in File->Settings->Default tags.



# Credits:

This software uses [settings.py by xaviergoby](https://gist.github.com/xaviergoby/a23edddc20894ae5ff3c278e7488dfd3)  for saving settings.
