# SIDECAR REST API VERSION 2.0

Sidecar REST API is to handel the nova-evacaute process.

## Commands

### For getting all avilable versions

```html
GET  /
```


#### Request Header

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

#### Request Body

It does not accept and Request Body

> Success Code: 200

> Error code: 401

#### Response Body

| Pareameters   | Data Type   | Description                                                            |
| ------------- |:-----------:|:----------------------------------------------------------------------:|
| versions      | JSON Object | Object containing array of diffrent versions                           |
| v2            | JSON Object | Object containing version 2 info                                       |
| date          | date time   | Release date of the version                                            |
| status        | string      | What is the status of theversion. `current`, `supported`, `dereciated` |


#### Example

> Request:

```html
curl -H 'Content-Type:application/json'\
     -H 'X-Auth-Token:cb5a9e2cc2a94077b209f29a32347b0c'\
     -L http://controller:9090
```

> RESPONSE:

```json
{
    "versions": [
        {
            "v2": {
                 "date": "2016-08-07T00:00:00", 
                 "status": "current"
            }
        }
    ]
}
```

----

### For getting version info v2.0

```html
GET  /v2/
```


#### Request Header

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

#### Request Body

It does not accept and Request Body

> Success Code: 200

> Error code: 401

#### Response Body

| Pareameters   | Data Type   | Description                                                            |
| ------------- |-----------:|:------------------------------------------------------------------------|
| v2            | JSON Object | Object containing version 2 info                                       |
| date          | date time   | Release date of the version                                            |
| status        | string      | What is the status of theversion. `current`, `supported`, `dereciated` |


#### Example

> Request:

```html
curl -H 'Content-Type:application/json'\
     -H 'X-Auth-Token:cb5a9e2cc2a94077b209f29a32347b0c'\
     -L http://controller:9090/v2/
```

> RESPONSE:

```json 
{
     "v2": {
          "date": "2016-08-07T00:00:00", 
          "status": "current"
     }
} 
```

----

## Nova Evacuates

### Listing and filtering events

```html
GET  /v2/evacuates/events
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |

##### Query Parameters

| Pareameters           | Data Type        | Description                                       |
| ----------------------|:---------------- | --------------------------------------------------|
| id                    | String           | Id of the event                                   |
| name                  | String           | name of the event                                 |
| node_uuid             | String           | UUID of the host                                  |
| event_create_time     | Date time        | event_creation_time filter                        |
| min_event_create_time | Date Time        | minimum value event creatuin time                 |
| max_event_create_time | Date time        | maximum value for event creation                  |
| marker                | String           | Last seen event id.                               |
| limit                 | positive integer |Number of results to be displayed. Defgault is 30  | 

> SUCCESS CODE: 200

> Error codes: 401, 403, 500

##### RESPONSE Parameters

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| events                | JSON OBJECT      | A json object containg array of events                |
| id                    | String           | Id of the event                                       |
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `created`, `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |
| event_create_time     | Date time        | When the event was created                            |
| event_complete_time   | Date time        | When the event was completed                          |
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. |
| extra                 | JSON OBJECT      | Extra data in json                                    |

#### Example

> Request:

```html
curl -H 'Content-Type:application/json'
     -H 'X-Auth-Token:0d7f16c43bcc47b69bcc8dddf262097e' 
     -L http://controller:9090/v2/evacuates/events/?limit=30
```

> RESPONSE:

```json 
{
     "events": [
          {
               "id": "59ca965bef7e4a8f99088ac6f50a2e35", 
               "name": "Hello256", 
               "event_status": "created", 
               "event_create_time": "2016-09-02 14:32:17", 
               "event_complete_time": null, 
               "node_uuid": "test", 
               "vm_uuid_list": ["123", "4565"], 
               "extra": null
          }, 
          {
               "id": "7e1318856d7240728e511013c049876e", 
               "name": "Hello2567", 
               "event_status": "created", 
               "event_create_time": "2016-09-02 13:46:32", 
               "event_complete_time": null, 
               "node_uuid": "test", 
               "vm_uuid_list": ["123", "4565"], 
               "extra": null
          }
     ]
}
```

### Get detail of an event

```html
GET  /v2/evacuates/events/{event_id}
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ---------------------------------:|
| Content-Type  | String     |  application/json. It is optional |
| X-Auth-Token  | string     |  Authorization Token              |


> SUCCESS CODE: 200

> Error codes: 401, 403, 500

##### RESPONSE Parameters

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| event                 | JSON OBJECT      | A json object containg the event detail               |
| id                    | String           | Id of the event                                       |
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `created`, `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |
| event_create_time     | Date time        | When the event was created                            |
| event_complete_time   | Date time        | When the event was completed                          |
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. |
| extra                 | JSON OBJECT      | Extra data in json                                    |

