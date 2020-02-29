---
layout: post
title: Flyway migrations and Continuous Deployment
date: 2018-08-25 10:41:38.000000000 +02:00
published: true
tags:
- Flyway
- continuous deployment
- database migrations
---

Flyway is a tool that allows you to version your database schema changes. In this post I explain a bit how we use it at work (so far), in the context of automated deployments and GitHub Flow branching model.

<!--more-->

First, a gentle introduction to our way of working. We follow the <a href="https://guides.github.com/introduction/flow/">GitHub Flow</a> branching model, with one exception: only the master branch gets deployed automatically to production.

<strong>Branches:</strong> A developer branches out of master and works on his/her ticket there. Although branches are the opposite of integration, we have to use them in order to have pull requests and code reviews <em>before</em> merging to master.

<strong>Build pipeline:</strong> Every commit (of every branch) goes automatically through the build pipeline. That includes the usual stuff, linting (checkstyle), unit tests, code coverage, integration tests. Integration tests are run against an <em>ephemeral</em> database. Instead of an in-memory database like H2, we use PostgreSQL on Docker, spawned effortlessly with Bitbucket Pipelines. This brings us closer to a production-like database and gives us less potential worries about different SQL dialects.

<strong>Deployment for feature branches</strong>: If the build passes, the application is automatically deployed to the test environment. The test environment's database is also PostgreSQL, but, unlike the integration tests, it is always on. It is thus more similar to the production database.

<strong>Deployment for master branch</strong>: When the build is green and the pull request is reviewed and approved, it is merged to master. That triggers the same build pipeline, but with the extra step of automatically deploying to production. That's the only difference with GitHub flow.

<figure><img src="{{ site.baseurl }}/assets/2018/branching-model.jpg" /><figcaption>Our branching model</figcaption></figure>

The application(s) are using Spring Boot 2 (Java 8). Flyway migrations are automatically run when the application starts.

Now, let's discuss about Flyway. Here's what a simple database migration with Flyway might look like:

```
CREATE TABLE user (
  id int not null,
  name varchar(100) not null
);
```

This would be stored in the folder <code>src/main/resources/db/migration</code>, which is the default location Flyway looks for migrations. The filename is important. It needs to follow a <a href="https://flywaydb.org/documentation/migrations#naming">specific convention</a>:

<code>V{version}__{description}.sql</code>
<ul>
<li>it starts with a capital V</li>
<li>next comes the version. This determines the <strong>order</strong> by which migrations will be picked up.</li>
<li>then two underscores</li>
<li>and finally a description</li>
</ul>

Our example above might be called <code>V1__create-user-table.sql</code>

Flyway keeps track of which migrations have been applied, so that it doesn't have to apply them again next time. The history information is stored in a table automatically created by Flyway.

In that table, Flyway also keeps a checksum of the applied migration. If the SQL file's content changes, the checksum changes and Flyway will stop with an error. This will prevent the application from starting.

<img src="{{ site.baseurl }}/assets/2018/if-flyway-cant-apply-your-migrations-youre-gonna-have-a-bad-time.jpg" />

This takes us to the first problem with our branching model. We always deploy green builds to the test environment. So if I start working on my branch and create the above migration <code>V1__create-user-table.sql</code>, it will be applied automatically on my first green build. If I have made a mistake in my branch, I can't edit the file anymore, because Flyway will complain about the modified checksum.

So what can I do, if I realize that the user table actually needs an extra field? Notice that the migration is already applied on the test database and I don't want to manually delete the table.

Solution: I can always add another migration in my branch.

I need to create <code>V2__forgot-is-enabled-field.sql</code> :

```
ALTER TABLE user (
  ADD COLUMN is_enabled BIT NOT NULL
);
```

Note: please note that I'm writing the SQL off the top of my head and it most likely will contain errors... treat it as pseudo-SQL :-)

This works, but the downside is that you repository will look messy in the end. After all, all these will need to be merged into master. It doesn't look pretty (arguably) to have all these fix-ups in your mainline branch.

