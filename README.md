# INF226 Mandatory Assigment 2B

> Fabio Gaiba

# Documentation

## Design choices

This application is implemented through flask and sqlite, directly following from the [excercise](https://git.app.uib.no/inf226/22h/login-server)

The two main design choices during the developing of this minimal web application were:

1. Implement just the needed features.
   
   - Generally speaking, the more **complex** is the app the greater is the **attack surface**.
   - Compared to the exercise, I got rid of the announcments and some more minor details

2. Leave as much responsibility as possibles to the libraries.
   
   - As good as a developer can be, relieng on libraries it's not bad at all. The are more secure, more tested, updated more often and probably also faster. 
   - The managing of the session, as well as authentication and authorization is done hand in hand with *flask*

3. Every user input must be checked 

    - A great effort is made to make sure that every user input is treated carefully. 

4. Split code across multiple file (with relative meaning)

    - The code provided in the **exercise** were poorly structered. A good part of this project was just refactoring the code provided. What I tried to do is to split the code across multiple files and wrapping some useful function for reutilization. 
    - The result is not great. Given more time I would have spent more energy into improving the quality of the code, as many security flwas usually come from messy logic. It was pretty difficult working with many unseen (for me) technologies.


## Features

The application is a minimal groupchat. It is possible to:

- **create an account**
    - Username must contain letters
    - the passwords are safely hashed and stored in a database. 
    - Assuming `HTTPS`, nobody (even who runs the server) won't be able to see the password.
- send private messages to another user
- send messages to all users
- reply to a certain message
- retrieve a particular message (given that the user is one of the retriever or the sender)
- retrieve all messages sent to the user



