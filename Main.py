import bsddb3 as bsddb
import random
import sys
import os
import time
import subprocess

def BackExit():
    print ("1,Back\n2,Exit")
    while True:
        choice = input("Enter [1,or,2]")  
        if choice == 1 or choice == '1':
            return True
        elif choice == 2 or choice == '2':
            return False
        else:
            print ("invalid input [1,2]")
            
def get_random():
    return random.randint(0, 63)
def get_random_char():
    return chr(97 + random.randint(0, 25))

           
def Createandpopulateadatabase(mode):
    DB_SIZE = 1000
    SEED = 10000000
    
    if mode == 1:
        DA_FILE = "/tmp/weijie2_db/bt_db"        
        invertDA_FILE = "/tmp/weijie2_db/invert_bt_db"    
        try:
            db = bsddb.btopen(DA_FILE, "w")
            invertdb = bsddb.btopen(invertDA_FILE, "w")
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.btopen(DA_FILE, "c")
            invertdb = bsddb.btopen(invertDA_FILE, "c")
        random.seed(SEED)
    elif mode == 2 :
        DA_FILE = "/tmp/weijie2_db/hash_db"
        invertDA_FILE = "/tmp/weijie2_db/invert_hash_db"
        try:
            db = bsddb.hashopen(DA_FILE, "w")
            invertdb = bsddb.hashopen(invertDA_FILE, "w")
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.hashopen(DA_FILE, "c")
            invertdb = bsddb.hashopen(invertDA_FILE, "c")
        random.seed(SEED)        
    elif mode == 3:
        DA_FILE = "/tmp/weijie2_db/indexfile_db"
        invertDA_FILE = "/tmp/weijie2_db/invert_indexfile_db"
        try:
            db = bsddb.btopen(DA_FILE, "w")
            invertdb = bsddb.btopen(invertDA_FILE, "w")
        except:
            print("DB doesn't exist, creating a new one")
            db = bsddb.btopen(DA_FILE, "c")
            invertdb = bsddb.btopen(invertDA_FILE, "c")
        random.seed(SEED)            
    
    index = 0
    while index < DB_SIZE:
        k = 64+random.randint(0, 63)
        key = ""
        for i in range(k):
            key += str(chr(97 + random.randint(0, 25)))
        v = 64+random.randint(0, 63)
        value = ""
        for j in range(v):
            value += str(chr(97 + random.randint(0, 25)))
            
        print ("key:",key,"\nvalue:",value,"\n",i)
        key = key.encode(encoding='UTF-8')
        value = value.encode(encoding='UTF-8')
        db[key] = value
        invertdb[value] = key
        index += 1
    try:
        db.close()
        invertdb.close()
    except Exception as e:        
        print (e)

def Retrieverecordswithagivenkey(mode):
    if mode == 1:
        DA_FILE = "/tmp/weijie2_db/bt_db"
        db = bsddb.btopen(DA_FILE,"w")
    elif mode == 2:
        DA_FILE = "/tmp/weijie2_db/hash_db"
        db = bsddb.hashopen(DA_FILE,"w")
        
    elif mode == 3:
        DA_FILE = "/tmp/weijie2_db/indexfile_db"
        #db = bsddb.btopen(DA_FILE,"w")
    else:
        print ("Mode error")
        return 1
    while True:
        
        try:
            if mode == 1:
                DA_FILE = "/tmp/weijie2_db/bt_db"
                db = bsddb.btopen(DA_FILE, "r")
                key = input("Input a Valid Key :").encode(encoding='UTF-8')
                start = time.time()
                try:
                    value = db[key]
                    print ("found")
                except:
                    print ("Key does not exist")
                print ("value is :",value)
                end = time.time()      
                decodevalue = value.decode(encoding='UTF-8')                
                
                print ("Time:", 1000000*(end-start),"micro seconds")
                file = open("answers","a")
                file.write(str(key)+"\n")
                file.write(str(decodevalue)+"\n\n")
                file.close()
                break
        
            elif mode == 2:
                DA_FILE = "/tmp/weijie2_db/hash_db"
                db = bsddb.hashopen(DA_FILE, "r")
                key = input("Input a Valid Key :").encode(encoding='UTF-8')
                start = time.time()
                try:
                    value = db[key]
                    print ("found")
                except :
                    print ("Key does not exist")
                print ("value is :", value)
                end = time.time()
                decodevalue = value.decode(encoding='UTF-8')                
                print ("Time:", 1000000*(end-start),"micro seconds")
                file = open("answers","a")
                file.write(str(key)+"\n")
                file.write(str(decodevalue)+"\n\n")
                file.close()
                break   
            elif mode == 3:
                DA_FILE = "/tmp/weijie2_db/indexfile_db"
                db = bsddb.btopen(DA_FILE, "r")
                key = input("Input a Valid Key :").encode(encoding='UTF-8')
                start = time.time()
                try:
                    value = db[key]
                    print ("found")
                except :
                    print ("Key does not exist")
                end = time.time()
                print ("value is :", value)
                decodevalue = value.decode(encoding='UTF-8')                
                print ("Time:", 1000000*(end-start),"micro seconds")
                file = open("answers","a")
                file.write(str(key)+"\n")
                file.write(str(decodevalue)+"\n\n")
                file.close()
                break            
            db.close()    
        except Exception as e:
            print (e)


