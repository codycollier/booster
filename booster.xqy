xquery version "1.0-ml";

(:------------------------------------------------------------------------------
 :
 : Module Name: booster.xqy
 :
 : Proprietary Extensions: functx 1.0, MarkLogic Server 4.2
 :
 : XQuery Specification: XQuery 1.0 / MarkLogic Server Enhanced 1.0-ml
 :
 : Module Overview: Booster is a small xquery module which provides an http 
 :   interface to a portion of the MarkLogic Admin API. It is intended to reside
 :   within the default MarkLogic Admin app server and provide a remotely 
 :   accessible hook for automated configuration. 
 :
 :
 : Copyright 2010 Cody Collier (cody@telnet.org)
 : 
 :   Licensed under the Apache License, Version 2.0 (the "License");
 :   you may not use this file except in compliance with the License.
 :   You may obtain a copy of the License at
 :
 :       http://www.apache.org/licenses/LICENSE-2.0
 :
 :   Unless required by applicable law or agreed to in writing, software
 :   distributed under the License is distributed on an "AS IS" BASIS,
 :   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 :   See the License for the specific language governing permissions and
 :   limitations under the License.
 :
 :----------------------------------------------------------------------------:)

 (:~
  : Booster provides a thin wrapper around the MarkLogic Admin and Sec API 
  : methods.  It allows a user to issue a single http request to perform admin 
  : tasks such as create a user, create a group, change a group config, and so 
  : on.  There is a rough 1:1 mapping between http requests and a given api 
  : method.  So, a user can string together many http requests to complete a 
  : series of custom configuration steps for a MarkLogic cluster.  These calls 
  : can easily be scripted with any language and http client, such as bash 
  : and curl.
  : 
  : Not all of the Admin and Security api methods are implemented, but more 
  : can be added upon request.  Also, users should refer to the formal MarkLogic
  : documentation for more specific details on method parameters as needed. 
  :
  : Developers:  Note that all parameters in action function definitions must 
  : be listed in alphabetical order.
  :
  : @see http://developer.marklogic.com/
  : @see http://developer.marklogic.com/pubs/4.2/apidocs/All.html
  : @see http://www.xqueryfunctions.com/
  :)


import module namespace admin = "http://marklogic.com/xdmp/admin" 
    at "/MarkLogic/admin.xqy";
import module namespace sec = "http://marklogic.com/xdmp/security" 
    at "/MarkLogic/security.xqy";
import module namespace functx = "http://www.functx.com" 
    at "/MarkLogic/functx/functx-1.0-nodoc-2007-01.xqy";

(:~
 : This variable holds xml that represents the main querystring parameters, 
 : their allowed values, and any other querystring parameters that are also 
 : required.  This structure is used for parameter validation.
 :)