Now, if we could go back in time before we wrote the V1 migration... maybe we would do things differently?

Flyway offers a feature called <strong>repeatable migrations</strong> (also known as idempotent migrations). In this case, Flyway calculates the checksum, but instead of complaining when it changes, it will re-apply the changed migration. These migrations however need to be written in such a way that they <em>can</em> be run multiple times. That's your responsibility.

The naming convention is different:

<code>R__{description}.sql</code>:
<ul>
<li>this time it starts with a capital R</li>
<li>again followed by two underscores</li>
<li>it does not have a version component, because they are allowed to change</li>
<li>again followed by a description</li>
</ul>

Notice that the description controls the <strong>order</strong> that they will be applied. Also, repeatable migrations will be applied <strong>after</strong> the normal migrations.

With that in mind, here's how our first commit could have been, with a file <code>R__create-users-table.sql</code>:

```
CREATE TABLE IF NOT EXISTS user (
  id int not null,
  name varchar(100) not null
);
```

and the fix-up commit would have touched the same file:

```
CREATE TABLE IF NOT EXISTS user (
  id int not null,
  name varchar(100) not null,
  is_enabled bit not null
);

ALTER TABLE user (
  ADD COLUMN IF NOT EXISTS is_enabled bit not null
);
```

I added the <code>is_enabled</code> both in the <code>CREATE TABLE</code> and in the <code>ALTER TABLE</code>. I did this on purpose, because on the back of my head I am thinking that in the future, after I merge this to master and goes to production, I will be able to create a cleanup PR, to simplify this repeatable migration:

```
CREATE TABLE IF NOT EXISTS user (
  id int not null,
  name varchar(100) not null,
  is_enabled bit not null
);
```

Sweet clean history.

Note: depending on your database, idempotent migrations might be (and probably will be) more cumbersome to write than the pseudo-SQL written above.

One more challenge with versioned migrations is that <strong>multiple people might be working on different branches</strong>, all trying to create a new database migration. Following a simple numeric incremental versioning, like 1, 2, 3, etc, will cause conflicts. If a developer is creating <code>V2__add-password-field.sql</code> while another one is creating <code>V2__create-article-table.sql</code> (two completely unrelated migrations), whoever goes to the test environment first wins and the last one loses. The reason is that Flyway uses the version component (V2) as a key and as far as it is concerned, this is the same error as a checksum change.

One way to mitigate this is to use repeatable migrations. <code>R__add-password-field.sql</code> and <code>R__create-article-table.sql</code> are not considered the same version at all and will both be applied. The key here is the entire filename.

Another way is to use a versioning scheme which is less likely to cause conflicts, e.g. a date time stamp: <code>V2018.08.25.09.34__add-password-field.sql</code> and <code>V2018.08.25.09.41__create-article-table.sql</code> (in this case, specific up to the minute).

In that case, you will probably need to set these two properties in the configuration:
<ul>
<li><code>spring.flyway.outOfOrder=true</code>. This will apply migrations that exist in the code, but not in the database, and are <em>older</em> than the database's latest version. So if the "create articles table" feature branch is already deployed, this will allow the older (timestamp wise) "add password field" feature branch to apply its migration too.</li>
</ul>

<img src="{{ site.baseurl }}/assets/2018/flyway-out-of-order.jpg" />
<ul>
<li><code>spring.flyway.ignoreMissingMigrations=true</code>. This takes care of the opposite order, where migrations exist in the database but not in the code. This is the case where the "add password field" has applied already its migration and the "create articles table" is trying to apply its own.</li>
</ul>

<img src="{{ site.baseurl }}/assets/2018/flyway-ignore-missing-migrations.jpg" />

Some parting thoughts:
<ul>
<li><a href="{{ site.baseurl }}/2017/04/17/validate-filename-conventions-with-maven-enforcer-plugin.html">validate the filename conventions of your migration files</a></li>
<li>use a datetime version scheme for regular versioned migrations</li>
<li>consider using the same datetime prefix for repeatable migrations</li>
</ul>
