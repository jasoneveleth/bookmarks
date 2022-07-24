#!/usr/bin/python3
import os

prefix = """
<!DOCTYPEhtml>
<html>
<head>
<title>Bookmarks</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
html {
font-size: 62.5%;
}
body {
max-width: 620px;
margin: 50px auto;
padding: 20px;
font-family: Helvetica, sans-serif;
background-color: #282C34;
color: #FFFFFF;
font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Oxygen-Sans,Ubuntu,Cantarell,"Helvetica Neue",sans-serif;
}
h1 {
cursor: pointer;
margin: 0;
font-size: 2.2rem;
color: inherit;
display: inline-block;
}
h1:hover {
margin: -1px;
border: 1px solid #FFFFFF;
border-radius: 5px;
}
a {
color: inherit;
font-family: inherit;
text-decoration: none;
font-family: Helvetica, sans-serif;
font-size: 2.2rem;
}
a:hover {
margin: -1px;
border: 1px solid #FFFFFF;
border-radius: 5px;
}
ul {
color: inherit;
font-family: inherit;
}
li {
margin: 0.66rem 0;
list-style-type: none;
color: inherit;
font-family: inherit;
}
iframe{
transform:translate(-101%, -50%);
display:none;
position:absolute;
border:2px solid #E5C07B;
width:320px;
height:180px;
}
.button {
    margin: auto;
    background-color: rgba(40, 44, 52, 0.4);
    border-style: solid;
    border-color: #fff;
    text-align: center;
    letter-spacing: 0.2em;
    font-weight: bold;
    font-size: 1.2rem;
    width: fit-content;
    text-transform: uppercase;
    padding: 0.8rem;
    display: block;
    cursor: pointer;
}
.button:hover {
    background-color: #fff;
    color: #282C34;
}
</style>
</head>
<body>
<div class="button" onClick="togglePreview()">Toggle Preview On</div>
<ul>
"""

path = "$HOME/src/bookmarks/"
path = os.path.expandvars(path)
m = open(f'{path}input.md', 'r')
h = open(f'{path}bookmarks.html', 'w')
h.write(prefix)
l = []
for line in m.readlines():
    if line[0] == '[':
        title = line.split(']')[0][1:]
        link = line.split('(')[-1][:-2]
        line = "<li><a href=\"" + link + "\" onmouseover=\"preview(this)\" onmouseout=\"reset(this)\">" + title + "</a></li>"
    elif line == '\n':
        l.pop()
        line = '</li></ul>'
    else:
        l.append(0)
        line = '<li><h1 onClick="toggle(this)">&#9654 ' + line[:-1] + '</h1><ul style=\'display:none\'>'
    h.write(line + '\n')

postfix = """
</ul>
</li>
</ul>
<script>
let t;
let hoverTime = 500;
let showPreview = false;

function togglePreview() {
state = showPreview ? 'on' : 'off'
showPreview = !showPreview
document.getElementsByClassName('button')[0].innerText = 'Toggle Preview ' + state
}

function preview(ele) {
if (showPreview) {
t = setTimeout(makeFrame, hoverTime, ele);
}
}

function makeFrame(ele) {
if (ele.href.slice(12,19) === "youtube") {
return;
} else if (ele.children.length === 0) {
frame = document.createElement('iframe');
frame.src = ele.href;
ele.appendChild(frame);
} else {
frame = ele.children[0]
}
frame.style.display = "block";
}

function reset(ele) {
if (showPreview) {
clearTimeout(t);
if (ele.children.length !== 0) {
frame = ele.children[0];
frame.style.display = "none";
}
}
}

function toggle(ele) {
children = Array.from(ele.parentNode.children).slice(1);
if (children.length == 0) {
return;
}
attr = (children[0].style.display === "none") ? "block" : "none";
for (child of children) {
child.style.display = attr;
}
ele.innerText = ((children[0].style.display === "none") ? String.fromCharCode(9654) : String.fromCharCode(9660)) + ele.innerText.slice(1)
}
</script>
</body>
</html>
"""

h.write(postfix)

print('created bookmarks.html')
if "y" == input("do you want to overwrite index.html (y/N) "):
    os.remove(f'{path}index.html')
    os.rename(f'{path}bookmarks.html', f'{path}index.html')
    print("moved bookmarks.html to index.html")

