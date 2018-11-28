---
layout: post
title: Terraform secrets
date: 2018-10-06
published: true
categories:
- Code
tags:
- terraform
- helm
- bash
---
Since the beginning of this year, I've been using [Terraform] to manage
infrastructure. I use it with both AWS and Azure and so far I haven't
encountered any problems. The documentation is quite good and you get that happy
feeling when things just work as expected.

The infrastructure I need to manage is things like the runtime where my services
run (AWS Elastic Beanstalk and AKS), Docker container registries, DNS records,
message brokers, databases, etc. All these are managed services offered by AWS
and Azure.

In the beginning I was running Terraform manually on my laptop but soon enough I
moved it at the deployment pipeline so that everyone can use it. Anyone who can
create a pull request can also add a new database server, just by modifying the
Terraform code (provided the PR is approved of course).

I've setup the following structure:

- resources that belong to multiple microservices have their own git repository.
  I named the repository *velara*, out of the Star Trek TNG episode [Home Soil].

  A typical example of what goes in this repo is a message broker
  (e.g. Azure Event Hub Namespace) because multiple services talk with the
  broker.

- resources that belong to a single microservice go to the microservice's own
  git repository, under a folder named, well, *terraform*.

  An example of such a resource is a database.

Further down, infrastructure needs to be classified as _environment specific_ or
_global_. By environment I mean of course the classic DTAP. This is done by
plain old folders and Terraform *modules* to reduce code repetition. With
Terraform, it's quite easy to define a template that describes one environment
and reuse it as a module, simply changing a few variables as needed.

One cool thing I did recently is to pass sensitive information from Terraform
into my application without storing them anywhere.

My microservice is on Azure (Azure Kubernetes Service). A rough description of
what happens on each build:

- after the CI pipeline succeeds, a Docker image is published to Azure
- during the deployment pipeline (per environment):
  - first, we *apply* Terraform changes. This will automatically create, update
    or delete the infrastructure of the environment.
  - next, we deploy the application using [Helm].

Due to a new requirement, the microservice needs to store some data. Using
Terraform, we add a new CosmosDB account (using its MongoDB interface, in order
to stay platform agnostic).

If you login to the Azure portal, you will see that the database is protected.
You need a connection string to access it and it includes base64-encoded
authentication information. It's worth noting that Azure generates this
connection string for me, so I can't predict it in advance.

The simplest way to go, I guess, is to copy paste this connection string into
the application properties, or in the Helm chart as an environment variable,
commit it to git, and call it a day.

There are a few problems with this:

1. committing sensitive information in git is a security risk. That's a big
   topic on its own, too big to discuss here.
2. if for whatever reason you need to re-create the database, the connection
   string will change. The chances are you will forget to update it in the code
   until you (or your users) have noticed something is broken.

Terraform to the rescue! Terraform offers *outputs*. Outputs are values from
your infrastructure that you'd like Terraform to be able to print.

Here's our CosmosDB use case:

```
resource "azurerm_cosmosdb_account" "db" {
  name                = "monty-correos-events"
  resource_group_name = "acme"
  location            = "West Europe"
  offer_type          = "Standard"
  kind                = "MongoDB"

  consistency_policy {
    consistency_level = "Session"
  }

  geo_location {
    location          = "West Europe"
    failover_priority = 0
  }
}

output "db_connection_string" {
  value = "${azurerm_cosmosdb_account.db.connection_strings.0}"
}
```

The `resource` block will create the CosmosDB account and the `output` block
will expose the connections string as `db_connection_string`. We can then
retrieve it with this command:

```bash
$ terraform output db_connection_string
mongodb://acme:very-long-string-base64@acme.documents.azure.com:10255/?ssl=true
```

How do we pass the value to the application? Now this is where Helm comes to the
rescue. And of course a little bit of bash kung fu magic.

When deploying a Helm chart, it is possible to supplement the chart with one or
more [values file]. I am already using this feature to provide a different
values file per environment. I need to convert the output from terraform into a
values file.

Somewhere in my Helm's `deployment.yaml` I need this environment variable
definition:

{% raw %}
```yaml
spec:
  containers:
  - name: {{ .Chart.Name }}
    image: "{{ .Values.image.repository }}:{{ .Values.image.tag }}"
    imagePullPolicy: {{ .Values.image.pullPolicy }}
    env:
    - name: SPRING_DATA_MONGODB_URI
      value: "{{ .Values.db_connection_string }}"
```
{% endraw %}

This says that my application's connection string will be in the standard
Spring environment variable `SPRING_DATA_MONGODB_URI` and the value of that
environment variable will come from a custom value file under the key
`db_connection_string`.

Now I need to create such a values file which should look like this:

```yaml
db_connection_string: mongodb://acme:very-long-string-base64@acme.documents.azure.com:10255/?ssl=true
```

There's one small caveat specific to this problem. The connection string I get
from Azure does not specify a database name. I'd like to specify a database
and I'd like each envirnoment to use a different one. For example, my test
environment should use the database `my-app-test` and my production environment
should use `my-app-production`. So the yaml file should actually look like this:

```yaml
db_connection_string: mongodb://acme:very-long-string-base64@acme.documents.azure.com:10255/my-app-my-environment?ssl=true
```

This is where the bash kung fu comes in. Why bash? It's difficult. It's cryptic.
I can't understand my own code the next day, unless I comment it sufficiently.
It is also however the least common denominator of programming languages that
I can program with inside a Docker container.

```bash
#!/bin/bash

output=$(terraform output db_connection_string)
# At this point $output will contain a value like this:
# mongodb://acme:very-long-string-base64@acme.documents.azure.com:10255/?ssl=true

# We need to inject the database name before ?ssl=true
db_name=my-app-${ENVIRONMENT}

# strip the ?ssl=true suffix
db_connection_string=$(echo ${output} | sed -r -e 's/^(.+)\?.+/\1/')

# inject the db name and put the ?ssl=true suffix back where it was
db_connection_string="${db_connection_string}${db_name}?ssl=true"

# Create YAML file for the connection string
echo "db_connection_string: \"${db_connection_string}\"" >> values-from-terraform.yaml
```

If I run the previous script after applying Terraform changes and before
deploying with Helm, I can provide my application with the correct connection
string, without even me knowing what that connection string is! That's
pretty awesome.

The safest secret is the secret nobody knows :-)

[Terraform]: https://www.terraform.io/
[Home Soil]: https://en.wikipedia.org/wiki/Home_Soil
[Helm]: https://helm.sh/
[values file]: https://docs.helm.sh/chart_template_guide/#values-files
