# Digital market for stationery materials

##System architecture diagram - lab 2
![System architecture diagram](https://github.com/AndreeaCvl/PAD-lab-1/blob/main/system_diagram_v2.jpg)


## Application Suitability
The app is suitable for this project because:
- as the marketplace grows, specific services which require more resources can be scaled. Such as payment processing, inventory management or search functionality. 
- Each service can be developed and tested independently.
- The fault of one microservice, let's say payment, won't stop the entire marketplace from working.
- Each resource can be optimized for its specific workload, 
There are a lot of similar apps using microservices. Any online marketplace such as Amazon or Ebay, or if talking about stationery materials - Etsy may be a more suitable example.

![System architecture diagram](https://github.com/AndreeaCvl/PAD-lab-1/blob/main/system_diagram.png)


## Service Boundaries
1. User microservice: 
will encapsulate the log in and register functionalities and the management of user rules and permissions.

2. Product Catalog Microservice
will encapsulate functionalities such as product management (creating and modifying products), search by some criteria and viewing product details. 


## Technology stack and communication patterns

1. API Gateway - Golang.
API Gateways usually need to handle a large number of incoming requests and route them, and Go is a good choice ecause of its performance. It is also designed for concurrent programming.

2. Favorites microservice - Python with Flask.
This will allow adding products to favorites and to view a user's favorite products. Flask aligns well with the microservices architecture and Python has strong database support.

3. Product Catalog Microservice - Python with Flask.
This will allow creating new products, deleting products by the seller, and searching for products by the users. Flask aligns well with the microservices architecture and Python has strong database support.

4. Communication patterns - REST API.
They follow the standard HTTP methods, are compatible with the web infrastructure and the supports caching.

## Data management
### User microservice
**POST /add_product** - Adding a new product
Request Body:
```json
{
    "user_id": "5",
    "product_name": "product name",
    "product_description": "product description",
    "price": 7
}
```
Response Body:
```json
{
    "product_id": "e75e82fe-7971-4ca6-94c8-a93e131decf7",
    "user_id": "5",
    "product_name": "product name",
    "product_description": "product description",
    "price": 7
}
```
**GET /search_products?name=<name>** - search product by name
Query Parameters - The name of the product to search for.
Response Body:
```json
[
  {
    "productId": "string",
    "userId": "string",
    "name": "string",
    "productDescription": "string",
    "price": "numeric",
    "favorites": "numeric",
    "timestamp": "string"
  },
  {
    "productId": "string",
    "userId": "string",
    "name": "string",
    "productDescription": "string",
    "price": "numeric",
    "favorites": "numeric",
    "timestamp": "string"
  },
  // More matching products can be included here
]
```
**GET /search_all_products** - get all available products
Response Body:
```json
[
  {
    "productId": "string",
    "userId": "string",
    "name": "string",
    "productDescription": "string",
    "price": "numeric",
    "favorites": "numeric",
    "timestamp": "string"
  },
  {
    "productId": "string",
    "userId": "string",
    "name": "string",
    "productDescription": "string",
    "price": "numeric",
    "favorites": "numeric",
    "timestamp": "string"
  },
  // More matching products can be included here
]
```

**POST /users/<user_id>/favorites/add** - add product to favorites
Request Body:
```json
{
  "productId": "string"
}
```
Response body
```json
"Product with ID 7 <product_id> added to favorites for user ID: <user_id>"
```

**GET /users/<user_id>/favorites** - add product to favorites
Response body
```json
"Favorites for User ID 6: <product_id>, <product_id>, ...."
```

**DELETE delete_product/<product_id>** - delete product from sale
Response Body:
```json
"Product with ID e75e82fe-7971-4ca6-94c8-a93e131decf7 has been deleted successfully"
```

## Running the code
To create the databases enter the command
```docker-compose up --build``` inside the project directory.

In order to run the code, please run the following files:
```python favourites.py```,
```python products.py ```,
```go run main.go```.

Creating docker for the whole system in progress...

To test the app you can use the requests from the [Postman Collection](https://github.com/AndreeaCvl/PAD-labs/blob/main/PAD%20lab%201.postman_collection.json). Use the requests from the ```gateway``` folder.




