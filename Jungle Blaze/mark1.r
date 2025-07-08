Name=input("Enter the Name:")
Rollno=int(input("Enter the roll no:"))
mark1=int(input("Enter Mark 1:"))
mark2=int(input("Enter Mark 2:"))
mark3=int(input("Enter mark 3:"))
total=mark1+mark2+mark3
average=total/3
print("Name:",Name)
print("Roll no:",Rollno)
print("Mark 1 is:",mark1)
print("Mark 2 is:",mark2)
print("mark 3 is:",mark3)
print("Total Mark is:",total)
print("Average is:",average)
if
average>90:
print("Grade is A")
elif average>80 and average<=90:
print("Grade is B")
elif average<=80 and average>70:
print("Grade is C")
else:
print("Grade is D")