declare variable $CONFIG:= 
<CONFIG>
    <parameters>
        <param name="debug" />
        <param name="action">
            <valid-options>
                <option value="appserver-delete"> 
                    <required>appserver-name</required>
                    <required>group-name</required>
                </option>
                <option value="appserver-create-http"> 
                    <required>appserver-name</required>
                    <required>group-name</required>
                    <required>root</required>
                    <required>port</required>
                    <required>modules-name</required>
                    <required>database-name</required>
                </option>
                <option value="appserver-create-webdav"> 
                    <required>appserver-name</required>
                    <required>group-name</required>
                    <required>root</required>
                    <required>port</required>
                    <required>database-name</required>
                </option>
                <option value="appserver-create-xdbc"> 
                    <required>appserver-name</required>
                    <required>group-name</required>
                    <required>root</required>
                    <required>port</required>
                    <required>modules-name</required>
                    <required>database-name</required>
                </option>
                <option value="database-attach-forest"> 
                    <required>database-name</required>
                    <required>forest-name</required>
                </option>
                <option value="database-detach-forest"> 
                    <required>database-name</required>
                    <required>forest-name</required>
                </option>
                <option value="database-create"> 
                    <required>database-name</required>
                    <required>security-db-name</required>
                    <required>schema-db-name</required>
                </option>
                <option value="database-delete">
                  <required>database-name</required>
                </option>
                <option value="forest-create"> 
                    <required>forest-name</required>
                    <required>host-name</required>
                    <required>data-directory</required>
                </option>
                <option value="forest-delete">
                  <required>forest-name</required>
                  <required>delete-data</required>
                </option>
                <option value="group-create"> 
                    <required>group-name</required>
                </option>
                <option value="group-delete">
                  <required>group-name</required>
                </option>
                <option value="host-set-group">
                    <required>host-name</required> 
                    <required>group-name</required>
                </option>
                <option value="user-create">
                    <required>user-name</required>
                    <required>description</required>
                    <required>password</required>
                    <required>role-names</required>
                    <required>permissions</required>
                    <required>collections</required>
                </option>
                <option value="user-delete">
                    <required>user-name</required>
                </option>
                <option value="appserver-set">
                    <required>appserver-name</required>
                    <required>group-name</required>
                    <required>setting</required>
                    <required>value</required>
                    <allowed-settings>
                        <setting cast="xs:string">address</setting>
                        <setting cast="xs:string">authentication</setting>
                        <setting cast="xs:unsignedInt">backlog</setting>
                        <setting cast="xs:string">collation</setting>
                        <setting cast="xs:boolean">compute-content-length</setting>
                        <setting cast="xs:unsignedInt">concurrent-request-limit</setting>
                        <setting cast="xs:boolean">debug-allow</setting>
                        <setting cast="xs:unsignedInt">default-time-limit</setting>
                        <setting cast="xs:string">default-xquery-version</setting>
                        <setting cast="xs:boolean">display-last-login</setting>
                        <setting cast="xs:boolean">enabled</setting>
                        <setting cast="xs:string">error-handler</setting>
                        <setting cast="xs:unsignedInt">keep-alive-timeout</setting>
                        <setting cast="xs:boolean">log-errors</setting>
                        <setting cast="xs:unsignedInt">max-time-limit</setting>
                        <setting cast="xs:string">name</setting>
                        <setting cast="xs:string">output-encoding</setting>
                        <setting cast="xs:string">output-sgml-character-entities</setting>
                        <setting cast="xs:unsignedInt">port</setting>
                        <setting cast="xs:unsignedInt">pre-commit-trigger-depth</setting>
                        <setting cast="xs:unsignedInt">pre-commit-trigger-limit</setting>
                        <setting cast="xs:boolean">profile-allow</setting>
                        <setting cast="xs:unsignedInt">request-timeout</setting>
                        <setting cast="xs:string">root</setting>
                        <setting cast="xs:unsignedInt">session-timeout</setting>
                        <setting cast="xs:boolean">ssl-allow-sslv3</setting>
                        <setting cast="xs:boolean">ssl-allow-tls</setting>
                        <setting cast="xs:string">ssl-ciphers</setting>
                        <setting cast="xs:string">ssl-hostname</setting>
                        <setting cast="xs:boolean">ssl-require-client-certificate</setting>
                        <setting cast="xs:unsignedInt">static-expires</setting>
                        <setting cast="xs:unsignedInt">threads</setting>
                        <setting cast="xs:string">url-rewriter</setting>
                    </allowed-settings>
                </option>
                <option value="database-set">
                    <required>database-name</required>
                    <required>setting</required>
                    <required>value</required>
                    <allowed-settings>
                        <setting cast="xs:boolean">attribute-value-positions</setting>
                        <setting cast="xs:boolean">collection-lexicon</setting>
                        <setting cast="xs:string">directory-creation</setting>
                        <setting cast="xs:boolean">element-value-positions</setting>
                        <setting cast="xs:boolean">element-word-positions</setting>
                        <setting cast="xs:boolean">enabled</setting>
                        <setting cast="xs:string">expunge-locks</setting>
                        <setting cast="xs:boolean">fast-case-sensitive-searches</setting>
                        <setting cast="xs:boolean">fast-diacritic-sensitive-searches</setting>
                        <setting cast="xs:boolean">fast-element-character-searches</setting>
                        <setting cast="xs:boolean">fast-element-phrase-searches</setting>
                        <setting cast="xs:boolean">fast-element-trailing-wildcard-searches</setting>
                        <setting cast="xs:boolean">fast-element-word-searches</setting>
                        <setting cast="xs:boolean">fast-phrase-searches</setting>
                        <setting cast="xs:boolean">fast-reverse-searches</setting>
                        <setting cast="xs:string">format-compatibility</setting>
                        <setting cast="xs:unsignedInt">in-memory-limit</setting>
                        <setting cast="xs:unsignedInt">in-memory-list-size</setting>
                        <setting cast="xs:unsignedInt">in-memory-range-index-size</setting>
                        <setting cast="xs:unsignedInt">in-memory-reverse-index-size</setting>
                        <setting cast="xs:unsignedInt">in-memory-tree-size</setting>
                        <setting cast="xs:string">index-detection</setting>
                        <setting cast="xs:boolean">inherit-collections</setting>
                        <setting cast="xs:boolean">inherit-permissions</setting>
                        <setting cast="xs:boolean">inherit-quality</setting>
                        <setting cast="xs:unsignedInt">journal-size</setting>
                        <setting cast="xs:string">journaling</setting>
                        <setting cast="xs:string">language</setting>
                        <setting cast="xs:string">locking</setting>
                        <setting cast="xs:boolean">maintain-directory-last-modified</setting>
                        <setting cast="xs:boolean">maintain-last-modified</setting>
                        <setting cast="xs:boolean">merge-enable</setting>
                        <setting cast="xs:unsignedInt">merge-max-size</setting>
                        <setting cast="xs:unsignedInt">merge-min-ratio</setting>
                        <setting cast="xs:unsignedInt">merge-min-size</setting>
                        <setting cast="xs:string">merge-priority</setting>
                        <setting cast="xs:unsignedLong">merge-timestamp</setting>
                        <setting cast="xs:string">name</setting>
                        <setting cast="xs:boolean">one-character-searches</setting>
                        <setting cast="xs:unsignedInt">positions-list-max-size</setting>
                        <setting cast="xs:boolean">preallocate-journals</setting>
                        <setting cast="xs:boolean">preload-mapped-data</setting>
                        <setting cast="xs:string">range-index-optimize</setting>
                        <setting cast="xs:boolean">reindexer-enable</setting>
                        <setting cast="xs:unsignedInt">reindexer-throttle</setting>
                        <setting cast="xs:unsignedInt">reindexer-timestamp</setting>
                        <setting cast="xs:string">stemmed-searches</setting>
                        <setting cast="xs:boolean">three-character-searches</setting>
                        <setting cast="xs:boolean">three-character-word-positions</setting>
                        <setting cast="xs:boolean">trailing-wildcard-searches</setting>
                        <setting cast="xs:boolean">trailing-wildcard-word-positions</setting>
                        <setting cast="xs:boolean">two-character-searches</setting>
                        <setting cast="xs:boolean">uri-lexicon</setting>
                        <setting cast="xs:boolean">word-positions</setting>
                        <setting cast="xs:boolean">word-searches</setting>
                    </allowed-settings>
                </option>
                <option value="group-set">
                    <required>group-name</required>
                    <required>setting</required>
                    <required>value</required>
                    <allowed-settings>
                        <setting cast="xs:boolean">audit-enabled</setting>
                        <setting cast="xs:string">audit-outcome-restriction</setting>
                        <setting cast="xs:unsignedInt">compressed-tree-cache-partitions</setting>
                        <setting cast="xs:unsignedInt">compressed-tree-cache-size</setting>
                        <setting cast="xs:unsignedInt">compressed-tree-read-size</setting>
                        <setting cast="xs:unsignedInt">expanded-tree-cache-partitions</setting>
                        <setting cast="xs:unsignedInt">expanded-tree-cache-size</setting>
                        <setting cast="xs:boolean">failover-enable</setting>
                        <setting cast="xs:string">file-log-level</setting>
                        <setting cast="xs:unsignedInt">host-initial-timeout</setting>
                        <setting cast="xs:unsignedInt">host-timeout</setting>
                        <setting cast="xs:unsignedInt">http-timeout</setting>
                        <setting cast="xs:string">http-user-agent</setting>
                        <setting cast="xs:unsignedInt">keep-audit-files</setting>
                        <setting cast="xs:unsignedInt">keep-log-files</setting>
                        <setting cast="xs:unsignedInt">list-cache-partitions</setting>
                        <setting cast="xs:unsignedInt">list-cache-size</setting>
                        <setting cast="xs:string">name</setting>
                        <setting cast="xs:unsignedInt">retry-timeout</setting>
                        <setting cast="xs:string">rotate-audit-files</setting>
                        <setting cast="xs:string">rotate-log-files</setting>
                        <setting cast="xs:string">smtp-relay</setting>
                        <setting cast="xs:unsignedInt">smtp-timeout</setting>
                        <setting cast="xs:string">system-log-level</setting>
                        <setting cast="xs:boolean">trace-events-activated</setting>
                        <setting cast="xs:boolean">xdqp-ssl-allow-sslv3</setting>
                        <setting cast="xs:boolean">xdqp-ssl-allow-tls</setting>
                        <setting cast="xs:string">xdqp-ssl-ciphers</setting>
                        <setting cast="xs:boolean">xdqp-ssl-enabled</setting>
                        <setting cast="xs:unsignedInt">xdqp-timeout</setting>
                    </allowed-settings>
                </option>
            </valid-options>
        </param>
    </parameters>
