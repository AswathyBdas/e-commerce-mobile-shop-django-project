from django.shortcuts import render
from mob import dbconnection
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.core.files.storage import FileSystemStorage

def index(request): 
    return render(request,'index.html')
def login(request):
    if request.method=="POST":
        e=request.POST.get("e")
        p=request.POST.get("p")
        sql="select * from admin where email='"+e+"' and password='"+p+"'"
        data=dbconnection.selectone(sql)
        if data:
           request.session['email']=e
           if data[3]=='admin':
               return HttpResponseRedirect("adminhome")
        else:
            msg="invalid username or password"
            return render(request,"login.html",{"msg":msg})
    return render(request,'login.html')
def userlogin(request):
    if request.method=="POST":
        e=request.POST.get("e")
        p=request.POST.get("p")
        sql="select * from admin where email='"+e+"' and password='"+p+"'"
        data=dbconnection.selectone(sql)

        if data:
           request.session['email']=e
           if data[3]=='user':
               return HttpResponseRedirect("user")
        else:
            msg="invalid username or password"
            return render(request,"userlogin.html",{"msg":msg})

    return render(request,'userlogin.html')

def adminhome(request):
    return render(request,'adminhome.html')
def addcompany(request):
    if request.method=="POST":
        cn=request.POST.get("cn")
        co=request.POST.get("co")
        up=request.FILES["f"]
        fs=FileSystemStorage()
        fs.save("mob/static/upload/"+up.name,up)
        sql1="insert into addcompany(companyname,companyowner,logo)values('"+cn+"','"+co+"','"+up.name+"')"
        dbconnection.insert(sql1)
        return HttpResponseRedirect('addcompany')
    sql="select * from addcompany"
    d=dbconnection.selectall(sql)
    return render(request,'addcompany.html',{'data':d})
def addproduct(request):
    if request.method=="POST":
        cn=request.POST.get("cn")
        pdt=request.POST.get("pdt")
        d=request.POST.get("d")
        p=request.POST.get("p")
        fe=request.POST.get("fe")
        upl=request.FILES["img"]
        fs=FileSystemStorage()
        fs.save("mob/static/upload/"+upl.name,upl)
        co=request.POST.get("co")
        sql="insert into addproduct(companyname,product,discount,price,feactures,image,color)values('"+cn+"','"+pdt+"','"+d+"','"+p+"','"+fe+"','"+upl.name+"','"+co+"')"
        dbconnection.insert(sql)
        return HttpResponseRedirect('addproduct')
    return render(request,'addproduct.html')
def viewrequest(request):
    return render(request,'viewrequest.html')

def register(request):
    if request.method=="POST":
        n=request.POST.get("n")
        a=request.POST.get("a")
        if a<='18':
            return render(request,'register.html',{'message':'cannot be register'})
        else:
            return render(request,'register.html')    
        e=request.POST.get("e")
        p=request.POST.get("p")
        if len(p)<8:
            return render(request,'register.html',{'message1':'password must be 8 characters'})
        else:
            return render(request,'register.html')
        sql1="insert into register(name,age,email,password)values('"+n+"','"+a+"','"+e+"','"+p+"')"
        dbconnection.insert(sql1)
        sql2="insert into admin(email,password,login)values('"+e+"','"+p+"','user')"
        dbconnection.insert(sql2)
        return HttpResponseRedirect('user')
    return render(request,'register.html')
def product(request):
    if request.POST.get('sub'):
        co=request.POST.get('co')
        cl=request.POST.get('cl')
        sql="select * from addproduct where color='"+cl+"' and companyname='"+co+"'"
        data=dbconnection.selectone(sql)
        if data:
            sql1="select * from addproduct where companyname='"+co+"' and color='"+cl+"'"
            d=dbconnection.selectall(sql1)
            return render(request,'filter.html',{'d':d})
        sql1="select * from addproduct where companyname='"+co+"'"
        data=dbconnection.selectone(sql1)
        if data:
            sql1="select * from addproduct where companyname='"+co+"'"
            d=dbconnection.selectall(sql1)
            return render(request,'filter.html',{'d':d})
        sql2="select * from addproduct where color='"+cl+"'"
        data=dbconnection.selectone(sql2)
        if data:
            sql1="select * from addproduct where color='"+cl+"'"
            d=dbconnection.selectone(sql1)
            return render(request,'filter.html',{'d':d})
        p=request.POST.get('p')
        if p>="30000":
            sql="select * from addproduct where price>=30000"
            d=dbconnection.selectall(sql)
            return render(request,'filter.html',{'d':d})
    sql="select * from addproduct"
    data=dbconnection.selectall(sql)
    return render(request,'product.html',{'data':data})
