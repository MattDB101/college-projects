package sample;

import javafx.application.Application;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.*;
import javafx.stage.Stage;
import java.io.IOException;
import java.text.DecimalFormat;
import java.time.LocalDate;


public class Main extends Application {
    private ObservableList names = FXCollections.observableArrayList();
    private Controller control;
    private Stage window;
    private ListView<Contact> listView;
    private ListView<Meeting> closeContactsList;
    private ComboBox<String> contact1DropDown;
    private ComboBox<String> contact2DropDown;
    private ComboBox<String> findContactsDropDown;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception {

        control = new Controller();
        window = primaryStage;
        window.setTitle("COVID-19 | Close Contact Tracker");
        window.setOnCloseRequest(e -> {
            e.consume();
            control.closeProgram(window);
        });



        // H1BOX
        HBox h1Box = new HBox();
        Text h1 = new Text("Add a Contact");
        h1.setTextAlignment(TextAlignment.CENTER);
        h1.setFont(Font.font("Dubai", FontWeight.NORMAL, FontPosture.REGULAR, 25));
        h1.setFill(Color.WHITE);
        h1Box.setStyle("-fx-padding: 25 0 10 0;");
        h1Box.setAlignment(Pos.CENTER);
        h1Box.getChildren().addAll(h1);
        h1Box.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));


        // FNAME LABEL
        Label fnameLabel = new Label("First Name: ");
        fnameLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        fnameLabel.setTextFill(Color.WHITE);


        // LNAME LABEL
        Label lnameLabel = new Label("Last Name: ");
        lnameLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        lnameLabel.setTextFill(Color.WHITE);


        // NAME LABEL BOX
        HBox nameLabelBox = new HBox();
        nameLabelBox.getChildren().addAll(fnameLabel, lnameLabel);
        nameLabelBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        nameLabelBox.setAlignment(Pos.CENTER_LEFT);
        nameLabelBox.setSpacing(145);
        GridPane.setConstraints(nameLabelBox, 0, 0);


        // FNAME INPUT
        TextField fnameInput = new TextField();
        fnameInput.setPromptText("First Name");
        fnameInput.setPrefWidth(175);


        // LNAME INPUT
        TextField lnameInput = new TextField();
        lnameInput.setPrefWidth(175);
        lnameInput.setPromptText("Last Name");


        // NAME INPUT BOX
        HBox nameInputBox = new HBox();
        nameInputBox.getChildren().addAll(fnameInput, lnameInput);
        nameInputBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        nameInputBox.setSpacing(50);
        nameInputBox.setAlignment(Pos.CENTER);
        GridPane.setConstraints(nameInputBox, 0, 1);


        // ID LABEL
        Label idLabel = new Label("Unique ID: ");
        idLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        idLabel.setTextFill(Color.WHITE);


        // PHONE LABEL
        Label phoneLabel = new Label("Phone Number: ");
        phoneLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        phoneLabel.setTextFill(Color.WHITE);


        // ID/PHONE LABEL BOX
        HBox idPhoneLabelBox = new HBox();
        idPhoneLabelBox.getChildren().addAll(idLabel, phoneLabel);
        idPhoneLabelBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        idPhoneLabelBox.setAlignment(Pos.CENTER_LEFT);
        idPhoneLabelBox.setSpacing(150);
        GridPane.setConstraints(idPhoneLabelBox, 0, 2);


        // ID INPUT
        TextField idInput = new TextField();
        idInput.setPromptText("Numeric ID");
        idInput.setPrefWidth(175);


        // PHONE INPUT
        TextField phoneInput = new TextField();
        phoneInput.setPrefWidth(175);
        phoneInput.setPromptText("Phone");


        // ID/PHONE INPUT BOX
        HBox idPhoneInputBox = new HBox();
        idPhoneInputBox.getChildren().addAll(idInput, phoneInput);
        idPhoneInputBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        idPhoneInputBox.setSpacing(50);
        idPhoneInputBox.setAlignment(Pos.CENTER);
        GridPane.setConstraints(idPhoneInputBox, 0, 3);


        // LISTVIEW
        listView = new ListView<>();
        listView.getSelectionModel().setSelectionMode(SelectionMode.MULTIPLE);
        listView.setBackground(new Background(new BackgroundFill(Color.rgb(249, 249, 249), new CornerRadii(5), Insets.EMPTY)));
        listView.setPrefHeight(180);
        GridPane.setConstraints(listView, 0, 8);
        GridPane.setColumnSpan(listView, 2);


        // ADD-USER BUTTON
        Button addUserButton = new Button("Add User");
        addUserButton.setMinWidth(75);
        addUserButton.setOnAction(e -> {
            control.addUser(idInput, fnameInput, lnameInput, phoneInput);
            contact1DropDown.getItems().add(idInput.getText() + " - " + fnameInput.getText() + " " + lnameInput.getText());
            contact2DropDown.getItems().add(idInput.getText() + " - " + fnameInput.getText() + " " + lnameInput.getText());
            findContactsDropDown.getItems().add(idInput.getText() + " - " + fnameInput.getText() + " " + lnameInput.getText());
            control.updateList(listView);
            idInput.clear();
            fnameInput.clear();
            lnameInput.clear();
            phoneInput.clear();
        });


        // REMOVE BUTTON
        Button removebutton = new Button("Remove");
        removebutton.setMinWidth(75);
        removebutton.setOnAction(e -> {
            ObservableList<Contact> removedContacts;
            removedContacts = listView.getSelectionModel().getSelectedItems();
            for(int i=0;i<removedContacts.size();i++){
                control.remContactByID(removedContacts.get(i).getId());
                contact1DropDown.getItems().remove(removedContacts.get(i).getId() + " - " + removedContacts.get(i).getFirstName() + " " + removedContacts.get(i).getLastName());
                contact2DropDown.getItems().remove(removedContacts.get(i).getId() + " - " + removedContacts.get(i).getFirstName() + " " + removedContacts.get(i).getLastName());
                findContactsDropDown.getItems().remove(removedContacts.get(i).getId() + " - " + removedContacts.get(i).getFirstName() + " " + removedContacts.get(i).getLastName());
            }
            control.updateList(listView);
        });


        // UPDATE BUTTON
        Button showButton = new Button("Update List");
        showButton.setMinWidth(75);
        showButton.setOnAction(e -> control.updateList(listView));


        // BUTTON BOX 1
        HBox buttonBox1 = new HBox(15);
        buttonBox1.getChildren().addAll(addUserButton, removebutton, showButton);
        buttonBox1.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        GridPane.setConstraints(buttonBox1, 0, 6);
        GridPane.setColumnSpan(buttonBox1, 2);


        // SAVE BUTTON
        Button saveButton = new Button("Save");
        saveButton.setMinWidth(75);
        saveButton.setOnAction(e -> {

            boolean ans = ConfirmBox.display("Save", "Are you sure you want to overwrite past data with current data?", "Save.", "Cancel.");
            if (ans) {

                try {
                    control.save();
                    //control.save("contacts.txt");
                } catch (IOException ioException) {
                    ioException.printStackTrace();
                }
            }
        });


        // LOAD BUTTON
        Button loadButton = new Button("Load");
        window.close();
        loadButton.setMinWidth(75);
        loadButton.setOnAction(e -> loadAndUpdate());





        // BUTTON BOX 2
        HBox buttonBox2 = new HBox(15);
        buttonBox2.getChildren().addAll(saveButton, loadButton);
        buttonBox2.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        GridPane.setConstraints(buttonBox2, 0, 10);
        GridPane.setColumnSpan(buttonBox2, 2);


        // EXIT BUTTON
        Button exitButton = new Button("Exit");
        exitButton.setMinWidth(75);
        exitButton.setOnAction(e -> control.closeProgram(window));


        // EXIT BOX
        HBox exitBox = new HBox(15);
        exitBox.getChildren().add(exitButton);
        exitBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        exitBox.setAlignment(Pos.BOTTOM_RIGHT);
        exitBox.setPadding(new Insets(10, 10, 10, 10));


        // GRIDPANE
        GridPane grid = new GridPane();
        grid.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        grid.setAlignment(Pos.BASELINE_CENTER);
        grid.setVgap(10);
        grid.setHgap(10);
        grid.getChildren().addAll(nameLabelBox, nameInputBox, idPhoneInputBox, idPhoneLabelBox, buttonBox1, listView, buttonBox2);


        // BORDERPANE
        BorderPane borderPane1 = new BorderPane();
        borderPane1.setTop(h1Box);
        borderPane1.setCenter(grid);
        borderPane1.setBottom(exitBox);


        //Creating a TabPane
        TabPane tabPane = new TabPane();
        Tab tab1 = new Tab();
        tab1.setText("Add a contact");
        tab1.setContent(borderPane1);
        control.load();
        control.updateList(listView);


        // TAB 2

        // H1BOX
        HBox h1Box2 = new HBox();
        Text h2 = new Text("Record a Close Contact");
        h2.setTextAlignment(TextAlignment.CENTER);
        h2.setFont(Font.font("Dubai", FontWeight.NORMAL, FontPosture.REGULAR, 25));
        h2.setFill(Color.WHITE);
        h1Box2.setStyle("-fx-padding: 25 0 10 0;");
        h1Box2.setAlignment(Pos.BASELINE_CENTER);
        h1Box2.getChildren().addAll(h2);
        h1Box2.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));


        // CONTACT1 LABEL
        Label c1Label = new Label("First Contact: ");
        c1Label.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        c1Label.setTextFill(Color.WHITE);


        // CONTACT2 LABEL
        Label c2Label = new Label("Second Contact: ");
        c2Label.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        c2Label.setTextFill(Color.WHITE);


        // CONTACT LABEL BOX
        HBox contactLabelBox = new HBox();
        contactLabelBox.getChildren().addAll(c1Label, c2Label);
        contactLabelBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        contactLabelBox.setAlignment(Pos.CENTER_LEFT);
        contactLabelBox.setSpacing(110);
        GridPane.setConstraints(contactLabelBox, 0, 2);
        GridPane.setColumnSpan(contactLabelBox, 2);

        // CONTACT1 INPUT
        contact1DropDown = new ComboBox<>();
        for (int i=0; i<control.getSize(); i++){
            contact1DropDown.getItems().add(control.getContact(i).getId() + " - " + control.getContact(i).getFirstName() + " " + control.getContact(i).getLastName());
        }
        contact1DropDown.setPrefWidth(175);
        contact1DropDown.getSelectionModel().selectFirst();

        // CONTACT2 INPUT
        contact2DropDown = new ComboBox<>();


        contact2DropDown.setPrefWidth(175);
        contact2DropDown.getSelectionModel().select(1);

        // CONTACT INPUT BOX
        HBox contactInputBox = new HBox();
        contactInputBox.getChildren().addAll(contact1DropDown, contact2DropDown);
        contactInputBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        contactInputBox.setSpacing(25);
        contactInputBox.setAlignment(Pos.CENTER_LEFT);
        GridPane.setConstraints(contactInputBox, 0, 3);
        GridPane.setColumnSpan(contactInputBox, 2);

        // DATE LABEL
        Label dateLabel = new Label("Date: ");
        dateLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        dateLabel.setTextFill(Color.WHITE);


        // TIME LABEL
        Label timeLabel = new Label("Time: ");
        timeLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        timeLabel.setTextFill(Color.WHITE);


        // DATE TIME LABEl BOX
        HBox dateTimeLabelBox = new HBox();
        dateTimeLabelBox.getChildren().addAll(dateLabel, timeLabel);
        dateTimeLabelBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        dateTimeLabelBox.setAlignment(Pos.CENTER_LEFT);
        dateTimeLabelBox.setSpacing(160);
        GridPane.setConstraints(dateTimeLabelBox, 0, 5);
        GridPane.setColumnSpan(dateTimeLabelBox, 4);

        // DATE INPUT
        DatePicker datePicker = new DatePicker(LocalDate.now());
        datePicker.getEditor().setDisable(true);


        // TIME INPUT
        DecimalFormat twodigits = new DecimalFormat("00");
        ComboBox<String> hourDropDown = new ComboBox<>();
        ComboBox<String> minuteDropDown = new ComboBox<>();
        ComboBox<String> amPmDropDown = new ComboBox<>();
        for (int i=1; i<=12; i++){ hourDropDown.getItems().add(twodigits.format(i)); }
        for (int i=0; i<60; i++){ minuteDropDown.getItems().add(twodigits.format(i)); }
        amPmDropDown.getItems().addAll("AM","PM");
        hourDropDown.setPrefWidth(55);
        hourDropDown.getSelectionModel().selectLast();
        minuteDropDown.setPrefWidth(55);
        minuteDropDown.getSelectionModel().selectFirst();
        amPmDropDown.setPrefWidth(65);
        amPmDropDown.getSelectionModel().selectLast();
        HBox timeInputBox = new HBox();
        timeInputBox.getChildren().addAll(hourDropDown, minuteDropDown, amPmDropDown);
        timeInputBox.setAlignment(Pos.CENTER_LEFT);
        timeInputBox.setSpacing(2);


        // DATETIME INPUT BOX
        HBox dateTimeInputBox = new HBox();
        dateTimeInputBox.getChildren().addAll(datePicker,timeInputBox);
        dateTimeInputBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        dateTimeInputBox.setSpacing(27);
        dateTimeInputBox.setAlignment(Pos.CENTER_LEFT);
        GridPane.setConstraints(dateTimeInputBox, 0, 6);
        GridPane.setColumnSpan(dateTimeInputBox, 2);


        // WARNING TEXT
        Label warningText = new Label("");
        warningText.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 13));
        warningText.setTextFill(Color.RED);


        // WARNING TEXTBOX
        HBox warningTextBox = new HBox();
        warningTextBox.getChildren().addAll(warningText);
        warningTextBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        warningTextBox.setAlignment(Pos.CENTER_LEFT);
        GridPane.setConstraints(warningTextBox, 0, 8);


        // ADD-MEETING BUTTON
        Button addfindContactsButton = new Button("Record Close Contact");
        addfindContactsButton.setMinWidth(75);
        addfindContactsButton.setOnAction(e -> {
            warningText.setText("");
            Contact c1 = control.findByID(contact1DropDown.getValue().substring(0,2));
            Contact c2 = control.findByID(contact2DropDown.getValue().substring(0,2));
            String date = String.valueOf(datePicker.getValue());
            String time = hourDropDown.getValue() + ":" + minuteDropDown.getValue() + " " + amPmDropDown.getValue();
            control.addCloseContact(c1,c2, date, time, warningText);
        });


        // BUTTON BOX 3
        HBox buttonBox3 = new HBox(15);
        buttonBox3.getChildren().addAll(addfindContactsButton);
        buttonBox3.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        GridPane.setConstraints(buttonBox3, 0, 10);
        GridPane.setColumnSpan(buttonBox3, 2);


        // EXIT BUTTON
        Button exitButton2 = new Button("Exit");
        exitButton2.setMinWidth(75);
        exitButton2.setOnAction(e -> control.closeProgram(window));


        // EXIT BOX
        HBox exitBox2 = new HBox(15);
        exitBox2.getChildren().add(exitButton2);
        exitBox2.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        exitBox2.setAlignment(Pos.BOTTOM_RIGHT);
        exitBox2.setPadding(new Insets(10, 10, 10, 10));


        // GRIDPANE
        GridPane grid2 = new GridPane();
        grid2.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        grid2.setAlignment(Pos.BASELINE_CENTER);
        grid2.setVgap(10);
        grid2.setHgap(10);
        grid2.getChildren().addAll(contactLabelBox, contactInputBox, dateTimeLabelBox, dateTimeInputBox, buttonBox3, warningTextBox);


        // BORDERPANE
        BorderPane borderPane2 = new BorderPane();
        borderPane2.setTop(h1Box2);
        borderPane2.setCenter(grid2);
        borderPane2.setBottom(exitBox2);


        Tab tab2 = new Tab();
        tab2.setText("Record a close contact");
        tab2.setContent(borderPane2);

        // END OF TAB 2



        // TAB 3

        // H1BOX
        HBox h1Box3 = new HBox();
        Text h3 = new Text("View Close Contacts");
        h3.setTextAlignment(TextAlignment.CENTER);
        h3.setFont(Font.font("Dubai", FontWeight.NORMAL, FontPosture.REGULAR, 25));
        h3.setFill(Color.WHITE);
        h1Box3.setStyle("-fx-padding: 25 0 10 0;");
        h1Box3.setAlignment(Pos.CENTER);
        h1Box3.getChildren().addAll(h3);
        h1Box3.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));


        // FIND CONTACTS LABEL
        Label findContactsLabel = new Label("Covid Positive Contact: ");
        findContactsLabel.setFont(Font.font("helvetica", FontWeight.NORMAL, FontPosture.REGULAR, 15));
        findContactsLabel.setTextFill(Color.WHITE);


        // FIND CONTACTS LABEL BOX
        HBox findContactsLabelBox = new HBox();
        findContactsLabelBox.getChildren().addAll(findContactsLabel);
        findContactsLabelBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        findContactsLabelBox.setAlignment(Pos.CENTER);
        GridPane.setConstraints(findContactsLabelBox, 0, 2);
        GridPane.setColumnSpan(findContactsLabelBox, 2);


        // CLOSECONTACTS LISTVIEW
        closeContactsList = new ListView<>();
        closeContactsList.setBackground(new Background(new BackgroundFill(Color.rgb(249, 249, 249), new CornerRadii(5), Insets.EMPTY)));
        closeContactsList.setPrefWidth(400);
        GridPane.setConstraints(closeContactsList, 0, 8);
        GridPane.setColumnSpan(closeContactsList, 2);


        // FIND CONTACTS INPUT
        findContactsDropDown = new ComboBox<>();
        updateDropDowns();
        findContactsDropDown.valueProperty().addListener((obs, oldItem, newItem) -> {
                    control.updateCloseContactList(control.findByID(newItem.substring(0, 2)), closeContactsList);
                });


        // FIND CONTACTS INPUT BOX
        HBox findContactsInputBox = new HBox();
        findContactsInputBox.getChildren().addAll(findContactsDropDown, closeContactsList);
        findContactsInputBox.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        findContactsInputBox.setAlignment(Pos.CENTER);
        GridPane.setConstraints(findContactsInputBox, 0, 4);
        GridPane.setColumnSpan(findContactsInputBox, 2);


        // UPDATE LIST BUTTON
        Button updateListButton = new Button("Update List");
        updateListButton.setMinWidth(75);
        updateListButton.setOnAction(e -> control.updateCloseContactList(control.findByID(findContactsDropDown.getValue().substring(0, 2)), closeContactsList));


        // SORT BY NAME BUTTON
        Button sortNameButton = new Button("Sort By Name");
        sortNameButton.setMinWidth(75);
        sortNameButton.setOnAction(e -> {
            Contact c = control.findByID(findContactsDropDown.getValue().substring(0, 2));
            control.sortByName(c);
            control.updateCloseContactList(c, closeContactsList);
        });


        // SORT BY DATE BUTTON
        Button sortDateButton = new Button("Sort By Date");
        sortDateButton.setMinWidth(75);
        sortDateButton.setOnAction(e -> {
            Contact c = control.findByID(findContactsDropDown.getValue().substring(0, 2));
            control.sortByDate(c);
            control.updateCloseContactList(c, closeContactsList);
        });


        // EXIT BUTTON
        Button exitButton3 = new Button("Exit");
        exitButton3.setMinWidth(75);
        exitButton3.setOnAction(e -> control.closeProgram(window));


        // EXIT BUTTON BOX
        HBox exitBox3 = new HBox(15);
        exitBox3.getChildren().addAll(sortDateButton, sortNameButton, updateListButton, exitButton3);
        exitBox3.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        exitBox3.setAlignment(Pos.BOTTOM_RIGHT);
        exitBox3.setPadding(new Insets(10, 10, 10, 10));


        // GRIDPANE
        GridPane grid3 = new GridPane();
        grid3.setBackground(new Background(new BackgroundFill(Color.rgb(48, 48, 48), new CornerRadii(0), Insets.EMPTY)));
        grid3.setAlignment(Pos.BASELINE_CENTER);
        grid3.setVgap(10);
        grid3.setHgap(10);
        grid3.getChildren().addAll(findContactsLabelBox, findContactsInputBox, closeContactsList);


        // BORDERPANE
        BorderPane borderPane3 = new BorderPane();
        borderPane3.setTop(h1Box3);
        borderPane3.setCenter(grid3);
        borderPane3.setBottom(exitBox3);


        Tab tab3 = new Tab();
        tab3.setText("View Close Contacts");
        tab3.setContent(borderPane3);


        tabPane.getTabs().addAll(tab1, tab2, tab3);
        tabPane.setTabClosingPolicy(TabPane.TabClosingPolicy.UNAVAILABLE);
        Scene scene = new Scene(tabPane, 500, 500);


        // STAGE
        window.setScene(scene);
        window.setMinWidth(500);
        window.setMinHeight(600);
        window.show();

    }


    private void updateDropDowns() {
        contact1DropDown.getItems().removeAll(contact1DropDown.getItems());
        contact2DropDown.getItems().removeAll(contact2DropDown.getItems());
        findContactsDropDown.getItems().removeAll(findContactsDropDown.getItems());
        for (int i=0; i<control.getSize(); i++){
            contact1DropDown.getItems().add(control.getContact(i).getId() + " - " + control.getContact(i).getFirstName() + " " + control.getContact(i).getLastName());
            contact2DropDown.getItems().add(control.getContact(i).getId() + " - " + control.getContact(i).getFirstName() + " " + control.getContact(i).getLastName());
            findContactsDropDown.getItems().add(control.getContact(i).getId() + " - " + control.getContact(i).getFirstName() + " " + control.getContact(i).getLastName());
        }
    }


    private void loadAndUpdate() {
        boolean ans = ConfirmBox.display("Load", "Are you sure you want to load saved data? \n\tAny unsaved changes will be lost.", "Load.", "Cancel.");
        if (ans) {
            try {
                control.load();
            } catch (IOException | ClassNotFoundException ioException) {
                ioException.printStackTrace();
            }
            try {
                control.load();
            } catch (IOException ioException) {
                ioException.printStackTrace();
            } catch (ClassNotFoundException classNotFoundException) {
                classNotFoundException.printStackTrace();
            }
            control.updateList(listView);
            updateDropDowns();
        }
    }
}