</CONFIG> ;


(:----------------------------------------------------------------------------:)
(:----------------------------- action functions -----------------------------:)
(:----------------------------------------------------------------------------:)

(:---------- appservers ------------------------------------------------------:)

(:~
 : Create an http app server
 :   wraps: admin:http-server-create
 : 
 : @param $appserver-name The name of the appserver to be created
 : @param $database-name The name of the documents db for the appserver
 : @param $group-name The name of the group where the appserver should live
 : @param $modules-name The name of the modules db for the appserver
 : @param $port The port on which the appserver will listen
 : @param $root The root path for the appserver
 : @return Returns status 201 on success and 409 if appserver already exists
 :)
declare function local:appserver-create-http($appserver-name as xs:string,
                    $database-name as xs:string, $group-name as xs:string,
                    $modules-name as xs:string, $port as xs:string,
                    $root as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $group-id := admin:group-get-id($config, $group-name)
    return 
        if (admin:appserver-exists($config, $group-id, $appserver-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                fn:concat("App server '", $appserver-name, "' already exists")))
        else (
            let $database-id := xdmp:database($database-name)
            let $modules-id := if ($modules-name eq "file-system") 
                                then "file-system" 
                                else xdmp:database($modules-name)
            let $_port := $port cast as xs:unsignedLong 
            let $new-config := admin:http-server-create($config, $group-id, 
                                $appserver-name, $root, $_port, $modules-id, 
                                $database-id)
            return
                admin:save-configuration($new-config),
                xdmp:set-response-code(201, "Created"))
};