def Retrieverecordswithagivendata(mode):
    if mode == 1:
        DA_FILE = "/tmp/weijie2_db/bt_db"
        db = bsddb.btopen(DA_FILE, "r")
        invertDA_FILE = "/tmp/weijie2_db/invert_bt_db"    
        invertdb = bsddb.btopen(invertDA_FILE, "r")
    elif mode == 2:
        DA_FILE = "/tmp/weijie2_db/hash_db"
        db = bsddb.hashopen(DA_FILE, "r")
        invertDA_FILE = "/tmp/weijie2_db/invert_hash_db"
        invertdb = bsddb.hashopen(invertDA_FILE, "r")
    elif mode == 3:
        DA_FILE = "/tmp/weijie2_db/indexfile_db"
        db = bsddb.btopen(DA_FILE, "r")
        invertDA_FILE = "/tmp/weijie2_db/invert_indexfile_db"
        invertdb = bsddb.btopen(invertDA_FILE, "r")        
    while True:
        try:
            if mode == 1:
                value = input("Input a Valid value:").encode(encoding = 'UTF-8')
                keyList = []
                start = time.time()
                try:
                    for key in db.keys():
                        if db[key] == value:
                            keyList.append(key.decode(encoding = 'UTF-8'))
                except:
                    print ("not found")
                    break
                end = time.time()
                print ("Time:", 1000000*(end-start),"micro seconds")
                print("Receive",len(keyList),"records")
                for i in keyList:
                    print ("Key is:",i)
                db.close()
                break
            elif mode == 2:
                value = input("Input a Valid value:").encode(encoding = 'UTF-8')
                keyList = []
                start = time.time()
                try:
                    for key in db.keys():
                        if db[key] == value:
                            keyList.append(key.decode(encoding = 'UTF-8'))
                except:
                    print ("not found")
                    break
                end = time.time()
                print("Time :",1000000*(end-start),"micro seconds")
                print("Receive",len(keyList),"records")
                for i in keyList:
                    print ("Key is:",i)
                db.close()
                break
            elif mode == 3:
                value = input("Input a Valid value:").encode(encoding = 'UTF-8')
                keyList = []
                start = time.time()
                try:
                    for key in db.keys():
                        if db[key] == value:
                            keyList.append(key.decode(encoding = 'UTF-8'))
                except:
                    print ("not found")
                    break
                end = time.time()
                print ("Time:", 1000000*(end-start),"micro seconds")
                print("Receive",len(keyList),"records")
                for i in keyList:
                    print ("Key is:",i)
                db.close()
                break                
        except Exception as e:
            print (e)
    return 0       

