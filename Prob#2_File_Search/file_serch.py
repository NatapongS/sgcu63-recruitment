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
"""
#jsonObject = ''' {
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
"""

"""
jsonObject = ''' {
    "I" : {
        "_files" : ["her"] ,
        "hate" : {
            "_files" : ["me", "you"] ,
            "hater" : {
                "_files" : ["gonna hate hate hate hate hate"]
            } 
        } ,
        "love" : {
            "_files" : ["you", "adfafdfa", "xx", "xy"]
        }, 
        "hate that" :{
            "_files" : ["weekly cp problems"],
            "I love" : {
                
                "_files" : ["you", "me", "teemo"]
            }
        },
        "Don't want to" : {
            "_files" : ["DIEEEE", "Sometime I wish I never been born at all"],
            ", but I can put" : {
                "_files" : ["on clothes"],
                "nobody else" : {
                    "_files" : ["love me", "like you do"],
                    "aboves" : {
                        "_files" : ["you", "me", "pizza"]
                    }

                }
            }
        }

    }

}
'''
print(fileSearch("you", jsonObject))
"""