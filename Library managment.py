def Database():
    import mysql.connector as ms
    cobj=ms.connect(host='localhost',user='root',passwd='****')
    if cobj.is_connected():
        cur=cobj.cursor()
        cur.execute('CREATE DATABASE IF NOT EXISTS libt')
        cur.execute('USE libt')
        cur.execute('CREATE TABLE IF NOT EXISTS bookrec (bno int(10), bname varchar(100), auth varchar(100), price int(10), qty int(10))')
        cur.execute('CREATE TABLE IF NOT EXISTS member (mno int(5), mname varchar(50), dom date, cont varchar(50))')
        cur.execute('CREATE TABLE IF NOT EXISTS rec (bno int(5), mno varchar(50), dos date, stat varchar(20))')
        cur.close()
        cobj.close()

def insb():
    #insert book
    bno=int(input('Enter book number:'))
    bname=input('Enter book name:')
    auth=input("Enter book's author:")
    price=int(input("Enter book's price:"))
    qty=int(input('Enter quantity purchased:'))
    qry="INSERT INTO bookrec VALUES ({},'{}','{}',{},{})".format(bno,bname,auth,price,qty)
    cur.execute(qry)
    cobj.commit()
    print('RECORD INSERTED SUCCESSFULLY')
    
def delb():
    #delete book
    bno = input("Enter Book Code of Book to be deleted from the Library:")
    qry ="DELETE FROM bookrec WHERE bno = {}".format(bno)
    cur.execute(qry)
    cobj.commit()
    print('RECORD DELETED SUCCESSFULLY')

def updb():
    #update book
    bno = int(input("Enter Book Code of Book to be Updated from the Library:"))
    print("Enter new data")
    bname = input("Enter Book Name:")
    auth = input("Enter Book Author's Name:")
    price = int(input("Enter Book Price:"))
    qty = int(input("Enter Quantity purchased:"))
    Qry ="UPDATE bookrec SET bname='{}', auth='{}', price={}, qty={} WHERE bno={}".format(bname, auth, price, qty, bno)
    cur.execute(Qry)
    cobj.commit()
    print('RECORD UPDATED SUCCESSFULLY')
    
def serbn():
    #search by book name
    bname = input('Enter book name to search:')
    Qry="SELECT * FROM bookrec WHERE bname = '{}'".format(bname)
    cur.execute(Qry)
    data=cur.fetchall()
    if len(data)==0:
        print('NO RECORDS FOUND')
    else:
        for i in data:
            print(i)
            print('RECORD(S) FOUND')

def serba():
    #search by author
    auth = input('Enter author to search:')
    Qry="SELECT * FROM bookrec WHERE auth='{}'".format(auth)
    cur.execute(Qry)
    data=cur.fetchall()
    if len(data)==0:
        print('NO RECORDS FOUND')
    else:
        for i in data:
            print(i)
            print('RECORD(S) FOUND')
        
def im():
    #insert member
    from datetime import date
    mno = int(input("Enter Member Code:"))
    mname = input("Enter Member Name:")
    print("Enter Date of Membership (Date,Month and Year) seperately):")
    DD = int(input("Enter Date:"))
    MM = int(input("Enter Month:"))
    YY = int(input("Enter Year:"))
    cont = input("Enter contact details of member:")
    Qry ="INSERT INTO member VALUES({}, '{}', '{}', '{}')".format(mno,mname,date(YY,MM,DD),cont)
    cur.execute(Qry)
    cobj.commit()
    print('MEMBER REGISTRATION DONE')

def dm():
    #delete member
    mno = int(input("Enter Member number to be deleted from the Library:"))
    Qry ="DELETE FROM member WHERE mno = {}".format(mno)
    cur.execute(Qry)
    cobj.commit()
    print('MEMBER DELETED SUCCESSFULLY')

