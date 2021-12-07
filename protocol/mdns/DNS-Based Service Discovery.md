# DNS-Based Service Discovery

> From: https://tools.ietf.org/html/rfc6763

Service Instance Enumeration (Browsing) .............................6

Service Instance Resolution ........................................10

Service Names ......................................................19

Service Type Enumeration ...........................................27

Discovery of Browsing and Registration Domains (Domain Enumeration).28


`DNS-Based Service Discovery` document specifies how DNS resource records are named and structured to facilitate service discovery.  **Given a type of service that a client is looking for, and a domain in which the client is looking for that service, this mechanism allows clients to discover a list of named instances of that desired service, using standard DNS queries.**  This mechanism is referred to as DNS-based Service Discovery, or DNS-SD.

This document specifies that a particular service instance can be described using a DNS SRV [RFC2782] and DNS TXT [RFC1035] record. The SRV record has a name of the form "<Instance>.<Service>.<Domain>" and gives the target host and port where the service instance can be reached. The DNS TXT record of the same name gives additional information about this instance, in a structured form using key/value pairs, described in Section 6.  A client discovers the list of available instances of a given service type using a query for a DNS PTR [RFC1035] record with a name of the form "<Service>.<Domain>", which returns a set of zero or more names, which are the names of the aforementioned DNS SRV/TXT record pairs.

Of the many properties a good service discovery protocol needs to have, three of particular importance are:

    (i) The ability to query for services of a certain type in a certain logical domain, and receive in response a list of named instances (network browsing or "Service Instance Enumeration").

    (ii) Given a particular named instance, the ability to efficiently resolve that instance name to the required information a client needs to actually use the service, i.e., IP address and port number, at the very least (Service Instance Resolution).

    (iii) Instance names should be relatively persistent.  If a user selects their default printer from a list of available choices today, then tomorrow they should still be able to print on that printer -- even if the IP address and/or port number where the service resides have changed -- without the user (or their software) having to repeat the step (i) (the initial network browsing) a second time.

### Service Instance Enumeration (Browsing)

   Traditional DNS SRV records [RFC2782] are useful for locating instances of a particular type of service when all the instances are effectively indistinguishable and provide the same service to the client.

   For example, SRV records with the (hypothetical) name "_http._tcp.example.com." would allow a client to discover servers implementing the "_http._tcp" service (i.e., web servers) for the "example.com." domain.
   
   
### Structured Service Instance Names

This document borrows the logical service-naming syntax and semantics from DNS SRV records, but adds one level of indirection. Instead of requesting records of type "SRV" with name "_ipp._tcp.example.com.", the client requests records of type "PTR" (pointer from one name to another in the DNS namespace) [RFC1035].

In effect, if one thinks of the domain name "_ipp._tcp.example.com." as being analogous to an absolute path to a directory in a file system, then DNS-SD's PTR lookup is akin to performing a listing of that directory to find all the entries it contains.
   
The result of this PTR lookup for the name `"<Service>.<Domain>"` is a set of zero or more PTR records giving Service Instance Names of the form:

    Service Instance Name = <Instance> . <Service> . <Domain>

### 4.1.1. Instance Names

The `<Instance>` portion of the Service Instance Name is a user-friendly name consisting of arbitrary Net-Unicode text [RFC5198]. It MUST NOT contain ASCII control characters (byte values 0x00-0x1F and 0x7F) [RFC20] but otherwise is allowed to contain any characters, without restriction, including spaces, uppercase, lowercase, punctuation -- including dots -- accented characters, non-Roman text, and anything else that may be represented using Net-Unicode.

The `<Instance>` portion of the name of a service being offered on the network SHOULD be configurable by the user setting up the service, so that he or she may give it an informative name.  However, the device or service SHOULD NOT require the user to configure a name before it can be used.  A sensible choice of default name can in many cases allow the device or service to be accessed without any manual configuration at all.  The default name should be short and descriptive, and SHOULD NOT include the device's Media Access Control (MAC) address, serial number, or any similar incomprehensible hexadecimal string in an attempt to make the name globally unique.
