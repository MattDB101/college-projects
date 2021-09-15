const express = require("express")
const MongoClient = require("mongodb").MongoClient
const bcrypt = require("bcrypt")

const router = express.Router()
const url= "mongodb://localhost:27017/" // set the db connection URL
const dbname = "SSWebDev" // set the db name
const coll = "users" // set the db collection


router.get("/", (req, res) => { 
    if (req.signedCookies.user === "admin") { // check if user has admin permissions
        MongoClient.connect(url, (err, db) => { // if user has admin permission connect to db
        if (err) throw err
    
        db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
            if (err) throw err
            res.render("admin.ejs", { title: "User List", userData: data, tableData: null}) //render admin page, pass data from the database request to generate dropdown list tableData is only used when viewing user's details
            db.close() // close db connection
            })
        })

    } else { // if user tries to access admin panel without admin permissions
        return res.status(401).render("error.ejs", {loggedIn: req.signedCookies.user, errorMessage: "Error 401, You aren't authorized to view this page."}) //render error page, set status 401, show error message that the user isn't authorized to view that page
    }
})
  
router.post("/registeruser", (req, res) => {
    (MongoClient.connect(url, (err, db) => { // connect to db
        if (err) throw err
        db.db(dbname).collection(coll).find({username: req.body.registerUsername}).toArray( async (err, result) => { // check if input username is already in use
            if (err) throw err
            if (result[0] != null) { // if username is already in use
                db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                if (err) throw err
                res.render("admin.ejs", { title: "User List", userData: data, tableData: null, registerMessage: "Username is already in use"}) // render admin panel with error message that the username is already in use
                db.close() // close db connection
            })

            } else { // if username is not already in use
                if(req.body.registerPassword !== req.body.registerConfirmPassword) { // if input passwords do not match one another
                db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                    if (err) throw err
                    res.status(400).render("admin.ejs", { title: "User List", userData: data, tableData: null, registerMessage: "Passwords must be identical"})  // render admin panel with error message that the passwords do not match each other
                    db.close() // close db connection
                })

                } else { // if input passwords match one another
                    let encryptedPassword = await bcrypt.hash(req.body.registerPassword, 10) // encrypt password
                    if (err) throw err
                    db.db(dbname).collection(coll).insertOne({ username: req.body.registerUsername, password: encryptedPassword, role: req.body.role}, (err, res) => { // add user's name, encrypted password & role to the database
                        if (err) throw err
                        db.close() // close db connection
                    })

                    db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                        if (err) throw err
                        res.render("admin.ejs", { title: "User List", userData: data, tableData: null, registerMessage: "User successfully added"}) // render admin panel with message that the user was added
                        db.close() // close db connection
                    })
                }
            }
        })
    }))
})


router.post("/view", (req, res) => { 
    MongoClient.connect(url, (err, db) => { // connect to the db
        if (err) throw err
        if (req.body.viewUser == ""){ // if the user chooses to view all users
            db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users
                if (err) throw err
                res.render("admin.ejs", { title: "User List", userData: data, tableData: data, viewMessage: "All Users:"}) // render admin panel and give all data from the db to the table
                db.close() // close the connection
                })

        } else { // if user chooses to view an invidual user 
            db.db(dbname).collection(coll).find({}).toArray((err, Alldata, fields) => { // get all users, this is used to fill dropdown menu of all users
                if (err) throw err
                db.db(dbname).collection(coll).find({username: req.body.viewUser}).toArray((err, data, fields) => { // get data of user requested
                    if (err) throw err   
                    res.render("admin.ejs", { title: "User List", userData: Alldata, tableData: data, viewMessage: "User's Details:"}) // render admin panel and given requested user's data from the db to the table
                    db.close() // close the connection
                })
            })
        }
    })
})   

router.post("/modify", (req, res) => {
    (MongoClient.connect(url, (err, db) => { // connect to the db
        if (err) throw err
        db.db(dbname).collection(coll).find({username: req.body.modifyUser}).toArray(async(err, result) => { // get requested user's data from db
            if (err) throw err
            if (result[0] != null) { // check if user to be modified exsists
                if(req.body.changePassword.length > 0 && req.body.role == "") { // if an admin changes the users password and not the user's role
                let encryptedPassword = await bcrypt.hash(req.body.changePassword, 10) // encrypt the new password
                db.db(dbname).collection(coll).updateOne({username: req.body.modifyUser}, {$set: {password: encryptedPassword}}, (err, res) => { // update the database
                    if (err) throw err })

                    db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                        if (err) throw err
                        res.render("admin.ejs", { title: "User List", userData: data, tableData: null, modifyMessage: "User's password successfully modified"}) // render admin panel with message that the change to the user's password were successful
                        db.close() // close the connection
                    })
                }

                if(req.body.role != "" && req.body.changePassword.length == 0){ // if an admin changes the user's role and not the user's password
                db.db(dbname).collection(coll).updateOne({username: req.body.modifyUser}, {$set: {role: req.body.role}}, (err, res) => { // update the database
                    if (err) throw err })

                    db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                        if (err) throw err
                        res.render("admin.ejs", { title: "User List", userData: data, tableData: null, modifyMessage: "User's role successfully modified"}) // render admin panel with message that the change to the user's role was successful
                        db.close() // close the connection
                    })   
                }

                if(req.body.role != "" && req.body.changePassword.length > 0){ // if an admin changes both the user's role and password
                let encryptedPassword = await bcrypt.hash(req.body.changePassword, 10) // encrypt the new password
                db.db(dbname).collection(coll).updateOne({username: req.body.modifyUser}, {$set: {password: encryptedPassword, role: req.body.role}}, (err, res) => { // update the database
                    if (err) throw err
                })

                    db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                        if (err) throw err
                        res.render("admin.ejs", { title: "User List", userData: data, tableData: null, modifyMessage: "User successfully modified"})  // render admin panel with the message that the alterations were succesful
                        db.close() // close the connection
                    }) 
                }

            } else { // if the user cannot be found on the db
                db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                    if (err) throw err
                    res.render("admin.ejs", { title: "User List", userData: data, tableData: null, modifyMessage: "That username does not belong to a user"}) // render the admin panel with the error message that the user couln't be found
                    db.close() // close the connection
                })
            }

        })
    }))
})

router.post("/removeuser", (req, res) => {
    (MongoClient.connect(url, (err, db) => { // connect to the db
        if (err) throw err
        db.db(dbname).collection(coll).find({username: req.body.removeUser}).toArray((err, result) => { // get requested user's data from db
            if (err) throw err
            if (result[0] != null) { // check if user to be deleted exsists (when an admin removes a user and refreshes the page it show the correct information)
                db.db(dbname).collection(coll).deleteOne({username: req.body.removeUser}, (err, result) => { // if the user exsists, delete them from the db
                if(err) throw err
                db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                if (err) throw err
                res.render("admin.ejs", { title: "User List", userData: data, tableData: null, removeMessage: "User successfully removed" }) // render the admin panel with the message that the user was successfully removed
                db.close() // close the connection
                })
                })
        
            } else { // if the user cannot be found on the db
                db.db(dbname).collection(coll).find({}).toArray((err, data, fields) => { // get all users, this is used to fill dropdown menu of all users
                    if (err) throw err
                    res.render("admin.ejs", { title: "User List", userData: data, tableData: null, removeMessage: "That user does not exist"}) // render the admin panel with the error message that the user doesn't exist
                    db.close() // close the connection
                })
            }
        })
    }))
})
    
module.exports = router; // export