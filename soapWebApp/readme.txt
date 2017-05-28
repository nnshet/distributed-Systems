#Name - Neha Shet
#UTA ID - 1001387308
#Language used - Java

#How to run the program?
	First import the project in the Eclipse go to the package weatherclient and select WeatherSoapClient.java and run as java application. Just make sure that you have tomcat configured.	

#Code description:
	- The user has to enter latitide and longitude of the location in order to get the mintemp, maxtemp, wind speed, wind direction, dew point temp etc.	

	- There are 4 functions getValuesFromDom,convertStringToDocument,getWeatherDataForInputValues and isRefreshed.
		The function convertStringToDocument is used for converting the received data, which was in the string format, into XML.
		The function getValuesFromDom actually fetches and extract the data from XML and returns the required field.
		The function isRefreshed asks the user for the input if he wants to refresh the request
		The function is getWeatherDataForInputValues takes the coordinate values from user and makes an soap request to the web service

Limitaton:
 	-No user interface created.

References:
	https://graphical.weather.gov/xml/SOAP_server/ndfdXMLserver.php
	https://graphical.weather.gov/xml/
	https://www.tutorialspoint.com/java_xml/java_xpath_parse_document.htm
	http://www.journaldev.com/1237/java-convert-string-to-xml-document-and-xml-document-to-string
 
	