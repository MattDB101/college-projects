const express = require("express")
const MongoClient = require("mongodb").MongoClient
const bcrypt = require("bcrypt")

const router = express.Router()
const url= "mongodb://localhost:27017/" // set the db connection URL
const dbname = "SSWebDev" // set the db name
const coll = "users" // set the db collection

router.get("/", (req, res) => {
  res.render("index.ejs", {loggedIn: req.signedCookies.user, auth:req.signedCookies.user === "admin"}) //render home page, check if user is logged & if user has auth perms
})

router.get("/login", (req, res) => {
  if (req.signedCookies.user) { // check if user is logged in
    res.status(400).render("error.ejs", {loggedIn: req.signedCookies.user, errorMessage: "Error 400, You're already logged in.", auth: req.signedCookies.user === "admin"}) // if user is logged in error
  } else { res.render("login.ejs")} // render login page
})

router.post("/login", (req, res) => {
  (MongoClient.connect(url, (err, db) => { // coonect to db
    if (err) throw err
    db.db(dbname).collection(coll).find({username: req.body.username}).toArray( async (err, result) => { // check if theres a matching username on the db to that of the username the user input
      if (err) throw err
      if (result[0] != null) { // if there is a matching username
        if(!(await bcrypt.compare(req.body.password, result[0].password))){ // check if theres a matching password on the db to that of the password the user input
          res.statusCode = 200; // set status code
          res.setHeader("Content-Type", "text/html");
          res.render("login.ejs", {loginMessage: "Incorrect password"}) // if theres no match render the login page with the failure message

        } else {
            if(result[0].role == "Admin") { // if password matches and the user on the db has admin permissions
              res.cookie("user","admin",{signed: true}); // place cookie with admin value in users browser
              res.redirect("/admin") } // redirect to admin panel
              
            if(result[0].role == "Ordinary") { // if password matches and the user on the db has ordinary permissions
              res.cookie("user","ordinary",{signed: true}); // place cookie with ordinary value in users browser
              res.redirect("/about") } // redirect to about panel
    
            if(result[0].role == "Guest") { // if password matches and the user on the db has guest permissions
              res.cookie("user","guest",{signed: true}); // place cookie with guest value in users browser
              res.redirect("/contact") } // redirect to contact panel
          } 

      } else { // if theres no matching username
        res.statusCode = 200; // set status code
        res.setHeader("Content-Type", "text/html");
        res.render("login.ejs", {loginMessage: "Incorrect Username"})  // if theres no match render the login page with the failure message
      }  
    })
  }))
})

router.get("/help", (req, res) => { // render help page, check if user is logged & if user has auth perms
  res.render("help.ejs", {loggedIn: req.signedCookies.user, auth: req.signedCookies.user === "admin"})
})
  
router.get("/about", (req, res) => { // render about  page, check if user is logged & if user has auth perms
  res.render("about.ejs", {loggedIn: req.signedCookies.user, auth: req.signedCookies.user === "admin"})
})

router.get("/contact", (req, res) => { // render contact page, check if user is logged & if user has auth perms
  res.render("contact.ejs", {loggedIn: req.signedCookies.user, auth: req.signedCookies.user === "admin"})
})

router.get("/logout", (req, res) => { // render home page
  if (req.signedCookies.user) { // check if user is logged
      res.clearCookie("user") // remove loggedin cookie from users browser
      res.redirect("/"); // redirect to home page
  } else {
      res.redirect("/login"); // if user isn't logged in when they try to lougout, redirect to login page
  }
});

module.exports = router; // export