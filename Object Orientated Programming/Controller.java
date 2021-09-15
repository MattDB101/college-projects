package sample;

import javafx.scene.control.Label;
import javafx.scene.control.ListView;
import javafx.scene.control.TextField;
import javafx.stage.Stage;
import java.io.*;
import java.util.ArrayList;


public class Controller {
    private Contact contact;
    private ContactList contactList = new ContactList();


    public void save() throws IOException {
        contactList.saveAllList();
    }

    public void load() throws IOException, ClassNotFoundException {

        File f = new File("ContactList.txt");
        if (f.exists()) {
            contactList.loadAllList();
        } else {
            System.out.println("No prior save to be loaded.");
        }
    }


    public void addUser(TextField idInput, TextField fnameInput, TextField lnameInput, TextField phoneInput) {
        if (isCorrect(idInput, fnameInput, lnameInput, phoneInput)) {
            fnameInput.setPromptText("First Name");
            fnameInput.setStyle(null);
            lnameInput.setPromptText("Last Name");
            lnameInput.setStyle(null);
            idInput.setPromptText("Unique ID");
            idInput.setStyle(null);
            phoneInput.setPromptText("Phone Number");
            phoneInput.setStyle(null);
            contactList.addContact(new Contact(idInput.getText(), fnameInput.getText(), lnameInput.getText(), phoneInput.getText()));
        }
    }


    private boolean isCorrect(TextField idInput, TextField fnameInput, TextField lnameInput, TextField phoneInput) {
        boolean ans = true;
        if (!isUniqueID(idInput)) {
            idInput.setPromptText("Contact ID must be unique.");
            idInput.setStyle("-fx-prompt-text-fill: red");
            ans = false;
        }

        if (!isAlpha(fnameInput)) {
            fnameInput.setPromptText("Alphabetic characters only.");
            fnameInput.setStyle("-fx-prompt-text-fill: red");
            ans = false;
        }

        if (!isAlpha(lnameInput)) {
            lnameInput.setPromptText("Alphabetic characters only.");
            lnameInput.setStyle("-fx-prompt-text-fill: red");
            ans = false;
        }

        if (!isPhone(phoneInput)) {
            phoneInput.setPromptText("9-14 digits & \"+\" character.");
            phoneInput.setStyle("-fx-prompt-text-fill: red");
            ans = false;
        }
        return ans;
    }


    private boolean isPhone(TextField input) {
        boolean ans = false;
        if (input.getText().matches("^[+0-9]{9,14}$")) {
            ans = true;
        }
        return ans;
    }


    private boolean isUniqueID(TextField input) {
        boolean ans = true;
        for (int i = 0; i < contactList.getSize(); i++) {
            if (contactList.getContact(i).getId().equalsIgnoreCase(input.getText())) {
                ans = false;
            }
        }
        if (input.getText().isEmpty()) {
            ans = false;
        }
        return ans;
    }


    private boolean isAlpha(TextField input) {
        String name = input.getText();
        return name.matches("[a-zA-Z ?\\s]+");
    }


    public void remContactByID(String id) {
        contactList.remContactByID(id);
    }


    public Contact getContact(int i) {
        return contactList.getContact(i);
    }

    public Contact findByID(String id) {
        return contactList.findByID(id);
    }

    public ArrayList<Contact> getContactList() {
        return contactList.getContactList();
    }

    public int getSize() {
        return contactList.getSize();
    }

    public Boolean addCloseContact(Contact c1, Contact c2, String date, String time, Label warningText) {
        boolean success = true;
        if (c1.equals(c2)) {
            success = false;
            warningText.setText("Please select two separate contacts.");

        } else {
            for (int i = 0; i < c1.closeContactsSize(); i++) {
                if (c1.getCloseContact(i).getDate().equals(date) && c1.getCloseContact(i).getTime().equals(time) && c1.getCloseContact(i).getContact().equals(c2)) {
                    success = false;
                    warningText.setText("Meeting already exists.");
                }
            }
            if (success) {
                c1.addCloseContact(c2, date, time);
                c2.addCloseContact(c1, date, time);
                success = true;
            }
        }
        return success;
    }

    public void updateCloseContactList(Contact c, ListView closeContactsList) {
        closeContactsList.refresh();
        closeContactsList.getItems().clear();
        for (int i = 0; i < c.closeContactsSize(); i++) {
            closeContactsList.getItems().add(c.getCloseContact(i));
        }
    }

    public void updateList(ListView listView) {
        listView.refresh();
        listView.getItems().clear();
        for (int i = 0; i < getSize(); i++) {
            listView.getItems().add(getContact(i));
        }
    }

    public void closeProgram(Stage window) {
        boolean ans = ConfirmBox.display("Quit", " Are you sure you want to close? \nAny unsaved changes will be lost.", "Save & Quit.", "Exit without saving.");
        if (ans) {
            try {
                save();
                //save("contacts.txt");
            } catch (IOException ioException) {
                ioException.printStackTrace();
            }
            window.close();
        } else {
            window.close();
        }
    }

    public void sortByName(Contact contact){
        contact.sortListByName();
    }

    public void sortByDate(Contact contact){
        contact.sortListByDate();
    }


}