(:~
 : Create an xdbc app server
 :   wraps: admin:xdbc-server-create
 : 
 : @param $appserver-name The name of the appserver to be created
 : @param $database-name The name of the documents db for the appserver
 : @param $group-name The name of the group where the appserver should live
 : @param $modules-name The name of the modules db for the appserver
 : @param $port The port on which the appserver will listen
 : @param $root The root path for the appserver
 : @return Returns status 201 on success and 409 if appserver already exists
 :)
declare function local:appserver-create-xdbc($appserver-name as xs:string,
                    $database-name as xs:string, $group-name as xs:string,
                    $modules-name as xs:string, $port as xs:string,
                    $root as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $group-id := admin:group-get-id($config, $group-name)
    return 
        if (admin:appserver-exists($config, $group-id, $appserver-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                fn:concat("App server '", $appserver-name, "' already exists")))
        else (
            let $database-id := xdmp:database($database-name)
            let $modules-id := if ($modules-name eq "file-system") 
                                then "file-system" 
                                else xdmp:database($modules-name)
            let $_port := $port cast as xs:unsignedLong 
            let $new-config := admin:xdbc-server-create($config, $group-id, 
                                $appserver-name, $root, $_port, $modules-id, 
                                $database-id)
            return
                admin:save-configuration($new-config),
                xdmp:set-response-code(201, "Created"))
};

(:~
 : Create a webdav app server
 :   wraps: admin:webdav-server-create
 : 
 : @param $appserver-name The name of the appserver to be created
 : @param $database-name The name of the documents db for the appserver
 : @param $group-name The name of the group where the appserver should live
 : @param $port The port on which the appserver will listen
 : @param $root The root path for the appserver
 : @return Returns status 201 on success and 409 if appserver already exists
 :)
declare function local:appserver-create-webdav($appserver-name as xs:string,
                    $database-name as xs:string, $group-name as xs:string,
                    $port as xs:string, $root as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $group-id := admin:group-get-id($config, $group-name)
    return 
        if (admin:appserver-exists($config, $group-id, $appserver-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                fn:concat("App server '", $appserver-name, "' already exists")))
        else (
            let $database-id := xdmp:database($database-name)
            let $_port := $port cast as xs:unsignedLong 
            let $new-config := admin:webdav-server-create($config, $group-id, 
                                $appserver-name, $root, $_port, $database-id)
            return
                admin:save-configuration($new-config),
                xdmp:set-response-code(201, "Created"))
};

(:~
 : Delete an app server from a group by name
 :   wraps: admin:appserver-delete
 :
 : @param $appserver-name The name of an app server
 : @param $group-name The name of the group in which the appserver resides
 : @return Returns status 200 on success and 404 if appserver does not exist
 :)
declare function local:appserver-delete($appserver-name as xs:string, 
                    $group-name as xs:string) 
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $group-id := admin:group-get-id($config, $group-name)
    return 
        if (fn:not(admin:appserver-exists($config, $group-id, $appserver-name)))
        then (
            xdmp:set-response-code(404, "Not Found"),
            xdmp:add-response-header("x-booster-error", 
                fn:concat("Appserver '", $appserver-name, "' does not exist")))
        else (
            let $appserver-id := admin:appserver-get-id($config, $group-id, 
                                                            $appserver-name)
            let $new-config := admin:appserver-delete($config, $appserver-id)
            return
                admin:save-configuration($new-config),
                xdmp:set-response-code(200, "OK"))
};

(:~
 : Update a given appserver setting with the given value
 :   wraps: admin:appserver-set-*
 : 
 : This function will accept a setting and a value to set for an appserver.  It 
 : will confirm the setting name exists in the config xml and it will cast the 
 : value as the type specified in the config xml.  The relevant admin method 
 : call will then be dynamically generated and applied.
 : 
 : @param $appserver-name The name of the appserver to edit
 : @param $group-name The name of the group in which the appserver resides
 : @param $setting The name of the setting to be changed
 : @param $value The value to apply to the setting
 : @return Returns 200 on success or 404 if appserver or setting do not exist
 :)
