a=int(input("Enter a number:"))
print("The odd numbers from 1 to",a,"is")
for i in range(1,a+1):
 if i%2!=0:
  print(i)
print("The even numbers from 1 to",a,"is")
i=1
while i<=a:
 if i%2==0:
  print(i)
i=i+1
