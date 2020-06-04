import json
def is_json(value):
    try :
        json.dumps(value)
        return True
    except:
        return False

def fileSearch(fileToSearch, filesObject):
    thisJson = json.loads(filesObject)
    print(thisJson)
    print('-----')
    pathFound = []
    for key in thisJson:
        if key == '_files':
            if thisJson[key].count(fileToSearch) != 0:
                pathFound.append('/' + fileToSearch)
        else:
            if is_json(thisJson[key]):
                newPathFound = fileSearch(fileToSearch, json.dumps(thisJson[key]))
                for i in range(len(newPathFound)):
                    newPathFound[i] = '/' + key + newPathFound[i]
                pathFound.extend(newPathFound)
    return pathFound

jsonObject = ''' {
    "FolderA": {
    "_files": [ "file1", "file2" ] ,
    "SubfolderC": {
    "_files": [ "file1" ]
    } ,
    "SubfolderB": {
    "_files" : [ "file1" ]
    }
    }
    } 
    '''
print(fileSearch('file1', jsonObject))
