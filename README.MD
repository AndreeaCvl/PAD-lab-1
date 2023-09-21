# Digital market for stationery materials

## Application Suitability
The app is suitable for this project because:
- as the marketplace grows, specific services which require more resources can be scaled. Such as payment processing, inventory management or search functionality. 
- Each service can be developed and tested independently.
- The fault of one microservice, let's say payment, won't stop the entire marketplace from working.
- Each resource can be optimized for its specific workload, 
There are a lot of similar apps using microeservices. Any online marketplace such as Amazon or Ebay, or if talking about stationery materials - Etsy may be a more suitable example.

![System architecture diagram](https://github.com/AndreeaCvl/PAD-lab-1/blob/main/system_diagram.png)


## Service Boundaries
1. User microservice: 
will encapsulate the log in and register functionalities and the management of user rules and permissions.

2. Product Catalog Microservice
will encapsulate functionalities such as product management (creating and modifying products), search by some criteria and viewing product details. 


## Technology stack and communication patterns

1. API Gateway - Golang.
API Gateways usually need to handle a large number of incoming requests and route them, and Go is a good choice ecause of its performance. It is also designed for concurrent programming.

2. User microservice - Python with Flask.
This will allow user registration and authentication and will manage the roles (seller/buyer). Flask aligns well with the microservices architecture and Python has strong database support.

3. Product Catalog Microservice - Python with Flask.
This will allow creating new products, deleting products by the seller, and searching for products by the users. Flask aligns well with the microservices architecture and Python has strong database support.

4. Communication patterns - REST API.
They follow the standard HTTP methods, are compatible with the web infrastructure and the supports caching.

## Data management
### User microservice
**POST /users/register** - register
Request Body:
```json
{
  "username": "string",
  "password": "string",
  "role": "string"
}
```
Response Body:
```json
{
  "userId": "string",
  "username": "string",
  "role": "string"
}
```
**POST /users/login** - login
Request Body:
```json
{
  "username": "string",
  "password": "string",
}
```
Response Body:
```json
{
  "userId": "string",
  "username": "string",
  "role": "string",
  "accessToken": "string"
}
```

**POST /users/wishlist/add** - add product to wishlist
Request Body:
```json
{
  "userId": "string",
  "productId": "string"
}
```
Response body
```json
{
  "message": "Product added to the wishlist successfully."
}
```



### Product catalog microservice
**POST /products** - add product for sale
Request Body:
```json
{
  "userId": "string",
  "name": "string",
  "productDescription": "string",
  "price": "numeric"
}
```
Response Body:
```json
{
  "productId": "string"
  "userId": "string"
  "name": "string",
  "productDescription": "string",
  "price": "numeric",
  "favorites": "numeric",
  "timestamp": "string"
}
```
**DELETE /products/{productId}** - delete product from sale
Response Body:
```json
{
  "message": "string"
}
```

**GET /products/search** - search product by name
Query Parameters - The name of the product to search for.
```json
{
  "name": "string" 
}
```
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


