# OkHttpClient print SSL certficate information

How do I inspect the information of the SSL Certificate that the device is seeing when hitting my endpoint?

A simple `Interceptor` was implemented to inspect the certificates, given a valid handshake:


```
public class ServiceGenerator {
    private static class SslCertificateLogger implements Interceptor {
        @Override
        public Response intercept(Chain chain) throws IOException {
            Request request = chain.request();
            Response response;
            try {
                response = chain.proceed(request);
            } catch (Exception e) {
                XLog.d("<-- HTTP FAILED: " + e);
                //XLog.e((((java.security.cert.CertificateException)((javax.net.ssl.SSLHandshakeException)e).getCause())).getCause());
                XLog.e(((java.security.cert.CertPathValidatorException) e.getCause().getCause()).getCertPath());
                XLog.e(((java.security.cert.CertPathValidatorException) e.getCause().getCause()).getIndex());
                XLog.e(((java.security.cert.CertPathValidatorException) e.getCause().getCause()).getReason());
                XLog.e(request.url());
                throw e;
            }

            Handshake handshake = response.handshake();
            if (handshake == null) {
                XLog.d("no handshake");
                return response;
            }


            XLog.d("handshake success");
            List<Certificate> certificates = handshake.peerCertificates();
            if (certificates == null) {
                XLog.d("no peer certificates");
                return response;
            }

            String s;
            for (Certificate certificate : certificates) {
                s = certificate.toString();
                XLog.d(s);
            }

            return response;
        }
    }

    private static final OkHttpClient client = new OkHttpClient.Builder()
            .addInterceptor(new SslCertificateLogger())
            .build();
}
```

Reference:
[Log the SSL Certificate programmatically](https://stackoverflow.com/questions/52254272/log-the-ssl-certificate-programmatically)