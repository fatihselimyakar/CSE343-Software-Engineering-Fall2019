import os
import xml.etree.ElementTree as ET
import json
import requests
import shutil
import subprocess


data = json.loads(testData)
address = data["repository_url"]
address = address.replace("https://","https://"+data["github_login"]+":"+data["github_password"]+"@")


projectName = subprocess.check_output(['basename', address, ".git"])
projectName = projectName[:-1]

def start_testing():
    print("Project Name: "+projectName)
    print("Cloning Repo...")
    os.system("pwd")
    os.system("git clone "+address)
    filePath = subprocess.check_output(["pwd"])
    filePath = filePath[:-1]
    os.chdir(filePath+"/"+projectName)
    print("Cloned into:")
    os.system("pwd")
    print("Maven Test Starting...")
    os.system("mvn test")
    path = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(path, os.pardir)))

def parse_result():
    path = projectName+"/target/surefire-reports"
    for filename in os.listdir(path):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(path, filename)
        tree = ET.parse(fullname)
    root = tree.getroot()
    return root

def create_json():
    global address
    if parse_result().attrib["failures"] != "0":
        data = {}
        data["origin"] = 7
        data["destination"] = 2
        data["testresult"] = "fail"
        data["repository_url"] = address
        data["failures"] = int(parse_result().attrib["failures"])
        data["cases"] = {}
        data["cases"]["tests"] = parse_result().attrib["tests"]
        data["cases"]["testcase"] = {}
        for testCases in parse_result().findall("testcase"):
            data["cases"]["testcase"][testCases.attrib["name"]] = {}
            data["cases"]["testcase"][testCases.attrib["name"]]["classname"] = testCases.attrib["classname"]
            data["cases"]["testcase"][testCases.attrib["name"]]["teststatus"] = "passed"
            if(testCases.getchildren()):
                data["cases"]["testcase"][testCases.attrib["name"]]["failure"] = testCases.find("failure").attrib["message"]
                data["cases"]["testcase"][testCases.attrib["name"]]["teststatus"] = "failed"
        json_data = json.dumps(data)
        req = requests.post("http://localhost:8081", data= json_data)
        print(json_data)
    else:
        data = {}
        data["origin"] = 7
        data["destination"] = 2
        data["testresult"] = "success"
        data["repository_url"] = address
        data["failures"] = int(parse_result().attrib["failures"])
        data["cases"] = {}
        data["cases"]["tests"] = parse_result().attrib["tests"]
        data["cases"]["testcase"] = {}
        for testCases in parse_result().findall("testcase"):
            data["cases"]["testcase"][testCases.attrib["name"]] = {}
            data["cases"]["testcase"][testCases.attrib["name"]]["classname"] = testCases.attrib["classname"]
            if(testCases.getchildren()):
                data["cases"]["testcase"][testCases.attrib["name"]]["failure"] = testCases.find("failure").attrib["message"]
        json_data = json.dumps(data)
        req = requests.post("http://localhost:8081", data= json_data)
        print(json_data)
        data["destination"] = 3
        json_data = json.dumps(data)
        req = requests.post("http://localhost:8081", data= json_data)
        print(json_data)
def delete_test_env():
    print("Test environment deleting...")
    if os.path.exists(projectName) and os.path.isdir(projectName):
        shutil.rmtree(projectName)

start_testing()
parse_result()
create_json()
delete_test_env()

