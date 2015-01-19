# Zorp

Zorp is a library for easing the creation and use of remote procedure calls over [ZeroMQ](http://zeromq.org/) sockets.

**Z**er**o**MQ **RP**C ;)

# Server Features

## Remote method decorator

Any function can be defined as a remote method that's callable using Zorp.

    from zorp import remote_method

    # This method will be identified by the name "hello_world"
    @remote_method
    def hello_world():
        return "Hello, world!"

    # This method will be identified by the name "say_goodbye"
    @remote_method("say_goodbye")
    def goodbye_world(name):
        return "Goodbye, {}"".format(name)

## Server

Starting a server is easy.

    from zorp import Server

    # Start a server
    Server()

By default, the server will:

* Listen on all interfaces
* Listen on TCP port 5560

These can be overridden with parameters:

    Server("127.0.0.1", port=8001)

While running, the server will:

* Wait for requests
* On receiving a request:
    * Identify the remote method to be executed
    * Parse any parameters
    * Return an error if the request is badly formed
    * Call the remote method with any parameters passed.
    * Return the response back to the requester
* Repeat forever :)

# Client Features

An easy way to call a remote method

    from zorp import Client

    # Configure the client
    client = Client("127.0.0.1")

    # Call a remote method
    response = client.call("hello_world")
    # response contains "Hello, world!"

    # Call another
    response = client.call("say_goodbye", "Arthur")
    # response contains "Goodbye, Arthur!"

By default, the client will:

* Connect to port 5560 of the server
* Retry requests after a 10 second timeout if no response is received.
* Give up after 3 timeouts have elapsed

These can be overridden with parameters:

    # Connect to 127.0.0.1:8001 with a 5 second timeout
    # And a maximum of 3 attempts
    client = Client("127.0.0.1", port=8001, timeout=5000, max_tries=3)

The `call` method of the client will:

* Create a connection to the specified server
* Create a valid message
* Pass it to the server
* Throw an exception if there are any failures
* Retry sending the message if the server does not respond within a timeout
* Throw an exception if the maximum number of tries has been reached
* Return the response :)
