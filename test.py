'''l1=[1,2,3]
l2=[4,5,6]
ans=[]
for i in range(len(l1)):
    ans.append(l1[i]*l2[i])
print(ans)

t1=(1,2,3)
lt1=list(t1)
t2=(4,5,6)
lt2=list(t2)
EmpList=[]
for i in range(len(t1)):
    EmpList.append(lt1[i]*lt2[i])
MyTuple=tuple(EmpList)
print(MyTuple)

dict1={"name":"anu","age":22}
for key,value in dict1.items():
    print(key,"=",value)

D={}
n=int(input("enter how many key_value pairs you want insert in the dictionary:"))

for i in range(n):
    a=input("enter the key:")
    b=input("enter the value:")
    D[a]=b

print(D)'''

class User:
    name=""
    def greet(self):
        print("hello",self.name)

user1=User()
user1.name="shravani"
user1.greet()

class bird:
    def sound(self):
        print("bird is chirping")

    def sound(self):
        print("dog is barking")


