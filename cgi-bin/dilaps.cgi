#!/usr/bin/python

import cgi
import os
import time
import sys, re
import glob
import geocoder
import cgitb
cgitb.enable()
# example to get image
returnedform = cgi.FieldStorage(keep_blank_values=1)
dictionary = {}


def search_bar():
	return """
	<form class="form-inline" method="POST" style="padding-bottom: 20px">
        <input type="text" name="search_val" class="form-control" style="width:93%" placeholder="Search for anything..." autofocus>
        <input type="submit" name="search_btn" style="float:right" class="btn btn-success" value="Search">
    </form>
    """

def search(term):
	term = str(term).lower()
	print "<b>Search results for '" + term + "'...</b>"
	for jobnumber in dictionary:
		if term in str(jobnumber):
			print job_holder(jobnumber)
		else:
			for item in dictionary[jobnumber]:
				if term in dictionary[jobnumber][item].lower():
					dictionary[jobnumber][item] = dictionary[jobnumber][item].replace(term, "<b>" + term + "</b>")
					print job_holder(jobnumber)
					break;


def page_header():
	return """
	<!DOCTYPE html>
	<html lang="en">
	<head>
	 <meta charset="utf-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>Dilap</title>
	<!-- Bootstrap core CSS -->
	<link href="/css/bootstrap.min.css" rel="stylesheet">
	<!-- Bootstrap theme -->
	<link href="/css/bootstrap-theme.min.css" rel="stylesheet">
	<link href="/css/carousel.css" rel="stylesheet">
	<!-- Sign in theme -->
	<link href="/css/signin.css" rel="stylesheet">
	<!-- Custom styles for this template -->
	<link href="/css/bootstrap-theme.css" rel="stylesheet">
	</head>
	<body style="background-color: white">
	<div class="container" style="background-color: rgba(255,255,255,0.8)">
	<center><img src="https://media.licdn.com/mpr/mpr/shrink_100_100/AAEAAQAAAAAAAALuAAAAJGY3M2Y5OTk4LTZlMDYtNDFjMy05NTJmLTQwNmYzNWQyM2I3MQ.png"><p style="font-size: 20px"><b>A</b>ustralian <b>C</b>onsulting <b>E</b>ngineers</p></center>
	<center style="padding-bottom: 15px">Dilapidation Department</center>
	"""

def page_trailer():
	return """
	</div> <!-- /container -->
	<!-- Bootstrap core JavaScript
	================================================== -->
	<!-- Placed at the end of the document so the pages load faster -->
	<script src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js'></script>
	<script src='/js/bootstrap.min.js'></script>
	<script>
	$('.row .btn').on('click', function(e) {
    e.preventDefault();
    var $this = $(this);
    var $collapse = $this.closest('.collapse-group').find('.collapse');
    $collapse.collapse('toggle');
	});
	
	$("tableX").each(function() {
        var $this = $(this);
        var newrows = [];

        $this.find("tr").each(function(){
            var i = 0;

            $(this).find("td").each(function(){
                i++;
                if(newrows[i] === undefined) { newrows[i] = $(""); }
                newrows[i].append($(this));
            });
        });

        $this.find("tr").remove();
        $.each(newrows, function(){
            $this.append(this);
        });
    });
	</script>

	</html>
	"""

# modify this later...
def job_holder(jobnumber):
	customer = dictionary[jobnumber]['customer']
	address = dictionary[jobnumber]['address']
	notes = dictionary[jobnumber]['notes']

	locator = geocoder.google(address)
	latitude = locator.lat
	longitude = locator.lng
	img = """ <a target="_blank" href="http://maps.googleapis.com/maps/api/staticmap?center=%s,%s&size=600x600&zoom=18&sensor=false&maptype=satellite">%s</a> """ % (latitude, longitude, address)
	if latitude == None:
		img = "<p>%s</p>" % (address)
	
	neighbouringproperties = dictionary[jobnumber]['neighbouringproperties'].split(';')
	councilassets = dictionary[jobnumber]['councilassets'].split(';')
	letters = dictionary[jobnumber]['letters']

	to_return = """
	<table class="table" style="table-layout:fixed; margin: 0">
    <col width="100px" />
    <col width="250px" />
    <col width="250px" />
    <col width="500px" />
    <col width="50px" />
	<tr>
        <td><b>%s</b></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td> 
        <td><p><button class="btn btn-info" data-toggle="collapse" data-target="#viewdetails%s">&#9660;</button></p></td>
    </tr>
    </table>
    <div class="container">
	    <div class="span4 collapse-group">
	        <div class="collapse" style="margin:0" id="viewdetails%s">
	        	<table class="table" id="tableX">
	        	<col width="33" />
	    		<col width="33" />
	    		<col width="33" />
			      <p><span style="float:left"><i>Last Modifed: %s</i></span></p>
			      <thead>
			        <th>Council Assets</th>
			        <th>Neighbouring Properties</th>
			        <th>Letters</th>
			      </thead>
			      """ % (jobnumber, customer, img, notes, jobnumber, jobnumber, time.ctime(os.path.getmtime('jobs/' + jobnumber + '.txt')))
		
	to_return += """
	        <tr>
	        <td>%s</td>
		    <td>%s</td>
			<td>%s</td>
			</tr>
			""" % (neighbouringproperties, councilassets, letters)
	

	to_return += """ </table>
	    	</div>
	    </div>
    </div>
	"""
	return to_return

