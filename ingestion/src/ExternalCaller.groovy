package com.example.processor

class ExternalCaller {

    /**
     * Perform a simple HTTP GET and return the response body.
     * Throws RuntimeException on non-2xx responses or other failures.
     */
    String callApi(String urlStr, int timeoutMs = 5000) {
        URL url = new URL(urlStr)
        HttpURLConnection conn = (HttpURLConnection) url.openConnection()
        conn.setRequestMethod('GET')
        conn.setConnectTimeout(timeoutMs)
        conn.setReadTimeout(timeoutMs)
        conn.setRequestProperty('Accept', 'application/json')

        try {
            int code = conn.getResponseCode()
            InputStream is = (code >= 200 && code < 300) ? conn.getInputStream() : conn.getErrorStream()
            String body = is ? is.getText('UTF-8') : ''

            if (code < 200 || code >= 300) {
                throw new RuntimeException("HTTP ${code}: ${body ?: '<empty response>'}")
            }

            return body
        } finally {
            conn.disconnect()
        }
    }

    static void main(String[] args) {
        def endpoint = args.length ? args[0] : 'https://httpbin.org/get'
        def caller = new ExternalCaller()

        try {
            println "Calling ${endpoint} ..."
            def resp = caller.callApi(endpoint)
            println "Response (truncated 500 chars):\n${resp.length() > 500 ? resp.substring(0,500) + '...' : resp}"
        } catch (Exception e) {
            System.err.println("Failed to call external API: ${e.message}")
            e.printStackTrace()
            // Optionally: write an error log to ingestion/log
            try {
                def logDir = new File('ingestion/log')
                if (!logDir.exists()) logDir.mkdirs()
                def logFile = new File(logDir, 'external_api_error.txt')
                def entry = [
                    timestamp: new Date().format("yyyy-MM-dd'T'HH:mm:ss.SSSXXX"),
                    level: 'ERROR',
                    messege: "Failed calling external API: ${endpoint}",
                    service: 'external-caller',
                    stacktrace: e.toString() + '\n' + (e.stackTrace.collect { it.toString() }.join('\n'))
                ]
                logFile << (new groovy.json.JsonBuilder(entry).toString() + System.lineSeparator())
            } catch (Exception ignored) {
                // ignore logging failures
            }
            System.exit(1)
        }
    }
}
