import time
import csv
from bs4 import BeautifulSoup
import bs4
import requests
import re
from datetime import date
from datetime import datetime

HTML = """
<!DOCTYPE html>
<html>
    <head>
    </head>
    <body width="100%" style="padding: 0; margin: 0;background-color: #007da3;">
        <center class="wrapper" style="width: 600px;margin: auto;table-layout: fixed;background-color: white;border-style: solid;border-color: #007da3;border-width: 20px;padding-bottom: 20px;">
            <div class="webkit" style="max-width: 600px;background-color: white;">
                <table class="outer" align="center" cellspacing="0" cellpadding="0" border="0" style="background-color: white;max-width: 600px;border-spacing: 0;font-family: Arial, Helvetica, sans-serif;color: #4a4a4a;">

                    <tr>
                    <td colspan="3">
                    <table align="center" cellspacing="0" cellpadding="0" border="0">
                        <tr>
                            <td style="background-color: white; justify-content: center; text-align: center; width:100%;">
                                <a href="#">
                                <img alt="img" src="data:image/png;base64,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

                                BJRU5ErkJggg==" />
                                
                                </a>
                            </td>
                        </tr>
                    </table>
                    </td>
                    </tr>
                    

                    <tr>
                        <td>
                            &nbsp
                        </td>
                        <td style="background-color: white; border: solid; border-color: #cacaca; width: 90%;">
                            <table cellspacing="0" cellpadding="0" border="0" style="justify-content: center;
                             border-spacing: 0; height: 400px; width: 100%; border-collapse: collapse;">
                                <tbody style="height:100%; width: 100%">
                                    <tr>
                                        <td height="20px" colspan="3">
                                            &nbsp
                                        </td>
                                    </tr>
                                    <tr>
                                        <td colspan="3">
                                            <table align="center" cellspacing="0" cellpadding="0" border="0" style="width: 100%;">
                                                <tr>
                                                    <td style="text-align: center; color: #007da3; font-size: 20px; justify-content: center;">
                                                        UPCOMING COURSES 
                                                    </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>

                                    <tr>
                                        <td height="20px" colspan="3">
                                            &nbsp
                                        </td>
                                    </tr>

                                    {0}                         

                                    <tr>
                                        <td height="10px" colspan="3">
                                            &nbsp
                                        </td>
                                    </tr>

                                </tbody>
                            </table>
                        </td>

                        <td>
                            &nbsp
                        </td>

                    </tr>

                    <tr height="20px">
                        <td>
                            &nbsp
                        </td>
                    </tr>


                    
                    
                    <tr>
                        <td>
                            &nbsp &nbsp &nbsp &nbsp 
                        </td>
                        <td style="background-color: white;  border: solid; border-color: #cacaca;">
                          <table border="0" cellspacing="0" cellpadding="0" style="justify-content: center;
                           width: 100%;">

                            <tr height="20px">
                                <td colspan="5" style="border: 0;">
                                    &nbsp
                                </td>
                            </tr>

                            <tr>
                            <td>
                                &nbsp &nbsp &nbsp &nbsp &nbsp 
                            </td>
                            <td align="center" style="border-radius: 3px; border: 0;" bgcolor="#007da3">
                                <a href="http://www.healthstream.com/HSAPP/CourseCatalog?categoryId=5328ee1b-3683-e111-9dc1-001517135351&recordsPerPage=20%C2%A4tPage=1&CategoryName=MGH%20Research&showFilterModal=True&IsCategoryCollapsed=True&courseCatalogSortType=BestMatch&recordsPerPageForRecommendation=0%C2%A4tPageForRecommendation=1&isFromSearch=False" target="_blank" style="font-size: 14px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; text-decoration: none;border-radius: 2px; padding: 6px 8px; border: 2px solid #007da3; display: inline-block; margin:0px 14px 0px 14px;letter-spacing: 0.5px;">Online Courses</a>
                            </td>
                            <td>
                                &nbsp &nbsp &nbsp  &nbsp &nbsp 
                            </td>
                              <td align="center" style="border-radius: 3px; border: 0;" bgcolor="#007da3">
                                <a href="https://learn.partners.org/org/mgh-research-institute/date/" target="_blank" style="font-size: 14px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; text-decoration: none;border-radius: 2px; padding: 6px 8px; border: 2px solid #007da3; display: inline-block; margin:0px 14px 0px 14px; letter-spacing: 0.5px;">Live Webinar</a>
                            </td>
                            <td>
                                &nbsp &nbsp &nbsp  &nbsp &nbsp 
                            </td>
                            </tr>

                            

                            <tr>
                                <td colspan="5" style="text-align: center; padding-top: 20px;">
                                    Questions? Visit our <a href="https://www.massgeneral.org/research/division-clinical-research/" target="_blank">DCR Website</a> | <a href="https://www.massgeneral.org/research/division-clinical-research/centers-units-and-faculty/" target="_blank">Resources</a> | <a href="mailto:dcredu@partners.org" target="_blank">Email</a>
                                </td>
                            </tr>

                            <tr height="20px">
                                <td colspan="5" style="border: 0;">
                                    &nbsp
                                </td>
                            </tr>

                          </table>
                        </td>
                        <td>
                            &nbsp &nbsp &nbsp &nbsp
                        </td>
                      </tr>

                      <tr height="20px">
                        <td>
                            &nbsp
                        </td>
                    </tr>
                </table>
                
            </div>

        </center>
    </body>
</html>                    
"""




