---
layout: post
title: How to create self-signed certificates
date: 2020-03-07 04:50:45 +02:00
tags:
  - ssl
  - certificates
  - self-signed
  - certutil
  - Windows
  - openssl
  - bash
---

If you need a certificate for development purposes, you can generate one by
yourself. This post shows how to do it step by step.

The following assumes Windows and openssl (which should come with Git Bash). The
Wikipedia page on
[public key certificate](https://en.wikipedia.org/wiki/Public_key_certificate)
contains valuable information about what we'll be doing next so it's definitely
worth reading first. We'll be creating a **root certificate** and an
**end-entity certificate**, with the intention of using it for a website
(HTTPS).

## Root certificate (Certificate Authority)

First we need to generate the root certificate. We'll use it soon to sign our
end-entity certificate. This is the relevant `openssl req` command:

```sh
MSYS_NO_PATHCONV=1 openssl req -new -x509 -nodes -out rootCA.crt \
  -newkey rsa:2048 -keyout rootCA.key -days 100 \
  -subj "/C=NL/L=Amsterdam/emailAddress=nikolaos@acme-issuer.dev/CN=acme-issuer.dev/"
```

The `MSYS_NO_PATHCONV=1` is needed only for Git Bash. Without it, the `subj`
argument `/C=NL` is mistaken for a path and it gets prefixed with
`C:\Program Files\Git` (see also [Windows and Docker
paths]({% post_url /2019/2019-12-25-windows-docker-and-paths %})).

Here are the parameters of the `openssl req` command explained one by one:

- `-new`: New request
- `-x509`: Output a x509 structure instead of a certificate request. A
  certificate request is a step in between that we don't need, we just need the
  certificate here.
- `-nodes` : Don't encrypt the output key. If we don't specify this, we'll need
  to provide a passphrase for the key. Since this is just for development, we
  can skip it.
- `-out rootCA.crt`: The filename where the certificate will be stored
  (`rootCA.crt`)
- `-newkey rsa:2048` the type of the new key and the bits
- `-keyout rootCA.key`: The filename where the private key will be stored
  (`rootCA.key`)
- `-days 100`: How many days the certificate is valid for
- `-subj value`: the subject of the certificate

The subject is specified in this format:
`/key1=value1/key2=value2/.../keyN=valueN`. The keys that are used above are `C`
for country, `L` for city, `emailAddress` for, well, email address and finally
`CN` for canonical name. The canonical name is important, especially for the
end-entity certificate we'll be making soon. From
[Wikipedia](https://en.wikipedia.org/wiki/Public_key_certificate):

> A client connecting to that server will perform the certification path
> validation algorithm:
>
> 1. The subject of the certificate matches the hostname (i.e. domain name) to
>    which the client is trying to connect;
> 2. The certificate is signed by a trusted certificate authority.
>
> The primary hostname (domain name of the website) is listed as the Common Name
> in the Subject field of the certificate.

We can import this in Windows with:

```sh
certutil -addstore -user "Root" rootCA.crt
```

This will install it only for the current user (`-user`) in the trusted root
certification authorities section. This is our way of telling Windows to trust
any certificate signed by our root certificate.

To delete it, we can run:

```sh
certutil -delstore -user "Root" acme-issuer.dev
```

Notice that we imported the certificate by its filename but we delete it by its
canonical name.

## End-entity certificate

First, we create the certificate request:

```sh
MSYS_NO_PATHCONV=1 openssl req -new -nodes -out acme.csr \
  -newkey rsa:2048 -keyout acme.key \
  -subj "/C=NL/L=Amsterdam/emailAddress=nikolaos@acme.dev/CN=acme.dev/"
```

This command is the same as the one we run for the certificate authority, except
that it misses the `-x509` argument. This will generate a certificate request
instead of a certificate. In the next command, we will use the certificate
request to generate a certificate signed by our certificate authority:

```sh
openssl x509 -req -in acme.csr \
  -CA rootCA.crt -CAkey rootCA.key -CAcreateserial \
  -out acme.crt -days 100 -extfile v3.ext
```

The arguments of the `openssl x509` command:

- `-req`: Input is a certificate request, sign and output
- `-in acme.csr`: The input file
- `-CA rootCA.crt`: The certificate of the authority
- `-CAkey rootCA.key`: The key of the authority
- `-CAcreateserial`: Create a serial file for the authority if it is missing
- `-out acme.crt`: The certificate output file
- `-days`: How many days the certificate is valid for
- `-extfile file`: File with X509V3 extensions to add (more on this later)

We can import this in Windows with:

```sh
certutil -addstore -user "My" acme.crt
```

This will install it again only for the current user, but under the "personal"
section.

We can delete it later with:

```sh
certutil -delstore -user "My" acme.dev
```

## Extfile (X509V3 extensions)

In theory, we have a certificate that is signed by an authority that we told
Windows to trust, so we should be good. If we try however to use this
certificate in a web server, Chrome will complain that the certificate is not
good enough:

> This server could not prove that it is acme.dev; its security certificate does
> not specify Subject Alternative Names. This may be caused by a
> misconfiguration or an attacker intercepting your connection.

This is where the `-extfile` parameter comes in. We need to provide an extra
configuration file that specifies the Subject Alternative Names that Chrome
complains about:

```ini
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = acme.dev
```

This
[reference documentation](https://access.redhat.com/documentation/en-US/Red_Hat_Certificate_System/8.0/html/Admin_Guide/Standard_X.509_v3_Certificate_Extensions.html)
might be interesting.

With this in place, the certificate is good enough for Chrome and Edge. Firefox
still complains, probably because we're lacking an intermediate certificate, but
that's an exercise for another time.

## One script to rule them all

This script combines all the steps together. Save it somewhere as
`self-sign-cert.sh` and you can run it as:

- `self-sign-cert.sh www.hello.dev` : it will create and install the root and
  end certificate for `www.hello.dev`
- `self-sign-cert.sh www.hello.dev delete` : it will uninstall the root and end
  certificate it installed before

```sh
#!/bin/bash
set -e
DOMAIN=$1
if [[ -z "$DOMAIN" ]]; then
  echo "Please give the domain as the first parameter"
  exit 1
fi

if [[ "$2" == "delete" ]]; then
  certutil -delstore -user "My" $DOMAIN
  certutil -delstore -user "Root" issuer-$DOMAIN
  exit 0
fi

export MSYS_NO_PATHCONV=1
ROOT_CRT="$DOMAIN-root.crt"
ROOT_KEY="$DOMAIN-root.key"
openssl req -x509 -new -nodes -out $ROOT_CRT \
  -newkey rsa:2048 -keyout $ROOT_KEY \
  -days 100 \
  -subj "/C=NL/L=Amsterdam/emailAddress=nikolaos@issuer-$DOMAIN/CN=issuer-$DOMAIN/"
certutil -addstore -user "Root" $ROOT_CRT
ACME_CSR="$DOMAIN.csr"
ACME_KEY="$DOMAIN.key"
ACME_CRT="$DOMAIN.crt"
ACME_V3_EXT="$DOMAIN.v3.ext"
tee $ACME_V3_EXT <<-HERE >/dev/null
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names

[alt_names]
DNS.1 = $DOMAIN
HERE

openssl req -new -nodes -out $ACME_CSR \
  -newkey rsa:2048 -keyout $ACME_KEY \
  -subj "/C=NL/L=Amsterdam/emailAddress=nikolaos@$DOMAIN/CN=$DOMAIN/"
openssl x509 -req -in $ACME_CSR \
  -CA $ROOT_CRT -CAkey $ROOT_KEY -CAcreateserial \
  -out $ACME_CRT -days 100 -extfile $ACME_V3_EXT
certutil -addstore -user "My" $ACME_CRT
```

As always, it works on my machine.