def um():
    #update member
    from datetime import date
    mno = int(input("Enter Member number of Member to be Updated from the Library:"))
    print("Enter new data")
    mname = input("Enter Member Name:")
    print("Enter Date of Membership (Date,Month and Year seperately):")
    DD = int(input("Enter Date:"))
    MM = int(input("Enter Month:"))
    YY = int(input("Enter Year:"))
    cont = input("Enter Member's contact details:")
    DOM = date(YY,MM,DD)
    Qry ="UPDATE member SET mname='{}', DOM='{}', cont='{}' WHERE mno={}".format(mname,DOM,cont,mno)
    cur.execute(Qry)
    cobj.commit()
    print('MEMBER DETAILS UPDATED SUCCESSFULLY')
    
def sm():
    #search member
    mno=int(input('Enter member number to search:'))
    Qry="SELECT * FROM member WHERE mno={}".format(mno)
    cur.execute(Qry)
    data=cur.fetchall()
    if len(data)==0:
        print('NO RECORDS FOUND')
    else:
        for i in data:
            print(i)
            print('RECORD(S) FOUND')

def ib():
    #issue book
    from datetime import date
    bno = int(input("Enter Book number to issue:"))
    mno = int(input("Enter Member number:"))
    print("Enter Date Issue (Date,Month and Year separately):")
    DD = int(input("Enter Date:"))
    MM = int(input("Enter Month:"))
    YY = int(input("Enter Year:"))
    stat = input('Write(Reading):')
    #Qry = 
    cur.execute("INSERT INTO rec VALUES({}, {}, '{}', '{}')".format(bno,mno,date(YY,MM,DD),stat))
    cobj.commit()
    print('BOOK ISSUED')
    
def rb():
    #return book
    bno = int(input("Enter Book number to return:"))
    mno = int(input("Enter Member number:"))
    stat = input('Write(Lost,Returned):')
    Qry= "UPDATE rec SET stat='{}' WHERE mno = {} AND bno = {}".format(stat,mno,bno)
    cur.execute(Qry)
    cobj.commit()
    print('BOOK RETURNED')

def sib():
    #search issued books
    stat=input('Enter Lost, Returned, Reading books:')
    Qry = "SELECT * FROM rec WHERE stat='{}'".format(stat)
    cur.execute(Qry)
    data=cur.fetchall()
    if len(data)==0:
        print('NO RECORDS FOUND')
    else:
        for i in data:
            print(i)
            print('RECORD(S) FOUND')
    
Database()
import mysql.connector as ms
cobj=ms.connect(host='localhost',user='root',passwd='****',database='libt')
if cobj.is_connected():
    print('WELCOME TO LIBRARY MANAGEMENT SOFTWARE')
    cur=cobj.cursor()
    print("\t1.  Insert a book's data")
    print("\t2.  Update a book's data")
    print("\t3.  Delete a book's data")
    print("\t4.  Search a book's data")
    print("\t5.  Insert a member's data")
    print("\t6.  Delete a member's data")
    print("\t7.  Update a member's data")
    print("\t8.  Search a member's data")
    print('\t9.  Issue a book')
    print('\t10. Return a book')
    print('\t11. Search issued books')
    print('\t12. Exit')
    choice = int(input('Enter your choice (Sr.No.):'))
    while True:
        if choice==1:
            insb()
        elif choice==2:
            updb()
        elif choice==3:
            delb()
        elif choice==4:
            print('1.Search by book name')
            print('2.Search by author')
            print('3.exit')
            choice1=int(input("Enter your choice:"))
            while True:
                if choice1==1:
                    serbn()
                elif choice1==2:
                    serba()
                elif choice1==3:
                    break
                choice1=int(input("Enter your choice:"))
        elif choice==5:
            im()
        elif choice==6:
            dm()
        elif choice==7:
            um()
        elif choice==8:
            sm()
        elif choice==9:
            ib()
        elif choice==10:
            rb()
        elif choice==11:
            sib()
        elif choice==12:
            cur.close()
            cobj.close()
            break
        choice = int(input('Enter your choice (Sr.No.):'))
