# facetag-services

Face tagging services using Azure functions, CosmosDB, Azure Blob Storage for backend


**Table of Contents**
<!-- TOC -->

- [facetag-services](#facetag-services)
    - [Features](#features)
    - [Architecture](#architecture)
        - [Flow of trainining of faces of a person](#flow-of-trainining-of-faces-of-a-person)
        - [Face recognition flow](#face-recognition-flow)
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

<!-- /TOC -->

## Features
- Train faces of a person
- Photo Uploading
- Identify faces of a person in uploaded photos
- Management API for Users, Assets, Persons, and Photos

## Architecture



### Flow of trainining of faces of a person

1. A user uploads photos to user container for face training
    - Create user blob container
    - Regist CosmosDB
    - Upload Images
2. Trigger training
    - Send Message to Queue (user_id)
3. QueueTrigger Functions (Background Job)
    - Get userinfo from CosmosDB using user_id
    - Glob upload images
    - Create usergroup if not exists
    - Create persion if not exists
    - Add faces to persion
    - Train the user group
    - Update status in CosmosDB

### Face recognition flow
1. Upload images
    - Get userinfo from CosmosDB using user_id
    - Create user blob container if needed
    - Regist CosmosDB
        - mapping: container_name - user_id
    - Upload Images
2. EventGrid Trigger Function
    - Get user_id from container_name
    - Get userinfo from CosmosDB using user_id
    - Identify faces 
    - Regist face tags

## REST APIs
### Authentication
FIXME

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
```
<created_person_id>
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
| `person_id`| string | Yes | Person ID |
| `order`| string |  | ASC or DESC (default) |
| `offset`| number |  | Offset position of result items(Default 0) |
| `limit`| number |  | limit number of result items (Default 100) |

Example request
```json
{
  "user_id": "nogizaka46",
  "person_id": "a654f4c2-dc7d-43dc-a95a-8819da69587a",
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