def filter(request):
    return render(request,'filter.html')
def cart(request):
    return render(request,'cart.html')
def details(request):
    import datetime
    id=request.GET['id']
    did=request.session['email']
    d=datetime.date.today()
    sql2="select * from comment where productid='"+id+"'"
    data1=dbconnection.selectall(sql2)
    sql="select * from addproduct where id='"+id+"'"
    data=dbconnection.selectone(sql)
    if request.POST.get("sub1"):
        a=request.POST.get('a')
        im=request.FILES['b']
        fs=FileSystemStorage()
        fs.save("mob/static/upload/"+im.name,im)
        sql="insert into comment(comment,name,productid,date,photo)values('"+a+"','"+did+"','"+id+"','"+str(d)+"','"+im.name+"')"
        dbconnection.insert(sql)
        return HttpResponseRedirect("details?id="+id)
    if request.POST.get("rat1"):
        p_name=data[2]
        rate=request.POST.get('rate')
        sql1="insert into rating(customername,product,rating)values('"+did+"','"+p_name+"','"+rate+"')"
        dbconnection.insert(sql1)
        return HttpResponseRedirect("details?id="+id)
    #return render(request,'details.html',{"data1":data1,"data2":data2})
    
    if request.POST.get("sub2"):
        p_name=data[2]
        sql1="insert into cart(customername,product,date) values('"+did+"','"+p_name+"','"+str(d)+"')"
        dbconnection.insert(sql1)
        return HttpResponseRedirect("details?id="+id)
    return render(request,'details.html',{"data":data,'data1':data1})
    #if request.POST.get("sub3"):
        #return render(request,'buynow.html')
    

    

    # if request.POST.get("sub2"):
    #     d=datetime.date.today()
    #     #na=request.session['email']
    #     sql1="select *from product where id='"+id+"'"
    #     data1=dbconnection.selectone(sql1)
    #     p_name=data[2]
    #     sql="select * from cart where customername='"+na+"' and product='"+p_name+"'"
    #     data2=dbconnection.selectone(sql)
    #     if data2:
    #         return render(request,'details.html',{'message':'already exist','data':data})
    #     else:
    #         sql2="insert into cart(customername,product,date)values('"+na+"','"+p_name+"','"+str(d)+"')"  
    #         dbconnection.insert(sql2)
    #         return render(request,'details.html')
def search(request):
#     if request.POST.get('su1'):
    #     product=request.POST.get('p')
    #     if product=="":
    #         return render(request,'search.html',{'message':'please fill'})
    #     else:
    #         sql="select * from addproduct where product='"+product+"'"
    #         data=dbconnection.selectall(sql)
    #         if data:
    #             return render(request,'search.html',{'data':data,'price':'price:'})
    #         else:
    #             return render(request,'search.html',{"msg3":'product not available'})
    # elif request.POST.get('su2'):
    #     company=request.POST.get('c')
    #     if company=="":
    #         return render(request,'search.html',{'message1':'please fill'})
    #     sql="select * from addproduct where companyname='"+companyname+"'"
    #     data=dbconnection.selectall(sql)
    #     if data:
    #         return render(request,'search.html',{'data':data})
    #     else:
    #         return render(request,'search.html',{"msg4":'product not available'})
    # elif request.POST.get('su3'):
    #     price=request.POST.get('pr')
    #     if price=="":
    #         return render(request,'search.html',{'message2':'please fill'})
    #     else:
    #         sql="select * from addproduct where price <='"+price+"'"
    #         data=dbconnection.selectall(sql)
    #         if data:
    #             return render(request,'search.html',{'data':data,'price':'price:'})
    #         else:
    #             return render(request,'search.html',{"msg5":'product not available'})
    # elif request.POST.get('su4'):
    #     price=request.POST.get('g')
        # if price=="":
        #     return render(request,'search.html',{'message2':'please fill'})
        # else:
        #     sql="select * from addproduct where price >='"+price+"'"
        #     data=dbconnection.selectall(sql)
        #     if data:
        #         return render(request,'search.html',{'data':data,'price':'price:'})
        #     else:
        #         return render(request,'search.html',{"msg6":'product not available'})
    # elif request.POST.get('su5'):
    #     start=request.POST.get('s')
    #     stop=request.POST.get('st')
    #     if start=="" or stop=="":
    #         return render(request,'search.html',{'message3':'please fill'})
    #     elif start=="" and stop=="":
    #         return render(request,'search.html',{'message4':'please fill'})
    #     else:
    #         sql="select * from addproduct where price between '"+start+"' and '"+stop+"'"
    #         data=dbconnection.selectall(sql)
    #         if data:
    #             return render(request,'search.html',{'data':data})
    #         else:
    #             return render(request,'search.html',{"msg6":'product not available'})
    return render(request,'search.html')
