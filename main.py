import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets,QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate,Qt,QTimer
import sqlite3
from PyQt5 import QtGui


class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("Welcome_page.ui", self)
        self.login.clicked.connect(self.gotologin)
        self.create.clicked.connect(self.gotosignup)

    def gotologin(self):
        login = LoginScreen()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    
    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class LoginScreen(QDialog):
    def __init__(self):
        super(LoginScreen, self).__init__()
        loadUi("Login_page.ui", self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login2.clicked.connect(self.loginFunction)
        self.create.clicked.connect(self.gotosignup)

    def loginFunction(self):
        user=self.Email.text()
        password=self.Password.text()
        if len(user)==0 or len(password)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        elif user=='admin' and password=='admin':
            self.gotoadmin1()
        else:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            query = "SELECT Email, Password FROM login WHERE Email ='"+user+"'"
            cur1.execute(query)
            result = cur1.fetchone()
            print(result)
            if result is None:
                self.success.setText("")
                self.error.setText("incorrecte email")
            else:
                if user==result[0] and password==result[1]:
                    #self.error.setText("")
                    #self.success.setText("Successfuly connected")
                    self.gotouser()

                elif password != result[1]:
                    self.success.setText("")
                    self.error.setText("incorrecte password")
             
    def gotosignup(self):
        signup = SignupScreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotoadmin1(self):
        admin1 = Admin1()
        widget.addWidget(admin1)
        widget.setCurrentIndex(widget.currentIndex() + 1) 
    def gotouser(self):
        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        query = "SELECT id,Nom,Tel, Email FROM login WHERE Email ='"+self.Email.text()+"'" 
        cur1.execute(query)
        result = cur1.fetchone()
        conn.close()

        if result is not None:
            id_c = result[0]
            Nom = result[1]
            Tel = result[2]
            username = result[3]
            user = Filter(id_c,Nom,Tel,username)
            widget.addWidget(user)
            widget.setCurrentIndex(widget.currentIndex() + 1)


class SignupScreen(QDialog):
    def __init__(self):
        super(SignupScreen, self).__init__()
        loadUi("Createaccount_page.ui", self)
        self.Password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.CPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signup.clicked.connect(self.SignupFunction)
        self.Retour.clicked.connect(self.retour)
    
    def SignupFunction(self):
        nom_c=self.Nom.text()
        prenom_c=self.Prenom.text()
        cin_c=self.Cin.text()
        adress_c=self.Adress.text()
        tel_c=self.Tel.text()
        email_c=self.Email.text()
        password_c=self.Password.text()
        CPassword_c=self.CPassword.text()
        if len(nom_c)==0 or len(prenom_c)==0 or len(cin_c)==0 or len(adress_c)==0 or len(tel_c)==0 or len(email_c)==0 or len(password_c)==0 or len(CPassword_c)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        elif CPassword_c != password_c:
            self.success.setText("")
            self.error.setText("Passwords does not match")
        else:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            user_info=[nom_c,prenom_c,cin_c,adress_c,tel_c,email_c,password_c]
            cur1.execute('INSERT INTO login(Nom,Prenom,Cin,Adress,Tel,Email,Password) VALUES(?,?,?,?,?,?,?)',user_info)
            conn.commit()
            self.error.setText("")
            self.success.setText("Added successfully")
            conn.close()
            
    def retour(self):
        retour = WelcomeScreen()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    
        


class Filter(QDialog):
    def __init__(self,id_c,Nom,Tel,username):
        super(Filter, self).__init__()
        loadUi("Choice_test.ui", self)
        self.DateDebut.setCalendarPopup(True)
        self.DateDebut.setMinimumDate(QDate(2023, 5, 1))
        self.DateFin.setCalendarPopup(True)
        self.DateFin.setMinimumDate(QDate(2023, 5, 1))
        self.Retour.clicked.connect(self.retour)
    

        output_text = f"Welcome {Nom}"
        self.username.setText(output_text)
        self.id_c = id_c
        self.nom = Nom
        self.tel = Tel
        
        self.Submit.clicked.connect(self.execution)
        
        layout=QVBoxLayout()
        self.setLayout(layout)
    def retour(self):
        retour = LoginScreen()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1)
   

    def execution(self):
        
        self.filter=self.Filter.currentText()
        print(self.filter)
        self.choice=self.Choice.text().lower()
        print(self.choice)
        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        query = f"SELECT DISTINCT Matricule,Marque,Modele,Image,Type_carburant,Nombre_places,Transmission,Prix_location,Disponibilite FROM voiture WHERE {self.filter} = ? AND Disponibilite != 1"
        
        self.Liste_choix.clearContents()  # Clear the table before executing the search query

        self.Liste_choix.setRowCount(10)
        self.Liste_choix.resizeColumnToContents(3)
        self.Liste_choix.setColumnCount(10)

        # Create a radio button group to ensure only one item is selected
        radio_group = QButtonGroup(self.Liste_choix)
        radio_group.setExclusive(True)
        

        for i in range(self.Liste_choix.rowCount()):
            radio_button = QRadioButton()
            radio_group.addButton(radio_button)
            self.Liste_choix.setCellWidget(i, 0, radio_button)
            radio_button.setObjectName("re")
            radio_button.clicked.connect(self.radio_button_clicked) 
       

        tablerow = 0
        for r in cur1.execute(query, (self.choice,)):
            radio_button = self.Liste_choix.cellWidget(tablerow, 0)
            radio_button.setChecked(False)
           

            self.Liste_choix.setItem(tablerow, 1, QTableWidgetItem(str(r[0])))
            self.Liste_choix.setItem(tablerow, 2, QTableWidgetItem(str(r[1])))
            self.Liste_choix.setItem(tablerow, 3, QTableWidgetItem(str(r[2])))
            

            image_data = r[3]
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            self.Liste_choix.setCellWidget(tablerow, 4, image_label)

            self.Liste_choix.setItem(tablerow, 5, QTableWidgetItem(str(r[4])))
            self.Liste_choix.setItem(tablerow, 6, QTableWidgetItem(str(r[5])))
            self.Liste_choix.setItem(tablerow, 7, QTableWidgetItem(str(r[6])))
            self.Liste_choix.setItem(tablerow, 8, QTableWidgetItem(str(r[7])))
            self.Liste_choix.setItem(tablerow, 9, QTableWidgetItem(str(r[8])))
            tablerow += 1

       
       
    def radio_button_clicked(self):
        for row in range(self.Liste_choix.rowCount()):
            radio_button = self.Liste_choix.cellWidget(row, 0)
            matricule_item = self.Liste_choix.item(row, 1)
            if matricule_item is None :
                continue
            elif radio_button is not None and radio_button.isChecked():
                matricule = matricule_item.text()
                self.marque = self.Liste_choix.item(row, 2).text()
                self.modele = self.Liste_choix.item(row, 3).text()
                self.prix_location = self.Liste_choix.item(row, 8).text()
                date_debut = self.DateDebut.text()
                date_fin = self.DateFin.text()
                self.dat_debut = self.DateDebut.date().toPyDate()
                self.dat_fin = self.DateFin.date().toPyDate()
                print(date_debut)
                
                if date_debut < date_fin:
                    conn = sqlite3.connect("verification.sqlite")
                    cur1 = conn.cursor()
                    cur1.execute("INSERT INTO reservation (Matricule, Marque, Modele, id, Nom, Tel,Prix_location,Date_Debut,Date_Fin) SELECT ?, ?, ?, ?, ?, ?, ?,?,? WHERE NOT EXISTS (SELECT 1 FROM reservation WHERE  id = ? AND Matricule= ? )", (matricule, self.marque, self.modele, self.id_c, self.nom, self.tel,self.prix_location,date_debut,date_fin,self.id_c,matricule))
                    matricule_row = cur1.execute('SELECT Matricule FROM reservation WHERE id=? AND Matricule=?', (self.id_c, matricule)).fetchone()
                    if matricule_row:
                        cur1.execute('UPDATE voiture SET Disponibilite = ? WHERE Matricule = ?', [1, matricule])
                        conn.commit()
                        conn.close()
                        self.gotofacture()
 


    
    def gotofacture(self):
        date_d=self.dat_debut
        date_f=self.dat_fin
        prix=self.prix_location
        marque = self.marque
        modele =self.modele
        facture = Facture(date_d,date_f,prix,marque,modele)
        widget.addWidget(facture)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class Facture(QDialog):
    def __init__(self,date_d,date_f,prix,marque,modele):
        super(Facture, self).__init__()
        loadUi("Facture.ui", self)
        self.Facture.setRowCount(1)
        self.Facture.setColumnCount(5)
        if date_d < date_f:
            days = (date_f - date_d).days
            re=int(prix)*days
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            
            cur1.execute('INSERT INTO Facture(Voiture,Modele,Prix_location,Duree,Total) VALUES(?,?,?,?,?)', (marque, modele, prix, days, re))
            conn.commit()
            conn.close()
            self.Facture.setItem(0, 0, QTableWidgetItem(marque))
            self.Facture.setItem(0, 1, QTableWidgetItem(modele))
            self.Facture.setItem(0, 2, QTableWidgetItem(str(prix)))
            self.Facture.setItem(0, 3, QTableWidgetItem(str(days)))
            self.Facture.setItem(0, 4, QTableWidgetItem(str(re)))
        

            self.Payer.clicked.connect(QApplication.instance().quit)
            
        


            

               






           

        


    