print page_header()
print search_bar()
print """
	<button class="btn btn-info" style="width: 100%" data-toggle="collapse" data-target="#createjobformdiv">Create Job &#9660;</button>
	<div class="span4 collapse" id="createjobformdiv">
	<form class="form-inline" style="padding-bottom: 20px" method="POST">        
      	<input type="text" name="jobnumber" style="width: 100%"class="form-control" placeholder="######" required autofocus></td>
      	<input type="text" name="customer" style="width: 100%" class="form-control" placeholder="Customer Name" required autofocus></td>
        <input type="text" name="address" style="width: 100%" class="form-control" placeholder="Address" required></td>
		<input type="text" name="councilassets" style="width: 100%" class="form-control" placeholder="Enter Council Assets seperated by a semicolon (';')"></td>
       	<input type="text" name="neighbouringproperties" style="width: 100%" class="form-control" placeholder="Enter Neighbouring Properties seperated by a semicolon (';')"></td>
       	<input type="text" name="letters" style="width: 100%" class="form-control" placeholder="Letters"></td>        
       	<input type="text" name="notes" style="width: 100%" class="form-control" placeholder="Some notes on the job..."></td>
       	<input type="submit" name="createjob" style="width: 100%" class="btn btn-primary" value="Add Job"></td>
    </form>
    </div>
	<table class="table" style="table-layout: fixed; margin: 0; padding-top: 20px">
    <col width="100px" />
    <col width="250px" />
    <col width="250px" />
    <col width="500px" />
    <col width="50px" />
    <thead>
      <tr>
        <th>Job</th>
        <th>Customer</th>
        <th>Address</th>
        <th>Notes</th>
      </tr>
    </thead>
    </table>
    """

searchVar = False
if 'search_btn' in returnedform:
	searchVar = True

if 'createjob' in returnedform:
	if os.path.exists('/jobs/' + returnedform['jobnumber'].value + '.txt'):
		print "File exists"
	else:
		with open('/jobs/' + returnedform['jobnumber'].value + '.txt', 'w') as f:
			f.write('customer: ' + returnedform['customer'].value + '\n')
			f.write('address: ' + returnedform['address'].value + '\n')
			
			if 'notes' in returnedform:
				f.write('notes: ' + returnedform['notes'].value + '\n')
			
			if 'neighbouringproperties' in returnedform:
				f.write('neighbouringproperties: ' + returnedform['neighbouringproperties'].value + '\n')
			
			if 'councilassets' in returnedform:
				f.write('councilassets: ' + returnedform['councilassets'].value + '\n')
			
			if 'letters' in returnedform:	
				f.write('letters: ' + returnedform['letters'].value + '\n')

filesarray = glob.glob('jobs/*.txt')
filesarray.sort(key=os.path.getmtime, reverse = True)

for files in filesarray:
	try:
		with open(files) as f:
			
			jobnumber = re.sub('.*/', '', files)
			jobnumber = re.sub('.txt', '', jobnumber)
			dictionary[jobnumber] = {}
			
			for line in f:
				line = line.strip()
			   
				keyword = line.split(':', 1)[0].strip()
				value = line.split(':', 1)[1].strip()
				
				dictionary[jobnumber][keyword] = value

			if not searchVar:
				print job_holder(jobnumber)

	except EnvironmentError:
		print "Oops! It looks like that job doesn't exist!"

if searchVar:
	search(returnedform['search_val'].value)

print page_trailer()