def Receivetracekeyrange(mode):
    while True:
        try:
            while True:
                  
                lower = input("Please enter your lower bound key:").encode(encoding='UTF-8')
                upper = input("Please enter your upper bound key:").encode(encoding='UTF-8')
                
                if lower > upper:
                    print ("invalid input lower should before upper ")    
                else:
                    break
            if mode == 1:
                try:
                    DA_FILE = "/tmp/weijie2_db/bt_db"
                    db = bsddb.btopen(DA_FILE,"r")
                except:
                    print ("open error")
                    return 0 
                file = open("answers","a")
                start = time.time()
                count = 0
                for key in db.keys():
                    if key >= lower and key <= upper:
                        count += 1
                        file.write(key.decode(encoding='UTF-8')+"\n")
                        file.write(db[key].decode(encoding='UTF-8')+"\n\n")
                end = time.time()
                print ("There are totall",count,"records in this range.")
                print ("Time :",1000000*(end-start),"micro seconds")
                file.close()
            elif mode == 2:
                try:
                    DA_FILE = "/tmp/weijie2_db/hash_db"
                    db = bsddb.hashopen(DA_FILE,"r")
                except:
                    print ("open error")
                    return 0             
                file = open("answers","a")
                start = time.time()
                count = 0
                for key in db.keys():
                    if key >= lower and key <= upper:
                        count += 1
                        file.write(key.decode(encoding='UTF-8')+"\n")
                        file.write(db[key].decode(encoding='UTF-8')+"\n\n")
                end = time.time()
                print ("There are totall",count,"records in this range.")
                print ("Time :",1000000*(end-start),"micro seconds")        
                file.close()
            elif mode == 3:
                try:
                    DA_FILE = "/tmp/weijie2_db/indexfile_db"
                    db = bsddb.btopen(DA_FILE,"r")      
                except:
                    print ("open error")
                    return 0                     
                file = open("answers","a")
                keys = db.keys()
                begin = binarysearch(keys,lower)
                finish = binarysearch(keys,upper)
                count = 0
                start = time.time()
                while begin <= finish:
                    key = keys[begin]
                    count +=1 
                    file.write(key.decode(encoding='UTF-8')+"\n")
                    file.write(db[key].decode(encoding='UTF-8')+"\n\n")
                    begin +=1
                end = time.time()
                print ("Time :",1000000*(end-start),"micro seconds")
                print ("There are",count,"records in this range.")
            break
        
        except Exception as e:
            print (e)

def binarysearch(keys,target):
    low = 0
    high = len(keys)-1
    while low < high:
        mid = (low+high)//2
        if target == keys[mid]:
            return mid
        elif target < keys[mid]:
            high = mid-1
            result = high
        else:
            low = mid+1
            result = mid +1
    return result

def Setup():
    global file
    try:
        os.stat("/tmp/weijie2_db")
    except:
        os.mkdir("/tmp/weijie2_db")
        print ("Create")
        
    try:
        file = open("results","w")
    except:
        print ("error")
    
def DestroyTheDatabase (opt):

    if opt == 1:
        subprocess.call(['rm','-r','/tmp/weijie2_db/bt_db'])
        subprocess.call(['rm','-r','/tmp/weijie2_db/invert_bt_db'])
                     
    if opt == 2:
        subprocess.call(['rm','-r','/tmp/weijie2_db/hash_db'])
        subprocess.call(['rm','-r','/tmp/weijie2_db/invert_hash_db'])
        
    if opt == 3:
        os.system("rm /tmp/weijie2_db/indexfile_db")    
        
def main():
    Setup()
    
    if sys.argv[1].lower() == "btree":
        print("B Tree")
        mode = 1
    elif sys.argv[1].lower() == "hash":
        print("Hash Table")
        mode = 2
    elif sys.argv[1].lower() == "index":
        print("Index")
        mode = 3
    else:
        print ("mode type error")
        return 0
        
    print ("====== Welcome ======")   
    boolean = True
    while boolean:
        print ("1 Create and populate a database")
        print ("2 Retrieve records with a given key")
        print ("3 Retrieve records with a given data")
        print ("4. Retrieve records with a given range of key values")    
        print ("5. Destroy the database")
        print ("6. Quit")        
        while True:
            try:
                choice = int(input("Please enter the number:"))
                if choice <= 6 and choice >= 0:
                    break
                else:
                    print ("Invalid input")                
            except:
                print ("Invalid input")
            
        if choice == 1:

            Createandpopulateadatabase(mode)
            boolean = BackExit()
            
            
        elif choice == 2:

            Retrieverecordswithagivenkey(mode)
            boolean = BackExit()
            
        elif choice == 3:

            Retrieverecordswithagivendata(mode)
            boolean = BackExit()
            
        
        elif choice == 4:
 
            Receivetracekeyrange(mode)
            boolean = BackExit()
            
            
        elif choice == 5:
            
            DestroyTheDatabase(mode)        
            print ("You can only pick 1 or 6")
            boolean = BackExit()
            
    
        elif choice == 6:
            boolean = False
            
    print ("Goodbye!")
main()
