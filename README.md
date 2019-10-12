# facetag-services

Face tagging services is a collection of APIs that allow you to build photo sharing services where you can find a person's photos easily. It is full serverless services built using Azure functions, CosmosDB, Azure Blob Storage for backend.

**Table of Contents**
<!-- TOC -->

- [facetag-services](#facetag-services)
    - [Features](#features)
    - [Architecture](#architecture)
    - [Example Operations](#example-operations)
        - [Training faces of persons](#training-faces-of-persons)
        - [Uploading photos and identifying faces of persons](#uploading-photos-and-identifying-faces-of-persons)
    - [REST APIs](#rest-apis)
        - [Authentication](#authentication)
        - [Regist User](#regist-user)
        - [Delete User](#delete-user)
        - [Create Person](#create-person)
        - [Delete Person](#delete-person)
        - [Get Persons](#get-persons)
        - [Create Asset](#create-asset)
        - [Delete Asset](#delete-asset)
        - [Get Assets](#get-assets)
        - [Get Photos](#get-photos)
        - [Trigger Train](#trigger-train)
        - [Get Blob SAS Token](#get-blob-sas-token)

<!-- /TOC -->

## Features
- Train faces of a person
- Uploading photos
- Identify faces of a person in uploaded photos
- Management APIs for Users, Assets, Persons, and Photos

## Architecture
**Data flows of major operations**
![](assets/facetag-services-arch.png)

**Azure functions proxies: URI path and function mapping**
![](assets/proxies-uri-functions-mapping.png)

**Concept of user, person, and asset in facetag_services**

![](assets/concepts.png)


## Example Operations
### Training faces of persons
| Operation | Example |
|---|---|
| 1. Register user using [Regist User](#regist-user) API (Only if not yet registerd user) | Regist a user with user_id "nogizaka46" |
| 2. Create a person for the user using [Create Person](#create-person) API. The API response contains `person_id` and `asset_id_for_train`. You'll use `person_id` for identifying the person, and `asset_id_for_train` for uploading photos of the person in order to train the face of the person. So please don't forget to get both info! | Create a person named "Mai Shiraishi", and get "063aa8ac-c9b3-4969-952f-26388ab67726" for `person_id` and "c4baf03e-1eb0-4dde-b0e6-b1d68e1f5df3" for `asset_id_for_train` |
| 3. Upload photos of the person to the prepared container ( container name == `asset_id_for_train` ) in Azure blob storage | Upload photos of a person "Mai Shiraishi" to the container named "c4baf03e-1eb0-4dde-b0e6-b1d68e1f5df3" (= `asset_id_for_train`, the one you got previously)  |
| 4. Trigger training of the person's face using [Trigger Train](#trigger-train) API. The training will be done asynchronously as a backgroud job | Trigger the training of a person "Mai Shiraishi" (`person_id`: "063aa8ac-c9b3-4969-952f-26388ab67726")'s faces |

### Uploading photos and identifying faces of persons 

| Operation | Example |
|---|---|
| 1. Create an asset for a certain category of photos that you want to upload using [Create Asset](#create-asset) API. The API response contains `asset_id` for the created asset. You'll use the `asset_id` for uploading photos of a certain category | Create an asset named "Album 2019" and you'll get an asset_id "52edcedb-f4c8-4ef5-8e16-9b56ab28346b" for the asset. |
| 2. Upload photos of the certain cateogry to the prepared container ( container name == asset_id) in Azure blob storage. As soon as the photos are uploaded, event-driven functions are triggerred to run in order to detect, identify, and tag faces of the persons that you created/trained. Identified face info is stored persistently in backend databases.  | |

## REST APIs
### Authentication
Add API Key for functions in HTTP header in REST API requests

```json
x-functions-key: {API_KEY}
```

> Example request for getperson API: 
```bash
API_KEY="abcdefgxxxxxxxxxyyyyyyyyzzzzzzzz******=="
curl -s \
 -H "Content-Type: application/json"\
 -H "x-functions-key: ${API_KEY}"\
 -XPOST https://myfacetagsvc.azurewebsites.net/person -d'
{
  "person_name": "Mai Shiaishi"
}'
```

### Regist User 
Regist a user 

> POST /user

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
| `user_id`| string | Yes | User ID. It has to be unique across the whole  service. Only allow only alphanumeric and underscore in user_id. |
| `user_name`| string |  | Name of User |

Example Body
```json
{
  "user_id": "nogizaka46",
  "user_name": "Nogizaka 46 Group"
}
```

**Response**

```
Status: 200 OK
```
```
<user_id>
```

### Delete User
Delete a user 

> DELETE /user/{user_id}

**Response**

```
Status: 200 OK
```
```
<user_id>
```

### Create Person
Create a new person for a user. A created person ID will be returned as reseponse body.

> POST /user/{user_id}/person

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
| `person_name`| string |  | Name of Person |

Example Body
```json
{
  "person_name": "Mai Shiraishi"
}
```

**Response**

```
Status: 200 OK
```
```json
{
   "person_id": "063aa8ac-c9b3-4969-952f-26388ab67726",
   "person_name": "Mai Shiraishi",
   "asset_id_for_train": "c4baf03e-1eb0-4dde-b0e6-b1d68e1f5df3"
}
```

### Delete Person
Delete person from a person group of a user

> DELETE /api/deleteperson?user_id={user_id}&person_id={person_id}
**Response**

```
Status: 200 OK
```
```
<deleted_person_id>
```

### Get Persons
Get the list of persons for a user

> GET /user/{user_id}/persons

**Response**

```
Status: 200 OK
```
```json
[
  "a654f4c2-dc7d-43dc-a95a-8819da69587a",   // ID for person1
  "3dad91b4-fa4c-4c11-b9c0-e240a579c253",   // ID for person2
  ...,
  "b89387bf-5a0e-48a2-bf58-49b6f1f78982",   // ID for personN
]
```

### Create Asset
Create an asset of a user

Create a new asset for a user. A created asset ID will be returned as reseponse body.

> POST /user/{user_id}/asset

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
| `asset_name`| string |  | Name of asset |

Example Body
```json
{
  "asset_name": "Album 2019"
}
```

**Response**

```
Status: 200 OK
```
```
<created_asset_id>
```

### Delete Asset
Delete an asset of a user

> DELETE /api/deleteasset?user_id={user_id}&asset_id={asset_id}

**Response**

```
Status: 200 OK
```
```
<deleted_asset_id>
```

### Get Assets
Get the list of assets of a user

> GET /user/{user_id}/assets

**Response**

```
Status: 200 OK
```
```json
[
  {
    "asset_id": "5x472930-x3c6-55df-93x2-z9900a2b2300",
    "asset_name": "Album 2017",
    "user_id": "nogizaka46"
  },  
  {
    "asset_id": "2d447b84-e2c4-4eed-93b6-e6600a2b5608",
    "asset_name": "Album 2018",
    "user_id": "nogizaka46"
  },
  {
    "asset_id": "2b48152d-02b1-443f-9617-eaa499fb0a93",
    "asset_name": "Album 2019",
    "user_id": "nogizaka46"
  },
  ...
]
```

### Get Photos
Get the list of photos of a user. You can filter photos by a Person ID, Asset ID, and a User ID.

> POST /photos

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
| `user_id`| string | Yes | User ID |
| `person_id`| string |  | Person ID |
| `asset_id`| string |  | Asset ID |
| `order`| string |  | ASC or DESC (default) |
| `offset`| number |  | Offset position of result items(Default 0) |
| `limit`| number |  | limit number of result items (Default 100) |

Example 1: Get photos of a person in a user group (user_id + person_id)
```json
{
  "user_id": "nogizaka46",
  "person_id": "a654f4c2-dc7d-43dc-a95a-8819da69587a",
  "order": "DESC",
  "offset": "0",
  "limit": "50"
}
```

Example 2: Get photos stored in a asset (user_id + asset_id)
```json
{
  "user_id": "nogizaka46",
  "person_id": "a654f4c2-dc7d-43dc-a95a-8819da69587a",
  "order": "DESC",
  "offset": "0",
  "limit": "50"
}
```

Example 3: Get photos in a user group (user_id)
```json
{
  "user_id": "nogizaka46",
  "order": "DESC",
  "offset": "0",
  "limit": "50"
}
```

**Response**

```
Status: 200 OK
```
```json
[
  {
    "photo_id": "114a2d4a36340e0726e1079145d8e8c6794b8b7541c334edae997691248b01e7",
    "asset_id": "2d447b84-e2c4-4eed-93b6-e6600a2b5608",
    "blob_name": "mai-shiraishi-0.jpg",
    "user_id": "nogizaka46",
    "persons": [
      {
        "person_id": "a654f4c2-dc7d-43dc-a95a-8819da69587a"
      }
    ],
    "last_updated": 1569808309
  },
  {
    "photo_id": "4369e41be321894298ed3188f715dc4f14a8ae51d1bcd1dcd21c2dc2ce162af9",
    "asset_id": "2d447b84-e2c4-4eed-93b6-e6600a2b5608",
    "blob_name": "mai-shiraishi-1.jpg",
    "user_id": "nogizaka46",
    "persons": [
      {
        "person_id": "a654f4c2-dc7d-43dc-a95a-8819da69587a"
      }
    ],
    "last_updated": 1569808315
  },
  {
    "photo_id": "0321b08d15c1065569b0bcda5bc726ea9473b3107f78d15c323b0bf621add9f4",
    "asset_id": "2d447b84-e2c4-4eed-93b6-e6600a2b5608",
    "blob_name": "nobody-0.jpg",
    "user_id": "nogizaka46",
    "persons": [],
    "last_updated": 1569808340
  }
  ...
]
```

### Trigger Train

Trigger training of a person's faces

> PUT /user/{user_id}/person/{person_id}/trigger

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
| `user_id`| string | Yes | User ID |
| `person_id`| string | Yes | Person ID |

**Response**

```
Status: 200 OK
```

### Get Blob SAS Token

Get a SAS token for Azure Storage for the specified container and blob name. You can also specify access permissions for the container/blob name and optionally its token time-to-live period. The SAS token expires in an hour by default.

> POST /blobsastoken

**Request**

|Name|Type| Requred |Description|
|---|---|---|---|
|`permission`| string | Yes | Signed permission for shared access signature | 
|`container` | string | Yes | Container name to access |
|`blobname`  | string | | Blob object name to access |
| `ttl`      | string | | Token time to live period in hours. 1hour by default |

- The following values can be used for permissions: 
 `a` (Add), `r` (Read), `w` (Write), `d` (Delete), `l` (List)
- Concatenate multiple permissions, such as `rwa` = Read, Write, Add

Sample Request Body
```json
 {
    'permission': "rl",
    'container': "functions",
    'blobname': "yokawasa.png"
 }
```
**Response** 
Response body format
```json
HTTP response body format is:
{
    'token': '<Shared Access Signature Token string>',
    'url' :  '<SAS resource URI>'
}
```

Sample Response Body
```json
{
  "token": "sv=2018-03-28&ss=b&srt=o&sp=rl&se=2019-03-29T14%3A02%3A37Z&st=2019-03-29T11%3A57%3A37Z&spr=https&sig=Sh7RAa5MZBk7gfv0haCbEbllFXoiOWJDK9itzPeqURE%3D",
  "url": "https://azfuncv2linuxstore.blob.core.windows.net/functiontest/sample.jpg?sv=2018-03-28&ss=b&srt=o&sp=rl&se=2019-03-29T14%3A02%3A37Z&st=2019-03-29T11%3A57%3A37Z&spr=https&sig=Sh7RAa5MZBk7gfv0haCbEbllFXoiOWJDK9itzPeqURE%3D" 
}
```