class Admin1(QDialog):
    def __init__(self):
        super(Admin1, self).__init__()
        loadUi("Adminfirst_page.ui", self)
        self.ajout.clicked.connect(self.gotoadmin2) 
        self.liste_v.clicked.connect(self.liste_voiture)
        self.list_c.clicked.connect(self.liste_clients)
        self.liste_r.clicked.connect(self.liste_reservation)
        self.Retour.clicked.connect(self.retour)
    def retour(self):
        retour = LoginScreen()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def gotoadmin2(self):
        admin2 = Admin2()
        widget.addWidget(admin2)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def liste_voiture(self):
        liste_v = Liste_v()
        widget.addWidget(liste_v)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def liste_clients(self):
        liste_c = Liste_c()
        widget.addWidget(liste_c)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    
    def liste_reservation(self):
        liste_r = Liste_r()
        widget.addWidget(liste_r)
        widget.setCurrentIndex(widget.currentIndex() + 1)



class Admin2(QDialog):
    def __init__(self):
        super(Admin2, self).__init__()
        loadUi("Adminsecond_page.ui", self)
        self.button = self.findChild(QPushButton, "Image")
        self.label = self.findChild(QLabel, "test")
        self.Ajouter.clicked.connect(self.Ajouter_voiture)
        self.button.clicked.connect(self.clicker)
        self.binary_code = None
        self.Retour.clicked.connect(self.retour)
    
    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All files (*);;Python Files(*.py)")
        if fname[0] :
            self.error.setText("")
            self.fname = fname[0]
            with open(self.fname, "rb") as binary_image:
                self.binary_code = binary_image.read()
                print(self.binary_code)
        else:
            self.error.setText("error")

    def Ajouter_voiture(self):
        self.Marque_v = self.Marque.text().lower()
        Modele_v = self.Modele.text()

        Type_v = self.Type_carburant.text().lower()
        Place_v = self.Nombres_place.text()
        Transmission_v = self.Transmission.currentText().lower()
        Prix_v = self.Prix_loc.text()
        Dispo_v = self.Disponibilite.text()
        print(self.Marque_v)
        print(Transmission_v)
        if len(self.Marque_v)==0 or len(Modele_v)==0 or self.binary_code is None or len(Type_v)==0 or len(Place_v)==0 or len(Transmission_v)==0 or len(Prix_v)==0 or len(Dispo_v)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        else:
            self.error.setText("")
            self.success.setText("Added successfully")
            QTimer.singleShot(2000, self.reload_admin2)

        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        user_info = [self.Marque_v, Modele_v, self.binary_code, Type_v, Place_v, Transmission_v, Prix_v, Dispo_v]
        cur1.execute('INSERT INTO voiture(Marque, Modele, Image, Type_carburant, Nombre_places, Transmission, Prix_location, Disponibilite) VALUES(?,?,?,?,?,?,?,?)', user_info)
        conn.commit()
        conn.close()

    def reload_admin2(self):
        admin2 = Admin2()
        widget.addWidget(admin2)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def retour(self):
        retour = Admin1()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        
    
        
	
            
    
	


        
            


