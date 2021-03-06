---
layout: post
title: Terraform secrets part 2 - Randomize it
date: 2018-11-04
published: true
tags:
  - terraform
  - helm
  - kubernetes
---

In a [previous post], I used Terraform and Helm to pass the connection string of an Azure
CosmosDB database to the service that needs it without storing it anywhere in
between. In this post, I'll do something similar for a PostgreSQL database and
beef up the security a bit.

In the case of CosmosDB, Azure generates the connection string for us. Terraform
exposes it as an output. With a bash script, we pass the output to Helm as a
supplementary set of values. This ends up as an environment variable to the
application at runtime.

<figure><img src="{% link /assets/2018/11/deployment-cosmosdb.png %}" /><figcaption>Getting secret connection string from Azure</figcaption></figure>

For PostgreSQL (still in Azure), we need to tell Azure what username and
password we prefer. We want to create the database via Terraform automatically
during deployment, so those values have to come from somewhere.

One solution could be to define them as environment variables in the CI server.
It can get a bit complicated with supporting different credentials per
environment but it's doable, although a bit messy.

What I tried instead is to let Terraform generate a **random password** for me.
Like I said in the last post, the best secret is the one nobody knows. Here's
how it's done:

```
resource "random_string" "db-password" {
  length      = 16
  min_upper   = 1
  min_lower   = 1
  min_numeric = 1
  min_special = 1
}
```

This defines a random string resource named `db-password`. It specifies the
length of the password (16) and also that it needs to consist of at least one
uppercase letter, one lowercase letter, one number and one special character.

We can use it in the definition of the database server:

```
resource "azurerm_postgresql_server" "acme-db-server" {
  [...]
  administrator_login_password = "${random_string.db-password.result}"
  [...]
}
```

Terraform will generate the password once and then store it in its state file.
So it won't create a different password on each deployment.

To pass the password to the outside world, we need to define an output (just
like in the last post):

```
output "db_password" {
  value     = "${azurerm_postgresql_server.acme-db-server.administrator_login_password}"
  sensitive = true
}
```

The `sensitive` attribute (which I forgot last time) tells Terraform to mask the
password when it's printing it to the summary of available outputs. This
enhances our security game because now the password will also be **hidden from
the build logs**.

One small side note on Terraform: read the documentation carefully. Some
attributes cannot be changed without destroying and re-creating the resource.
Luckily the password is not such a case, but the username is. Be extra careful
and always run Terraform first (automatically) to all environments before
running it on production.

Back to the random password. We now have a random password and we can pass it
all the way to the application running in the Kubernetes cluster via extra
values in the Helm deployment. We can also strengthen the security a bit on the
Kubernetes side as well by using a **Kubernetes secret**.

In Helm, we create a new template `secret.yaml`:

{% raw %}

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: for-your-eyes-only
type: Opaque
data:
  dbPassword: "{{ .Values.dbPassword | b64enc }}"
```

{% endraw %}

and we change the environment variable definition in `deployment.yaml` to get
the value from the secret:

{% raw %}

```yaml
- name: SPRING_DATASOURCE_PASSWORD
  valueFrom:
    secretKeyRef:
      name: for-your-eyes-only
      key: dbPassword
```

{% endraw %}

This has no impact to the application (it still reads the same value). It just
protects the password from unauthorized eyes. In order to read the value of the
secret you need to be authorized by your Kubernetes administrator.

<figure><img src="{% link /assets/2018/11/deployment-postgresql.png %}" /><figcaption>Random password and Kubernetes secret</figcaption></figure>

With all these changes we have achieved:

- no passwords in the source code
- no passwords in the build logs
- password generated by Terraform and stored in Terraform state (with
  controllable access)
- password stored in Kubernetes as a secret (with controllable access)

As long as humans are involved in the process, a password can still leak (if you
will pardon my bias). If that happens, using the Terraform `taint` command we
can force a new random password to be created on the next deployment.

For me this is already a great improvement on security, but I still like to keep
improving. An idea might be to automatically taint the password every N days (or
every N deployments). I'm also curious to play with a system like
[Vault](https://www.vaultproject.io/) (which comes from the same company as
Terraform, HashiCorp).

[previous post]: {% post_url 2018/2018-10-06-terraform-secrets %}
