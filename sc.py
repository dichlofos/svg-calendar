#!/usr/bin/python
# coding: utf-8

"""
SVG Calendar
Based on original work of Anatoly Rr (anatoly.rr@gmail.com)
"""

__author__    = "Mikhail Veltishchev <dichlofos-mv@yandex.ru>"
__version__   = "2015"
__date__      = "2015-12-31"
__copyright__ = "(c) 2015, Anatoly Rr, Mikhail Veltishchev"
__license__   = "BSD"


from calendar import Calendar # used in render_month
import sys

class SvgCalendar:

    def __init__ (self,year):

        self.year = year

        font = 'Arial'

        self.style = {
            'units'  : 'mm',

            'width'  : 100,
            'height' : 70,

            'border-color' : '#ccc',

            'year-color' : '#666666',
            'year-padding-top' : 5,
            'year-padding-left': 2,
            'year-font-family' : font,
            'year-font-size'   : 5,

            'month-width'  : 24,
            'month-height' : 21,

            'day-width'  : 23.0 / 7.0,
            'day-height' : 12.0 / 5.0,

            'month-margin-right' : 0,
            'month-margin-bottom' : 0,

            'month-font-family' : font,
            'month-font-size' : 3,
            'month-color' : '#000000',
            'month-padding-top' : 3,

            'month-offset-top' : 5,

            'week-padding-top' : 6,
            'week-font-family' : font,
            'week-font-size'   : 1.5,

            'day-padding-top' : 6,
            'day-font-family' : font,
            'day-font-size'   : 2.5,

            'day-color' : '#000000',
            'day-holiday-color' : '#7f7f7f',

            'week-color' : '#999',
            'week-holiday-color' : '#7f7f7f',
        }


        self.year_name = "0x" + hex(year)[2:].upper()
        self.month_names = [
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь',
        ]
        self.weekdays_names = ['П', '010', '011', '100', '101', '110', '111']
        self.days_names = ["%2d" % (i + 1) for i in range(32)]

        # tuples (month, day)
        self.holidays = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 7), (2, 23), (3, 8), (4, 4), (5, 1), (5, 9), (6, 12), (9, 13), (11, 4)]
        # (4, 4) - Webmasters' Day;  (9, 13) - Programmers' Day

        self.not_holidays = [] # [ (1,11) ]


    def is_holiday(self, month, day, day_of_week):

        if day_of_week in [5, 6]:
            return (month, day) not in self.not_holidays
        return (month, day) in self.holidays


    def render_day(self, x, y, month, day, day_of_week):
        svg = ''
        if self.is_holiday (month, day,  day_of_week):
            color = self.style ['day-holiday-color']
        else:
            color = self.style ['day-color']
        svg += '<g><rect x="%smm" y="%smm" width="%smm" height="%smm" rx="3mm" fill="#fff" stroke="#9f9f9f" stroke-width="0.3mm"/></g>' % (
            x - 0.1*self.style['day-width'],
            y - 0.5*self.style['day-width'],
            self.style['day-width'],
            self.style['day-height'],
        )
        svg += '<text x="%smm" y="%smm" font-family="\'%s\'" font-weight="bold" font-size="%smm" fill="%s" text-anchor="right">' % (
            x + 0.52*self.style['day-width'],
            y + 0.29*self.style['day-width'],
            self.style['day-font-family'],
            self.style['day-font-size'],
            color,
        )
        svg += '%s' % self.days_names [day-1]
        svg += '</text>'
        return svg


    def render_week(self, x, y):
        svg = ''
        svg += '<g>'
        for i in range(7):
            if i < 5:
                color = self.style['week-color']
            else:
                color = self.style['week-holiday-color']
            svg += (
                '<text x="%smm" y="%smm" font-family="\'%s\'" font-size="%smm" text-anchor="middle" fill="%s">' %
                (x + (i + 0.5)* self.style['day-width'],y, self.style['week-font-family'], self.style['week-font-size'], color)
            )
            svg += '%s' % (self.weekdays_names [i])
            svg += '</text>'
        svg += '</g>'
        return svg

    def render_month(self, x, y, month_no):
        svg = ''

        svg += '<g>'
        svg += (
            '<text x="%smm" y="%smm" font-family="\'%s\'" font-weight="bold" font-size="%smm" text-anchor="middle" fill="%s">' %
            (x + self.style['month-width']/2,y+self.style['month-padding-top'], self.style['month-font-family'], self.style['month-font-size'], self.style['month-color'])
        )
        svg += '%s' % (self.month_names [month_no-1])
        svg += '</text>'
        #svg += self.render_week (x, y+self.style['week-padding-top'])

        day_of_week = -1 # will start from Monday
        week_no = 0

        c = Calendar (0)
        for day_no in c.itermonthdays (self.year, month_no):

            day_of_week = (day_of_week + 1) % 7
            if day_of_week == 0:
                week_no += 1

            if day_no == 0:
                continue # month not yet started

            xx = x + self.style['day-width'] * (day_of_week)
            yy = y + self.style['day-padding-top'] + week_no * self.style['day-height']

            svg += self.render_day (xx, yy, month_no, day_no, day_of_week)

        svg += '</g>'
        return svg

    def render_2months(self, x, y, month_no):
        svg = ''
        svg += '<g>'
        for i in range(2):
            xx = 0
            yy = i
            svg += self.render_month(
                x + xx*self.style['month-width'] + xx*self.style['month-margin-right'],
                y + self.style['month-offset-top'] + yy*self.style['month-height'] + yy*self.style['month-margin-bottom'],
                i + 1
            )
        svg += '</g>'
        return svg



    def render_year(self, x, y):
        svg = ''
        svg += '<g>'
        svg += (
            '<text x="%smm" y="%smm" font-family="\'%s\'" font-size="%smm" text-anchor="middle" fill="%s">' %
            (x + self.style['width']/2,y+self.style['year-padding-top'], self.style['year-font-family'], self.style['year-font-size'], self.style['year-color'])
        )
        svg += self.year_name
        svg += '</text>'
        for i in range(12):
            xx = i % 4
            yy = i / 4
            svg += self.render_month(
                x + xx*self.style['month-width'] + xx*self.style['month-margin-right'],
                y + self.style['month-offset-top'] + yy*self.style['month-height'] + yy*self.style['month-margin-bottom'],
                i+1
            )
        svg += '</g>'
        return svg


    def render(self):
        svg = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">'
        svg += (
            '<svg width="%smm" height="%smm" version="1.1" xmlns="http://www.w3.org/2000/svg"><desc>Calendar 2015</desc>' %
            (self.style['width'], self.style['height'])
        )
        svg += (
            '<g><rect x="0" y="0" width="%smm" height="%smm" rx="2.5mm" fill="#fff" stroke="%s" stroke-width="0.5mm"/></g>' %
            (self.style['width'], self.style['height'], self.style['border-color'])
        )
        svg += self.render_month(self.style['year-padding-left'], 0, int(sys.argv[1]))
        svg += '</svg>'
        return svg


if __name__ == '__main__':

    c = SvgCalendar(2015)

    # normal
    if False:
        print c.render()

    # a4
    if True:
        k = 3;
        c.style.update ({
            'units'  : 'mm',

            'border-color' : '#fff',

            'width'  : 270,
            'height' : 210,

            'year-padding-top' : 6 * k,
            'year-padding-left': 2 * k,
            'year-font-size'   : 5 * k,

            'month-width'  : 81 * k ,
            'month-height' : 80 * k,

            'day-width'  : 88.0 * k / 7.0,
            'day-height' : 54.0 * k / 5.0,

            'month-margin-right' : 9,
            'month-margin-bottom' : 1,

            'month-font-size' : 2 * k,
            'month-padding-top' : 3 * k,

            'month-offset-top' : 2 * k,

            'week-padding-top' : 9 * k,
            'week-font-size'   : 1.5 * k,

            'day-padding-top' : 0 * k,
            'day-font-size'   : 3 * k,
        })
        print c.render()