def search2(request):
    return render(request,"search2.html")
def bank(request):
    if request.method=="POST":
        em=request.POST.get("em")
        pa=request.POST.get("pa")
        sql="select * from banklogin where email='"+em+"' and password='"+pa+"'"
        data=dbconnection.selectone(sql)
        if data:
               return HttpResponseRedirect("bankhome")
        else:
            msg="invalid username or password"
            return render(request,"bank.html",{"msg":msg})
    return render(request,'bank.html')
def bankhome(request):
    return render(request,'bankhome.html')
def newaccount(request):
    if request.method=="POST":
        fs=request.POST.get("fs")
        ls=request.POST.get("ls")
        mo=request.POST.get("mo")
        fa=request.POST.get("fa")
        ad=request.POST.get("ad")
        g=request.POST.get("g")
        do=request.POST.get("do")
        pi=request.POST.get("pi")
        adr=request.POST.get("adr")
        em=request.POST.get("em")
        import random
        ac=random.randrange(10000,20000)
        newac="AC001"+str(ac)
        sql="insert into newaccount(firstname,lastname,mothername,fathername,address,gender,dob,pincode,aadhar_number,email,accountnumber)values('"+fs+"','"+ls+"','"+mo+"','"+fa+"','"+ad+"','"+g+"','"+do+"','"+pi+"','"+adr+"','"+em+"','"+str(newac)+"')"
        dbconnection.insert(sql)
        return HttpResponseRedirect('newaccount')
    return render(request,'newaccount.html')
def deposit(request):
    if request.method=="POST":
        ac=request.POST.get("ac")
        no=request.POST.get("no")
        sql="select * from newaccount where accountnumber='"+str(ac)+"'"
        data=dbconnection.selectone(sql)
        crd=int(data[12])+int(no)
        sql1="update newaccount set credit='"+str(crd)+"'where accountnumber='"+ac+"'"
        dbconnection.update(sql1)
        return HttpResponseRedirect('deposit')
    return render(request,'deposit.html')
def accountstatus(request):
    if request.method=="POST":
        na=request.POST.get("na")
        ac=request.POST.get("ac")
        sql="select * from newaccount where accountnumber='"+str(ac)+"'"
        data=dbconnection.selectall(sql)
        if data:
            sql1="select * from status where amounto='"+str(ac)+"'"
            d=dbconnection.selectone(sql1)
            sql2="select * from status where amountfrom='"+str(ac)+"'"
            data=dbconnection.selectone(sql2)
            sql3="select * from newaccount where accountnumber='"+str(ac)+"'"
            data1=dbconnection.selectall(sql3)
    return render(request,'accountstatus.html')
def buynow(request):
    if request.method=="POST":
        import datetime
        ac=request.POST.get("ac")
        mo=request.POST.get("mo")
        am=request.POST.get("am")
        sql="select * from addproduct where id='"+id+"'"
        data=dbconnection.selectone(sql)
        sql="select * from newaccount where accountnumber='"+str(ac)+"'"
        data=dbconnection.selectone(sql)
        newde=int(am)
        cr=data[10]
        newcr=cr-newde
        bal=cr-newde
        date=str(datetime.date.today())
        if cr<=int(am):
            return render(request,'buynow.html',{'msg':'YOUR ACCOUNT BALANCE IS LESS TO PURCHASE THIS ITEM'})
        else:
            sql1="update newaccount set credit='"+str(newcr)+" where accountnumber='"+ac+"'"
            dbconnection.update(sql1)
            sql2="update newaccount set debit='"+str(newde)+"' where accountnumber='"+ac+"'"
            dbconnection.update(sql2)
            sql4="update status set amountto='"+mo+"' where amountfrom='"+ac+"'"
            dbconnection.update(sql4)
            sql5="insert into status(date,amountfrom,amountto,credit,debit,balance)values('"+str(date)+"','"+ac+"','"+mo+"','"+str(cr)+"','"+am+"','"+str(bal)+"')"
            return HttpResponseRedirect("buynow")
    return render(request,'buynow.html',{"data":data})
def new(request):
    return render(request,'new.html')
            










        
    

 



