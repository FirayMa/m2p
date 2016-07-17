import MySQLdb
import pdb
import os
import datetime
from e_mail import EmailEx

try:#OperationalError
        filename = 'mailer_send_email.txt'
        if os.path.isfile(filename):
                log_file = open(filename, 'a')
                        
        else:
                log_file = open(filename, 'w')
                
        
        
        con= MySQLdb.connect(host='localhost',user='root',passwd='sqlroot',db='mapfamily')
        
        msg = ('\n[%s] ----[connected] ---- connected to DB'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p')))
        log_file.write(msg)
        log_file.flush()
        
        cursor =con.cursor()
        
        
                        
        sql ="select * from mailer_lastinfo where is_sent='0'"
        cursor.execute(sql)
        rows=cursor.fetchall()
        
        msg = ('\n[%s] ----[fetchall] ---- fetched all.'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p')))
        log_file.write(msg)
        log_file.flush()

        
        email_instance = EmailEx()

        
        for row in rows:
                id      = row[0]
                 
                days    = int(row[1])-1
                if id == 19:
                        sql_user ="select email from administration_user where id = "+ str(row[4]) #row4 is user id
                        cursor.execute(sql_user)
                        user = cursor.fetchone()
                        
                        sql_l_receivers ="select * from mailer_l_receiver where lastinfo_pk_id= "+ str(id)
                        cursor.execute(sql_l_receivers)
                        rows_l_receivers =cursor.fetchall()
                        #send email
                        try:
                              for receiver in rows_l_receivers:
                                       
                                      email     = receiver[1]
                                      Subject   = row[5] #the title of email
                                      content   = row[2] #the msg of email
                                      email_instance.send_text_email(Subject, content, email, user[0])
                                      msg = ('\n[%s] ----[sent email OK] ---- email[%s] has been sent.'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),email))
                                      log_file.write(msg)
                                      log_file.flush()
                              try:
                                   update_sql = "update mailer_lastinfo set is_sent='1' where id=" + str(id)
                                   cursor.execute(update_sql)
                                   con.commit()
                                   msg = ('\n[%s] ----[update col[is_sent] ] ---- id : [%d] ---- DB has been updated'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),id))
                              except MySQLdb.Error as e:
                                   con.rollback()
                                   msg = ('\n[%s] ----[update col[is_sent] error] ---- ERROR : [%s]'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),e))
                              log_file.write(msg)
                              log_file.flush()
                        except Exception, e:
                              msg = ('\n[%s] ----[sent email error] ---- ERROR:[%s].'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),e))
                              log_file.write(msg)
                              log_file.flush()
                                
                else:
                        #update DB
                        try:
                                update_sql = "update mailer_lastinfo set days="+str(days)+" where id=" + str(id)
                                cursor.execute(update_sql)
                                con.commit()
                                msg = ('\n[%s] ----[update record] ---- id : [%d] ---- days:[%d]'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),id, days))
                        except MySQLdb.Error as e:
                                con.rollback()
                                msg = ('\n[%s] ----[update record error] ---- ERROR : [%s]'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),e))
                        log_file.write(msg)
                        log_file.flush()
                                 
        #close connection
        cursor.close()
        con.close()
        msg = ('\n[%s] ----[close] Closed'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p')))
        log_file.write(msg)
        log_file.close()
except MySQLdb.Error as e:
        print e
        msg = ('\n[%s] ----[error] ---- ERROR : [%s]'%(datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p'),e))
        log_file.write(msg)
        log_file.close()
'''
fi 
'''
