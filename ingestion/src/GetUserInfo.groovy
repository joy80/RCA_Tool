package com.example.processor

class GetUserInfo {

    // helper that will throw GroovyRuntimeException when 'items' is null
    def getSize(items) {
        // If 'items' is null, accessing 'size' triggers:
        // groovy.lang.GroovyRuntimeException: Cannot get property 'size' on null object
        return items.size
    }

    // method that will throw IndexOutOfBoundsException when list is too small
    def process(items) {
        // getSize() call (this could produce the GroovyRuntimeException if items == null)
        def size = getSize(items)
        println "size = ${size}"

        // access index 10 (this will throw java.lang.IndexOutOfBoundsException when size <= 10)
        def value = items[10]
        println "value = ${value}"
    }

    static void main(String[] args) {
        def p = new Processor()

        // Case 1: small list -> triggers IndexOutOfBoundsException
        try {
            def smallList = [0,1,2,3,4]
            p.process(smallList)
        } catch (Exception e) {
            e.printStackTrace()
        }

        // Case 2: null list -> triggers GroovyRuntimeException (cannot access .size on null)
        try {
            p.process(null)
        } catch (Exception e) {
            e.printStackTrace()
        }
    }
}