FORMAT_STRING = """<tr>
                                        <td>
                                            &nbsp &nbsp &nbsp &nbsp
                                        </td>
                                        <td>
                                            <table align="center" cellspacing="0" cellpadding="0" border="0" style="table-layout: fixed; width: 90%;">


                                                <tr>
                                                    <td height="10px">
                                                    <hr />
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td style="font-size: 16px; text-align: left; color: #007da3;">
                                                        {0}
                                                    </td>
                                                </tr>

                                                <tr>
                                                    <td height="10px">
                                                        &nbsp;
                                                    </td>
                                                </tr>



                                                <tr>
                                                    <td  style="font-size: 14px;">
                                                        <b>Speaker:</b> {1}
                                                </tr>
                
                                                <tr>
                                                    <td style="font-size: 14px;">
                                                        <b>When:</b> {2}
                                                    </td>
                                                </tr>
                                                <tr>
                                                    <td style="font-size: 14px;">
                                                        <b>Location:</b> {3}
                                                    </td>
                                                </tr>


                                                <tr>
                                                    <td>
                                                        <table>
                                                            <tr>
                                                                <td align="center" style="border-radius: 3px;" bgcolor="#007da3">
                                                                    <a href="{4}" target="_blank" style="font-size: 12px; font-family: Helvetica, Arial, sans-serif; color: #ffffff; text-decoration: none; text-decoration: none;border-radius: 2px; padding: 6px 8px; border: 2px solid #007da3; display: inline-block;letter-spacing: 0.5px;">Register Now</a>
                                                                </td>
                                                            </tr>
                                                        </table>
                                                    </td>      
                                                </tr>
                                                
                                            </table>
                                        </td>
                                        <td>
                                            &nbsp &nbsp &nbsp &nbsp &nbsp
                                        </td>
                                    </tr>"""

#@param: course content filled with unneccessary whitespace and newlines
#@return: course content without unneccesary whitespace or newlines
def clean_content(text):
    text = text.split()
    text = ' '.join(text)
    return text

def extract_source(url):
     agent = {"User-Agent":"Mozilla/5.0"}
     source=requests.get(url, headers=agent).text
     return source


#@param: source - html code for webpage with list of upcoming courses 
#@return - a list of the URLs of each individual course
def get_course_links(source):
    flag = 0
    soup=bs4.BeautifulSoup(source, 'lxml')
    links = soup.findAll('div', {'onclick': re.compile('/courses/')})
    links_list = []
    for i in links:
        link = i['onclick'][22:-2]
        href = 'https://learn.partners.org' + link
        if is_same_day(extract_source(href), href) and flag == 0:
            continue
        flag = 1
        links_list.append(href)
        if len(links_list) == 3:
            break
        

    #info = soup.findAll('div', {'class': re.compile('contents container')})
    #for i in info:
    #    print(i.contents[6].get_text())
    #    print(1)
    return links_list



#@param: source - html code for webpage with list of upcoming courses 
#@return: a list of the following course attributes in this format:
#[0] - the course name
#[1] - the course speaker
#[2] - date of the course
#[3] - location of where the course takes place
#[4] - the course URL
#if there is no speaker listed in the course page then the return list will not include a speaker name
#if the course takes place the same day as TODAY then returns None
def get_course_attributes(source, url):

    table_index = 0
    soup=bs4.BeautifulSoup(source, 'lxml')

    course_name = soup.findAll('h2', {'class': 'course-name'})
    course_name = clean_content(course_name[0].get_text())

    speaker = soup.findAll('p')
    speaker_name = ''
    for i in speaker:
        if "Speaker:" in i.get_text():
            speaker_name = i.get_text()[9:]
    when = clean_content((soup.findAll('div', {'class': 'col-12 col-sm-8 col-md-9'}))[0].contents[1].contents[0])
    exact_day = int(re.findall('(\d+),', when)[0])
    
    course_dates = soup.findAll('span', {'class':'d-none d-md-block'})
    for j,i in enumerate(course_dates):
        course_day = clean_content(i.get_text())
        course_day_number = int(re.findall('(\d+),', course_day)[0])
        if exact_day == course_day_number: #checking if the date on list is same as date on title
            course_date = course_day
            table_index = j
            break
        #print(1)
    #course_date = clean_content(course_date[0].get_text())

    meeting_time = soup.findAll('td', {'class':'d-none d-md-table-cell'})
    meeting_time = clean_content(meeting_time[table_index].get_text())
    

    when = course_date + ' | ' + meeting_time

    location = "Zoom"

    if speaker_name == '':
        return [course_name, 'MGH Division of Clinical Research', when, location, url]
    else:
        return [course_name, speaker_name, when, location, url]

#driver function for this whole program
def generate_html():
    output_strings = []
    page_url = "https://learn.partners.org/org/mgh-research-institute/date/"

    links_list = get_course_links(extract_source(page_url))

    attr_list = []

    for link in links_list:

        attr = get_course_attributes(extract_source(link), link)
        attr_list.append(attr)

    for entry in attr_list:
        output_strings.append(FORMAT_STRING.format(entry[0], entry[1], entry[2], entry[3], entry[4]))
    output_string = " ".join(output_strings)
    output = HTML.format(output_string)
    with open("test.html", "w") as doc:
        doc.write(output)
    return
    
#removes same-day courses
def is_same_day(source, url):
    soup=bs4.BeautifulSoup(source, 'lxml')
    when = clean_content((soup.findAll('div', {'class': 'col-12 col-sm-8 col-md-9'}))[0].contents[1].contents[0])
    exact_day = int(re.findall('(\d+),', when)[0])
    today = date.today()
    if exact_day == today.day:
        return True


        
generate_html()
    




#page_url = "https://learn.partners.org/org/mgh-research-institute/date/"

#course_url = "https://learn.partners.org/courses/5644/"

#get_course_attributes(extract_source(course_url), course_url)

