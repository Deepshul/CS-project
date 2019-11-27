from django.shortcuts import render,redirect
from django.http import HttpResponse
from Index.models import Login
import csv
import mysql.connector

mycon=mysql.connector.connect(host="localhost",user="root",passwd="root",database="project_ad")
cursor=mycon.cursor()


def display():
    
        sql1="select shows.show_code,movies.moviename,movie_genres.genre_name,language.lang_name,theatres.theatre,shows.date,shows.start_time,shows.end_time from movies,movie_genres,language,theatres,shows where language.lang_code=shows.lang_code and theatres.theatre_code=shows.theatre_code and movie_genres.genre_code=movies.genre_code and movies.movie_id=shows.movie_id"
        cursor.execute(sql1)
        result=cursor.fetchall()
        return result
y=display()

U,P,C="","",()
# Create your views here.
def signup(request):
        if request.method=="POST":
                u=request.POST['username']
                p=request.POST['password']
                print(u)
                print(p)
                global U
                global P
                U=u
                P=p
                if u==p=='':
                    return render(request,'index.html')
                lst=Login()
                lst.username=u
                lst.password=p
                lst.save()
        
                with open('signupdata.csv','a') as csvfile:
                    wcs=csv.writer(csvfile)
                    wcs.writerow(['USERNAME',u])
                    wcs.writerow(['PASSWORD',p])
                #return render(request,'index.html',{"key":y})
                return redirect('/signup/index/')
        else:
                return render(request,'signup.html')

def login(request):
        if request.method=="POST":
                mycon=mysql.connector.connect(host="localhost",user="root",passwd="root",database="project_ad")
                u=request.POST['username']
                p=request.POST['password']
                cursor=mycon.cursor()
                global U
                global P
                U=u
                P=p
                lusers=[]
                lpwd=[]

                sql1="select username from index_login"
                cursor.execute(sql1)
                result=cursor.fetchall()

                for i in result:
                    lusers=lusers+[i[0]]
                print(lusers)

                sql2="select password from index_login"
                cursor.execute(sql2)
                result2=cursor.fetchall()

                for j in result2:
                    lpwd=lpwd+[j[0]]
                print(lpwd)

                l=(dict(zip(lusers,lpwd)))
                if (u in l) and l[u]==p:
                        return redirect('/signup/index/')
                else:
                        return render(request,'login.html')
        else:
                return render(request,'login.html')

def book(choice):
        if choice.method=="POST":
                s=(choice.POST)
                keys, values = zip(*s.items())
                global C
                global U
                print("here",values)
                C=values
                code=values[1]
                print("code",code)
                print(type(C))
                print("C",C)
                mycon=mysql.connector.connect(host="localhost",user="root",passwd="root",database="project_ad")
                cursor=mycon.cursor()
                sql1="select shows.show_code,movies.moviename,movie_genres.genre_name,language.lang_name,theatres.theatre,shows.date,shows.start_time,shows.end_time from movies,movie_genres,language,theatres,shows where language.lang_code=shows.lang_code and theatres.theatre_code=shows.theatre_code and movie_genres.genre_code=movies.genre_code and movies.movie_id=shows.movie_id and show_code like '{}'".format(code)
                cursor.execute(sql1)
                C=cursor.fetchall()
                C=C[0]
                print ("here it is",C)
                cursor.execute("select book_id from bookings where book_id like (select max(book_id) from bookings)")
                i=cursor.fetchall()
                print(i)
                i=int(i[0][0])+1
                print(i)
                print("check",i,C[0],C[1],C[2],C[3],C[4],C[5],C[6],C[7])
                sql="insert into bookings values({},'{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(i,U,C[0],C[1],C[2],C[3],C[4],C[5],C[6],C[7])
                cursor.execute(sql)
                mycon.commit()
                sql="select * from bookings where username like '{}'".format(U)
                cursor.execute(sql)
                P=cursor.fetchall()
                q=len(P)
                mycon.close()
                
                return render(choice,'thankyou.html',{'bookinfo':C,'username':[U],'bookings':P,'l':[q]})
        return render(choice,'index.html',{"key":y})

def thanks(t):
       
        return render(t,'thankyou.html')


'''mycon=mysql.connector.connect(host="localhost",user="root",passwd="root",database="project_ad")
cursor=mycon.cursor()
sql="select username from index_login where sno=(select max(sno) from index_login)"
x=cursor.execute(sql)
print(x)
'''
                
                



