package sample;

import java.io.*;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

class Contact implements Serializable {
    private String firstName;
    private String lastName;
    private String id;
    private String phone;
    private ArrayList<Meeting> closeContacts = new ArrayList<>();

    public Contact(String id, String firstName, String lastName,  String phone) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.id = id;
        this.phone = phone;
    }

    public void setFirstName(String firstName) {
        this.firstName =  firstName;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setLastName(String lastName) {
        this.lastName =  lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getFullName() {
        return firstName + " " + lastName;
    }

    public void setId(String id) {
        this.id =  id;
    }

    public String getId () {
        return id;
    }

    public void setPhone(String phone) {
        this.phone = phone;
    }

    public String getPhone () {
        return phone;
    }

    public void addCloseContact(Contact C, String date, String time){
        closeContacts.add(new Meeting(C, date, time));
    }

    public Meeting getCloseContact(int i){
        if ((i>-1) && (i < closeContacts.size()))
            return closeContacts.get(i);
        return null;
    }

    public int closeContactsSize (){
        return closeContacts.size();
    }

    public String toString() {
        return (getId() + " - " + getFirstName() + " " + getLastName() + ", " + getPhone());
    }


    public void sortListByName(){
        closeContacts.sort(new Comparator<Meeting>() {
            public int compare(Meeting m1, Meeting m2) {
                return m1.compareName(m2);
            }
        });
    }

    public void sortListByDate(){
        Collections.sort(closeContacts, new Comparator<Meeting>() {
            public int compare(Meeting m1, Meeting m2) {
                return m1.compareDate(m2);
            }
        });
    }

    void saveAllCloseContactList() {
        try {
            ObjectOutputStream os = new ObjectOutputStream(new FileOutputStream("Meeting.txt"));{
                os.writeObject(closeContacts);
            }
            os.close();
        } catch (Exception ex) {
            System.out.println("Failed to save.");
            ex.printStackTrace();
        }
    }

}
