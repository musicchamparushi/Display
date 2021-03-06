import webbrowser,os,sys

d = sys.argv[1]

#storing chat file location in a variable
for file in os.listdir(sys.argv[1]):
	if file.endswith(".txt"):
		d=os.path.join(d,file)

#file reading

fp=open(d,"r")
a=fp.read()

name1=""

template = '''<html>

<head>
<title>Your whatsapp chat</title>
<style>

li.b {
	text-align:right;
}

.date {
	border: 1px solid black;
	padding: 3px;
	text-align: center;
}

li.c {
	text-align:left;
	
}

li {
	margin-bottom: 14px;
}

span.c {
	box-shadow: 0 0 2px;
	border-width: thin;
	border-radius:6px;
	padding:5px;
	
	border-color:white;
}

span.time{
		font-size:10px;
		margin-left:6px;
}
span.b{

	border:1px solid;
	border-width: thin;
	border-radius:6px;
	padding:5px;
	border-color:rgb(214,248,183);
	box-shadow: 0 0 2px;
	background-color: rgb(214,248,183);
}
</style>
</head>
<body>
<ul style="list-style-type:none">
%s
</ul>
</body>
</html>
'''
date=""
lis = ""
img=""

lines=a.split("\n")
line1=lines[0]

#extract name of first person
name1=line1.split("-")[1:]
name1="-".join(name1)
name1=name1.split(":")[0].strip()

msg=""
time1=""
word=""
img=""

#traversing chat line-wise
for line in lines:
	
	#checking if continued message in new line
	x=line.split("-")[0]
	try:
		x=x.split(",")[1].strip()
		if x[-2:]!="AM" and x[-2:]!="PM":
			msg=msg+ "<br/>" + line
			continue
	except IndexError:
		msg=msg+ "<br/>" + line
		continue
	
	imgtag=""
	
	
	#extracting name of person
	name=line.split("-")[1:]
	name="-".join(name)
	name=name.split(":")[0].strip()

	#class allotment for css
	if (name==name1):
		clas="b"
	else:
		clas="c"

	#extracting date of message and checking if date is new
	date1=line.split(",")[0]
	if (date1!=date):
		date=date1	
		lis += '<li class="date"><span>%s</span></li>' % (date)

	#extracting time
	time1=line.split(",")[1:]
	time1=",".join(time1)
	time1=time1.split("-")[0].strip()

	#extracting message
	word=line.split(":")[2:]
	word=":".join(word).strip()

	#checking for image or video as message
	img=word.split(" ")[0]
	
	if img[0:3]=='IMG' and img[-4:]=='.jpg':
		imgtag='<img src='+os.path.join(sys.argv[1],img)+' width="200px" border="1">'
		imgtag ="<a target='_blank' href=" + os.path.join(sys.argv[1],img) + ">%s</a>" % imgtag
	if img[0:3]=='VID' and img[-4:]=='.mp4':
		imgtag='<video width="320" height="240" controls> \
  						<source src='+os.path.join(sys.argv[1],img)+' type="video/mp4"> \
 				</video>'

	#adding message to list depending on what type of message is it
	t="time"

	#for multiline message
	if msg:
		lis += '<li class=%s><span class=%s>%s<span class=%s>%s</span></span></li>' %(clas,clas,msg,t,time1)
	msg=""

	#for one-line message
	if (imgtag==""):
		lis += '<li class=%s><span class=%s>%s<span class=%s>%s</span></span></li>' %(clas,clas,word,t,time1)
	
	#for image or video message
	else:
		lis += '<li class=%s>%s<span class=%s>%s</span></li>' %(clas,imgtag,t,time1)

#creating html file with require display properties of message
output = template % lis
fp = open("output.html", "w")
fp.write(output)
webbrowser.open_new("file://" + os.getcwd() + "/output.html")
fp.close()
