# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import openpyxl as xl
from flask import Flask, render_template, jsonify, Response, request

app = Flask(__name__)




#Allows user to search for qualification and returns a dictionary
def Handle_Search(qualifications, course_name):

    if len(qualifications) <= 1:
        print('University does not have any qualifications available at the moment')
        return

    if len(course_name)== 0:
        print('type in a course')
        return

    mylist = list(qualifications[1:])

    #creating a dictionary which stores the related searched qualifications
    dic = {'Qualification': [], 'Module': [], 'Future_Skill_Module': [], 'Worthy': []}

    search_query = course_name.lower()  # searching for anything related to computers
    for x in mylist:
        checkvalid = False
        for y in x:
            if search_query in str(y).lower():
                checkvalid = True

        #accesing each column of the excel file to search for the user's keyword
        if checkvalid == True:
            dic['Qualification'].append(x[0])
            dic['Module'].append(x[1])
            dic['Future_Skill_Module'].append(x[2])
            dic['Worthy'].append(x[3])

    return dic

def convert_to_series(dic):
    # converting dic to series to make info easier to read

    QualName = pd.Series(dic['Qualification'], name='Qualification')
    ModName = pd.Series(dic['Module'], name='Module')
    SkillName = pd.Series(dic['Future_Skill_Module'], name='Future_Skill')
    worth = pd.Series(dic['Worthy'], name='Worth')

    University_df = pd.concat([QualName, ModName, SkillName, worth], axis=1)
    print(University_df)

    return University_df

#must take the varsity the user selected as parameter
def Prepare_data(university, course_name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

    modules_df = xl.load_workbook("./resources/University Modules.xlsx")
    user_varsity = university.upper()
    mdf_sheet = modules_df[user_varsity]
    qualifications = list(mdf_sheet.values)


    #handling user's search
    dic = Handle_Search(qualifications, course_name)

    #Converting dictionary to a series
    convert_to_series(dic)

    return dic

@app.route('/')
def index_view():
    return render_template('FrontEnd1.html')

@app.route('/templates', methods=['GET','POST','DELETE'])
def my_form_post():
    course = request.form.get('course')
    varsity = request.form.get('varsity')

    processed_text = Prepare_data(varsity,course)

    print(processed_text)

    return render_template('index.html', course=processed_text, len=len(processed_text['Qualification']))
    #return processed_text

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #Prepare_data('PyCharm')
    app.run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
