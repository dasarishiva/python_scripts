#from builtins import input
import getpass 
import pyodbc
#from unittest.mock import _return_values

def get_details_from_db(email, db_server, default_db, sql_login, sql_pwd):
    import pyodbc
    from pprint import pformat
    #from test import test_urllib_response
        
    con = pyodbc.connect('DRIVER={SQL Server};SERVER='+db_server+';DATABASE='+default_db+';UID='+sql_login+';PWD='+sql_pwd)
    #con = pyodbc.connect('Trusted_Connection=yes', driver = '{SQL Server}',server = 'db_server', database = 'db_name')
    #print('======>'+email+'<======')
    cur = con.cursor()
    querystring = """ select * from table where email = '"""+email+'\''
       
    cur.execute(querystring)
    res,res1,res2 = '','',''
    counter=0
    for row in cur:
            res1 = res1 + ', '.join(map(str,row))+'\n'
            counter+=1
    res1 = str([column[0] for column in cur.description]) +'\n'+res1
    header = '\n'+email+'\n--------------------------------\n\n'
    if(counter>0):
        msg = str(counter)+' email address entries found: \n'
        res1 = header + msg + res1
    else:
        res1 = header + 'No email address entries found. \n'
           
    
    querystring = """ select * from table where email = '"""+email+'\''
        
    cur.execute(querystring)
    counter=0
    for row in cur:
            res2 = res2 + ', '.join(map(str,row))+'\n'
            counter+=1
    res2 = str([column[0] for column in cur.description]) +'\n'+res2
    if(counter>0):
        msg = str(counter)+' surveys sent: \n '
        res2 = msg + res2
    else:
        res2 = 'No surveys sent. \n'
    
    
    res = res + '\n\n' + res1 +'\n\n'+ res2 
    con.commit()
    return res


def get_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd):
    from jira import JIRA
    from jira.resources import Issue
    jira = JIRA(basic_auth=(jira_usr, jira_pwd), options={'server':'https://jira.smc.com'})
    issue = jira.issue(jira_rtbf_issue)
    reporter = issue.fields.reporter.displayName
    print("\njira issue is reported by:"+reporter)
    desc = issue.fields.description
    
    import re
    while desc.__contains__("mailto:"):
        desc = desc[0:desc.index("|")]+desc[desc.index("]")+1:len(desc)]
    emails = set(re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", desc))
    emails = list(emails)
    print("\nemails found in the ticket:")
    print(emails)    
    return emails
    

def set_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd, result):
    from jira import JIRA
    from jira.resources import Issue
    jira = JIRA(basic_auth=(jira_usr, jira_pwd), options={'server':'https://jira.smc.com'})
    issue = jira.issue(jira_rtbf_issue)
    jira.add_comment(jira_rtbf_issue, result)
    issue.update(assignee={'name': (issue.fields.reporter.name)})
    issues_lst=[]
    issues_lst.append(issue.key)
    #spint_id 3844 is for 'COMPLETED GDPR Requests'
    jira.add_issues_to_sprint(3844,issues_lst)
    print('success')


def main():
    db_server = 'server_name'
    default_db = 'db_name'
    sql_login = 'sql_login'
    jira_rtbf_issue = input("enter jira issue: ").strip()
    jira_usr = getpass.getuser()
    jira_pwd = getpass.getpass(prompt="\nenter password for jira user '"+jira_usr+"' :", stream=None)
    
    emails = get_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd)
    sql_pwd = getpass.getpass(prompt="\nenter password for sql login '"+sql_login+"' to connect db server "+db_server+" :", stream=None)
    result = ''
    for email in emails:
        result = result + get_details_from_db(email, db_server, default_db, sql_login, sql_pwd)
    print(result)
    set_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd, result)
    
    
    prompt = input("\nwould you like to process another ticket? (y/n): ")
    while prompt.strip().lower().__eq__('y'):
            jira_rtbf_issue = input("enter jira issue: ").strip()
            emails = get_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd)
            result = ''
            for email in emails:
                result = result + get_details_from_db(email, db_server, default_db, sql_login, sql_pwd)
            print(result)
            set_jira_rtbf(jira_rtbf_issue, jira_usr, jira_pwd, result)
            prompt = input("\nwould you like to process another ticket? (y/n): ")
        

if __name__ == "__main__":
    main()        

    
