# Queries padctn to get current tax appraisal on properties

# table schema:
# Properties
# street, parcelID, 2012app, scraped

# Appraisal2013
# owner, street, zip, dist, parcelID, lastsaleprice, lastsaledate, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures

import scraperwiki
import lxml.html
import lxml.etree
import re
import resource
import xlrd
import cookielib, urllib2

from sys import exit
import geopy.geocoders
import geopy.distance

def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?",
        lambda mo: mo.group(0)[0].upper() +
            mo.group(0)[1:].lower(),
        s)

def getAppraisal(propID,parcelID,address,kenway1):
    try:
    #    print "propID = " + propID + "."
        pageURL = "http://www.padctnwebpro.com/WebproNashville/searchResults.asp?cboSearchType=Parcel&SearchVal1=" + propID
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        html = lxml.html.parse(opener.open(pageURL)).getroot()
    #    print html.text_content()
        links = html.cssselect('a')
        record = lxml.html.parse(opener.open("http://www.padctnwebpro.com/WebproNashville/" + links[0].get('href'))).getroot()
    #    print "link: " + links[0].get('href')
    #    print "record html: " + record.text_content()
        taxcard = lxml.html.parse(opener.open("http://www.padctnwebpro.com/WebproNashville/RecordCard.asp")).getroot()
    #    print "taxcard html: " + taxcard.text_content()
        fields = taxcard.cssselect('td')
    #    for i in range(0, len(fields)):
    #        print "field[" + repr(i) + "]: " + fields[i].text_content()
    #        if fields[i].text_content().find("Property Owner") > -1:
        owner = titlecase(fields[12].text_content().strip())
    #        if fields[i].text_content().find("Mailing Address") > -1:
        street = address
    #            print "Street address: " + street + "."
    #        if fields[i].text_content().find("Zip") > -1:
        zip = titlecase(fields[35].text_content().strip())
    #        if re.search("Sale Price", fields[i].text_content()) != None:
        lastsaleprice = fields[26].text_content().strip()
    #        if re.search("Most Recent Sale Date", fields[i].text_content()) != None:
        lastsaledate = fields[22].text_content().strip()
    #        if re.search("Total Value", fields[i].text_content()) != None:
        totalval = fields[54].text_content().strip()
    #        if re.search("Land Value", fields[i].text_content()) != None:
        landval = fields[51].text_content().strip()
    #        if re.search("Building Value", fields[i].text_content()) != None:
        impval = fields[56].text_content().strip()
    #        if re.search("Land Area", fields[i].text_content()) != None:
        acres = fields[37].text_content().strip().split()[0]
    #        if re.search("Finished Area", fields[i].text_content()) != None:
        sqft = fields[81].text_content().strip()
    #        if re.search("Year Built", fields[i].text_content()) != None:
        year = fields[71].text_content().strip()
    #        if re.search("Foundation", fields[i].text_content()) != None:
        foundation = titlecase(fields[65].text_content().strip())
    #        if re.search("Siding", fields[i].text_content()) != None:
        siding = titlecase(fields[79].text_content().strip())
    #        if re.search("Number Rooms", fields[i].text_content()) != None:
        rooms = fields[83].text_content().strip()
    #        if re.search("Number Beds", fields[i].text_content()) != None:
        bedrooms = fields[85].text_content().strip()
    #        if re.search("Full Baths", fields[i].text_content()) != None:
        fullbaths = fields[87].text_content().strip()
    #        if re.search("1/2 Baths", fields[i].text_content()) != None:
        halfbaths = fields[91].text_content().strip()
    #        if re.search("Total Fixtures", fields[i].text_content()) != None:
        fixtures = fields[93].text_content().strip()
        print "Saving parcel " + parcelID + " (" + owner + ", " + street + ")."
        geo = geopy.geocoders.GeocoderDotUS()
        dist = 0
        for j in range(1,10):
            try:
                _, coord = geo.geocode(street + ", Nashville, TN")
            except:
                if j == 10:
                    print "Couldn't get geo data for address: " + street
                    dist = 0
                continue
            else:
                try:
                    dist = geopy.distance.distance(kenway1, coord).miles
                except:
                    dist = 0
                break
        apprData = {'owner': owner,
            'street': street,
     #       'zip': zip,
            'dist': dist,
            'parcelID': parcelID,
            'lastsaleprice': lastsaleprice,
            'lastsaledate': lastsaledate,
            'totalval': totalval,
            'landval': landval,
            'impval': impval,
            'acres': acres,
            'sqft': sqft,
            'year': year,
            'foundation': foundation,
            'siding': siding,
            'rooms': rooms,
            'bedrooms': bedrooms,
            'fullbaths': fullbaths,
            'halfbaths': halfbaths,
            'fixtures': fixtures}
        scraperwiki.sqlite.save(unique_keys=["parcelID"], data=apprData, table_name="Appraisal2013")
    except:
        print "Could not get appraisal info for parcelID " + parcelID + " at " + address
            
    # owner, street, parcelID, lastsaleprice, lastsaledate, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures

def trash():
        if re.search("Mailing Address", fields[i].text_content()) != None:
            street = fields[i+1].text_content()
            print "Street address: " + street + "."
        if re.search("Total Value", fields[i].text_content()) != None:
            totalval = fields[i+1].text_content()
        if re.search("Land Value", fields[i].text_content()) != None:
            landval = fields[i+1].text_content()
        if re.search("Building Value", fields[i].text_content()) != None:
            impval = fields[i+1].text_content()
        if re.search("Land Area", fields[i].text_content()) != None:
            acres = fields[i+1].text_content()
        if re.search("Finished Area", fields[i].text_content()) != None:
            sqft = fields[i+1].text_content()
        if re.search("Year Built", fields[i].text_content()) != None:
            year = fields[i+1].text_content()
        if re.search("Foundation", fields[i].text_content()) != None:
            foundation = fields[i+1].text_content()
        if re.search("Siding", fields[i].text_content()) != None:
            siding = fields[i+1].text_content()
        if re.search("Number Rooms", fields[i].text_content()) != None:
            rooms = fields[i+1].text_content()
        if re.search("Number Beds", fields[i].text_content()) != None:
            bedrooms = fields[i+1].text_content()
        if re.search("Full Baths", fields[i].text_content()) != None:
            fullbaths = fields[i+1].text_content()
        if re.search("1/2 Baths", fields[i].text_content()) != None:
            halfbaths = fields[i+1].text_content()
        if re.search("Total Fixtures", fields[i].text_content()) != None:
            fixtures = fields[i+1].text_content()

#street, parcelID, totalval, landval, impval, acres, sqft, year, foundation, siding, rooms, bedrooms, fullbaths, halfbaths, fixtures

def getExcel():
    xlbin = scraperwiki.scrape("http://home.mcgehee.com/MLScomps.xls") 
    book = xlrd.open_workbook(file_contents=xlbin)
    sheet = book.sheet_by_index(0)
    for rownumber in range(0, sheet.nrows):
        print "street: " + repr(sheet.cell_value(rownumber,3))
        propData = {'street': sheet.cell_value(rownumber,3).strip(),
            'parcelID': sheet.cell_value(rownumber,17).strip(),
            'scraped': 0}
        scraperwiki.sqlite.save(unique_keys=["parcelID"], data=propData, table_name="Properties")

def cleanparcel():
    props = scraperwiki.sqlite.select("* FROM Properties")
    for i in props:
        parcelID = i['parcelID'].strip()
        scraperwiki.sqlite.execute("UPDATE Properties SET parcelID = " + parcelID + " WHERE street = '" + i['street'] + "'")
        street = i['street'].strip()
        scraperwiki.sqlite.execute("UPDATE Properties SET street = '" + street + "' WHERE parcelID = " + parcelID)
        scraperwiki.sqlite.commit()
        
def cleanResults():
    scraperwiki.sqlite.execute("DROP TABLE Appraisal2013")
    scraperwiki.sqlite.commit()

def cleanUtil():
    props = scraperwiki.sqlite.select("* FROM Properties WHERE parcelID = '130-04-0-045.00'")
    for i in props:
        scraperwiki.sqlite.execute("UPDATE Properties SET parcelID = '130-04-0-112.00' WHERE street = '" + i['street'] + "'")
        scraperwiki.sqlite.commit

# Main program

#getExcel()
props = {}
#cleanparcel()
#cleanResults()
#cleanUtil()
#scraperwiki.sqlite.execute("UPDATE Properties SET scraped = 0")
#scraperwiki.sqlite.commit()
props = scraperwiki.sqlite.select("* FROM Properties WHERE scraped = 0 ORDER BY parcelID ASC")
geo = geopy.geocoders.GeocoderDotUS()
_, kenway = geo.geocode("2842 Kenway Rd, 37215")


for i in props:
    parcelID = i['parcelID'].strip()
    newID = ''.join(parcelID.split("-"))
    newID = ''.join(newID.split(".")).strip()
    address = i['street'].strip()
    print "Getting 2013 appraised value for parcel " + parcelID + "."
    newApp = getAppraisal(newID, parcelID, address, kenway)
    scraperwiki.sqlite.execute("UPDATE Properties SET scraped = 1 WHERE parcelID = '" + parcelID + "'")
    scraperwiki.sqlite.commit()