#### Example

> Request:

```html
curl -X GET 
     -H 'Contrnt-Type:application/json'
     -H 'X-Auth-Token:2c213cc8f62e4c2086592cf7d52b7c21' 
     -L http://controller:9090/v2/evacuates/events/59ca965bef7e4a8f99088ac6f50a2e35
```

> RESPONSE:

```json 
{
     "event": {
          "event_complete_time": null, 
          "node_uuid": "test", 
          "event_create_time": "2016-09-02 14:32:17", 
          "name": "Hello256", 
          "vm_uuid_list": ["123", "4565"], 
          "extra": null, 
          "event_status": "created", 
          "id": "59ca965bef7e4a8f99088ac6f50a2e35"
     }
}
```


### Create a new event

```html
POST  /v2/evacuates/events
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ----------------------------------|
| Content-Type  | String     |  application/json.                |
| X-Auth-Token  | string     |  Authorization Token              |


> SUCCESS CODE: 201

> Error codes: 401, 403, 500, 409

##### RESPONSE Parameters

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| event                 | JSON OBJECT      | A json object containg the event detail               |
| id                    | String           | Id of the event                                       |
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `created`, `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |
| event_create_time     | Date time        | When the event was created                            |
| event_complete_time   | Date time        | When the event was completed                          |
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. |
| extra                 | JSON OBJECT      | Extra data in json                                    |

#### Example

> Request:

```html
curl -X POST 
     -H 'Content-Type:application/json' 
     -H 'X-Auth-Token:aef34829a88d4046bb9ac52b7e4824ca' 
     -L http://controller:9090/v2/evacuates/events 
     -d '{"event":{"name":"arte", "node_uuid":"234t7xut17t", "vm_uuid_list":["3232gjh", "jhcja7676"]}}' 
```

> RESPONSE:

```json 
{
     "event": {
          "event_complete_time": null, 
          "node_uuid": "234t7xut17t", 
          "event_create_time": "2016-09-07 03:44:14", 
          "name": "arte", 
          "vm_uuid_list": ["3232gjh", "jhcja7676"], 
          "extra": null, 
          "event_status": 
          "created", 
          "id": "c4eb2defb1094cb0b665ead9720000bb"
     }
}
```

### Edit a event

```html
PUT  /v2/evacuates/events/{event_id}
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ----------------------------------|
| Content-Type  | String     |  application/json.                |
| X-Auth-Token  | string     |  Authorization Token              |

##### Request body

| Pareameters           | Data Type        | Description                                           |
| ----------------------|:-----------------| ------------------------------------------------------|
| event                 | JSON OBJECT      | A json object containg the event detail               | 
| name                  | String           | name of the event                                     |
| event_status          | string           | What is the status of the event. The possible values: `completed`, `running` |
| node_uuid             | String           | UUID of the host                                      |  
| vm_uuid_list          | Aarry            | Array containg the vm ids, participated in the event. | 

> SUCCESS CODE: 204

> Error codes: 401, 403, 500, 409





#### Example

> Request:

```html
 curl -X PUT 
      -H 'Content-Type:application/json' 
      -H 'X-Auth-Token:c8813ebe6d99435ab2fe9ea502256cc8' 
      -L http://controller:9090/v2/evacuates/events/eba9897c33f14209ba28a82c22b8286c 
      -d '{
               "event":{
                    "name":"hhhhhh555", 
                    "event_status": "completed", 
                    "node_uuid":"7678687hghj", 
                    "vm_uuid_list":["tette", "jhsgjc"]
               }
          }'
```

> RESPONSE:

```json 
HEADER :
HTTP/1.1 204 No Content

```



### DELETE a event

```html
DELETE  /v2/evacuates/events/{event_id}
```
##### Request Headers

| Pareameters   | Data Type  | Description                       |
| ------------- |:----------:| ----------------------------------|
| Content-Type  | String     |  application/json.                |
| X-Auth-Token  | string     |  Authorization Token              |


> SUCCESS CODE: 204

> Error codes: 401, 403, 500, 409





#### Example

> Request:

```html
 curl -X DELETE 
      -H 'Content-Type:application/json' 
      -H 'X-Auth-Token:c8813ebe6d99435ab2fe9ea502256cc8' 
      -L http://controller:9090/v2/evacuates/events/eba9897c33f14209ba28a82c22b8286c  
```

> RESPONSE:

```json 
HEADER :
HTTP/1.1 204 No Content

```
