# -*- coding: utf-8 -*-
import scrapy
import re
from dateutil.parser import parse as dateParse
from datetime import datetime, timedelta
from scrapy.http import FormRequest
from scrapy.selector.lxmlsel import HtmlXPathSelector
from SWSpider.items import *


class Util(object):

    @classmethod
    def parseFlight(_class, string, date):

        # Remove keywords from flight string
        removeKeywords = ['Departing flight', 'depart', 'arrive',
                          'Change Planes in', 'stop', 'stops', 'Plane Change']
        regex = '|'.join(removeKeywords)
        # Turn into list and filter out blank [""] elements
        infoList = filter(
            lambda el: el != "", re.sub(regex, "", string).split(' '))

        # Parse number of layovers
        stops = int(infoList[4]) if infoList[4] != 'Non' else 0

        # Parse departure and arrival times
        departureDT = dateParse("%s %s" % (date, infoList[2]))
        arrivalDT = dateParse("%s %s" % (date, infoList[3]))

        # If your flight goes past midnight, it must arrive the next day
        if (arrivalDT < departureDT):
            departureDT += timedelta(days=1)

        price = infoList[1].split('$')[-1]

        # Build flight info dict
        flight = {
            'flights': tuple(infoList[0].split('/')),
            'price': price,
            'depDate': departureDT,
            'arrDate': arrivalDT,
            'stops': stops,
        }

        return flight


class SWSpider(scrapy.Spider):
    FORMNAME = "buildItineraryForm"
    name = "sw_spider"
    allowed_domains = ["southwest.com"]
    start_urls = ['http://www.southwest.com/flight/search-flight.html']
    cities = ['GSP', 'FNT', 'BOS', 'OAK', 'LIT', 'BOI', 'SAN', 'DCA', 'LBB',
              'BWI', 'PIT', 'RIC', 'SAT', 'JAX', 'IAD', 'JAN', 'HRL', 'CHS',
              'EYW', 'BNA', 'PHL', 'SNA', 'SFO', 'PHX', 'LAX', 'MAF', 'LAS', 'CRP', 'CMH', 'FLL',
              'DEN', 'DTW', 'BUR', 'ROC', 'GEG', 'BUF', 'GRR', 'BDL', 'DSM', 'EWR',
              'MHT', 'PBI', 'RNO', 'OKC', 'IND', 'ATL', 'ISP', 'SMF', 'BKG', 'PVD',
              'SEA', 'ECP', 'ICT', 'MDW', 'RDU', 'PDX', 'CLE', 'SJU', 'AUS', 'CLT',
              'SJC', 'ELP', 'OMA', 'MEM', 'TUS', 'ALB', 'TUL', 'ORF', 'MKE', 'MSY',
              'MSP', 'CAK', 'TPA', 'DAL', 'DAY', 'ONT', 'STL', 'ABQ', 'HOU', 'SLC',
              'MCO', 'RSW', 'BHM', 'MCI', 'PNS', 'LGA', 'AMA', 'SDF', 'PWM']

    def __init__(self, depCity='SAN', arrCity='LAS', x =0, y =0 ,filename = 'prices'):
        print('Spiding depCity:'+depCity+' arrCity:'+arrCity)
        self.depCity = depCity
        self.depDate = datetime.today() + timedelta(days=1)
        self.arrCity = arrCity
        self.x = x
        self.y = y
        self.filename = filename

    @classmethod
    def lookupCity(_class, cityCode):
        if cityCode in _class.cities:
            return cityCode
        else:
            raise Exception("Invalid city specified.")

    def buildQuery(self, depCity, arrCity):
        """Build the POST query string for searching flights."""
        queryData = {}
        queryData["transitionalAwardSelected"] = "false"
        queryData["twoWayTrip"] = "false"
        queryData["adultPassengerCount"] = "1"
        queryData["seniorPassengerCount"] = "0"
        queryData["outboundTimeOfDay"] = "ANYTIME"
        queryData["fareType"] = "DOLLARS"
        queryData["originAirport"] = self.lookupCity(depCity)
        queryData["destinationAirport"] = self.lookupCity(arrCity)
        queryData["outboundDateString"] = self.depDate.strftime("%m/%d/%Y")
        queryData["awardCertificateToggleSelected"] = "false"
        return queryData

    def parse(self, response):
        queryData = self.buildQuery(self.depCity,self.arrCity)
        return [FormRequest.from_response(response, formdata=queryData, formname=self.FORMNAME, callback=self.parseFlights)]

    def parseFlights(self, response):
        errors = response.xpath("//ul[@id='errors']/li/text()")
        # Catch errors given by Southwest's page
        if (len(errors) > 0):
            print("Error:"+self.depCity+" "+self.arrCity)
            return

        xpath = "//table[@id='faresOutbound']/tbody/tr"

        sels = response.xpath(xpath)
        for sel in sels:
            flight = Flight()
            flight['filename'] = self.filename
            flight['depCity'] = self.depCity
            flight['arrCity'] = self.arrCity
            flight['depDate'] = self.depDate
            flight['x'] = self.x
            flight['y'] = self.y
            priceXpath = "td[contains(@class,'price_column')]//div[@class='product_info']/input/@title"
            for priceString in sel.xpath(priceXpath).extract():
                if (priceString[0] == 'D'):
                    flightData = Util.parseFlight(
                        priceString, self.depDate.date())
                    for key in flightData:
                        flight[key] = flightData[key]
                else:
                    continue
            yield flight
