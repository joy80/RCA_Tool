package com.example.processor

class TypeCast {

    // Parsing a non-numeric string triggers NumberFormatException
    def parse(value) {
        def i = Integer.parseInt(value)  // For "abc" this will throw
        println "Parsed: ${i}"
    }

    static void main(String[] args) {
        def t = new TypeCast()
        try {
            // Intentionally pass a non-numeric string
            t.parse("abc")
        } catch (Exception e) {
            e.printStackTrace()
        }
    }
}
