package com.example.processor

class BadProperty {

    // Accessing nested property that may be null — triggers GroovyRuntimeException
    def doSomething(Map data) {
        // If data is null or data.user is null, the next line will raise:
        // groovy.lang.GroovyRuntimeException: Cannot get property 'name' on null object
        def name = data.user.name
        println "User name: ${name}"
    }

    static void main(String[] args) {
        def b = new BadProperty()
        try {
            // Intentionally pass null to reproduce the error
            b.doSomething(null)
        } catch (Exception e) {
            e.printStackTrace()
        }
    }
}
