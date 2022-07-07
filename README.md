# YpoxreotikiErgasia22_E16125_ALEXANDROS_SEVASTOS
Install
This project requires Python and the following Python libraries installed:

[Pymongo]
[Flask]
[json]
[uuid]
[time]
[bson.json_util]
[bson import ObjectId]


Τρόπος Λειτουργίας
Δημιουργία ενός docker image που συνδέεται με ένα container της MongoDB , εισαγωγή της βάσης δεδομένων DSMarkets που περιέχει τα collections "Notes" , "Users" στο image.
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


