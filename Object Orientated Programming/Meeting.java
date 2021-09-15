package sample;
import java.io.Serializable;

public class Meeting implements Serializable {
    private Contact contact;
    private String date;
    private String time;

    public Meeting(Contact contact, String date, String time) {
        this.contact = contact;
        this.date = date;
        this.time = time;
    }

    public Contact getContact() {
        return contact;
    }

    public String getDate() {
        return date;
    }

    public String getTime() {
        return time;
    }

    public String toString() {
        return (" | " + getDate() + " | " + getTime() + " | ID: " + getContact().getId() + " - " + getContact().getFirstName() + " " + getContact().getLastName() + " - Tel: " + getContact().getPhone());
    }

    public int compareName(Meeting m) {
        return getContact().getFullName().compareTo(m.getContact().getFullName());
    }


    public int compareDate(Meeting m) {
        return getDate().compareTo(m.getDate());
    }


}