class Liste_v(QDialog):
    def __init__(self):
        super(Liste_v, self).__init__()
        loadUi("Liste_voiture.ui", self)
        
        self.loaddata()
        self.Retour.clicked.connect(self.retour)

    def loaddata(self):
        conn = sqlite3.connect("verification.sqlite")
        cur1 = conn.cursor()
        query = "SELECT * FROM voiture"
        self.Listev.setRowCount(10)
        self.Listev.resizeColumnToContents(3)
        
        tablerow = 0
        for r in cur1.execute(query):
            self.Listev.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(str(r[0])))
            self.Listev.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(r[1])))
            self.Listev.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(r[2])))
            # retrieve the image from the database as binary data
            image_data = r[3]
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)

            # create a QLabel widget with the pixmap as its image
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            # set the QLabel widget as the cell widget
            self.Listev.setCellWidget(tablerow, 3, image_label)

            self.Listev.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(str(r[4])))
            self.Listev.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(str(r[5])))
            self.Listev.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(str(r[6])))
            self.Listev.setItem(tablerow, 7, QtWidgets.QTableWidgetItem(str(r[7])))
            self.Listev.setItem(tablerow, 8, QtWidgets.QTableWidgetItem(str(r[8])))

           
            modify_button = QPushButton("Modifier")
            modify_button.clicked.connect(self.modify_row)
            self.Listev.setCellWidget(tablerow, 9, modify_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(self.delete_row)
            self.Listev.setCellWidget(tablerow, 10 , delete_button)

            

            tablerow += 1

    def modify_row(self):
        
        row = self.Listev.currentRow()
        matricule = self.Listev.item(row, 0).text()
        marque = self.Listev.item(row, 1).text()
        modele = self.Listev.item(row, 2).text()
        type_carburant = self.Listev.item(row, 4).text()
        nombre_places= self.Listev.item(row, 5).text()
        transmission = self.Listev.item(row, 6).text()
        prix = self.Listev.item(row, 7).text()
        dispo = self.Listev.item(row, 8).text()


        update_v = Update_v(matricule,marque,modele,type_carburant,nombre_places,transmission,prix,dispo)
        widget.addWidget(update_v)
        widget.setCurrentIndex(widget.currentIndex() + 1)
    def delete_row(self):
        row = self.Listev.currentRow()
        matricule = self.Listev.item(row, 0).text()
        
        reply = QMessageBox.question(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer cette voiture ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            cur1.execute("DELETE FROM voiture WHERE Matricule=?", (matricule,))
            conn.commit()
            conn.close()
            liste_v = Liste_v()
            widget.addWidget(liste_v)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def retour(self):
        retour = Admin1()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1)       
           


class Update_v(QDialog):
    def __init__(self,matricule,marque,modele,type_carburant,nombre_places,transmission,prix,dispo):
        super(Update_v, self).__init__()
        loadUi("update_voiture.ui", self) 
        self.Ajouter.clicked.connect(self.Ajouter_voiture)
        self.Image.clicked.connect(self.clicker)
        self.binary_code = None

        self.matricule_v=matricule
        self.Marque.setText(marque)  
        self.Modele.setText(modele) 
        self.Type_carburant.setText(type_carburant)  
        self.Nombres_place.setText(nombre_places)  
        self.Transmission.setCurrentText(transmission)
        self.Prix_loc.setText(prix)  
        self.Disponibilite.setText(dispo)  

    def clicker(self):
        fname = QFileDialog.getOpenFileName(self, "Open File", "", "All files (*);;Python Files(*.py)")
        if fname[0] :
            self.error.setText("")
            self.fname = fname[0]
            with open(self.fname, "rb") as binary_image:
                self.binary_code = binary_image.read()
                print(self.binary_code)
        else:
            self.error.setText("error")

    def Ajouter_voiture(self):
   
        Marque_v = self.Marque.text().lower()
        Modele_v = self.Modele.text()
        Type_v = self.Type_carburant.text().lower()
        Place_v = self.Nombres_place.text()
        Transmission_v = self.Transmission.currentText().lower()
        Prix_v = self.Prix_loc.text()
        Dispo_v = self.Disponibilite.text()

   
        conn = sqlite3.connect("verification.sqlite")
        cur = conn.cursor()
        result=None
    
        if self.binary_code is None:
            cur.execute("SELECT Image FROM voiture WHERE Matricule=?", (self.matricule_v,))
            result = cur.fetchone()
        if result is not None:
            self.binary_code = result[0]

    
        user_info = [Marque_v, Modele_v, self.binary_code, Type_v, Place_v, Transmission_v, Prix_v, Dispo_v, self.matricule_v]
        cur.execute('UPDATE voiture SET Marque=?, Modele=?, Image=?, Type_carburant=?, Nombre_places=?, Transmission=?, Prix_location=?, Disponibilite=? WHERE Matricule=?', user_info)
        conn.commit()
        conn.close()
        liste_v = Liste_v()
        widget.addWidget(liste_v)
        widget.setCurrentIndex(widget.currentIndex() + 1)


      
        
        

        
   
       
       
       
       

   


class Liste_c(QDialog):
    def __init__(self):
        super(Liste_c, self).__init__()
        loadUi("Liste_clients.ui", self)
        self.loaddata()
        self.Retour.clicked.connect(self.retour)
    def loaddata(self):
        conn = sqlite3.connect("verification.sqlite")
        cur2 = conn.cursor()
        query1 = "SELECT * FROM login"
        self.listec.setRowCount(20)
        tablerow1 = 0
        for r2 in cur2.execute(query1):
            self.listec.setItem(tablerow1,0,QtWidgets.QTableWidgetItem(str(r2[0])))
            self.listec.setItem(tablerow1,1,QtWidgets.QTableWidgetItem(str(r2[1])))
            self.listec.setItem(tablerow1,2,QtWidgets.QTableWidgetItem(str(r2[2])))
            self.listec.setItem(tablerow1,3,QtWidgets.QTableWidgetItem(str(r2[3])))
            self.listec.setItem(tablerow1,4,QtWidgets.QTableWidgetItem(str(r2[4])))
            self.listec.setItem(tablerow1,5,QtWidgets.QTableWidgetItem(str(r2[5])))
            self.listec.setItem(tablerow1,6,QtWidgets.QTableWidgetItem(str(r2[6])))
            self.listec.setItem(tablerow1,7,QtWidgets.QTableWidgetItem(str(r2[7])))
            modify_button = QPushButton("Modifier")
            modify_button.clicked.connect(self.modify_row)
            self.listec.setCellWidget(tablerow1, 8, modify_button)

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(self.delete_row)
            self.listec.setCellWidget(tablerow1, 9 , delete_button)
            tablerow1+=1
    
    def modify_row(self):
        
        row = self.listec.currentRow()
        id_c = self.listec.item(row, 0).text()
        Nom = self.listec.item(row, 1).text()
        Prenom = self.listec.item(row, 2).text()
        Cin = self.listec.item(row, 3).text()
        Adress= self.listec.item(row, 4).text()
        Tel = self.listec.item(row, 5).text()
        Email = self.listec.item(row, 6).text()
        Password = self.listec.item(row, 7).text()

        


        update_v = Update_c(id_c,Nom,Prenom,Cin,Adress,Tel,Email,Password)
        widget.addWidget(update_v)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def delete_row(self):
        row = self.listec.currentRow()
        id_c = self.listec.item(row, 0).text()
        
        reply = QMessageBox.question(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer cette voiture ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            cur1.execute("DELETE FROM login WHERE id=?", (id_c,))
            conn.commit()
            conn.close()
            listec = Liste_c()
            widget.addWidget(listec)
            widget.setCurrentIndex(widget.currentIndex() + 1)
    def retour(self):
        retour = Admin1()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1) 

class Update_c(QDialog):
    def __init__(self,id_c,Nom,Prenom,Cin,Adress,Tel,Email,Password):
        super(Update_c, self).__init__()
        loadUi("update_client.ui", self) 
        self.signup.clicked.connect(self.Ajouter_clients)
        

        self.id=id_c
        self.Nom.setText(Nom)  
        self.Prenom.setText(Prenom) 
        self.Cin.setText(Cin)  
        self.Adress.setText(Adress)  
        self.Tel.setText(Tel)
        self.Email.setText(Email)
        self.Password.setText(Password)
        self.CPassword.setText(Password)






    def Ajouter_clients(self):
   
        nom_c=self.Nom.text()
        prenom_c=self.Prenom.text()
        cin_c=self.Cin.text()
        adress_c=self.Adress.text()
        tel_c=self.Tel.text()
        email_c=self.Email.text()
        password_c=self.Password.text()
        CPassword_c=self.CPassword.text()

        if len(nom_c)==0 or len(prenom_c)==0 or len(cin_c)==0 or len(adress_c)==0 or len(tel_c)==0 or len(email_c)==0 or len(password_c)==0 or len(CPassword_c)==0:
            self.success.setText("")
            self.error.setText("Fill all the blanks")
        elif CPassword_c != password_c:
            self.success.setText("")
            self.error.setText("Passwords does not match")
        else:
   
            conn = sqlite3.connect("verification.sqlite")
            cur = conn.cursor()
            user_info = [nom_c, prenom_c, cin_c, adress_c, tel_c, email_c, password_c, self.id]
            cur.execute('UPDATE login SET Nom=?, Prenom=?, Cin=?, Adress=?, Tel=?, Email=?, Password=? WHERE Id=?', user_info)
            conn.commit()
            conn.close()
            Listec = Liste_c()
            widget.addWidget(Listec)
            widget.setCurrentIndex(widget.currentIndex() + 1)   
    


class Liste_r(QDialog):
    def __init__(self):
        super(Liste_r, self).__init__()
        loadUi("Liste_reservation.ui", self)
        self.loaddata()
        self.Retour.clicked.connect(self.retour)
    def loaddata(self):
        conn = sqlite3.connect("verification.sqlite")
        cur = conn.cursor()
        query = "SELECT * FROM reservation"
        self.Lister.setRowCount(20)
        tablerow = 0
        for r in cur.execute(query):
            self.Lister.setItem(tablerow,0,QtWidgets.QTableWidgetItem(str(r[0])))
            self.Lister.setItem(tablerow,1,QtWidgets.QTableWidgetItem(str(r[1])))
            self.Lister.setItem(tablerow,2,QtWidgets.QTableWidgetItem(str(r[2])))
            self.Lister.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(r[3])))
            self.Lister.setItem(tablerow,4,QtWidgets.QTableWidgetItem(str(r[4])))
            self.Lister.setItem(tablerow,5,QtWidgets.QTableWidgetItem(str(r[5])))
            self.Lister.setItem(tablerow,6,QtWidgets.QTableWidgetItem(str(r[6])))
            self.Lister.setItem(tablerow,7,QtWidgets.QTableWidgetItem(str(r[7])))
            self.Lister.setItem(tablerow,8,QtWidgets.QTableWidgetItem(str(r[8])))

           

            delete_button = QPushButton("Supprimer")
            delete_button.clicked.connect(self.delete_row)
            self.Lister.setCellWidget(tablerow, 9 , delete_button)
            tablerow+=1
    
    

    def delete_row(self):
        row = self.Lister.currentRow()
        Matricule_r = self.Lister.item(row, 0).text()
        
        reply = QMessageBox.question(self, "Confirmation", "Êtes-vous sûr de vouloir supprimer cette voiture ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn = sqlite3.connect("verification.sqlite")
            cur1 = conn.cursor()
            rows_deleted = cur1.execute("DELETE FROM reservation WHERE Matricule=?", (Matricule_r,)).rowcount
        if rows_deleted:
            cur1.execute('UPDATE voiture SET Disponibilite = ? WHERE Matricule = ?', [0, Matricule_r])
            conn.commit()
            conn.close()
            lister = Liste_r()
            widget.addWidget(lister)
            widget.setCurrentIndex(widget.currentIndex() + 1)
        

    def retour(self):
        retour = Admin1()
        widget.addWidget(retour)
        widget.setCurrentIndex(widget.currentIndex() + 1) 






            
            



    
            
            
            


app = QApplication(sys.argv)
welcome = WelcomeScreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(welcome)
widget.setFixedHeight(391)
widget.setFixedWidth(651)
widget.setWindowTitle("Gestion de location de voiture")
widget.show()
try:
    sys.exit(app.exec())
except:
    print("Exiting")
