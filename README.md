Booster
=======

Booster is an xquery module which provides an http interface to a portion of the MarkLogic API for administrative tasks.  It is intended to reside within the default  Admin app server and provide a remotely accessible hook for automated configuration.

The current release is [https://github.com/downloads/codycollier/booster/booster-0.2.xqy booster 0.2].

Requires: MarkLogic Server 4.2+


Quick Start
-----------

*1. Install booster.xqy in the Admin app server root*

    [user@host ~]$ scp booster-0.2.xqy root@new-server:/opt/MarkLogic/Admin/booster.xqy


*2. Call booster to create, edit, or delete resources*

    # create a new group
    curl --digest -u"admin:pass" "http://new-server:8001/booster.xqy?action=create-group&group-name=eval-nodes"




What can booster do?
---------------------

Booster allows you to make http requests that map to MarkLogic administration actions like creating a user, creating a database, attaching a forest to a database, and so on.  The action and related parameters are passed as querystring variables.


Each http request must include a single action.  Each action then expects other related variables to be passed in the querystring.  For example, the action for creating a database is "database-create" and it expects "database-name", "security-db-name", and "schema-db-name" to also be passed in the request.  Here's a curl example:

    # create a new database
    curl --digest -u"admin:pass" \
    "http://server:8001/booster.xqy?\
    action=database-create&database-name=MyNewDatabase\
    &schema-db-name=Schemas&security-db-name=Security




With a small amount of shell scripting, you can string together these http calls and completely automate the configuration of a new or existing MarkLogic cluster.  You can read more about why this might be useful and more about installation automation at [WhyBooster](https://github.com/codycollier/booster/wiki/WhyBooster).


If you're ready for more details, you can read about the available actions on the [Actions](https://github.com/codycollier/booster/wiki/Actions) page.  You can find more examples on the [ActionExamples](https://github.com/codycollier/booster/wiki/ActionExamples) page.


You can view results from the functional test suite at [TestResults](https://github.com/codycollier/booster/wiki/TestResults).




