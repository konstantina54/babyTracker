import json




def display_data():
   with open('test.txt', 'r') as file:
    # Read each line in the file
        # df = pd.DataFrame(file)
        # print(df)
    for line in file:
        # print(line)
        data = clean_manual_data(line)
        display_formating(data)



def clean_manual_data(data):
    print(data + "this")
    # start_json = data.find("{")
    # if data.find(", I ") >0:
    #     last_json = data.find("} ")
    #     manual_inputs = data[start_json:last_json]
    # elif data.find(" A") >0:
    #     last_json = data.find(" A")
    #     manual_inputs = data[start_json:last_json]
    # print(manual_inputs)
    data = data.replace("'", '"')
    # manual_inputs = manual_inputs.replace("'", '"')
    activity_data = json.loads(data)
    return activity_data