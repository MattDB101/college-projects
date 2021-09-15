const cookieParser = require("cookie-parser");
const express = require("express")

const app = express()
const hostname = "localhost";
const port = 3000;

app.set("view engine", "ejs") //set view engine to use .ejs files
app.use(express.static("./public")) //set style.css location
app.use(express.urlencoded({ extended: false })) //read data from form
app.use(cookieParser("12345-67890-09876-54321")) // string used to make cookie secret
app.use("/", require("./routes/pages")) // when going to / look in /routes/pages
app.use("/admin", require("./routes/admin")) // when going to /admin/ look in /routes/admin

app.use((req, res, next) => { 
    res.status(404).render("error.ejs", {loggedIn: req.signedCookies.user, auth:req.signedCookies.user === "admin", errorMessage: "Error 404, Page not found."}) // 404 if page cannot be located
})

app.use((err, req, res, next) => {
    res.status(err.status || 500).render("error.ejs", {loggedIn: req.signedCookies.user, auth:req.signedCookies.user === "admin", errorMessage: err.message}) // generic error
})

app.listen(port,hostname,()=>{ // tell server to listen on set port on set host, in this case localhost and port 3000
    console.log(`server started on http://${hostname}:${port}`)
})
