# YpoxreotikiErgasia22_E16125_ALEXANDROS_SEVASTOS
Installation  
This project requires Python and the following Python libraries installed:

[Pymongo] 
[Flask] 
[json]  
[time]  



Τρόπος Λειτουργίας  
Δημιουργία ενός docker image που συνδέεται με ένα container της MongoDB , εισαγωγή της βάσης δεδομένων DSNotes που περιέχει τα collections "Notes" , "Users" στο image.
Εκκίνηση του Docker Image , εισαγωγή του κώδικα στο Visual Studio Code με την ονομασία app.py εκκίνηση του κώδικα με την επιλογή Flask.
Για την δοκιμή ανοίγουμε το postman και δημιουργούμε το request που επιθυμούμε να δοκιμάσουμε εισάγοντας στο url http://127.0.0.1:5000/ + το @app route του function. πχ. για το create_user http://127.0.0.1:5000/createUser έπειτα πατώντας body εισάγουμε στην επιλογή raw τις πληροφορίες σε μορφή json.
![image](https://user-images.githubusercontent.com/62871935/177761362-e8408b1d-416a-4e8b-b81e-1e02ba21391a.png) 

Κώδικας 
Σε όλα τα function εκτός του create_user():, υπαρχει ενα if οπού ελέγχει εάν η κατηγορία του χρήστη που έχει συνδεθεί έχει τη δικαιοδοσία να χρησιμοποιήσει τη συγκεκριμένη λειτουργία. πχ. ο admin να μην μπορει να φτιαξει notes και οι users να μην μπορουν να διαγραφουν αλλους users και τα αντιστοιχα notes τους

Function 1: Δημιουργία χρήστη - create_user():  
Έλεγχος αν το email και το username υπάρχουν ήδη μέσα στη βάση δεδομένων. Εφόσον δεν υπάρχει γίνεται εισαγωγή των στοιχείων του νέου χρήστη στη βάση δεδομένων μας ,αν δεν υπαρχουν διμηουργειται νεος χρηστης αλλιως δεν δημιουργειται και εμφανιζεται το αντιστοιχο μηνυμα. 
create user 

![image](https://user-images.githubusercontent.com/62871935/177762803-d8ccc4b2-5408-426c-9d72-a38afa6bc936.png)

couldnt create user

![image](https://user-images.githubusercontent.com/62871935/177762907-96ff6006-a848-4832-a99e-027138619d6b.png) 
  
Function 2: Εισοδος χρήστη - login(): 
Έλεγχος αν το email υπάρχει ήδη μέσα στη βάση δεδομένων. Εφόσον υπάρχει βρίσκουμε το password που του αντιστοιχεί και το αποθηκεύουμε σε μια νέα μεταβλητή , υστέρα κάνουμε έλεγχο αν το ζεύγος που λάβαμε ως εισαγωγή είναι το ίδιο με το ζεύγος που υπάρχει μέσα στη βάση δεδομένων μας. Έπειτα δημιουργούμε  δυο global μεταβλητές που αποθηκεύουμε το email, την κατηγορία,το username και το name του χρήστη.  
Succesfull login

![image](https://user-images.githubusercontent.com/62871935/177775598-e3699bb9-e9d1-49ff-a688-e0acd46d27e7.png)

Unsuccesfull login

![image](https://user-images.githubusercontent.com/62871935/177775767-a0be7e67-4604-42f6-8324-11c792d288b6.png)

το πρωτο εγινε succesfully Γιατι υπαρχει ο user αυτος στο collection Users  γιατι πρωηγουμενως τον φιαξαμε ενω το δευτερο δεν εγινε γιατι ο αλλος δεν υπαρχει

![image](https://user-images.githubusercontent.com/62871935/177776175-8f292e51-2b7c-44ed-b1e2-12261c663f05.png) 


Function 3 : Δημιουργια σημειωσης - insertNote(): 
το συγκεκριμένο function δεχόμαστε σαν εισαγωγή όλες τις πληροφορίες της σημειωσης και μόνο εφόσον υπάρχουν όλες στη σωστή μορφή η διαδικασία συνεχίζει, εφόσον όλα τα στοιχεία είναι σωστά τα προσθέτουμε σε μια καινούργια μεταβλητή user_note και υστέρα εισάγουμε την μεταβλητή στη βάση δεδομένων Notes μαζι με το username του χρηστη και την ημερομηνια δημιουργιας της. 

![image](https://user-images.githubusercontent.com/62871935/177779729-1e0f7264-2007-4c65-9b2e-55e87c0015a4.png) 
  
![image](https://user-images.githubusercontent.com/62871935/177779756-2aeedf48-d293-4d1a-8663-5b3ebc6de75d.png)  

Function 4 : Εμφανιση ολων των notes του χρηστη - myNotes():  

Στο συγκεκριμένο function παίρνουμε την global μεταβλητή user_notes και της βαζουμε την λιστα με ολα τα notes του χρηστη, αν είναι κενη επιστρέφουμε ότι δεν εχει notes ο χρηστης αλλιώς μας επιστρεφει μια λιστα με ολα τα notes του χρηστη απ την πιο παλια στην πιο καινουργια 

![image](https://user-images.githubusercontent.com/62871935/177780941-ea20265b-0d7c-4592-8df0-74df4b5f2e58.png) 


Function 5 : Εμφανιση ολων των notes του χρηστη - myNotesAsc(): ('/myNotes/Ascending) 

Στο συγκεκριμένο function παίρνουμε την global μεταβλητή user_notes και της βαζουμε την λιστα με ολα τα notes του χρηστη, αν είναι κενη επιστρέφουμε ότι δεν εχει notes ο χρηστης αλλιώς μας επιστρεφει μια λιστα με ολα τα notes του χρηστη απ την πιο καινουργια στην πιο παλια 

![image](https://user-images.githubusercontent.com/62871935/177781480-24c7ff84-2d58-47a3-b697-f5f34fef702c.png) 

Function 6 : Διαγραφη σημειωσης - DeleteNote(): 

Στο συγκεκριμένο function κανουμε search το note του χρηστη με τον τιτλο που επιλεξαμε,αν υπαρχει 1 η περισσοτερες σημειωσεις  με αυτον τον τιτλο διαγραφονται,αλλιως του εμφανιζεται μηνυμα πως δεν υπαρχει σημειωση με αυτον τον τιτλο. 

διαγραφη  

![image](https://user-images.githubusercontent.com/62871935/177782346-3d494d89-ae9a-459b-ab43-3c06e0a1abbf.png) 

μη επιτυχημενη αφου μολις την ειχαμε διαγραψει  

![image](https://user-images.githubusercontent.com/62871935/177782467-c9d27e58-6627-4997-bce8-27f1c62d2199.png) 

Function 7 :  -UpdateNote():  

Μη υλοποιημενη  

Function 8 : Αναζητηση σημειωσης βαση τιτλου η λεξης κλειδιου -SearchNote():  

Στο συγκεκριμένο function δεχόμαστε σαν εισαγωγή τον τιτλο η τις λεξεις κλειδια(δελ λειτουργει με ενα απ τα κλειδια περεπει να βαλουμε ολα τα κλειδια της σημειωσης) εάν βρεθεί μια η περισσοτερες σημειωσεις τις επιστρέφουμε αλλιώς επιστρέφουμε ότι δε βρέθηκε αποτέλεσμα. 

με λεξη κλειδι  

![image](https://user-images.githubusercontent.com/62871935/177798474-c0128347-c04f-47df-a174-e22e6653eea0.png) 

με τιτλο  
  
![image](https://user-images.githubusercontent.com/62871935/177798752-0b600c44-60d4-4699-8b2a-4a48e1c02268.png) 

και ενα δεν υπαρχει ο τιτλος  

![image](https://user-images.githubusercontent.com/62871935/177798987-aca563a4-5d0b-4f6c-8040-d07d59d5d54a.png) 



Function 9 : Διαγραφη χρηστη απ τον ίδιο τον χρήστη -deleteThisUser(): 

διαγραφή του χρήστη από την βάση δεδομένων μαζι με ολα τα notes του 

![image](https://user-images.githubusercontent.com/62871935/177799105-409471f9-4e0b-40a7-a207-17ff54341ccc.png) 

ADMIN 

παραδειγμα για τα permisions  

![image](https://user-images.githubusercontent.com/62871935/177800086-fbd16a03-1ac6-4c54-bf80-7d1607c76cbd.png) 

Function 10 : Δημιουργια νεου admin -create_admin():  

Στο συγκεκριμένο function αφου συνδεθει ο admin εισαγουμε τα στοιχεια για τον καινουργιο και τον φτιαχνουμε

![image](https://user-images.githubusercontent.com/62871935/177799743-5a1dbfb2-c914-430a-becb-081118f8bb60.png) 

φτιαχνει εναν καινουργιο admin  

![image](https://user-images.githubusercontent.com/62871935/177799879-6a7e9db7-3f91-401a-b8d6-3da7df9b0c98.png) 


Function 11 : Διαγραφη χρηστη απ τον admin -deleteUser(): 

![image](https://user-images.githubusercontent.com/62871935/177802499-b0a30bf6-fa4f-4ad8-8c81-d27a9cf37d40.png) 

![image](https://user-images.githubusercontent.com/62871935/177802556-89134ffa-5b19-4568-9873-67780664d411.png) 


χρησιμοποιωντας τον νεο admin επιλεγοντας το username ενος χρηστη,εαν υπαρχει θα διαγραφτει απ το collection Users αλλα και τα Notes του απ το collection Notes 

![image](https://user-images.githubusercontent.com/62871935/177800288-0a24285f-7690-4911-ba3b-55a4168d0894.png) 

Εαν δεν υπαρχει θα λαβουμε το αντιστοιχο μηνυμα 

![image](https://user-images.githubusercontent.com/62871935/177801963-7b48505c-196d-45ee-b2dd-cd432f491c03.png) 

![image](https://user-images.githubusercontent.com/62871935/177803416-05e4efa3-1a7e-429f-aa13-3909de06cc06.png) 

![image](https://user-images.githubusercontent.com/62871935/177803596-cdd17970-69cf-4e56-a51c-c23270be9da1.png) 


