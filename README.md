pyBulk
------
Simple bulk mailer with a personal touch. It allows to send the same message to a large number of reciptient w/ a personal salutation or a default greeting.

It uses SMTP with starttls().

####SMTP settings

SMTP settings are provided in a JSON, by default conf.json with all the necessary credentials.
```JSON
{
  "HOST" : "stmp.provider.com",
  "PORT" : 587,
  "USER" : "user@provider.com",
  "PASS" : "password",
  "FROM" : "Some sender string eg. your name"
}
```

####Recipients

The recipients are in a .csv file (usually provided in sys.argv) that contains address and an optional salutation. If no salutation is given, the default is used.

```csv
foo@bar.com, Dear Mr. Foo
spam@ham.com,
eggs@spam.com, My dear friend
```

####Other
upcoming

