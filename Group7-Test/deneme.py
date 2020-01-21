import os
import xml.etree.ElementTree as ET
import json
import requests
import shutil
import subprocess


data = json.loads(testData)
address = data["repository_url"]
git_id = data["github_login"]
git_pass = data["github_password"]
target_pass = data["targetPswd"]
addressClone = address.replace("https://","https://"+git_id+":"+git_pass+"@")
#New attribute
buildFolder = data["forBuild"]
projectName = data["project_name"]

#Clone dilen directory name bulmak icin yapiyoruz
cloneDirectoryName = subprocess.check_output(['basename', addressClone, ".git"])
cloneDirectoryName = cloneDirectoryName[:-1]
#Bize verilecek örnek repo adresi (direk pom.xml içinde)
#https://github.com/canerkarakas/GtuDevOps
#Updating project dir
#Ornek icin asagidaki concat islemi su path'i verir: GtuDev/Deneme12/SumNumbers-master
projectFolder = cloneDirectoryName+"/"+projectName+"/"+buildFolder
def start_testing():
    print("Project Name: "+projectName)
    print("Cloning Repo...")
    os.system("pwd")
    os.system("git clone "+addressClone+ " osman")
    filePath = subprocess.check_output(["pwd"])
    filePath = filePath[:-1]
    #Project ve pom.xml olan dizine giriliyor
    os.chdir(projectFolder)
    print("Cloned into:")
    os.system("pwd")
    print("Maven Test Starting...")
    #Test basliyor
    os.system("mvn test")
    path = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(path, os.pardir)))

def parse_result():
    filePath = subprocess.check_output(["pwd"])
    filePath = filePath[:-1]
    #Tekrardan report olan folder'a giriliyor. Eger hata varsa print ile dogru path'i ekleyin.
    filePath = filePath+"/"+buildFolder+"/target/surefire-reports"
    for filename in os.listdir(filePath):
        if not filename.endswith('.xml'): continue
        fullname = os.path.join(filePath, filename)
        tree = ET.parse(fullname)
    root = tree.getroot()
    return root

def create_json():
    global address
    if parse_result().attrib["failures"] != "0":
        data = {}
        data["origin"] = 7
        data["destination"] = 2
        data["git_id"] = git_id
        data["git_pass"] = git_pass
        data["testresult"] = "fail"
        data["deployment"] = "nodeploy"
        data["forBuild"] = buildFolder
        data["projectName"] = projectName
        data["targetPswd"] = target_pass
        data["repoUrl"] = address
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
        data["git_id"] = git_id
        data["git_pass"] = git_pass
        data["testresult"] = "success"
        data["deployment"] = "deploy"
        data["forBuild"] = buildFolder
        data["projectName"] = projectName
        data["targetPswd"] = target_pass
        data["repoUrl"] = address
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
    os.chdir("..")
    filePath = subprocess.check_output(["pwd"])
    filePath = filePath[:-1]
    if os.path.exists(filePath) and os.path.isdir(filePath):
        shutil.rmtree(filePath)

start_testing()
parse_result()
create_json()
delete_test_env()
