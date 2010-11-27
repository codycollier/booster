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
                <option value="get-group-names" />
                <option value="group-create"> 
                    <required>group-name</required>
                </option>
                <option value="group-delete">
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


(:---------- databases -------------------------------------------------------:)
(:---------- forests ---------------------------------------------------------:)

(:---------- groups ----------------------------------------------------------:)

(:~
 : Retrieve list of group names from the configuration
 : 
 : @return sequence of group names
 :)
declare function local:get-group-names() as xs:string*
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


(:---------- hosts -----------------------------------------------------------:)

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
        xdmp:add-response-header("x-booster-error", $err/error:message/text()),
        $err
    }
} catch ($err) { 
    xdmp:set-response-code(403, "Forbidden"),
    "Error: user must be assigned the admin role\r\n"
}


