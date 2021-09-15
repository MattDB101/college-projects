package sample;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.HBox;
import javafx.stage.Modality;
import javafx.stage.Stage;

public class ConfirmBox {

    private static boolean ans;

    public static boolean display(String title, String message, String b1text, String b2text) {
        Stage window = new Stage();
        window.initModality(Modality.APPLICATION_MODAL); //block events until this window has been dealt with.
        window.setTitle(title);
        window.setMinWidth(350);
        window.setMinHeight(200);
        Label l1 = new Label();
        l1.setText(message);

        Button yes = new Button(b1text);
        Button no = new Button(b2text);

        yes.setOnAction(e -> {
            ans = true;
            window.close();
        });

        no.setOnAction(e -> {
            ans = false;
            window.close();
        });

        HBox text = new HBox(10);
        text.getChildren().add(l1);
        text.setAlignment(Pos.CENTER);
        text.setPadding(new Insets(20, 0, 0, 0));

        HBox buttons = new HBox(10);
        buttons.setAlignment(Pos.BASELINE_CENTER);
        buttons.getChildren().addAll(no, yes);
        buttons.setPadding(new Insets(20, 0, 0, 0));

        BorderPane borderPane = new BorderPane();
        borderPane.setTop(text);
        borderPane.setCenter(buttons);
        Scene scene = new Scene(borderPane, 200, 100);
        window.setMinWidth(450);
        window.setMinHeight(155);
        window.setMaxWidth(450);
        window.setMaxHeight(155);
        window.setScene(scene);
        window.showAndWait();

        return ans;
    }

}
