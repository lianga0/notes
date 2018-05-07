### DNS Domain name syntax

The definitive descriptions of the rules for forming domain names appear in RFC 1035, RFC 1123, and RFC 2181. A domain name consists of one or more parts, technically called labels, that are conventionally concatenated, and delimited by dots, such as example.com.

The right-most label conveys the top-level domain; for example, the domain name www.example.com belongs to the top-level domain com.

The hierarchy of domains descends from right to left; each label to the left specifies a subdivision, or subdomain of the domain to the right. For example, the label example specifies a subdomain of the com domain, and www is a subdomain of example.com. This tree of subdivisions may have up to 127 levels.

A label may contain zero to 63 characters. The null label, of length zero, is reserved for the root zone. The full domain name may not exceed the length of 253 characters in its textual representation. In the internal binary representation of the DNS the maximum length requires 255 octets of storage, as it also stores the length of the name.

Although no technical limitation exists to use any character in domain name labels which are representable by an octet, hostnames use a preferred format and character set. The characters allowed in labels are a subset of the ASCII character set, consisting of characters a through z, A through Z, digits 0 through 9, and hyphen. This rule is known as the **LDH** rule (letters, digits, hyphen). Domain names are interpreted in case-independent manner. Labels may not start or end with a hyphen. An additional rule requires that top-level domain names should not be all-numeric.

##### Internationalized domain names

The limited set of ASCII characters permitted in the DNS prevented the representation of names and words of many languages in their native alphabets or scripts. To make this possible, ICANN(Internet Corporation for Assigned Names and Numbers) approved the Internationalizing Domain Names in Applications (IDNA) system, by which user applications, such as web browsers, map Unicode strings into the valid DNS character set using [Punycode](https://en.wikipedia.org/wiki/Punycode). In 2009 ICANN approved the installation of internationalized domain name country code top-level domains (ccTLDs). In addition, many registries of the existing top-level domain names (TLDs) have adopted the IDNA system.

##### Punycode

Punycode is a representation of Unicode with the limited ASCII character subset used for Internet host names. Using Punycode, host names containing Unicode characters are transcoded to a subset of ASCII consisting of letters, digits, and hyphen, which is called the Letter-Digit-Hyphen (LDH) subset. For example, München (German name for Munich) is encoded as Mnchen-3ya.

While the Domain Name System (DNS) technically supports arbitrary sequences of octets in domain name labels, the DNS standards recommend the use of the LDH subset of ASCII conventionally used for host names, and require that string comparisons between DNS domain names should be case-insensitive. The Punycode syntax is a method of encoding strings containing Unicode characters, such as internationalized domain names (IDNA), into the LDH subset of ASCII favored by DNS. It is specified in IETF Request for Comments 3492.

From: [Domain Name System](https://en.wikipedia.org/wiki/Domain_Name_System)

