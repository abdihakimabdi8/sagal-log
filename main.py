#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
home_page = open('homepage.html').read()
def code(lineHaul, fuelAdvance):
    brokerCommission = lineHaul*(float(.10))
    netOfCommision = lineHaul -int(brokerCommission)
    netHaul = netOfCommision - fuelAdvance
    return netHaul
def netPayForm(netpay):
    netPay = "<div id='net'> Net Pay<form method='post'><textarea>"+ netpay +"</textarea></form></div>"
    return netPay
class MainHandler(webapp2.RequestHandler):

    def get(self):

        content =  "<div id='forms1'><form method='post'><label>Load Number</label><br><input type='number'><br><label>Description</label><br><input type'number'><br><label>Line Haul Pay</label><br><input type='number' name='lineHaul' ><br><label>Fuel Advance </label><br><input type='number' name='fuelAdvance'><p><div class='continueform'><button><input type='submit' name='continue'></button></div></p></form></div>"
        header = home_page
        continuebutton = "<div id='continueform'><button type='Submit' name='continue'>Continue</button></div>"
        self.response.write( header + content)
    def post(self):
        lineHaul = int(self.request.get("lineHaul"))
        fuelAdvance = int(self.request.get("fuelAdvance"))
        net_pay = code(lineHaul, fuelAdvance)
        contentTwo = netPayForm(str(net_pay))
        contentOne = "<div id='forms1'><form method='post'><label>Load Number</label><br><input type='number'><br><label>Description</label><br><input type'number'><br><br><label>Line Haul Pay</label><br><input type='number' name='lineHaul' ><br><label>Fuel Advance </label><br><input type='number' name='fuelAdvance'></form></div>"
        continueForm = "<div id='continueform'>Continue</div>"
        self.response.write(home_page + contentOne + contentTwo + continueForm)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
