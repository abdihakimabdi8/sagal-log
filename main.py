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
def netPayForm (net_pay):

    net_payForm =   "<form method='post'><label>Net Pay  <textarea name='lineHaul' >" + net_pay + "</textarea></form>"
    return net_payForm
def forms(fuel_advan_amount):
    fuel_advance = "<form method='post'><label>Message  </label><textarea name='message' cols='' rows=''>" + textarea_content + "</textarea></form>"
    return fuel_advance
def code(lineHaul, fuelAdvance):
    brokerCommission = lineHaul*(float(.10))
    netOfCommision = lineHaul -int(brokerCommission)
    netHaul = netOfCommision - fuelAdvance
    return netHaul

class MainHandler(webapp2.RequestHandler):

    def get(self):

        header =  " <h2><div id='name'><ul><li>Sagal Logistics LLC</li><li>Sign In</li></ul></div></h2>"
        contentOne= "<div id='chooser'><strong>Process Load Payment</strong></div>"
        contentTwo =  "<form method='post'><div id='forms'><ul class='operation' style='list-style-type:none'><li>Owner-Operator</li><li>Driver</li></ul></div><div id='forms1'><ul class='amount' style='list-style-type:none'><li>Date<form method='post'><br><input type='number'></form></li><br><li>Load Number<form method='post'><input type='number'></form></li><br><li>Description<form method='post'><input type='number'></form></li><br><li>Line Haul<form method='post'><input type='number' name='lineHaul'></form></li><br><li>Fuel Advance<form method='post'><input type='number' name='fuelAdvance'></form></li><br><form><input type='Submit'></form></li><br></ul><div id='net'>Net Pay<form method='post'><input type='number'></form></div></form>"
        self.response.write( header + contentOne + contentTwo)
    def post(self):
        lineHaul = int(self.request.get("lineHaul"))
        fuelAdvance = int(self.request.get("fuelAdvance"))
        net_pay = code(lineHaul, fuelAdvance)
        content = netPayForm(str(net_pay))
        header = " <h2><div id='name'><ul><li>Sagal Logistics LLC</li><li>Sign In</li></ul></div></h2>"
        contentOne= "<div id='chooser'><strong>Process Load Payment</strong></div>"
        self.response.write(header + contentOne + content)
app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
