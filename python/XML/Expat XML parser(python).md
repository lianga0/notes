## Expat XML parser

> 2018.10.31

### What is Expat?

Welcome to Expat, a stream-oriented XML parser library written in C.

Expat is a stream-oriented parser in which an application registers handlers for things the parser might find in the XML document (like start tags).

Expat excels with files too large to fit RAM, and where performance and flexibility are crucial.

In computing, Expat is a stream-oriented XML 1.0 parser library, written in C. As one of the first available open-source XML parsers, Expat has found a place in many open-source projects. Such projects include the Apache HTTP Server, Mozilla, Perl, Python and PHP. It is also bound in many other languages.

There are a number of [applications and libraries using Expat](https://libexpat.github.io/doc/users/), as well as [bindings and 3rd-party wrappers](https://libexpat.github.io/doc/bindings/). Expat is [packaged everywhere](https://libexpat.github.io/doc/packages/).

An [introductory article](https://www.xml.com/pub/1999/09/expat/index.html) on using Expat is available on [xml.com](https://www.xml.com/pub/1999/09/expat/index.html).

### Overview of Expat

Expat is a stream-oriented parser. You register callback (or handler) functions with the parser and then start feeding it the document. As the parser recognizes parts of the document, it will call the appropriate handler for that part (if you've registered one). The document is fed to the parser in pieces, so you can start parsing before you have the whole document. This also allows you to parse really huge documents that won't fit into memory.

To use the Expat library, programs first register handler functions with Expat. When Expat parses an XML document, it calls the registered handlers as it finds relevant tokens in the input stream. These tokens and their associated handler calls are called *events*. Typically, programs register handler functions for XML element start or stop events and character events. Expat provides facilities for more sophisticated event handling such as XML Namespace declarations, processing instructions and DTD events.

**Expat's parsing events resemble the events defined in the [Simple API for XML (SAX)](https://en.wikipedia.org/wiki/Simple_API_for_XML), but Expat is not a SAX-compliant parser. Projects incorporating the Expat library often build SAX and possibly DOM parsers on top of Expat. While Expat is mainly a stream-based (push) parser, it supports stopping and restarting parsing at arbitrary times, thus making the implementation of a pull parser relatively easy as well.**

### Python XML Processing Modules

Python’s interfaces for processing XML are grouped in the `xml` package.

It is important to note that modules in the xml package require that there be at least one **SAX-compliant XML parser** available. The Expat parser is included with Python, so the `xml.parsers.expat` module will always be available.

The `xml.parsers.expat` module is a Python interface to the **Expat non-validating XML parser**. The module provides a single extension type, `xmlparser`, that represents the current state of an XML parser. After an `xmlparser` object has been created, various attributes of the object can be set to handler functions. When an XML document is then fed to the parser, the handler functions are called for the character data and markup in the XML document.

### xml.etree.ElementTree

The `ElementTree` wrapper adds code to load XML files as trees of `Element` objects, and save them back again. You can use the parse function to quickly load an entire XML document into an ElementTree instance.

The `Element` type is a flexible container object, designed to store hierarchical data structures in memory. The type can be described as a cross between a list and a dictionary.

Each element has a number of properties associated with it:

- a tag. This is a string identifying what kind of data this element represents (the element type, in other words).
- a number of attributes, stored in a Python dictionary.
- a text string to hold text content, and a tail string to hold trailing text
- a number of child elements, stored in a Python sequence

All elements must have a tag, but all other properties are optional. All strings can either be Unicode strings, or 8-bit strings containing US-ASCII only.

**`ElementTree` is only the warpper to load and save XML files. It has a `parse(source, parser=None)` function(or similar function `XML(text, parser=None)`) to use the `parser` to parse XML document and return an `Element` instance. `parser` is an optional parser instance. If not given, the standard `XMLParser` parser is used. class `xml.etree.ElementTree.XMLParser(html=0, target=None, encoding=None)` is `Element` structure builder for XML source data, based on the expat parser.**

### The cElementTree Module

cElementTree is included with Python 2.5 and later, as `xml.etree.cElementTree`.

The cElementTree module is a C implementation of the [ElementTree API](http://effbot.org/zone/element-index.htm), optimized for fast parsing and low memory use. On typical documents, cElementTree is 15-20 times faster than the Python version of ElementTree, and uses 2-5 times less memory. On modern hardware, that means that documents in the 50-100 megabyte range can be manipulated in memory, and that documents in the 0-1 megabyte range load in zero time (0.0 seconds). This allows you to drastically simplify many kinds of XML applications.

Reference:

[Welcome to Expat!](https://libexpat.github.io/)

[Expat (library)](https://en.wikipedia.org/wiki/Expat_(library))

[The cElementTree Module](http://effbot.org/zone/celementtree.htm)

[XML Processing Modules](https://docs.python.org/3/library/xml.html)

[xml.etree.ElementTree — The ElementTree XML API](https://docs.python.org/2.7/library/xml.etree.elementtree.html)

[Elements and Element Trees](http://effbot.org/zone/element.htm)

