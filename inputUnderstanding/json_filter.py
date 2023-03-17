import json

def json_file_filter_list(file):

    files = []
    results = []
    for line in open(file, 'r'):
        files.append(json.loads(line))
    for f in files:
        w = open("intents.txt", "a")
        w.write(f["intent"])
        w.write(',\n')
    w.close()
        # results.append(f["intent"])
    # return results

    
if __name__ == '__main__':

    #This method will read the value with the name matching with term from json file and return the filtered list
    json_file_filter_list(file='/home/branchleaf/Documents/Projects/project-sara/inputUnderstanding/test.json')
    # print(filter_list)