declare function local:appserver-set($appserver-name as xs:string, 
                    $group-name as xs:string, $setting as xs:string, 
                    $value as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $group-id := admin:group-get-id($config, $group-name)
    return
        if (fn:not(admin:appserver-exists($config, $group-id, $appserver-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Appserver '", $appserver-name, "' does not exist")))
        else (
            let $valid-settings := $CONFIG//option[@value="appserver-set"]/allowed-settings/setting/text()
            return 
                if (fn:not($setting eq $valid-settings)) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Appserver setting '", $setting, "' does not exist")))
                else (
                    let $appserver-id := admin:appserver-get-id($config, $group-id, $appserver-name)
                    (: cast the value according to the config specified @cast :)
                    let $val-type := $CONFIG//setting[text()=$setting]/@cast 
                    let $type-constructor := xdmp:function(xs:QName($val-type))
                    let $_value := xdmp:apply($type-constructor, $value)
                    (: construct and apply the appserver-set function with the newly cast value :)
                    let $func-name := fn:concat("admin:appserver-set-", $setting)
                    let $set-function := xdmp:function(xs:QName($func-name))
                    let $new-config := xdmp:apply($set-function, $config, $appserver-id, $_value)
                    return
                        admin:save-configuration($new-config),
                        xdmp:set-response-code(200, "OK")))
};

(:---------- databases -------------------------------------------------------:)

(:~
 : Create a database with the given name 
 :      wraps: admin:database-create
 : 
 : @param $database-name The name of the database to be created
 : @param $schema-db-name The name of the Schemas database for the new db
 : @param $security-db-name The name of the Security database for the new db
 : @return Returns status 201 on success, 409 if database exists
 :)
declare function local:database-create($database-name as xs:string,
                    $schema-db-name as xs:string, $security-db-name as xs:string) 
as empty-sequence()
{
    let $config := admin:get-configuration()
    return 
        if (admin:database-exists($config, $database-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                    fn:concat("Database '", $database-name, "' already exists")))
        else (
            let $security-db-id := xdmp:database($security-db-name)
            let $schema-db-id := xdmp:database($schema-db-name)
            let $new-config := admin:database-create($config, $database-name, 
                                                    $security-db-id, $schema-db-id)
            return 
                admin:save-configuration($new-config),
                xdmp:set-response-code(201, "Created"))
};

(:~
 : Delete the database with the given name 
 :      wraps: admin:database-delete
 : 
 : @param $database-name The name of the database to be deleted
 : @return Returns status 200 on success and 404 if database does not exist
 :)
declare function local:database-delete($database-name as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:database-exists($config, $database-name))) then (
            xdmp:set-response-code(404, "Not Found"),
            xdmp:add-response-header("x-booster-error",
                fn:concat("Database '", $database-name, "' does not exist")))
        else (
            admin:save-configuration(admin:database-delete($config, 
                                            xdmp:database($database-name))),
            xdmp:set-response-code(200, "OK"))
};

(:~
 : Attach a forest to a database
 :   wraps: admin:database-attach-forest
 : 
 : @param $database-name The name of the database
 : @param $forest-name The name of the forest
 : @return Returns 200 on success, 404 if db or forest do not exist, and 409 if 
 :              forest is already attached to a db
 :)
declare function local:database-attach-forest($database-name as xs:string, 
                    $forest-name as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:database-exists($config, $database-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Database '", $database-name, "' does not exist")))
        else (
            if (fn:not(admin:forest-exists($config, $forest-name))) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Forest '", $forest-name, "' does not exist")))
            else (
                let $database-id := xdmp:database($database-name)
                let $forest-id := xdmp:forest($forest-name)
                let $attached-db := admin:forest-get-database($config, $forest-id)
                return
                    if (fn:not(fn:empty($attached-db))) then (
                        xdmp:set-response-code(409, "Conflict"),
                        xdmp:add-response-header("x-booster-error",
                            fn:concat("Forest is already attached to a database")))
                    else ( 
                        let $new-config := admin:database-attach-forest($config, 
                                                    $database-id, $forest-id)
                        return
                            admin:save-configuration($new-config),
                            xdmp:set-response-code(200, "OK"))))
};

(:~
 : Detach a forest from a database
 :   wraps: admin:database-detach-forest
 : 
 : @param $database-name The name of the database
 : @param $forest-name The name of the forest
 : @return Returns 200 on success, 404 if db or forest do not exist, and 409 if 
 :              forest is not attached to db
 :)
declare function local:database-detach-forest($database-name as xs:string, 
                    $forest-name as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:database-exists($config, $database-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Database '", $database-name, "' does not exist")))
        else (
            if (fn:not(admin:forest-exists($config, $forest-name))) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Forest '", $forest-name, "' does not exist")))
            else (
                let $database-id := xdmp:database($database-name)
                let $forest-id := xdmp:forest($forest-name)
                let $attached-db := admin:forest-get-database($config, $forest-id)
                return 
                    if (fn:not($attached-db eq $database-id)) then (
                        xdmp:set-response-code(409, "Conflict"),
                        xdmp:add-response-header("x-booster-error",
                            fn:concat("Forest is not attached to given database")))
                    else ( 
                        let $new-config := admin:database-detach-forest($config, 
                                                    $database-id, $forest-id)
                        return
                            admin:save-configuration($new-config),
                            xdmp:set-response-code(200, "OK"))))
};

(:~
 : Update a given database setting with the given value
 :   wraps: admin:database-set-*
 : 
 : This function will accept a setting and a value to set for a database.  It 
 : will confirm the setting name exists in the config xml and it will cast the 
 : value as the type specified in the config xml.  The relevant admin method 
 : call will then be dynamically generated and applied.
 : 
 : @param $database-name The name of the database to edit
 : @param $setting The name of the setting to be changed
 : @param $value The value to apply to the setting
 : @return Returns 200 on success or 404 if database or setting do not exist
 :)
declare function local:database-set($database-name as xs:string,
                    $setting as xs:string, $value as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:database-exists($config, $database-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Database '", $database-name, "' does not exist")))
        else (
            let $valid-settings := $CONFIG//option[@value="database-set"]/allowed-settings/setting/text()
            return
                if (fn:not($setting eq $valid-settings)) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Database setting '", $setting, "' does not exist")))
                else (
                    let $database-id := xdmp:database($database-name)
                    (: cast the value according to the config specified @cast :)
                    let $val-type := $CONFIG//setting[text()=$setting]/@cast
                    let $type-constructor := xdmp:function(xs:QName($val-type))
                    let $_value := xdmp:apply($type-constructor, $value)
                    (: construct and apply the database-set function with the newly cast value :)
                    let $func-name := fn:concat("admin:database-set-", $setting)
                    let $set-function := xdmp:function(xs:QName($func-name))
                    let $new-config := xdmp:apply($set-function, $config, $database-id, $_value)
                    return
                        admin:save-configuration($new-config),
                        xdmp:set-response-code(200, "OK")))
};

(:---------- forests ---------------------------------------------------------:)

(:~
 : Create a forest with the given name 
 :      wraps: admin:forest-create
 : 
 : Note, an empty data-directory will result in private forest
 : 
 : @param $data-directory  The path for the forest
 : @param $forest-name The name of the forest to be created
 : @param $host-name The host name where the forest will be hosted or "localhost"
 : @return Returns status 201 on success, 409 if forest exists
 :)
declare function local:forest-create($data-directory as xs:string,
                    $forest-name as xs:string, $host-name as xs:string) 
as empty-sequence()
{
    let $config := admin:get-configuration()
    return 
        if (admin:forest-exists($config, $forest-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                    fn:concat("Forest '", $forest-name, "' already exists")))
        else (
            let $host-id := if ($host-name eq "localhost") 
                            then (xdmp:host())
                            else (xdmp:host($host-name))
            let $new-config := admin:forest-create($config, $forest-name, 
                                                    $host-id, $data-directory)
            return 
                admin:save-configuration($new-config),
                xdmp:set-response-code(201, "Created"))
};

(:~
 : Delete the forest with the given name 
 :      wraps: admin:forest-delete
 : 
 : @param $delete-data An indicator "true" or "false" of whether to delete data
 : @param $forest-name The name of the forest to be deleted
 : @return Returns status 200 on success and 404 if forest does not exist
 :)
declare function local:forest-delete($delete-data as xs:string,
                    $forest-name as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:forest-exists($config, $forest-name))) then (
            xdmp:set-response-code(404, "Not Found"),
            xdmp:add-response-header("x-booster-error",
                fn:concat("Forest '", $forest-name, "' does not exist")))
        else (
            let $forest-id := admin:forest-get-id($config, $forest-name)
            let $_delete-data := if ($delete-data eq "true")
                                    then (fn:true())
                                    else (fn:false())
            let $new-config := admin:forest-delete($config, $forest-id, 
                                                        $_delete-data)
            return
                admin:save-configuration($new-config),
                xdmp:set-response-code(200, "OK"))
};

(:---------- groups ----------------------------------------------------------:)

(:~
 : Retrieve list of group names from the configuration
 : 
 : @return sequence of group names
 :)
declare function local:group-names-retrieve() as xs:string*
{
    let $config := admin:get-configuration()
    let $group-names := for $grid in admin:get-group-ids($config)
                            return admin:group-get-name($config, $grid)
    return 
        $group-names, "",
        xdmp:set-response-code(200, "OK")
};

(:~
 : Create a new group with the provided name 
 :   wraps: admin:group-create
 : 
 : @param $group-name The desired name of the group
 : @return Returns status code 201 on success and 409 on failure 
 :)
declare function local:group-create($group-name as xs:string) as empty-sequence()
{
    let $config := admin:get-configuration()
    return 
        if (admin:group-exists($config, $group-name)) then (
            xdmp:set-response-code(409, "Conflict"),
            xdmp:add-response-header("x-booster-error", 
                    fn:concat("Group '", $group-name, "' already exists")))
        else (
            admin:save-configuration(admin:group-create($config, $group-name)),
            xdmp:set-response-code(201, "Created"))
};

(:~
 : Delete a group with the given name
 :   wraps: admin:group-delete
 : 
 : @param $group-name The name of the group to delete
 : @return Returns status code 200 on success and 404 if group does not exist
 :)
declare function local:group-delete($group-name as xs:string) as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:group-exists($config, $group-name))) then (
            xdmp:set-response-code(404, "Not Found"),
            xdmp:add-response-header("x-booster-error",
                fn:concat("Group '", $group-name, "' does not exist")))
        else (
            admin:save-configuration(admin:group-delete($config, 
                                        admin:group-get-id($config, $group-name))),
            xdmp:set-response-code(200, "OK"))
};

