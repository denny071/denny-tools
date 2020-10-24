import os
import json

writeProjectJsonPath = "/Users/denny/Library/Application Support/Code/User/globalStorage/alefragnani.project-manager/projects.json"
projectDirList = [
    "/Users/denny/Documents/GitHub/",
    "/Users/denny/Documents/Gitee/",
    # "/Users/denny/Documents/Gitlab/",
    # "/Users/denny/Documents/Code/",
    "/Users/denny/Documents/Go/src/@go",
    ]
 
projectJson = []
 
for projectDir in projectDirList:
    items = projectDir.rsplit("@",1)
    projectDir = items[0]
    displayName = projectDir.rsplit("/",2)[1] if len(items) == 1 else items[1];
   
    for projectName in os.listdir(projectDir):
        if os.path.isdir(os.path.join(projectDir + projectName)):
            projectJson.append({"name":"<"+displayName+">"+ projectName,"rootPath":projectDir + projectName,"paths":[],"group":displayName,"enabled":True})
with open(writeProjectJsonPath,"w") as file_object:
    file_object.write(json.dumps(projectJson,indent=4))


 