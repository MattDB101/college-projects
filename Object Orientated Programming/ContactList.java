package sample;


import java.io.*;
import java.util.ArrayList;

public class ContactList implements Serializable {
    private ArrayList<Contact> contacts;

    public ContactList()
    {
        contacts = new ArrayList<Contact> ();
    }

    public ArrayList<Contact> getContactList(){
        return contacts;
    }

    public void addContact(Contact c)
    {
        contacts.add(c);
    }

    public void remContact(int i)
    {
        if ((i>-1) && (i < contacts.size()))
            contacts.remove(i);
    }

    public void remContactByID(String id)
    {
        for (int i = 0 ; i< contacts.size(); i++)
            if (getContact(i).getId().equals(id))
                contacts.remove(i);
    }

    public void remAll() {
        for (int i = 0; i < contacts.size(); i++) {
            contacts.remove(i);
        }
    }

    public Contact getContact(int i) {
        if ((i>-1) && (i < contacts.size()))
            return contacts.get(i);
        return null;
    }

    public Contact findByID(String id) {
        Contact contact = null;
        for (int i = 0; i < contacts.size(); i++) {
            if (contacts.get(i).getId().equals(id)){
                contact = contacts.get(i);

            }
        }
        return contact;
    }

    public int getSize (){
        return contacts.size();
    }

    void saveAllList() {
        try {
            ObjectOutputStream os = new ObjectOutputStream(new FileOutputStream("ContactList.txt"));{
                os.writeObject(contacts);
            }
            os.close();
        } catch (Exception ex) {
            System.out.println("Failed to save.");
            ex.printStackTrace();
        }
    }


    void  loadAllList() {
        try {
            ObjectInputStream is = new ObjectInputStream(new FileInputStream("ContactList.txt"));
            contacts = ( ArrayList<Contact> ) is.readObject();
            is.close();
        }
        catch (Exception ex) {
            System.out.println("Failed to load.");
            ex.printStackTrace();
        }
    }

}
