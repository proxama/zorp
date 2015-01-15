# TODO

* `remote_method` decorator
    * if no name is passed in to the decorator, use the function's name
    * register the function and name with the registry

* remote method registry
    * maintain a list of functions, indexed by name
    * prepare json schema from registered function signature
    * return (schema, function) tuples from a provided method name

* server
    * open a zeromq socket using the specified bind address and port
    * wait for a request
    * verify the payload
    * identify the method
    * retrieve it from the registry
    * verify the parameters against the method schema
    * call the method
    * reply with the response

* client
    * open a zermq socket using the specified host and port
    * construct a request payload using the method name and any parameters supplied
    * send the request
    * wait for a response
    * if there has been no response within the timeout period, retry
    * fail when the maximum number of tries have timed out
    * parse and return the response
