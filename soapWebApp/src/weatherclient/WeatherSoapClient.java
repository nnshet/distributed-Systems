//Name : Neha Shet Student Id: 1001387308

package weatherclient;


import gov.weather.graphical.xml.DWMLgen.wsdl.ndfdXML_wsdl.NdfdXMLPortTypeProxy;
import gov.weather.graphical.xml.DWMLgen.wsdl.ndfdXML_wsdl.WeatherParametersType;

import java.io.StringReader;
import java.math.BigDecimal;
import java.rmi.RemoteException;
import java.util.Calendar;
import java.util.Date;
import java.util.GregorianCalendar;
import java.util.Scanner;

import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;

import org.w3c.dom.Document;
import org.xml.sax.InputSource;

public class WeatherSoapClient {

	static NdfdXMLPortTypeProxy proxy = null;
	static WeatherParametersType wp = null;
	public static void main(String[] args) throws RemoteException {
		// TODO Auto-generated method stub

		proxy = new NdfdXMLPortTypeProxy();
		wp = new WeatherParametersType();
		wp.setMint(true); // set setMint to True
		wp.setMaxt(true); // set setMaxt to True
		wp.setTemp(true); // set setTmp to True
		wp.setDew(true); // set setDew to True
		wp.setWspd(true); // set setWspd to True
		wp.setWdir(true); // set setWdir to True
		wp.setPop12(true); // set setPop12 to True
		
		//taking the input(latitude)from the user
		System.out.println("Please Enter latitude:");
		BigDecimal lat = getCoordinates();
		
		//taking the input(longitude)from the user
		System.out.println("Please Enter longitude(should be negative):");
		BigDecimal lon = getCoordinates();
		//lon = checkInput(lon);
		//System.out.println(lon);
		getWeatherDataForInputValues(lat,lon);
		
	}
//	private static BigDecimal checkInput(BigDecimal lon){
//		if(lon.compareTo(BigDecimal.ZERO) >= 0){
//
//			System.out.println("Please Enter valid longitude(should be negative):");
//			lon = getCoordinates();
//			checkInput(lon);
//		}
//		return lon;
//	}
	
	private static BigDecimal getCoordinates(){

		Scanner scanInput = new Scanner(System.in);
		return (BigDecimal) scanInput.nextBigDecimal();
	}
	
	//This function converts the received data into to xml document
	private static Document convertStringToDocument(String xmlStr) {
        DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();  
        DocumentBuilder builder;  
        try  
        {  
            builder = factory.newDocumentBuilder();  
            Document doc = builder.parse( new InputSource( new StringReader( xmlStr ) ) ); 
            return doc;
        } catch (Exception e) {  
            e.printStackTrace();  
        } 
        return null;
    }
	
	//This function extracts the data from the xml
	private static String getValuesFromDom(Document doc, XPath xpath, String typeAttr) {				// Function definition to get the value of POP12
       
		String attrValue = null;
        try {
            XPathExpression xpathExpression = xpath.compile("/dwml/data/parameters/"+typeAttr+"/value/text()");
            attrValue = (String) xpathExpression.evaluate(doc, XPathConstants.STRING);
            
        } catch (XPathExpressionException e) {
            e.printStackTrace();
        }
        if(attrValue.equals(null)||attrValue.equals("")){
        	return "NA";
        }
        return attrValue;
    }
	
	//This function consumes SOAP API for weather details
	private static void getWeatherDataForInputValues(BigDecimal lat, BigDecimal lon) throws RemoteException{
		
		Calendar  time = new GregorianCalendar();				// Pass this as a GregorianCalendar for the Calendar to understand
		time.setTime(new Date());
		System.out.println("Fetaching data from SOAP Web Service... Please wait");
		String result = proxy.NDFDgen(lat,lon,"time-series",time,time,"e",wp);
		Document dom= convertStringToDocument(result);
		try{
			//Displaying the result on the output screen
			XPathFactory xpathFactory = XPathFactory.newInstance();
			XPath xpath = xpathFactory.newXPath();
			System.out.println("Minimum Temperature: "+getValuesFromDom(dom,xpath,"temperature[@type='minimum']")); //print the minimum temp
			System.out.println("Maximum Temperature: "+getValuesFromDom(dom,xpath,"temperature[@type='maximum']")); // print the maximum temp
			System.out.println("Wind Direction: "+getValuesFromDom(dom,xpath,"direction")); // print the wind direction
			System.out.println("Wind Speed: "+getValuesFromDom(dom,xpath,"wind-speed")); // print the wind speed
			System.out.println("Temperature Dew point: "+getValuesFromDom(dom,xpath,"temperature[@type='dew point']")); // print the dew point temperature
			System.out.println("12 Hour Probability of Precipitation:"+getValuesFromDom(dom,xpath,"probability-of-precipitation"));
			String command = isRefreshed();
			if(command.trim().toLowerCase().equals("yes")){
				
				getWeatherDataForInputValues(lat,lon);
			}
			
		}catch(Exception e) {
			e.printStackTrace();
		}
	}
	
	//This function asks the user, if he/she wants to refresh the request
	private static String isRefreshed(){
		Scanner scanInput = new Scanner(System.in);
		System.out.println("Do you want to Refresh");
		System.out.println("Please Enter yes if you want to refresh else enter No");
		String command = scanInput.next();
		return command;
		
	}
}