(:~
 : Update a given group setting with the given value
 :   wraps: admin:group-set-*
 : 
 : This function will accept a setting and a value to set for a group.  It will 
 : confirm the setting name exists in the config xml and it will cast the 
 : value as the type specified in the config xml.  The relevant admin method 
 : call will then be dynamically generated and applied.
 : 
 : @param $group-name The name of the group to edit
 : @param $setting The name of the setting to be changed
 : @param $value The value to apply to the setting
 : @return Returns 200 on success or 404 if group or setting do not exist
 :)
declare function local:group-set($group-name as xs:string, 
                    $setting as xs:string, $value as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    return
        if (fn:not(admin:group-exists($config, $group-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Group '", $group-name, "' does not exist")))
        else (
            let $valid-settings := $CONFIG//option[@value="group-set"]/allowed-settings/setting/text()
            return 
                if (fn:not($setting eq $valid-settings)) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Group setting '", $setting, "' does not exist")))
                else (
                    let $group-id := admin:group-get-id($config, $group-name)
                    (: cast the value according to the config specified @cast :)
                    let $val-type := $CONFIG//setting[text()=$setting]/@cast 
                    let $type-constructor := xdmp:function(xs:QName($val-type))
                    let $_value := xdmp:apply($type-constructor, $value)
                    (: construct and apply the group-set function with the newly cast value :)
                    let $func-name := fn:concat("admin:group-set-", $setting)
                    let $set-function := xdmp:function(xs:QName($func-name))
                    let $new-config := xdmp:apply($set-function, $config, $group-id, $_value)
                    return
                        admin:save-configuration($new-config),
                        xdmp:set-response-code(200, "OK")))
};

(:---------- hosts -----------------------------------------------------------:)

(:~
 : Set the group membership for a given host
 :   wraps: admin:host-set-group
 :
 : @param $group-name The name of the group to set for the host
 : @param $host-name The name of the host to update or "localhost"
 : @return Returns 200 on success and 404 if host or group do not exist
 :)
declare function local:host-set-group($group-name as xs:string, 
                    $host-name as xs:string)
as empty-sequence()
{
    let $config := admin:get-configuration()
    let $_host-name := if ($host-name eq "localhost")
                        then (xdmp:host-name(xdmp:host()))
                        else ($host-name)
    return
        if (fn:not(admin:host-exists($config, $_host-name))) then (
                xdmp:set-response-code(404, "Not Found"),
                xdmp:add-response-header("x-booster-error",
                    fn:concat("Host '", $host-name, "' does not exist")))
        else (
            if (fn:not(admin:group-exists($config, $group-name))) then (
                    xdmp:set-response-code(404, "Not Found"),
                    xdmp:add-response-header("x-booster-error",
                        fn:concat("Group '", $group-name, "' does not exist")))
            else (
                let $group-id := admin:group-get-id($config, $group-name)
                let $host-id := xdmp:host($_host-name)
                let $new-config := admin:host-set-group($config, $host-id,
                                                            $group-id)
                return
                    admin:save-configuration($new-config),
                    xdmp:set-response-code(200, "OK")))
};


(:---------- users -----------------------------------------------------------:)

(:~
 : Create a new user with the provided configuration
 :   wraps: sec:create-user
 :
 : examples of special formatting for multi-value parameters:
 : collections: "http://marklogic.com/xdmp/alert, http://marklogic.com/xdmp/triggers"
 : permissions: "app-user,read;app-user,update"  csv pairs separated by semicolons 
 : role-names: "app-user,alert-user"
 : 
 : @param $collections A csv list of collection names to pass to the api method
 : @param $description A description for the user being created
 : @param $password A password for the user being created
 : @param $permissions Pairs of permissions to pass to the api method / csv + ;
 : @param $role-names A csv list of role names to assign to the user
 : @param $user-name The name of the user to create
 : @return Returns status code 201 on success and 409 if user already exists
 :)
declare function local:user-create(
                    $collections as xs:string, $description as xs:string,
                    $password as xs:string, $permissions as xs:string,
                    $role-names as xs:string, $user-name as xs:string)
as item()*
{
    if (sec:user-exists($user-name)) then (
        xdmp:set-response-code(409, "Conflict"),
        xdmp:add-response-header("x-booster-error", 
            fn:concat("User '", $user-name, "' already exists")))
    else (
        let $_collections := fn:tokenize($collections, ",")
        let $_role-names := fn:tokenize($role-names, ",")
        let $_permissions := for $p in fn:tokenize($permissions, ";")
                                let $pair := fn:tokenize($p, ",")
                                return xdmp:permission($pair[1], $pair[2])
        return 
            sec:create-user($user-name, $description, $password, $_role-names,
                            $_permissions, $_collections),
            xdmp:set-response-code(201, "Created"))
};

(:~
 : Delete a user with the given name
 :   wraps: sec:remove-user
 : 
 : @param $user-name The name of the user to delete
 : @return Returns status code 200 on success and 404 if user does not exist
 :)
declare function local:user-delete($user-name as xs:string)
as empty-sequence()
{
    if (fn:not(sec:user-exists($user-name))) then (
        xdmp:set-response-code(404, "Not Found"),
        xdmp:add-response-header("x-booster-error",
            fn:concat("User '", $user-name, "' does not exist")))
    else (
        sec:remove-user($user-name),
        xdmp:set-response-code(200, "OK"))
};


(:----------------------------------------------------------------------------:)
(:----------------------------- request processing ---------------------------:)
(:----------------------------------------------------------------------------:)

(:~
 : Validate the value of the action parameter against the config xml
 : 
 : @param none
 : @return Returns empty sequence on success and throws error on invalid action
 :)
declare function local:validate-action()
{
    let $action := xdmp:get-request-field("action", "None")
    let $valid-actions := $CONFIG/parameters/param[@name="action"]/valid-options/option/@value
    return 
        if ($action eq $valid-actions) then ()
        else if ($action = "None") then (
            fn:error((), fn:concat("An action must be supplied")))
        else fn:error((), fn:concat("The action '", $action, 
                                        "' is not a valid action") )
}; 

(:~
 : Validate correct parameters were passed along with a given action
 : 
 : @param none
 : @return Returns empty sequence on success and throws error on invalid params
 :)
declare function local:validate-action-args()
{
    let $action := xdmp:get-request-field("action", "error")
    let $action-args := functx:sort(functx:value-except(
                            xdmp:get-request-field-names(),
                            $CONFIG/parameters/param/@name) 
                                cast as xs:string*)
    let $valid-action-args := 
            functx:sort($CONFIG//option[@value=$action]/required/text()
                            cast as xs:string*)
    return
        if (fn:deep-equal($action-args, $valid-action-args))
        then ()
        else fn:error((), fn:concat("A valid set of arguments was not provided for '", 
                                $action, 
                                "' (received: ", 
                                fn:string-join($action-args, ","), 
                                ") (expected: ", 
                                fn:string-join($valid-action-args, ","), 
                                ")"))
};


(:~
 : Given an action and parameters, perform a call to the associated function
 : 
 : This is the core routing function for all incoming requests.  It is assumed 
 : that the parameters have been validated before this function is called. 
 : All legal action values map to a defined function name.  So, the action 
 : value and all the querystring parameters passed in are used to dynamically 
 : generate a function call which is run using xdmp:apply. 
 : 
 : http request -> validation -> action-handler -> action function
 : 
 : @param none
 : @return Returns whatever the called action function returns
 : @error If an exception occurs in the called action, then an http status code 
 :         of 500 is returned and the header x-booster-error is populated
 :)
declare function local:action-handler() as item()*
{
    (: force transaction to be an update statement so apply won't throw exception :)
    let $_ := xdmp:lock-for-update("/no-such-uri")

    (: retrieve the action name and the associated function :)
    let $action := xdmp:get-request-field("action")
    let $action-function-name := fn:concat("local:", $action)
    let $action-function := xdmp:function(xs:QName($action-function-name))

    (: retrieve the key/value pairs from the querystring, ordered by key :)
    let $request-fields := xdmp:get-request-field-names()
    let $arg-names := functx:sort(functx:value-except(
                        $request-fields, 
                        $CONFIG/parameters/param/@name 
                            cast as xs:string*))
    let $arg-values := ()
    let $arg-values := for $arg in $arg-names
                        return xdmp:get-request-field($arg)

    (: run the action function and pass in the args, ordered by key :)
    let $arg-count := fn:count($arg-values)
    return 
        try {
            if ($arg-count eq 0) then
                xdmp:apply($action-function)
            else if ($arg-count eq 1) then
                xdmp:apply($action-function, $arg-values[1])
            else if ($arg-count eq 2) then
                xdmp:apply($action-function, $arg-values[1], $arg-values[2])
            else if ($arg-count eq 3) then
                xdmp:apply($action-function, $arg-values[1], $arg-values[2],
                            $arg-values[3])
            else if ($arg-count eq 4) then
                xdmp:apply($action-function, $arg-values[1], $arg-values[2],
                            $arg-values[3], $arg-values[4])
            else if ($arg-count eq 5) then
                xdmp:apply($action-function, $arg-values[1], $arg-values[2],
                            $arg-values[3], $arg-values[4], $arg-values[5])
            else if ($arg-count eq 6) then
                xdmp:apply($action-function, $arg-values[1], $arg-values[2],
                            $arg-values[3], $arg-values[4], $arg-values[5],
                            $arg-values[6])
            else fn:error((), "There was an error with the argument count")
        } catch ($err) {
            xdmp:set-response-code(500, "Booster Error"),
            xdmp:add-response-header("x-booster-error", 
                fn:concat("Error running action '", $action, "'. Error: ", 
                $err/error:message/text())),
                $err
        }
};

(:----------------------------------------------------------------------------:)
(:---------------------------------- main ------------------------------------:)
(:----------------------------------------------------------------------------:)

 (: http request -> validation -> action-handler -> action function :)

try { 
    sec:check-admin(),
    try {
        local:validate-action(),
        local:validate-action-args(),
        local:action-handler()
    } catch ($err) {
        xdmp:set-response-code(400, "Bad Request"),
        xdmp:add-response-header("x-booster-error", $err/error:message/text())
    }
} catch ($err) { 
    xdmp:set-response-code(403, "Forbidden"),
    "Error: user must be assigned the admin role\r\n"
}


