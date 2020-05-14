import aiml
import mysql.connector

from flask import Flask,jsonify,request,render_template

app = Flask(__name__)





#mycursor.execute("CREATE TABLE InteractionDB (user VARCHAR(255), bot VARCHAR(255))")
#mycursor.execute("SHOW TABLES")
#print(mycursor)

# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("aiml.xml")
#kernel.respond("load aiml b")

# Press CTRL-C to break this loop
#while True:
#    x=input(">>")
 #   print(kernel.respond(x))

list_of_domain =[]
list_of_faculty=[]   

@app.route('/')
def create():
    return jsonify({'stores': 'Hello world'})

@app.route('/home/<string:name>')
def create_item_in_store(name):
    global list_of_domain
    global list_of_faculty
    #return kernel.respond(name)
    print("haha"+name)
    #sessionId = 12345
    #print(kernel.getSessionData(sessionId))
    string=kernel.respond(name)
    sql = "INSERT INTO interactiondb(user, bot) VALUES (%s, %s)"
    val = (name, string)
    print(val)
    print(string)
    print("hello")
    mydb = mysql.connector.connect(host="localhost",user="root",password="2017A7PS0056H@123",database="dhruv")

    print("bye")

    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()

    print(mycursor.rowcount, "record inserted.")
    #mycursor.execute("insert into CourseDB values("Mrs Shweta","Mathematics","Calculus");")
    
    
    if(string=="Can you let me know the name of the faculty you like?"):
        domain_string = kernel.getPredicate("domain_list")
        list_of_domain= domain_string.split(",")
        print(f"Domain Updated:{list_of_domain}")
    	
   
    if(string=="I can recommend you a few courses based on this."):
        string= "I have recommended few courses based on your interests.\n"
        faculty_str = kernel.getPredicate("faculty_list")
        list_of_faculty= faculty_str.split(",")
        print(f"Faculty Updated:{list_of_faculty}")
        print("printing listof faculty")
        print(list_of_faculty)
        print("domain")
        print(list_of_domain)
        for faculty in list_of_faculty:
            for domain in list_of_domain:
                print(faculty)
                print(domain)
                sql = "Select course from Coursedb where faculty=%s and domain=%s"
                val=(faculty,domain)
                #mycursor.execute("Select course from Coursedb where faculty="+str(faculty)+" and domain="+str(domain))
                mycursor.execute(sql, val)
                result=mycursor.fetchall()
                print("done here")
                if(len(result)!=0):
                    string += result[0][0]
                    string+="\n"
                print(string)
        print(string)
                

    return jsonify({'stores':string})

    


app.run(port=8080)

